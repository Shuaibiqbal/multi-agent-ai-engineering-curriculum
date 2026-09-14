"""
Converts every .md file under learning_langgraph/ into a matching .pdf,
right next to it. Internal links between .md files (like the Hint/Solution
links) get rewritten to point at the .pdf versions, so clicking a link in
one PDF opens the correct other PDF, not a .md file.

Run a full rebuild of everything:
    python3 build_pdfs.py

Run it for just one file (used by watch_pdfs.py, but works standalone too):
    python3 build_pdfs.py path/to/one_file.md

Needs (installed once, already done on this machine):
    pip install --user markdown playwright
Uses the system Google Chrome (no extra browser download needed).
"""

import html
import os
import pathlib
import re
import sys
import markdown
from playwright.sync_api import sync_playwright
from pypdf import PdfReader, PdfWriter
from pypdf.generic import NameObject, TextStringObject

# learning_langgraph/ is the parent of this tools/ folder
BASE = pathlib.Path(__file__).resolve().parent.parent

CHROME_PATH = "/usr/bin/google-chrome-stable"

CSS = """
<style>
  body {
    font-family: -apple-system, "Segoe UI", Helvetica, Arial, sans-serif;
    max-width: 860px;
    margin: 0 auto;
    padding: 32px 40px;
    color: #1a1a1a;
    line-height: 1.55;
    font-size: 14px;
  }
  h1 { font-size: 26px; border-bottom: 3px solid #2b2d42; padding-bottom: 8px; margin-top: 0; }
  h2 { font-size: 19px; border-bottom: 1px solid #ccc; padding-bottom: 4px; margin-top: 30px; }
  h3 { font-size: 15px; margin-top: 22px; color: #2b2d42; }
  code {
    background: #f2f2f5;
    padding: 1px 5px;
    border-radius: 4px;
    font-family: "SF Mono", Consolas, monospace;
    font-size: 12.5px;
  }
  pre {
    background: #f2f2f5;
    padding: 12px 14px;
    border-radius: 6px;
    overflow-x: auto;
    font-size: 12px;
    border: 1px solid #e0e0e5;
  }
  pre code { background: none; padding: 0; }
  blockquote {
    border-left: 4px solid #8d99ae;
    margin: 12px 0;
    padding: 4px 16px;
    color: #444;
    background: #f7f7fa;
  }
  table { border-collapse: collapse; width: 100%; margin: 14px 0; font-size: 12.5px; }
  th, td { border: 1px solid #ddd; padding: 6px 10px; text-align: left; vertical-align: top; }
  th { background: #2b2d42; color: white; }
  tr:nth-child(even) { background: #f7f7fa; }
  a { color: #1d4ed8; text-decoration: none; }
  a:hover { text-decoration: underline; }
  hr { border: none; border-top: 1px solid #ddd; margin: 28px 0; }
  ul, ol { padding-left: 24px; }
  li { margin: 3px 0; }
  strong { color: #2b2d42; }
  .page-break { page-break-after: always; break-after: page; border: none; margin: 0; padding: 0; height: 0; }
</style>
"""

MD_EXTENSIONS = ["tables", "fenced_code", "toc", "sane_lists", "attr_list"]

HEADER_TEMPLATE = """
<div style="font-size:9px; width:100%; padding:0 15mm; color:#777; font-family:Arial, sans-serif;">
  <span class="title"></span>
</div>
"""
FOOTER_TEMPLATE = """
<div style="font-size:8px; width:100%; text-align:center; color:#999; font-family:Arial, sans-serif;">
  <span class="pageNumber"></span> / <span class="totalPages"></span>
</div>
"""

# matches href="something.md" or href="something.md#anchor", but not external URLs
MD_LINK_RE = re.compile(r'href="((?!https?://)[^"]+?)\.md(#[^"]*)?"')

# matches the absolute file:// URI Chrome bakes into link annotations at print time
FILE_URI_RE = re.compile(r"^file://(/[^#]+)(#.*)?$")


def relativize_pdf_links(pdf_path: pathlib.Path) -> None:
    """Rewrite the absolute file:// links Chrome bakes into the PDF (tied to
    this machine's exact path) into relative paths, so the whole PDF set stays
    clickable after being copied anywhere else (e.g. rsynced to another machine)."""
    reader = PdfReader(str(pdf_path))
    writer = PdfWriter()
    writer.append(reader)
    # writer.append() does not carry over document metadata (Title, etc.) —
    # without this, every PDF's Title/Keywords silently end up empty after
    # this rewrite step, even though Chrome set them correctly at print time.
    if reader.metadata:
        title = reader.metadata.title or ""
        writer.add_metadata({
            "/Title": title,
            "/Keywords": title,
        })
    changed = False
    for page in writer.pages:
        annots = page.get("/Annots")
        if not annots:
            continue
        for annot in annots:
            obj = annot.get_object()
            a = obj.get("/A")
            if not a or "/URI" not in a:
                continue
            m = FILE_URI_RE.match(str(a["/URI"]))
            if not m:
                continue
            target = pathlib.Path(m.group(1))
            fragment = m.group(2) or ""
            rel = pathlib.Path(os.path.relpath(target, pdf_path.parent)).as_posix()
            a[NameObject("/URI")] = TextStringObject(rel + fragment)
            changed = True
    if changed:
        with open(pdf_path, "wb") as f:
            writer.write(f)


def rewrite_md_links_to_pdf(body_html: str) -> str:
    return MD_LINK_RE.sub(lambda m: f'href="{m.group(1)}.pdf{m.group(2) or ""}"', body_html)


def find_markdown_files():
    return sorted(BASE.rglob("*.md"))


def extract_title(text: str, fallback: str) -> str:
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("# "):
            return stripped[2:].strip()
    return fallback


def md_to_html_file(md_path: pathlib.Path) -> pathlib.Path:
    """Write the intermediate HTML right next to the real .md file, so relative
    links resolve to real learning_langgraph locations, not a temp path."""
    text = md_path.read_text(encoding="utf-8")
    body_html = markdown.markdown(text, extensions=MD_EXTENSIONS)
    body_html = rewrite_md_links_to_pdf(body_html)
    raw_title = extract_title(text, fallback=md_path.relative_to(BASE).as_posix())
    title = html.escape(raw_title)
    full_html = (
        f"<!doctype html><html><head><meta charset='utf-8'><title>{title}</title>"
        f"{CSS}</head><body>{body_html}</body></html>"
    )
    out_path = md_path.with_suffix(".html")
    out_path.write_text(full_html, encoding="utf-8")
    return out_path


def build_one(page, md_path: pathlib.Path) -> bool:
    html_path = md_to_html_file(md_path)
    pdf_path = md_path.with_suffix(".pdf")
    try:
        page.goto(f"file://{html_path}")
        page.pdf(
            path=str(pdf_path),
            display_header_footer=True,
            header_template=HEADER_TEMPLATE,
            footer_template=FOOTER_TEMPLATE,
            margin={"top": "18mm", "bottom": "14mm", "left": "15mm", "right": "15mm"},
            print_background=True,
        )
        relativize_pdf_links(pdf_path)
        return True
    finally:
        html_path.unlink(missing_ok=True)


def build_many(md_paths):
    ok, fail = 0, 0
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=CHROME_PATH)
        page = browser.new_page()
        for md_path in md_paths:
            try:
                build_one(page, md_path)
                ok += 1
                print(f"OK   {md_path.relative_to(BASE)}")
            except Exception as e:
                fail += 1
                print(f"FAIL {md_path.relative_to(BASE)} -> {e}", file=sys.stderr)
        browser.close()
    return ok, fail


def main():
    if len(sys.argv) > 1:
        # rebuild just the file(s) named on the command line
        md_paths = [pathlib.Path(arg).resolve() for arg in sys.argv[1:]]
    else:
        md_paths = find_markdown_files()

    ok, fail = build_many(md_paths)
    print(f"\n{ok} succeeded, {fail} failed, {len(md_paths)} total")


if __name__ == "__main__":
    main()
