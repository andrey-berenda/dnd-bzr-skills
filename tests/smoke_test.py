#!/usr/bin/env python3
"""Smoke test skripti – radi isto na Windows-u, macOS-u i Linux-u.

Upotreba:  python tests/smoke_test.py
Proverava: izdvajanje teksta iz .docx i .md, UTF-8 (č, š, ž, ć, đ), lint nalaze na test aktu,
pakovanje .skill arhive.
"""
import os
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "rs-bzr-akt-review" / "scripts"
FIXTURE = ROOT / "rs-bzr-akt-review" / "evals" / "fixtures" / "akt_sample_flawed.md"


if hasattr(sys.stdout, "reconfigure"):  # Windows konzola (cp1252) ne sme da pukne na č, š, ž, ć, đ
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def run(*args, stdin=None):
    env = dict(os.environ)
    env.pop("PYTHONUTF8", None)          # simulira podrazumevana podešavanja (na Windows-u cp1252/cp1250)
    env.pop("PYTHONIOENCODING", None)
    r = subprocess.run([sys.executable, *map(str, args)], capture_output=True, input=stdin, env=env)
    return r.returncode, r.stdout.decode("utf-8", "replace"), r.stderr.decode("utf-8", "replace")


def check(cond, msg):
    print(("OK   " if cond else "FAIL ") + msg)
    if not cond:
        check.failed = True


check.failed = False


def main():
    tmp = Path(tempfile.mkdtemp())

    # 1) extract iz md u fajl
    out = tmp / "akt.txt"
    rc, so, se = run(SCRIPTS / "extract_text.py", FIXTURE, "-o", out)
    check(rc == 0 and out.exists(), "extract_text.py -o radi na .md")
    txt = out.read_text(encoding="utf-8")
    check("težina" in txt.lower() or "štetnosti" in txt.lower(), "dijakritici (š, ž) su sačuvani u UTF-8")

    # 2) lint na test aktu
    rc, so, se = run(SCRIPTS / "lint_akt.py", out, "--today", "2026-10-10")
    for code in ("OBS-ZAKON", "OBS-PRAV-RIZIK", "OBS-TERM", "RIZIK-ARITMETIKA", "LICENCA-NEMA", "PH-ZAGRADA"):
        check(f"[{code}]" in so, f"lint nalazi {code}")
    check("„" in so, "izlaz sadrži Unicode navodnike bez greške kodiranja")

    # 3) stdin ('-')
    rc, so, se = run(SCRIPTS / "lint_akt.py", "-", "--today", "2026-10-10", stdin=out.read_bytes())
    check(rc == 0 and "RIZIK-ARITMETIKA" in so, "lint čita stdin ('-')")

    # 4) docx (napravljen u hodu, bez dodatnih biblioteka)
    docx = tmp / "t.docx"
    xml = ('<?xml version="1.0" encoding="UTF-8"?><w:document xmlns:w="http://schemas.openxmlformats.org/'
           'wordprocessingml/2006/main"><w:body><w:p><w:r><w:t>Šema gradilišta č ć đ ž</w:t></w:r></w:p>'
           '<w:tbl><w:tr><w:tc><w:p><w:r><w:t>V</w:t></w:r></w:p></w:tc><w:tc><w:p><w:r><w:t>3</w:t></w:r></w:p></w:tc>'
           '</w:tr></w:tbl></w:body></w:document>')
    with zipfile.ZipFile(docx, "w") as z:
        z.writestr("word/document.xml", xml)
    out2 = tmp / "d.txt"
    rc, so, se = run(SCRIPTS / "extract_text.py", docx, "-o", out2)
    t2 = out2.read_text(encoding="utf-8") if out2.exists() else ""
    check(rc == 0 and "Šema gradilišta č ć đ ž" in t2 and "V | 3" in t2, "extract_text.py čita .docx (pasus + tabela)")

    # 5) putanja sa razmakom
    spaced = tmp / "folder sa razmakom"
    spaced.mkdir()
    sp = spaced / "akt test.md"
    sp.write_bytes(FIXTURE.read_bytes())
    rc, so, se = run(SCRIPTS / "extract_text.py", sp, "-o", spaced / "izlaz.txt")
    check(rc == 0, "putanja sa razmacima radi")

    # 5b) popravka oštećenih dijakritika (funkcija direktno)
    sys.path.insert(0, str(SCRIPTS))
    import extract_text as et
    fixed, n = et.fix_diacritics("angaţuje ĉlan predviĊeno ĐORĐE Ţivot")
    check(fixed == "angažuje član predviđeno ĐORĐE Život" and n > 0, "fix_diacritics popravlja ĉ ţ Ċ (PDF sa starim fontovima)")

    # 6) pakovanje
    rc, so, se = run(ROOT / "package.py", "rs-bzr-akt-izrada")
    arc = ROOT / "dist" / "rs-bzr-akt-izrada.skill"
    ok = arc.exists() and "rs-bzr-akt-izrada/SKILL.md" in zipfile.ZipFile(arc).namelist()
    check(rc == 0 and ok, "package.py pravi .skill sa '/' putanjama")

    print("\nREZULTAT:", "NEUSPEH" if check.failed else "SVE U REDU")
    sys.exit(1 if check.failed else 0)


if __name__ == "__main__":
    main()
