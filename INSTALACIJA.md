# Instalacija

Dva skilla: `rs-bzr-akt-review` (revizija) i `rs-bzr-akt-izrada` (izrada nacrta). Instalirajte **oba** – izrada koristi propise i kontrolne liste iz revizije.

## 1. Python (potreban samo za pomoćne skripte)
Skripte (`extract_text.py`, `lint_akt.py`) izdvajaju tekst iz Word dokumenta i rade brze provere. Bez Pythona sami kontrolne liste i dalje postoje, ali automatske provere neće raditi. Potreban je **Python 3.9 ili noviji**; dodatne biblioteke nisu potrebne.

### Windows
1. Proverite da li već postoji: otvorite **PowerShell** i ukucajte `py -3 --version`. Ako ispiše `Python 3.x.x` – gotovo.
2. Ako ne postoji, instalirajte jednom od dve opcije:
   - preuzmite instalaciju sa https://www.python.org/downloads/ i u prvom prozoru **uključite „Add python.exe to PATH“**, zatim „Install Now“; ili
   - u PowerShell-u: `winget install Python.Python.3.12`
3. Zatvorite i ponovo otvorite PowerShell, pa `py -3 --version`.
4. Opciono (bezbednije čitanje Word fajlova): `py -3 -m pip install defusedxml`

### macOS
`python3 --version`. Ako nema: `brew install python` ili instalacija sa python.org.

### Linux
`python3 --version`. Ako nema: `sudo apt install python3`.

## 2. Dodavanje skillova u Claude
Pripremite arhive:
```
python package.py          # macOS/Linux: python3 package.py ; Windows: py -3 package.py
```
Dobijaju se `dist/rs-bzr-akt-review.skill` i `dist/rs-bzr-akt-izrada.skill`.

- **Claude (aplikacija / claude.ai):** u podešavanjima otvorite odeljak za skillove (Settings → Capabilities → Skills) i otpremite oba `.skill` fajla. Tačni nazivi menija zavise od verzije aplikacije.
- **Claude Code:** kopirajte oba foldera (`rs-bzr-akt-review`, `rs-bzr-akt-izrada`) u folder `skills` unutar `.claude`:
  - Windows: `%USERPROFILE%\.claude\skills\`
  - macOS/Linux: `~/.claude/skills/`

Napomena: tačne korake otpremanja u aplikaciji nismo proveravali na svakoj verziji – ako se meni razlikuje, potražite „Skills“ u podešavanjima.

## 3. Provera da radi
1. Iz foldera repozitorijuma: `py -3 tests/smoke_test.py` (Windows) ili `python3 tests/smoke_test.py`. Treba da ispiše `REZULTAT: SVE U REDU`.
2. U Claude-u priložite **Word (.docx)** akt i napišite: „Proveri ovaj akt o proceni rizika.“ Za PDF skill će tražiti Word fajl.

## Najčešći problemi
- `python` nije prepoznat na Windows-u → koristite `py -3`, ili ponovo instalirajte Python sa uključenim „Add python.exe to PATH“.
- Slova č, š, ž, ć, đ su pokvarena u izlazu → koristite opciju `-o` (`py -3 rs-bzr-akt-review\scripts\extract_text.py akt.docx -o akt.txt`), ne preusmeravanje `>` u PowerShell-u.
- Putanja sa razmacima → stavite je pod navodnike.
