#!/usr/bin/env python3
"""Brza mehanička provera teksta akta (posle extract_text.py).

Upotreba:  python lint_akt.py <tekst.txt | -> [--type risk|gradiliste|nalaz|auto] [--today YYYY-MM-DD]

Ovo su HEURISTIKE: nalaze sumnjiva mesta, a odluku donosi revizor. Ispisuje listu
nalaza „ŠIFRA – opis – red“. Ništa ne ispravlja. Samo standardna biblioteka.
Proverava: zastarele pozive i termine, oznake nedovršenosti, mešanje pisama u rečima,
prisustvo ključnih delova akta o proceni rizika, brojeve licenci, datume u dalekoj
budućnosti, usaglašenost tabela rizika (verovatnoća × težina = nivo).
"""
import argparse
import datetime as dt
import re
import sys
from collections import defaultdict

CYR = re.compile(r"[Ѐ-ӿ]")
LAT = re.compile(r"[A-Za-zČčĆćŽžŠšĐđ]")

OBSOLETE = [
    (r"101\s*/\s*(05|2005)", "OBS-ZAKON", "Poziv na zakon o BZR 101/2005 (zamenjen zakonom 35/2023)"),
    (r"\b72\s*/\s*(06|2006)\b", "OBS-PRAV-RIZIK", "Poziv na stari pravilnik o proceni rizika 72/2006 (zamenjen 76/2024)"),
    (r"\b(94\s*/\s*(06|2006)|15\s*/\s*2023)\b", "OBS-PRAV-PREGLED", "Poziv na stari pravilnik o pregledu opreme (94/2006 ili 15/2023; zamenjen 76/2024)"),
    (r"radn(a|oj|e|u)\s+okolin|радн(а|ој|е|у)\s+околин", "OBS-TERM", "Termin „radna okolina“ (u novim aktima „radna sredina“)"),
    (r"zakon\s+o\s+zaštiti\s+na\s+radu|закон\s+о\s+заштити\s+на\s+раду", "OBS-ZZNR", "„Zakon o zaštiti na radu“ – zastareli naziv"),
    (r"\b31\s*/\s*92\b|\b53\s*/\s*97\b", "OBS-STARO-92-97", "Poziv na veoma stari propis (31/92 ili 53/97) – proveriti da li je zamenjen"),
    (r"\b121\s*/\s*(12|2012)\b", "OBS-ELABORAT", "Poziv na pravilnik o elaboratu 121/2012 (zamenjen 4/2025)"),
]

PLACEHOLDERS = [
    (r"⟦[^⟧\n]{0,80}⟧", "PH-OTVORENO-POLJE", "Otvoreno polje ⟦POPUNITI⟧ (očekivano u nacrtu, ne u konačnoj verziji)"),
    (r"\bXXX+\b|\bTBD\b|\bTODO\b|\?\?\?+", "PH-OZNAKA", "Oznaka nedovršenosti"),
    (r"_{3,}", "PH-PRAZNO", "Prazno polje (donja crta)"),
    (r"\.{5,}|…{2,}", "PH-TACKICE", "Prazno polje (tačkice)"),
    (r"\[[^\]\n]{1,60}\]", "PH-ZAGRADA", "Tekst u uglastim zagradama – možda nepopunjen šablon"),
    (r"<[A-Za-zА-Яа-я][^>\n]{1,40}>", "PH-UGAONA", "Tekst u špicastim zagradama – možda nepopunjen šablon"),
]

RISK_PARTS = [
    ("Deo 1: opšti podaci o poslodavcu", r"op[sš]t[ie]\s+podac|општи\s+подац|poslovno\s+ime|пословно\s+име|matični\s+broj|ПИБ|PIB"),
    ("Deo 2: opis procesa/sredstava za rad", r"tehnološk|технолошк|radnog\s+procesa|радног\s+процеса|sredstava\s+za\s+rad|средстава\s+за\s+рад"),
    ("Deo 3: organizacija rada", r"organizacij\w+\s+rada|организациј\w+\s+рада|sistematizac|систематизац"),
    ("Deo 4: opasnosti i štetnosti", r"opasnost\w*\s+i\s+štetnost|опасност\w*\s+и\s+штетност|štetnosti|штетности"),
    ("Deo 5: procena rizika", r"procen\w+\s+rizik|процен\w+\s+ризик|verovatno[cć]|вероватно[ћc]|te[zž]in|тежин"),
    ("Deo 6: mere", r"\bmer[ae]\b|\bмер[еа]\b|način\s+i\s+rok|начин\s+и\s+рок"),
    ("Deo 7: zaključak", r"zaklju[cč]ak|закључак"),
    ("Deo 8: izmene i dopune", r"izmen\w+\s+i\s+dopun|измен\w+\s+и\s+допун"),
    ("Mesta sa povećanim rizikom", r"povećan\w+\s+rizik|повећан\w+\s+ризик"),
    ("Izjava poslodavca o primeni mera", r"izjav\w+|изјав\w+|obavezuje\s+se|обавезује\s+се"),
]


def line_of(text, pos):
    return text.count("\n", 0, pos) + 1


def find_all(patterns, text, flags=re.I):
    out = []
    for rx, code, desc in patterns:
        for m in re.finditer(rx, text, flags):
            out.append((code, f"{desc}: „{m.group(0).strip()[:50]}“", line_of(text, m.start())))
    return out


def mixed_script_words(text):
    out = []
    for m in re.finditer(r"\w{3,}", text):
        w = m.group(0)
        if CYR.search(w) and re.search(r"[A-Za-z]", w):
            out.append(("MESANO-PISMO", f"Reč meša ćirilicu i latinicu: „{w}“", line_of(text, m.start())))
    return out[:30]


def script_ratio(text):
    c, l = len(CYR.findall(text)), len(LAT.findall(text))
    tot = c + l
    if tot < 200:
        return []
    if min(c, l) / tot > 0.15:
        return [("MESANO-PISMO-DOK", f"U dokumentu su pomešani ćirilica ({c}) i latinica ({l}) – proveriti ujednačenost pisma", 1)]
    return []


def licence_check(text):
    if not re.search(r"licenc|лиценц", text, re.I):
        return [("LICENCA-NEMA", "Reč „licenca“ se ne pojavljuje: nema podataka o licenci procenjivača (pravilnik 76/2024 čl. 4)", 1)]
    nums = re.findall(r"(?:licenc\w*|лиценц\w*)[^\n]{0,60}?\b(\d{2,}[\w\-/\.]*)", text, re.I)
    if not nums:
        return [("LICENCA-BROJ", "Licenca se pominje, ali pored nje nije pronađen broj", 1)]
    return []


def future_dates(text, today):
    out = []
    for m in re.finditer(r"\b(\d{1,2})\.\s?(\d{1,2})\.\s?(20\d{2})\.?", text):
        d, mo, y = map(int, m.groups())
        try:
            dd = dt.date(y, mo, d)
        except ValueError:
            out.append(("DATUM-NEVAZECI", f"Nevažeći datum „{m.group(0)}“", line_of(text, m.start())))
            continue
        if dd > today + dt.timedelta(days=365 * 3):
            out.append(("DATUM-DALEKO", f"Datum veoma daleko u budućnosti: {m.group(0)} – greška u kucanju?", line_of(text, m.start())))
    return out[:20]


def risk_tables(text):
    """Traži redove oblika … a | b | c (mali celi brojevi) i proverava c == a*b i jednoznačnost."""
    rows = []
    for i, line in enumerate(text.splitlines(), 1):
        cells = [c.strip() for c in re.split(r"\||\t", line)]
        nums = [(idx, int(c)) for idx, c in enumerate(cells) if re.fullmatch(r"\d{1,2}", c)]
        if len(nums) >= 3:
            a, b, c = nums[-3][1], nums[-2][1], nums[-1][1]
            if 1 <= a <= 10 and 1 <= b <= 10:
                rows.append((i, a, b, c))
    out = []
    if len(rows) < 4:
        return out
    mult = sum(1 for _, a, b, c in rows if a * b == c)
    if mult / len(rows) >= 0.6:
        for i, a, b, c in rows:
            if a * b != c:
                out.append(("RIZIK-ARITMETIKA", f"Red: {a} × {b} = {a*b}, a u tabeli piše {c}", i))
    mapping = defaultdict(set)
    for _, a, b, c in rows:
        mapping[(a, b)].add(c)
    for (a, b), vals in mapping.items():
        if len(vals) > 1:
            out.append(("RIZIK-NEUSAGLASENO", f"Kombinacija ({a}, {b}) daje različite rezultate {sorted(vals)}", 0))
    return out[:30]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--type", default="auto", choices=["auto", "risk", "gradiliste", "nalaz"])
    ap.add_argument("--today", default=None)
    a = ap.parse_args()
    if hasattr(sys.stdout, "reconfigure"):  # Windows konzola: ne sme da pukne na č, š, ž, ć, đ
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if a.file == "-":
        text = sys.stdin.buffer.read().decode("utf-8-sig", errors="replace")
    else:
        text = open(a.file, encoding="utf-8-sig", errors="replace").read()
    today = dt.date.fromisoformat(a.today) if a.today else dt.date.today()

    t = a.type
    if t == "auto":
        if re.search(r"akt\s+o\s+proceni\s+rizika|акт\s+о\s+процени\s+ризика", text, re.I):
            t = "risk"
        elif re.search(r"elaborat|елаборат|gradili[sš]t|градилишт", text, re.I):
            t = "gradiliste"
        elif re.search(r"stručni\s+nalaz|стручни\s+налаз|izveštaj\s+o\s+ispitivanju|извештај\s+о\s+испитивању", text, re.I):
            t = "nalaz"
    findings = []
    findings += find_all(OBSOLETE, text)
    findings += find_all(PLACEHOLDERS, text)
    findings += mixed_script_words(text)
    findings += script_ratio(text)
    findings += future_dates(text, today)
    if t in ("risk", "gradiliste", "nalaz"):
        findings += licence_check(text)
    if t == "risk":
        for name, rx in RISK_PARTS:
            if not re.search(rx, text, re.I):
                findings.append(("DEO-NEDOSTAJE", f"Nisu pronađeni znaci odeljka: {name}", 1))
        findings += risk_tables(text)
        if not re.search(r"\brok\b|\brokovi\b|рок", text, re.I) or not re.search(r"odgovorn|одговорн", text, re.I):
            findings.append(("MERE-ODGOVORNI", "Nema reči „rok“ i/ili „odgovorni“ – mere možda nemaju rokove/odgovorna lica", 1))

    print(f"# lint_akt: {a.file} (tip: {t}, datum: {today})")
    if not findings:
        print("Nema nalaza (to ne dokazuje da nema grešaka).")
        return
    groups = defaultdict(list)
    for code, desc, ln in findings:
        groups[code].append((desc, ln))
    for code in sorted(groups):
        items = sorted(groups[code], key=lambda x: x[1])
        desc0, ln0 = items[0]
        loc = f"red {ln0}" if ln0 else "—"
        if len(items) == 1:
            print(f"- [{code}] {desc0} ({loc})")
        else:
            lines = ", ".join(str(l) for _, l in items[:6] if l)
            print(f"- [{code}] ×{len(items)} – npr. {desc0} ({loc}); redovi: {lines}{'…' if len(items) > 6 else ''}")
    print(f"\nUkupno nalaza: {len(findings)} u {len(groups)} grupa. Heuristike – potvrdi u tekstu.")


if __name__ == "__main__":
    sys.exit(main())
