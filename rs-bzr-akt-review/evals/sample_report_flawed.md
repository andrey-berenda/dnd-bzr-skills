# Revizija: Akt o proceni rizika — „Primer Trgovina d.o.o.“ (12.03.2026) — PRIMER IZVEŠTAJA

*Primer kako treba da izgleda izveštaj skilla na test dokumentu `fixtures/akt_sample_flawed.md` (izmišljena firma, greške su namerno ubačene). Izveštaj je sastavljen ručno prema kontrolnim listama; nije slepi test.*

**Ocena:** ☒ ne sme da se potpiše (postoje kritične primedbe)
**Provereno prema:** `check-akt-o-proceni-rizika.md`, lekarski pregledi iz `check-obuka-evidencije-lekarski.md` (odeljak 3); baseline 2026-10-10; pokrenut `lint_akt.py`.
**Fajl:** `akt_sample_flawed.md`, ~55 redova.

## Ukratko
Dokument je sastavljen po šablonu vezanom za propise koji su prestali da važe (ZBZR 101/05, pravilnik 72/06). Nisu uvrštena mesta sa povećanim rizikom vezana za transport, mere nemaju rokove ni odgovorna lica, zaključak je bez izjave poslodavca, a za procenjivača nema podataka o licenci. Struktura od 8 delova je formalno poštovana, ali je sadržaj delova 2, 3, 4 i 6 nepotpun.

## Primedbe
| Br. | Ozb. | Gde | Šta nije u redu | Osnov | Kako ispraviti | Pouzd. |
|---|---|---|---|---|---|---|
| 1 | K | Odeljak 1, „Lice koje je sprovelo procenu“ | Nema broja i datuma licence procenjivača | pravilnik 76/2024 čl. 4; ZBZR čl. 73 | Navesti broj, datum, rok važenja licence; proveriti da nije istekla na 12.03.2026. | visoka |
| 2 | K | Odeljak 1, „saradnik za BZR“, šifra 4690 | Trgovina na veliko spada u delatnosti u kojima je obavezan **savetnik** (≥ 240 ESPB), a ne saradnik | ZBZR čl. 48 | Imenovati savetnika ili obrazložiti drugačiju delatnost; uskladiti sa rešenjem o imenovanju | visoka |
| 3 | K | Odeljak 5, „Radna mesta sa povećanim rizikom“ | Uvršten je samo magacioner; **vozač viljuškara i vozač dostavnog vozila** (upravljanje vozilima/unutrašnji transport) nedostaju | ZBZR čl. 4 | Uvrstiti oba mesta; za njih – obuka ≤ 1 godina, lekarski pregledi na 12 meseci | visoka |
| 4 | K | Odeljak 5, magacioner | Za mesto sa povećanim rizikom nisu utvrđeni **posebni zdravstveni uslovi**; interval od 24 meseca nije obrazložen (za težak fizički rad i transport u Prilogu II – 12 meseci) | pravilnik 76/2024 čl. 13; ZBZR čl. 17; pravilnik 120/2007, Prilog II | Pribaviti ocenu službe medicine rada; uskladiti interval | srednja |
| 5 | K | Odeljak 6 „Mere“ | Mere nemaju **način, rok, odgovorno lice**; „poštovati propise“ je deklaracija. Za rizike iznad praga (R = 9–12) nema suštinskih mera (npr. „sudar sa licem“ R = 12 → „poštovati saobraćajne propise“) | ZBZR čl. 16; pravilnik čl. 11, 14 | Za svaki R > 6 – konkretna mera (obeležavanje, ograničenje brzine, signalizacija, obuka), rok, odgovorni | visoka |
| 6 | K | Odeljak 7 „Zaključak“ | Nema spiska procenjenih mesta, spiska mesta sa povećanim rizikom, prioriteta/mera/rokova i **izjave poslodavca** o primeni mera | pravilnik 76/2024 čl. 14 | Prepraviti prema četiri elementa | visoka |
| 7 | K | Odeljak 7 „obučeni u roku od 3 godine“ | Za mesta sa povećanim rizikom periodična obuka je **najkasnije u roku od 1 godine**; 3 godine važi samo za ostala mesta | ZBZR čl. 34 | Razdvojiti: ≤ 1 godina za mesta sa povećanim rizikom, ≤ 3 godine za ostala | visoka |
| 8 | Z | Osnov donošenja (preambula) | Pozivi na ZBZR 101/05, 91/15, 113/17 i pravilnik 72/06 – **prestali da važe**; termin „radna okolina“ | ZBZR 35/2023; pravilnik 76/2024 | Zameniti osnov; uskladiti strukturu i termine | visoka |
| 9 | Z | Odeljak 2 | Nema spiska i grupisanja opreme niti spiska LZO | pravilnik čl. 5 | Dodati: viljuškari (električni, ručni), vozila, kancelarijska oprema; LZO po mestima | visoka |
| 10 | Z | Odeljak 3 | Nema broja zaposlenih po polu, maloletnih, osoba sa invaliditetom; nema opisa poslova po mestu | pravilnik čl. 6 | Dodati prema kadrovskoj dokumentaciji | visoka |
| 11 | Z | Odeljak 4 | Opasnosti su nabrojane šablonski; nema štetnosti (mikroklima magacina, osvetljenost, ručno prenošenje van magacionera, ekran za administratora/komercijalistu, stres, rad sa strankama, vibracije kod vozača, hemija kod higijeničara) | pravilnik čl. 8–9 | Proći 5 grupa opasnosti i 4 grupe štetnosti za svako mesto | srednja |
| 12 | Z | Odeljak 5, red „Vozač dostavnog vozila“ | 2 × 5 = 10, a u tabeli piše **11**; skale V i T nisu opisane, prag (R ≤ 6) bez obrazloženja | pravilnik čl. 10 | Ispraviti vrednost; dodati opis skala i nivoa rizika | visoka |
| 13 | Z | Odeljak 8 „po potrebi“ | Nisu navedeni osnovi i postupak izmena (povreda, nova tehnologija, nalog inspektora i dr.) | pravilnik čl. 15–16, 20 | Nabrojati osnove i odgovorno lice | visoka |
| 14 | Z | Prilozi | Nema odluke o pokretanju postupka ni plana sprovođenja procene | pravilnik čl. 17, 19 | Priložiti ili pitati da li postoje zasebno | srednja |
| 15 | Z | Podaci | Nepopunjene adresa (`[adresa]`) i potpis direktora | ZBZR čl. 16 | Popuniti; potpisati | visoka |

## Šta nije provereno
- Sistematizacija i kadrovi, lekarski pregledi, nalazi, rešenje o imenovanju savetnika/saradnika nisu priloženi; unakrsne provere (odeljak I liste) su nepotpune.
- Pravilnici po vrstama štetnosti (ručno prenošenje tereta, unutrašnji transport) – brojevi Sl. glasnika nisu verifikovani u baseline.

## Pitanja autoru
1. Da li poslodavac ima druge lokacije (ogranke, skladišta)?
2. Koja je licenca/ESPB lica zaduženog za BZR i kako je imenovano?
