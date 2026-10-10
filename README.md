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
Detaljno: [`INSTALACIJA.md`](INSTALACIJA.md). Ukratko: instalirati [uv](https://docs.astral.sh/uv/) (Windows: `winget install --id=astral-sh.uv -e`), zatim `uv run package.py` pravi `dist/*.skill` koje treba otpremiti u Claude. Skripte pokreće `uv run ...` (sam preuzima Python i `defusedxml`). Ulaz je isključivo Word (`.docx`); PDF, skenovi i stari `.doc` se ne čitaju – skill traži Word fajl.

## Status
Radna verzija. Nije testirana na stvarnim aktima. Ne zamenjuje licencirano stručno lice i nije pravno mišljenje.
