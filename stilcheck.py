#!/usr/bin/env python3
"""
stilcheck.py — Automatischer Stil-Check für Kapitel von "Der Riss"

Prüft ein Kapitel gegen die harten Limits aus buch/02-stilregeln-v2.md.
Findet rhetorische Signposts, hypothetische Konstruktionen, Vergleiche,
Stakkato-Dichte und weitere Muster.

Nutzung:
    python stilcheck.py buch/kapitel/08-maren.md
    python stilcheck.py buch/kapitel/*.md          # mehrere Dateien
    python stilcheck.py buch/kapitel/08-maren.md --strict  # exit 1 bei Verstößen

Exit Code:
    0 = alle Limits eingehalten
    1 = mindestens ein hartes Limit überschritten (mit --strict)
    2 = Datei nicht lesbar / Fehler
"""

import re
import sys
import argparse
from pathlib import Path


# Harte Limits aus buch/02-stilregeln-v2.md
# Hinweis: "nicht_x_sondern_y" hat KEINE numerische Schwelle (Stand 2026-04-26).
# Pflicht-Pruefung pro Einsatz — siehe Master in buch/02-stilregeln-v2.md (Tabelle "Harte Limits").
# Das Tool listet alle Treffer mit Status "PRUEFEN", die Bewertung pro Vorkommen
# laeuft im Stil-Check-Skill bzw. in der Ausarbeitung.
LIMITS = {
    "wie_vergleiche": 2,      # metaphorische "wie..."-Vergleiche (Master: buch/02-stilregeln-v2.md)
    "als_hypothetisch": 6,    # "als hätte/wäre/könnte..."
    "deppenapostroph": 0,     # Haron's, Klaus's etc.
    # "stakkato_passagen" entfernt: Pflicht-Pruefung pro Einsatz, keine Schwelle
    # Master: buch/02-stilregeln-v2.md Sektion "Stakkato-Dosierung"
}


# Regex-Patterns
# "nicht X — sondern Y" mit Gedankenstrich (—, –, -)
# Erfasst auch "Nicht X — sondern Y" am Satzanfang
NICHT_SONDERN_DASH = re.compile(
    r'[Nn]icht\s+[^.!?—–\-]{1,60}?\s*[—–]\s*sondern\s+',
    re.UNICODE
)

# "nicht X, sondern Y" mit Komma (weniger hart, aber auch eine Form)
NICHT_SONDERN_COMMA = re.compile(
    r'[Nn]icht\s+[^.!?,]{1,60}?,\s*sondern\s+',
    re.UNICODE
)

# Hypothetische "als hätte/wäre/würde..."-Konstruktionen
ALS_HYPOTHETISCH = re.compile(
    r'\bals\s+(hätte|wäre|würde|sei|bestünde|zöge|hebe|schöbe|stecke|folge|'
    r'verbrenne|gehöre|wüsste|riebe|könnte|lasse|trüge|wollte|reagiere|'
    r'teilte|läge|käme|ginge|sähe|spräche|hielt|wisse|mache|tue)\b',
    re.UNICODE
)

# Deppenapostroph bei Figurennamen
DEPPENAPOSTROPH = re.compile(
    r"\b(Haron|Klaus|Vesper|Sorel|Alphina|Maren|Edric|Runa|Jara|Esther|Tohl|"
    r"Halvard|Henrik|Varen|Nyr|Talven|Keldan|Elke)'s\b",
    re.UNICODE
)

# Metaphorische "wie..."-Vergleiche — nur die Form "wie etwas das..."
# und "wie ein/eine/Substantiv das/die/der + Relativsatz"
# Diese rhetorische Form ist der eigentliche Ziel-Marker aus den Stilregeln.
WIE_VERGLEICH_STARK = re.compile(
    r'\bwie\s+(etwas|ein|eine|einen|einem|einer)\s+[A-Za-zäöüßÄÖÜ]+\s+(das|die|der|den|dem|des)\b',
    re.UNICODE
)

# Alternative: "wie X + Substantiv" OHNE Relativsatz (einfache Vergleiche)
# Diese sind weniger hart begrenzt, werden aber informativ gezählt.
WIE_VERGLEICH_WEICH = re.compile(
    r'\bwie\s+(ein|eine|einen|einem|einer)\s+[A-ZÄÖÜ][a-zäöüß]+',
    re.UNICODE
)


def count_fragments(text: str) -> int:
    """
    Zählt Stakkato-Passagen.
    Eine Stakkato-Passage = 3+ aufeinanderfolgende Fragmentsätze.
    Fragmentsatz = < 4 Wörter UND kein finites Verb.
    Alleinstehende Einwortsätze (Hammerschlag) sind KEINE Passage.
    """
    # Finite Verbformen (Präteritum primär für dieses Buch)
    verb_pat = re.compile(
        r'\b(war|hatte|ging|kam|sah|lag|stand|saß|sagte|dachte|wusste|hielt|'
        r'fiel|rief|trat|nahm|gab|fand|hörte|roch|schlug|schrieb|spürte|'
        r'atmete|wartete|blickte|lächelte|nickte|zog|legte|drückte|schob|'
        r'trank|aß|ist|hat|geht|kommt|sieht|liegt|steht|sitzt|war|waren|'
        r'waren|wurde|wurden|ließ|musste|konnte|wollte|sollte|dürfte)\b',
        re.UNICODE | re.IGNORECASE
    )
    passages = 0
    current_run = 0
    # Sätze aus dem gesamten Text
    body = re.sub(r'^#.*$', '', text, flags=re.MULTILINE)
    body = re.sub(r'^---.*$', '', body, flags=re.MULTILINE)
    # Absätze bewahren
    sents = re.split(r'(?<=[.!?])\s+', body)
    for sent in sents:
        s = sent.strip().rstrip(".!?—–\"'")
        if not s or s.startswith("*"):
            continue
        words = s.split()
        has_verb = bool(verb_pat.search(s))
        is_fragment = len(words) < 4 and not has_verb
        if is_fragment:
            current_run += 1
        else:
            if current_run >= 3:
                passages += 1
            current_run = 0
    if current_run >= 3:
        passages += 1
    return passages


def check_file(filepath: Path) -> dict:
    """Prüft eine Datei und gibt ein Dict mit Findings zurück."""
    try:
        text = filepath.read_text(encoding="utf-8")
    except Exception as e:
        return {"error": str(e)}

    # Zeilen für Locations
    lines = text.split("\n")

    # 1. "nicht X — sondern Y" (harte Form mit Gedankenstrich)
    nicht_sondern_dash_hits = []
    for lineno, line in enumerate(lines, 1):
        for m in NICHT_SONDERN_DASH.finditer(line):
            nicht_sondern_dash_hits.append((lineno, m.group(0)[:80]))

    # 1b. "nicht X, sondern Y" (weiche Form mit Komma) — informativ
    nicht_sondern_comma_hits = []
    for lineno, line in enumerate(lines, 1):
        # nicht matchen, wenn schon mit Gedankenstrich
        if NICHT_SONDERN_DASH.search(line):
            continue
        for m in NICHT_SONDERN_COMMA.finditer(line):
            nicht_sondern_comma_hits.append((lineno, m.group(0)[:80]))

    # 2. "als hätte/wäre..."-Konstruktionen
    als_hits = []
    for lineno, line in enumerate(lines, 1):
        for m in ALS_HYPOTHETISCH.finditer(line):
            als_hits.append((lineno, m.group(0)))

    # 3a. "wie etwas das..."-Vergleiche (harte Form)
    wie_stark_hits = []
    for lineno, line in enumerate(lines, 1):
        for m in WIE_VERGLEICH_STARK.finditer(line):
            wie_stark_hits.append((lineno, m.group(0)))

    # 3b. "wie ein/eine Substantiv" (weiche Form, informativ)
    wie_weich_hits = []
    for lineno, line in enumerate(lines, 1):
        for m in WIE_VERGLEICH_WEICH.finditer(line):
            wie_weich_hits.append((lineno, m.group(0)))

    # 4. Deppenapostroph
    apostroph_hits = []
    for lineno, line in enumerate(lines, 1):
        for m in DEPPENAPOSTROPH.finditer(line):
            apostroph_hits.append((lineno, m.group(0)))

    # 5. Stakkato
    stakkato_passagen = count_fragments(text)

    # Wortzahl (ohne Markdown-Header)
    body = re.sub(r'^#.*$', '', text, flags=re.MULTILINE)
    body = re.sub(r'^---.*$', '', body, flags=re.MULTILINE)
    word_count = len(body.split())

    return {
        "file": str(filepath),
        "words": word_count,
        "nicht_sondern_dash": nicht_sondern_dash_hits,
        "nicht_sondern_comma": nicht_sondern_comma_hits,
        "als_hypothetisch": als_hits,
        "wie_vergleich_stark": wie_stark_hits,
        "wie_vergleich_weich": wie_weich_hits,
        "deppenapostroph": apostroph_hits,
        "stakkato_passagen": stakkato_passagen,
    }


def format_report(result: dict) -> tuple[str, bool]:
    """Formatiert das Ergebnis als Report. Gibt (text, has_violations) zurück."""
    if "error" in result:
        return f"FEHLER: {result['error']}", True

    violations = False
    lines = []
    lines.append(f"## Stil-Check: {result['file']}")
    lines.append(f"Wörter: {result['words']}")
    lines.append("")
    lines.append("| Muster | Anzahl | Limit | Status |")
    lines.append("|--------|--------|-------|--------|")

    # nicht X — sondern Y — Pflicht-Pruefung pro Einsatz, keine numerische Schwelle
    # Master: buch/02-stilregeln-v2.md (Tabelle "Harte Limits" — Antithese)
    n = len(result["nicht_sondern_dash"])
    status = "PRUEFEN" if n > 0 else "OK"
    lines.append(f"| nicht X — sondern Y (Gedankenstrich) | {n} | Pflicht-Pruefung | {status} |")

    # Hypothetische als-Konstruktionen
    n = len(result["als_hypothetisch"])
    lim = LIMITS["als_hypothetisch"]
    status = "OK" if n <= lim else "UEBER"
    if n > lim:
        violations = True
    lines.append(f"| als hätte/wäre... (hypothetisch) | {n} | {lim} | {status} |")

    # wie etwas das... (harter Vergleich)
    n_stark = len(result["wie_vergleich_stark"])
    lim = LIMITS["wie_vergleiche"]
    status = "OK" if n_stark <= lim else "UEBER"
    if n_stark > lim:
        violations = True
    lines.append(f"| wie etwas das... (hart) | {n_stark} | {lim} | {status} |")

    # wie ein/eine + Substantiv (weich, informativ)
    n_weich = len(result["wie_vergleich_weich"])
    lines.append(f"| wie ein/eine Subst. (weich, Info) | {n_weich} | — | — |")

    # Deppenapostroph
    n = len(result["deppenapostroph"])
    lim = LIMITS["deppenapostroph"]
    status = "OK" if n <= lim else "UEBER"
    if n > lim:
        violations = True
    lines.append(f"| Deppenapostroph (Haron's) | {n} | {lim} | {status} |")

    # Stakkato — Pflicht-Pruefung pro Einsatz, keine numerische Schwelle
    # Master: buch/02-stilregeln-v2.md Sektion "Stakkato-Dosierung"
    n = result["stakkato_passagen"]
    status = "PRUEFEN" if n > 0 else "OK"
    lines.append(f"| Stakkato-Passagen | {n} | Pflicht-Pruefung | {status} |")

    # Details bei Verstößen
    if result["nicht_sondern_dash"]:
        lines.append("")
        lines.append("### nicht X — sondern Y (Gedankenstrich, hart)")
        for lineno, snippet in result["nicht_sondern_dash"]:
            lines.append(f"  Z{lineno}: {snippet}...")

    if result["nicht_sondern_comma"]:
        lines.append("")
        lines.append("### nicht X, sondern Y (Komma, weich, informativ)")
        for lineno, snippet in result["nicht_sondern_comma"][:10]:
            lines.append(f"  Z{lineno}: {snippet}...")
        if len(result["nicht_sondern_comma"]) > 10:
            lines.append(f"  ... und {len(result['nicht_sondern_comma']) - 10} weitere")

    if len(result["als_hypothetisch"]) > LIMITS["als_hypothetisch"]:
        lines.append("")
        lines.append("### als hätte/wäre... (ÜBER LIMIT)")
        for lineno, phrase in result["als_hypothetisch"]:
            lines.append(f"  Z{lineno}: {phrase}")

    if len(result["wie_vergleich_stark"]) > LIMITS["wie_vergleiche"]:
        lines.append("")
        lines.append("### wie etwas das... (ÜBER LIMIT)")
        for lineno, phrase in result["wie_vergleich_stark"]:
            lines.append(f"  Z{lineno}: {phrase}")

    if result["deppenapostroph"]:
        lines.append("")
        lines.append("### Deppenapostroph (HART, 0 erlaubt)")
        for lineno, phrase in result["deppenapostroph"]:
            lines.append(f"  Z{lineno}: {phrase}")

    return "\n".join(lines), violations


def main():
    parser = argparse.ArgumentParser(
        description="Stil-Check für Kapitel von Der Riss"
    )
    parser.add_argument("files", nargs="+", help="Kapitel-Dateien (.md)")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit 1 bei Verstößen (für CI/Hooks)",
    )
    args = parser.parse_args()

    any_violation = False
    for f in args.files:
        path = Path(f)
        if not path.exists():
            print(f"FEHLER: {f} nicht gefunden", file=sys.stderr)
            any_violation = True
            continue
        result = check_file(path)
        report, violated = format_report(result)
        print(report)
        print()
        if violated:
            any_violation = True

    if args.strict and any_violation:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
