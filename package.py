#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
"""Pakuje foldere skillova u .skill arhive (radi na Windows-u, macOS-u i Linux-u).

Upotreba:  uv run package.py            (spakuje sva tri skilla u folder dist/)
           uv run package.py rs-bzr-akt-review
"""
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SKILLS = ["rs-bzr-akt-review", "rs-bzr-akt-izrada", "rs-bzr-instalacija"]


def pack(name: str, out_dir: Path) -> Path:
    src = ROOT / name
    if not (src / "SKILL.md").is_file():
        sys.exit(f"Nema {src / 'SKILL.md'}")
    out_dir.mkdir(exist_ok=True)
    out = out_dir / f"{name}.skill"
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for p in sorted(src.rglob("*")):
            if p.is_file() and "__pycache__" not in p.parts:
                z.write(p, p.relative_to(ROOT).as_posix())  # uvek '/' u arhivi
    return out


def main():
    names = sys.argv[1:] or SKILLS
    for n in names:
        print("Spakovano:", pack(n, ROOT / "dist"))


if __name__ == "__main__":
    main()
