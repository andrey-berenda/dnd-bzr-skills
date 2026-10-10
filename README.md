# dnd-bzr-skills

Claude skillovi za konsultantski rad iz oblasti bezbednosti i zdravlja na radu (BZR) u Srbiji. Jezik rada skillova je srpski (latinica).

| Skill | Namena |
|---|---|
| [`rs-bzr-akt-review`](rs-bzr-akt-review/SKILL.md) | Revizija dokumenata: akt o proceni rizika, elaborat / plan preventivnih mera / prijava gradilišta, stručni nalaz o pregledu i ispitivanju, obuka, evidencije, lekarski pregledi, dozvola za rad, rad na visini |
| [`rs-bzr-akt-izrada`](rs-bzr-akt-izrada/SKILL.md) | Izrada nacrta istih dokumenata (oslanja se na kontrolne liste iz revizije) |

## Zašto dva skilla
- **`rs-bzr-akt-review`** je glavni: sadrži celu normativnu osnovu (`references/`), kontrolne liste, šablon izveštaja, skripte i testove.
- **`rs-bzr-akt-izrada`** je tanak pratilac: samo vodi izradu nacrta (prikupljanje podataka, struktura, pravila pisanja) i na kraju poziva reviziju. Nema sopstvenu kopiju propisa – koristi `references/` iz revizije, da se norme održavaju na jednom mestu.
Skillovi su odvojeni jer imaju različite okidače (proveri gotov dokument / napiši nov) i različito ponašanje; mogu se instalirati zajedno ili samo revizija.

## Normativna osnova
Stanje na dan **2026-10-10**: ZBZR 35/2023, pravilnik o proceni rizika 76/2024, pravilnik o pregledu opreme 76/2024, Uredba o gradilištima i dr.; rok primene više podzakonskih akata je **1.1.2027.** Svaka norma je označena nivoom pouzdanosti ([T] pročitan tekst, [S] sekundarni izvor, [?] nepotvrđeno) – vidi `rs-bzr-akt-review/references/baseline-propisi.md`.

Nije pokriveno: zaštita od požara, smanjenje rizika od katastrofa, upravljanje otpadom, hemikalije.

## Instalacija
Arhive se prave komandom `python package.py` (izlaz: `dist/*.skill`), zatim se dodaju u Claude. Skripte (`extract_text.py`, `lint_akt.py`) koriste samo standardnu biblioteku Pythona 3.9+.

### Windows
- Python 3 sa python.org (ili `py -3` iz Python launchera). Komande: `py -3 rs-bzr-akt-review\scripts\extract_text.py akt.docx -o akt.txt`, zatim `py -3 rs-bzr-akt-review\scripts\lint_akt.py akt.txt`.
- Uvek koristiti `-o`; preusmeravanje `>` u PowerShell-u kvari č, š, ž, ć, đ. Skripte čitaju i pišu UTF-8.
- PDF: `pip install pypdf` (ili `pdftotext` iz Poppler paketa). Skenirani PDF zahteva OCR.
- Opciono: `pip install defusedxml` (bezbednije čitanje .docx/.xlsx).
- Test: `python tests/smoke_test.py`; isti test se automatski izvršava na Windows-u, macOS-u i Linux-u (GitHub Actions).

## Status
Radna verzija. Nije testirana na stvarnim aktima. Ne zamenjuje licencirano stručno lice i nije pravno mišljenje.
