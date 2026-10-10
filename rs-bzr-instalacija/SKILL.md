---
name: rs-bzr-instalacija
description: Instalacija i provera okruženja za skillove rs-bzr-akt-review i rs-bzr-akt-izrada – instalira alat uv (koji sam obezbeđuje Python i biblioteke) na Windows-u, macOS-u ili Linux-u, proverava da pomoćne skripte rade i rešava tipične probleme. Koristi OBAVEZNO kada skript ne može da se pokrene jer `uv` nije pronađen ili nije instaliran, kada korisnik kaže „instaliraj“, „podesi“, „ne radi skripta“, „nema Pythona“, „uv nije prepoznat“, i kada ga pozove skill rs-bzr-akt-review ili rs-bzr-akt-izrada. Ako Claude može da izvršava komande na računaru, izvršava ih uz saglasnost korisnika; inače daje tačne komande koje korisnik sam kuca. Odgovara na srpskom.
---

# Instalacija okruženja (uv)

Skillovi za reviziju i izradu akata koriste dve pomoćne skripte (`extract_text.py` – tekst iz Word fajla, `lint_akt.py` – brze provere). Pokreću se alatom **uv**, koji sam preuzme odgovarajući Python i biblioteku `defusedxml` pri prvom pokretanju, bez administratorskih prava. Ovaj skill instalira uv i proveri da sve radi.

**Jezik:** srpski (latinica), kratko i korak po korak. Korisnici su obično stručnjaci za BZR, ne programeri – bez žargona, svaku komandu objasni jednom rečenicom.

## Načelo rada: ništa bez saglasnosti

Instalacija menja korisnikov računar, zato:
1. Pre svake komande koja nešto instalira ili preuzima – **reci šta radi i traži saglasnost** („Instaliram alat uv komandom … Da li da nastavim?“).
2. Ako možeš da izvršavaš komande (Claude Code / alat za terminal) – izvrši ih posle saglasnosti. Ako ne možeš (običan čat) – **daj komande u posebnim blokovima** i zamoli korisnika da ih iskuca i da ti nalepi ispis.
3. Instaliraj **samo uv**. Ne menjaj bezbednosna podešavanja sistema, ne isključuj antivirus, ne traži administratorska prava, ne instaliraj ništa drugo bez posebnog pitanja.
4. Komande koje preuzimaju i izvršavaju skriptu sa interneta (`irm … | iex`, `curl … | sh`) su manje bezbedne od menadžera paketa – koristi ih samo kad `winget`/`brew` nisu dostupni i reci to korisniku. Jedini dozvoljeni izvor je zvanični `astral.sh`.

## Korak 1. Da li već radi?

Proveri:
```
uv --version
```
- Ispisuje verziju → uv postoji. Idi na **Korak 3**.
- „nije prepoznat / command not found“ → idi na Korak 2.

Prvo odredi sistem (Windows / macOS / Linux). Na Windows-u koristi **PowerShell**, ne stari Command Prompt.

## Korak 2. Instalacija uv-a

### Windows (PowerShell)
Prva opcija (preporučena, bez skripti sa interneta):
```
winget install --id=astral-sh.uv -e
```
Ako `winget` nije dostupan ili ne uspe, zvanična skripta (jedna komanda; `ByPass` važi samo za ovu komandu):
```
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### macOS
```
brew install uv
```
ili, ako nema Homebrew-a: `curl -LsSf https://astral.sh/uv/install.sh | sh`

### Linux
```
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Posle instalacije:** PATH se osvežava samo u novom prozoru. Reci korisniku da **zatvori i ponovo otvori terminal** (u Claude Code-u – novi terminal/sesija) pa ponovi `uv --version`. Ako i dalje ne radi, na Windows-u pokušaj sa punom putanjom `%USERPROFILE%\.local\bin\uv.exe --version`.

### Ako instalacija ne može (nema interneta, politika firme blokira skripte, nema prava)
Ne pokušavaj alternativne puteve. Skillovi se pokreću isključivo preko uv-a. Objasni korisniku šta blokira (mreža/proxy, politika računara) i zamoli ga da se obrati IT službi; zatim stani – bez uv-a se automatske provere ne pokreću.

## Korak 3. Provera da skripte rade

Prvo pokretanje preuzima Python i biblioteku, pa traži internet i može potrajati minut.

Iz foldera gde su skillovi (npr. `…/skills/rs-bzr-akt-review`):
```
uv run scripts/extract_text.py --help
uv run scripts/lint_akt.py --help
```
Obe komande treba da ispišu uputstvo za upotrebu (bez greške). Ako postoji i repozitorijum sa testovima:
```
uv run tests/smoke_test.py
```
Očekivano: `REZULTAT: SVE U REDU`.

## Korak 4. Završetak

Kratko javi korisniku:
- šta je instalirano (samo uv; Python i biblioteka se preuzimaju same pri prvom pokretanju);
- da može da pošalje Word (.docx) akt na proveru;

Zatim se vrati zadatku zbog kojeg je instalacija pokrenuta (revizija ili izrada akta).

## Tipični problemi

| Simptom | Rešenje |
|---|---|
| `uv` nije prepoznat posle instalacije | Zatvoriti i ponovo otvoriti terminal; proveriti punu putanju (`%USERPROFILE%\.local\bin\uv.exe` na Windows-u, `~/.local/bin/uv` na macOS/Linux) |
| PowerShell: „running scripts is disabled“ | Koristiti `winget` varijantu ili komandu sa `-ExecutionPolicy ByPass` (važi samo za tu komandu) |
| `winget` nije prepoznat | Stariji Windows ili ograničen računar – koristiti PowerShell skriptu iz Koraka 2 |
| Greška pri preuzimanju (mreža/proxy) | Proveriti internet/proxy; zatražiti od IT-ja pristup `astral.sh`, `github.com` i `pypi.org` |
| Pokvarena slova č, š, ž, ć, đ u izlazu | Skripte pokretati sa opcijom `-o izlaz.txt`; ne koristiti preusmeravanje `>` u PowerShell-u |
| Putanja sa razmacima | Staviti je pod navodnike |
