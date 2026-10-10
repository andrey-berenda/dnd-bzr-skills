#!/usr/bin/env python3
"""Izdvaja tekst iz .docx / .xlsx / .pdf / .txt / .md za reviziju akata.

Upotreba:  python extract_text.py <fajl> [-o izlaz.txt]
(na Windows-u: py -3 extract_text.py <fajl> -o izlaz.txt; na macOS/Linux: python3 ...)
Preporuka: koristiti -o, jer preusmeravanje (>) u PowerShell-u može pokvariti kodiranje (č, š, ž, ć, đ).
Izlaz je uvek UTF-8.

- .docx: pasusi i tabele po redosledu u dokumentu (tabele – redovi sa razdvajačem " | ").
- .xlsx: svaki list, redovi sa " | ".
- .pdf: preko `pdftotext -layout` (ako ga nema – preko pypdf). Za skenirane PDF treba OCR.
- ostalo: čita se kao UTF-8 tekst.
Samo standardna biblioteka (+ za PDF: `pdftotext` ili `pip install pypdf`; defusedxml ako je instaliran).
"""
import argparse
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


def fix_diacritics(text):
    """Mnogi srpski PDF-ovi (stari fontovi) daju ĉ/ţ/Ċ umesto č/ž/đ. Popravlja samo ako su takvi znaci prisutni."""
    if not re.search(r"[ĉĈţŢĊ]", text):
        return text, 0
    n = len(re.findall(r"[ĉĈţŢĊ]", text))
    text = (text.replace("ĉ", "č").replace("Ĉ", "Č").replace("ţ", "ž").replace("Ţ", "Ž"))
    # Ċ je obično đ unutar reči malim slovima (predviĊeno), a Đ na početku reči/velikim slovima
    text = re.sub(r"(?<=[a-zčćšžđ])Ċ|Ċ(?=[a-zčćšžđ])", "đ", text)
    text = text.replace("Ċ", "Đ")
    return text, n


def pdf_text(path):
    if shutil.which("pdftotext"):
        r = subprocess.run(["pdftotext", "-layout", "-enc", "UTF-8", path, "-"],
                           capture_output=True, text=True, encoding="utf-8", errors="replace")
        if r.returncode == 0 and r.stdout.strip():
            return r.stdout
    try:
        from pypdf import PdfReader  # type: ignore
        return "\n".join((p.extract_text() or "") for p in PdfReader(path).pages)
    except Exception as e:  # noqa: BLE001
        sys.exit(f"Nije moguće izdvojiti tekst iz PDF-a ({e}). Instalirajte `pip install pypdf` (ili pdftotext); "
                 "ako je PDF sken – potreban je OCR.")


def main():
    ap = argparse.ArgumentParser(description="Izdvaja tekst iz docx/xlsx/pdf/txt (izlaz UTF-8).")
    ap.add_argument("file")
    ap.add_argument("-o", "--output", help="upisati rezultat u ovaj fajl (UTF-8) umesto na stdout")
    ap.add_argument("--no-fix-diacritics", action="store_true", help="ne popravljati oštećene dijakritike u PDF-u (ĉ→č, ţ→ž, Ċ→đ)")
    a = ap.parse_args()
    path = a.file
    low = path.lower()
    if _XML_FALLBACK and low.endswith((".docx", ".xlsx")):
        sys.stderr.write("[upozorenje] defusedxml nije instaliran (pip install defusedxml); koristi se standardni XML parser\n")
    if low.endswith(".docx"):
        text = docx_text(path)
    elif low.endswith(".xlsx"):
        text = xlsx_text(path)
    elif low.endswith(".pdf"):
        text = pdf_text(path)
        if not a.no_fix_diacritics:
            text, n = fix_diacritics(text)
            if n:
                sys.stderr.write(f"[info] popravljeno {n} oštećenih znakova (ĉ ţ Ċ → č ž đ); isključiti sa --no-fix-diacritics\n")
    elif low.endswith(".doc"):
        sys.exit("Stari .doc: sačuvajte kao .docx ili PDF (ili `soffice --headless --convert-to docx`).")
    else:
        text = open(path, encoding="utf-8-sig", errors="replace").read()
    if not text.strip():
        sys.exit("[Prazno: verovatno sken ili zaštićen fajl]")
    if a.output:
        with open(a.output, "w", encoding="utf-8", newline="\n") as f:
            f.write(text)
        sys.stderr.write(f"Upisano: {a.output} ({len(text)} znakova)\n")
    else:
        sys.stdout.buffer.write(text.encode("utf-8"))


if __name__ == "__main__":
    main()
