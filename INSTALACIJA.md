# Instalacija

Dva skilla: `rs-bzr-akt-review` (revizija) i `rs-bzr-akt-izrada` (izrada nacrta). Instalirajte **oba** – izrada koristi propise i kontrolne liste iz revizije.

## 1. uv (instalira i pokreće Python – ne treba posebno instalirati Python)
Pomoćne skripte (`extract_text.py`, `lint_akt.py`) izdvajaju tekst iz Word dokumenta i rade brze provere. Pokreću se alatom [uv](https://docs.astral.sh/uv/): on sam preuzme odgovarajući Python i potrebnu biblioteku (`defusedxml`) pri prvom pokretanju, bez administratorskih prava.

### Windows (PowerShell)
```
winget install --id=astral-sh.uv -e
```
ili, ako `winget` nije dostupan:
```
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```
Zatvorite i ponovo otvorite PowerShell, pa proverite: `uv --version`.

### macOS / Linux
```
brew install uv
```
ili `curl -LsSf https://astral.sh/uv/install.sh | sh`. Provera: `uv --version`.

Prvo pokretanje skripte traži internet (preuzimanje Pythona i `defusedxml`); posle toga radi iz keša.

## 2. Dodavanje skillova u Claude
Pripremite arhive iz foldera repozitorijuma:
```
uv run package.py
```
Dobijaju se `dist/rs-bzr-akt-review.skill` i `dist/rs-bzr-akt-izrada.skill`.

- **Claude (aplikacija / claude.ai):** u podešavanjima otvorite odeljak za skillove (Settings → Capabilities → Skills) i otpremite oba `.skill` fajla. Tačni nazivi menija zavise od verzije aplikacije.
- **Claude Code:** kopirajte oba foldera (`rs-bzr-akt-review`, `rs-bzr-akt-izrada`) u folder `skills` unutar `.claude`:
  - Windows: `%USERPROFILE%\.claude\skills\`
  - macOS/Linux: `~/.claude/skills/`

## 3. Provera da radi
1. Iz foldera repozitorijuma: `uv run tests/smoke_test.py`. Treba da ispiše `REZULTAT: SVE U REDU`.
2. U Claude-u priložite **Word (.docx)** akt i napišite: „Proveri ovaj akt o proceni rizika.“ Za PDF skill će tražiti Word fajl.

Ručno pokretanje skripti:
```
uv run rs-bzr-akt-review/scripts/extract_text.py akt.docx -o akt.txt
uv run rs-bzr-akt-review/scripts/lint_akt.py akt.txt
```

## Najčešći problemi
- `uv` nije prepoznat posle instalacije → zatvorite i ponovo otvorite terminal (PATH se osvežava pri novom prozoru).
- PowerShell blokira skripte (ExecutionPolicy) → koristite `winget` varijantu, ili komandu iz drugog bloka sa `-ExecutionPolicy ByPass`.
- Korporativni računar bez interneta ili sa proxy-jem → uv mora da preuzme Python/biblioteku; zatražite od IT-ja pristup ili instalirajte Python 3.9+ ručno i koristite `py -3` / `python3` umesto `uv run` (skripte rade i bez uv-a, samo uz upozorenje o `defusedxml`).
- Slova č, š, ž, ć, đ su pokvarena u izlazu → koristite opciju `-o`, ne preusmeravanje `>` u PowerShell-u.
- Putanja sa razmacima → stavite je pod navodnike.
