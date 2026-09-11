"""
Watches learning_langgraph/ for changes to any .md file, and automatically
rebuilds just that file's .pdf whenever it's saved. Leave this running in a
terminal while you edit — every save gets a fresh PDF within a couple seconds.

Run it:
    python3 watch_pdfs.py

Stop it:
    Ctrl+C

It checks every 2 seconds whether any .md file is newer than its .pdf (or has
no .pdf yet), and rebuilds only those. It does not need any extra package
beyond what build_pdfs.py already needs (markdown, playwright).
"""

import pathlib
import time

import build_pdfs

POLL_SECONDS = 2


def find_stale_files():
    stale = []
    for md_path in build_pdfs.find_markdown_files():
        pdf_path = md_path.with_suffix(".pdf")
        if not pdf_path.exists() or md_path.stat().st_mtime > pdf_path.stat().st_mtime:
            stale.append(md_path)
    return stale


def main():
    print(f"Watching {build_pdfs.BASE} for .md changes. Press Ctrl+C to stop.")
    print("Every saved .md file gets its .pdf rebuilt automatically.\n")

    try:
        while True:
            stale = find_stale_files()
            if stale:
                print(f"[{time.strftime('%H:%M:%S')}] {len(stale)} file(s) changed, rebuilding...")
                build_pdfs.build_many(stale)
                print()
            time.sleep(POLL_SECONDS)
    except KeyboardInterrupt:
        print("\nStopped.")


if __name__ == "__main__":
    main()
