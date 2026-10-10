#!/usr/bin/env python3
"""Izdvaja tekst iz .docx / .xlsx / .pdf / .txt / .md za reviziju akata.

Upotreba:  python3 extract_text.py <fajl> [> out.txt]

- .docx: pasusi i tabele po redosledu u dokumentu (tabele – redovi sa razdvajačem " | ").
- .xlsx: svaki list, redovi sa " | ".
- .pdf: preko `pdftotext -layout` (ako ga nema – preko pypdf). Za skenirane PDF treba OCR.
- ostalo: čita se kao UTF-8 tekst.
Samo standardna biblioteka (+ pdftotext/pypdf za PDF; defusedxml ako je instaliran).
"""
import re
import shutil
import subprocess
import sys
import zipfile

try:  # defusedxml štiti od XXE / „billion laughs“ u ulaznim fajlovima
    import defusedxml.ElementTree as ET  # type: ignore
except ImportError:  # standardni parser ne razvija spoljne entitete, ali je podložan širenju entiteta
    import xml.etree.ElementTree as ET  # noqa: S405
    _XML_FALLBACK = True
else:
    _XML_FALLBACK = False

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
S = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"


def _cell_text(tc):
    parts = []
    for p in tc.iter(W + "p"):
        parts.append("".join(t.text or "" for t in p.iter(W + "t")))
    return " ".join(x for x in parts if x).strip()


def docx_text(path):
    with zipfile.ZipFile(path) as z:
        root = ET.fromstring(z.read("word/document.xml"))
    body = root.find(W + "body")
    out = []

    def walk(parent):
        for el in parent:
            if el.tag == W + "p":
                txt = "".join(t.text or "" for t in el.iter(W + "t"))
                if txt.strip():
                    out.append(txt)
            elif el.tag == W + "tbl":
                for tr in el.iter(W + "tr"):
                    cells = [_cell_text(tc) for tc in tr.findall(W + "tc")]
                    out.append(" | ".join(cells))
                out.append("")
            elif el.tag == W + "sdt":
                content = el.find(W + "sdtContent")
                if content is not None:
                    walk(content)

    walk(body)
    return "\n".join(out)


def xlsx_text(path):
    with zipfile.ZipFile(path) as z:
        shared = []
        if "xl/sharedStrings.xml" in z.namelist():
            sroot = ET.fromstring(z.read("xl/sharedStrings.xml"))
            for si in sroot.iter(S + "si"):
                shared.append("".join(t.text or "" for t in si.iter(S + "t")))
        names = sorted(n for n in z.namelist() if re.match(r"xl/worksheets/sheet\d+\.xml$", n))
        out = []
        for n in names:
            out.append(f"=== {n.split('/')[-1]} ===")
            root = ET.fromstring(z.read(n))
            for row in root.iter(S + "row"):
                vals = []
                for c in row.iter(S + "c"):
                    v = c.find(S + "v")
                    if v is None or v.text is None:
                        vals.append("")
                    elif c.get("t") == "s":
                        vals.append(shared[int(v.text)])
                    else:
                        vals.append(v.text)
                out.append(" | ".join(vals))
        return "\n".join(out)


def pdf_text(path):
    if shutil.which("pdftotext"):
        r = subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True, text=True)
        if r.returncode == 0 and r.stdout.strip():
            return r.stdout
    try:
        from pypdf import PdfReader  # type: ignore
        return "\n".join((p.extract_text() or "") for p in PdfReader(path).pages)
    except Exception as e:  # noqa: BLE001
        sys.exit(f"Nije moguće izdvojiti tekst iz PDF-a ({e}). Verovatno je sken – potreban je OCR.")


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    path = sys.argv[1]
    low = path.lower()
    if _XML_FALLBACK and low.endswith((".docx", ".xlsx")):
        sys.stderr.write("[upozorenje] defusedxml nije instaliran (pip install defusedxml); koristi se standardni XML parser\n")
    if low.endswith(".docx"):
        text = docx_text(path)
    elif low.endswith(".xlsx"):
        text = xlsx_text(path)
    elif low.endswith(".pdf"):
        text = pdf_text(path)
    elif low.endswith(".doc"):
        sys.exit("Stari .doc: sačuvajte kao .docx ili PDF (ili `soffice --headless --convert-to docx`).")
    else:
        text = open(path, encoding="utf-8", errors="replace").read()
    sys.stdout.write(text)
    if not text.strip():
        sys.exit("\n[Prazno: verovatno sken ili zaštićen fajl]")


if __name__ == "__main__":
    main()
