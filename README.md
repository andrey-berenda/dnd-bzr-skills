# dnd-bzr-skills

Claude skillovi za konsultantski rad iz oblasti bezbednosti i zdravlja na radu (BZR) u Srbiji. Jezik rada skillova je srpski (latinica).

| Skill | Namena |
|---|---|
| [`rs-bzr-akt-review`](rs-bzr-akt-review/SKILL.md) | Revizija dokumenata: akt o proceni rizika, elaborat / plan preventivnih mera / prijava gradilišta, stručni nalaz o pregledu i ispitivanju, obuka, evidencije, lekarski pregledi, dozvola za rad, rad na visini |
| [`rs-bzr-akt-izrada`](rs-bzr-akt-izrada/SKILL.md) | Izrada nacrta istih dokumenata (oslanja se na kontrolne liste iz revizije) |

## Normativna osnova
Stanje na dan **2026-10-10**: ZBZR 35/2023, pravilnik o proceni rizika 76/2024, pravilnik o pregledu opreme 76/2024, Uredba o gradilištima i dr.; rok primene više podzakonskih akata je **1.1.2027.** Svaka norma je označena nivoom pouzdanosti ([T] pročitan tekst, [S] sekundarni izvor, [?] nepotvrđeno) – vidi `rs-bzr-akt-review/references/baseline-propisi.md`.

Nije pokriveno: zaštita od požara, smanjenje rizika od katastrofa, upravljanje otpadom, hemikalije.

## Instalacija
Preuzeti `.skill` iz Releases (ili spakovati folder skilla u zip sa ekstenzijom `.skill`) i dodati u Claude. Skripte (`extract_text.py`, `lint_akt.py`) koriste samo standardnu biblioteku Pythona 3; za PDF je potreban `pdftotext`.

## Status
Radna verzija. Nije testirana na stvarnim aktima. Ne zamenjuje licencirano stručno lice i nije pravno mišljenje.
