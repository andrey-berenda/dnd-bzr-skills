---
name: rs-bzr-akt-izrada
description: Pomoć zaposlenima konsultantske kuće za bezbednost i zdravlje na radu u Srbiji pri izradi dokumenata – akt o proceni rizika (prema pravilniku 76/2024), elaborat o uređenju gradilišta, plan preventivnih mera, prijava gradilišta, program obuke, dozvola za rad, obrasci evidencija. Koristi kada korisnik traži „sastavi/pripremi/popuni akt“, „napravi nacrt akta o proceni rizika“, „napravi elaborat“, „izradi plan preventivnih mera“, ili da upitnik klijenta / spisak radnih mesta. Gradi dokument prema obaveznoj strukturi, ne izmišlja licence i merenja, nepoznato označava poljem ⟦POPUNITI⟧ i na kraju proverava nacrt kontrolnim listama skilla rs-bzr-akt-review. Odgovara na srpskom.
---

# Izrada dokumenata iz oblasti BZR (Srbija)

Ovaj skill je radni generator nacrta. Oslanja se na normativnu osnovu i kontrolne liste skilla **rs-bzr-akt-review**: pre rada pozovi ga preko Skill alata (ili pročitaj njegov `references/baseline-propisi.md` i odgovarajući `check-*.md`). Tako su struktura dokumenta i završna provera izgrađene na istim normama.

**Jezik:** sve – dokument, komentari, pitanja korisniku – na **srpskom**, latinicom (osim ako klijent traži ćirilicu; tada ćirilicom, ne mešaj pisma).

Ključno načelo: nacrt mora biti **iskren**, a ne glatko napisan. Licence, rezultati merenja, datumi lekarskih pregleda, broj zaposlenih i radna mesta su činjenice klijenta; ako ih nema, stavi vidljivu oznaku `⟦POPUNITI: …⟧` (ista oznaka u celom tekstu, da je linter pronađe), a ne uverljivu vrednost. Klijent potpisuje dokument i snosi kaznu do 2 mil. RSD (ZBZR čl. 100).

## Korak 1. Prikupljanje ulaznih podataka

Pre pisanja razjasni (postavi pitanja u listi, ako nešto nedostaje; ne pitaj ono što se vidi iz fajlova):
- Poslodavac: naziv, PIB/MB, adrese sedišta i izdvojenih jedinica, šifra delatnosti, broj zaposlenih (po polu, maloletni, osobe sa invaliditetom), smene, noćni rad.
- Akt o organizaciji i sistematizaciji radnih mesta; opis tehnološkog procesa; spisak opreme (sa fabričkim brojevima), opasne materije (sa bezbednosnim listovima), LZO.
- Procenjivači: ime, zvanje, **broj i datum licence** (ili licencirano pravno lice + ugovor).
- Postojeći nalazi (oprema, elektro, gromobran, sredina), povrede u poslednjih 3–5 godina, lekarski pregledi, prethodni akt.
- Vrsta dokumenta i datum donošenja.

## Korak 2. Struktura

**Akt o proceni rizika** (pravilnik 76/2024 čl. 3–14) – 8 delova: (1) opšti podaci o poslodavcu i procenjivačima sa licencama; (2) tehnološki/radni proces, sredstva za rad, spisak i grupisanje opreme, LZO; (3) organizacija rada (prema sistematizaciji; provera faktičkog stanja); (4) prepoznavanje opasnosti (5 grupa) i štetnosti (4 grupe); (5) procena rizika (verovatnoća i težina; dozvoljene vrednosti); (6) mere (tehničke, organizacione, obuka, osposobljavanje, LZO, zdravstvene, higijenske, ostale) sa **načinom, rokom, odgovornim licem**; program postupnog otklanjanja pri većim ulaganjima; posebni zdravstveni uslovi za mesta sa povećanim rizikom; (7) zaključak – sva mesta, mesta sa povećanim rizikom, prioriteti/mere/rokovi/odgovorni, **izjava poslodavca**; (8) postupak izmena. Prilozi: odluka o pokretanju postupka, plan sprovođenja procene (pravilnik čl. 17, 19).

**Elaborat o uređenju gradilišta** – šema/situacioni plan; opis radova; mere BZR; prilozi-spiskovi (vidi `check-gradiliste.md`). **Plan preventivnih mera** – Uredba Prilog 5. **Prijava gradilišta** – Prilog 3.

**Ostalo** (program obuke, dozvola za rad, obrasci evidencija) – prema odgovarajućim odeljcima `check-obuka-evidencije-lekarski.md`.

## Korak 3. Pravila pisanja

1. Počni karticom podataka klijenta, zatim tabelom radnih mesta; svako mesto dobija svoj blok opasnosti/štetnosti/rizika/mera – ne piši „za sva mesta isto“ bez osnova.
2. Svaka opasnost iz grupa čl. 8–9 je ili razmotrena, ili izričito „nije primenljivo“ sa razlogom.
3. Zakonska mesta sa povećanim rizikom (visina ≥ 2 m, dubina > 1 m, transport) unesi automatski ako takvih radova ima; za njih – periodičnost obuke 1 godina, lekarski pregledi (Prilog II pravilnika 120/2007: visina 12 meseci, noćni rad 18, transport 12), dozvola za rad (ZBZR čl. 27).
4. Skale rizika opiši u tekstu akta (šta znače bodovi, gde je prag prihvatljivog); tabele računaj programski ili proveri ručno.
5. Mere su konkretne (šta, gde, ko, kada); izostanak roka nije opcija.
6. Koristi aktuelne pozive: ZBZR 35/2023, pravilnik 76/2024, „radna sredina“. Ne citiraj brojeve kojih nema u baseline.
7. Ne ubacuj prava imena zaposlenih i zdravstvene podatke ako nisu potrebni; za demonstraciju koristi anonimizovane primere.

## Korak 4. Samoprovera pre predaje

1. Izvezi nacrt u tekst (UTF-8), pokreni `uv run scripts/lint_akt.py nacrt.txt` iz rs-bzr-akt-review (bez uv-a: `py -3` / `python3`; oznake `⟦POPUNITI⟧` su očekivane – nabroj ih kao otvorena pitanja).
2. Prođi kontrolnu listu odgovarajuće vrste dokumenta (odeljci A–J za akt) i ispravi pronađeno.
3. U odgovoru: šta je pripremljeno, spisak otvorenih polja `⟦POPUNITI⟧`, koje činjenice su potrebne od klijenta, šta treba da proveri licencirano stručno lice pre potpisa. Ne nazivaj dokument „spremnim za potpis“.

## Oblik izlaza

Podrazumevano – Markdown nacrt u radnom folderu. Ako treba Word – koristi docx skill. Ne objavljuj i ne šalji dokument trećim licima bez izričitog zahteva.

## Opseg

Isti kao kod rs-bzr-akt-review: zaštita od požara, katastrofe, otpad i hemikalije nisu pokriveni; ako klijent traži takav dokument, reci da za tu oblast nema proverene normativne osnove.
