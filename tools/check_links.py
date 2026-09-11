"""
Verifies every internal PDF link in learning_langgraph resolves correctly:
the target file exists, and (if the link has a #fragment) the target PDF
actually has a matching named destination for it.

Run after every build_pdfs.py run:
    python3 check_links.py                # checks every PDF in the repo
    python3 check_links.py ../01_python_foundations   # checks one folder
"""
import pathlib
import sys
from pypdf import PdfReader

BASE = pathlib.Path(__file__).resolve().parent.parent


def check(root: pathlib.Path) -> int:
    pdfs = sorted(root.rglob("*.pdf"))
    dest_cache = {}

    def get_dests(p):
        if p not in dest_cache:
            try:
                dest_cache[p] = set(PdfReader(str(p)).named_destinations.keys())
            except Exception:
                dest_cache[p] = None
        return dest_cache[p]

    problems = []
    for pdf in pdfs:
        try:
            r = PdfReader(str(pdf))
        except Exception as e:
            problems.append((pdf, "(whole file)", f"UNREADABLE: {e}"))
            continue
        for page in r.pages:
            for annot in (page.get("/Annots") or []):
                obj = annot.get_object()
                a = obj.get("/A")
                if not a or "/URI" not in a:
                    continue
                uri = str(a["/URI"])
                if uri.startswith(("http://", "https://", "mailto:")):
                    continue
                target_str, _, frag = uri.partition("#")
                target = (pdf.parent / target_str).resolve() if target_str else pdf.resolve()
                if not target.exists():
                    problems.append((pdf, uri, f"MISSING FILE: {target}"))
                    continue
                if frag:
                    dests = get_dests(target)
                    if dests is None:
                        problems.append((pdf, uri, "TARGET UNREADABLE"))
                    elif f"/{frag}" not in dests:
                        problems.append((pdf, uri, f"MISSING NAMED DEST '#{frag}' in {target.name}"))

    print(f"checked {len(pdfs)} pdfs under {root.relative_to(BASE) if root != BASE else '.'}")
    if problems:
        print(f"\n{len(problems)} PROBLEMS:")
        for pdf, uri, msg in problems:
            print(f"  {pdf.relative_to(BASE)}: {uri}  ->  {msg}")
    else:
        print("ALL LINKS VALID")
    return len(problems)


def main():
    root = pathlib.Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else BASE
    n = check(root)
    sys.exit(1 if n else 0)


if __name__ == "__main__":
    main()
