#!/usr/bin/env python3
"""
entwurfs-check.py — Auto-Patterns fuer /entwurf Phase 4.1

Prueft einen Entwurfs-File gegen die Top-8 wiederkehrenden Findings aus
buch/_meta/entwurfs-qualitaet.md. Output: Markdown-Tabelle.

Aufruf: python scripts/entwurfs-check.py B1-K30
"""
import sys
import re
from pathlib import Path

# Windows-Konsole: stdout auf UTF-8 zwingen (sonst UnicodeEncodeError bei ⚠/—/„")
try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, Exception):
    pass

REPO = Path(__file__).resolve().parent.parent

# === Patterns ===

MONATSNAMEN = [
    "Januar", "Februar", "März", "Maerz", "April",
    "Juni", "Juli", "August",
    "September", "Oktober", "November", "Dezember",
]
MONATE_REGEX = re.compile(r"\b(" + "|".join(MONATSNAMEN) + r")\b")

# 'Mai' nur in Datum-Kontext, nicht als Eigenname
MAI_REGEX = re.compile(
    r"\b(im Mai|des Mai|bis Mai|Mai \d{4}|Anfang Mai|Mitte Mai|Ende Mai|\d+\.\s*Mai)\b"
)

NICHT_SONDERN_REGEX = re.compile(
    r"\bnicht\b[^,.;\n]{1,40},?\s+sondern\b", re.IGNORECASE
)

HALB_REGEX = re.compile(r"\bhalb(?:en?|er?|e?)\s+\w+", re.IGNORECASE)

ANGLIZISMEN = [
    "Debugging", "Debug", "Charge", "Drift", "Setup",
    "Feedback", "Input", "Output", "Update",
    "gecheckt", "gefixt", "Workflow", "Briefing", "Tool",
]
ANGLIZISMEN_REGEX = re.compile(
    r"\b(" + "|".join(ANGLIZISMEN) + r")\b", re.IGNORECASE
)

KLEIDUNG_REGEX = re.compile(r"\b(Jacke|Bluse|Jacken|Blusen|Jackentasche)\b")

METRISCHE_REGEX = re.compile(
    r"\b\d+\s*(Meter|Kilometer|Zentimeter|Millimeter|Kilogramm|cm|km|kg|mm)\b"
)

MORAGH_REGEX = re.compile(r"\bMoragh\b")

SEIN_VERBEN = [
    "lag", "lagen", "war", "waren",
    "stand", "standen", "saß", "saßen", "sass", "sassen",
]
SEIN_VERBEN_REGEX = re.compile(
    r"\b(" + "|".join(SEIN_VERBEN) + r")\b", re.IGNORECASE
)

# Bonus: Negations-Cluster (3+ "kein/nicht/nichts" in einem Absatz)
NEGATION_REGEX = re.compile(r"\b(kein|keine|keinen|keiner|nicht|nichts|niemand)\b", re.IGNORECASE)


# === Hilfsfunktionen ===

def find_pattern(text, pattern):
    """Returns list of (line_num, match_text, snippet)."""
    findings = []
    for i, line in enumerate(text.splitlines(), 1):
        for m in pattern.finditer(line):
            snippet = line.strip()
            if len(snippet) > 110:
                snippet = snippet[:107] + "..."
            findings.append((i, m.group(0), snippet))
    return findings


def check_stakkato(text):
    """3+ aufeinanderfolgende Saetze < 6 Woerter in Prosa-Zeilen (nicht Listen/Header)."""
    findings = []
    lines = text.splitlines()
    for i, line in enumerate(lines, 1):
        s = line.strip()
        if not s or s.startswith("#") or s.startswith("-") or s.startswith("|") or s.startswith("*"):
            continue
        # Prosa-Zeile: zaehle Saetze < 6 Woerter
        sentences = re.split(r"(?<=[.!?])\s+", s)
        run = 0
        triggered = False
        for sent in sentences:
            wc = len(sent.split())
            if 0 < wc < 6 and sent[-1:] in ".!?":
                run += 1
                if run >= 3 and not triggered:
                    snippet = s[:110] + ("..." if len(s) > 110 else "")
                    findings.append((i, "3+ Kurzsaetze", snippet))
                    triggered = True
            else:
                run = 0
    return findings


def check_sein_verben_haeufung(text, block_size=150, threshold=2):
    """Pro 150-Wort-Block: > threshold gleicher Sein-Verb-Form."""
    findings = []
    words = text.split()
    block_idx = 0
    for pos in range(0, len(words), block_size):
        block_text = " ".join(words[pos:pos + block_size])
        counts = {}
        for verb in SEIN_VERBEN:
            c = len(re.findall(r"\b" + verb + r"\b", block_text, re.IGNORECASE))
            if c > threshold:
                counts[verb] = c
        if counts:
            preview = block_text[:100] + ("..." if len(block_text) > 100 else "")
            findings.append((block_idx + 1, counts, preview))
        block_idx += 1
    return findings


def check_negation_cluster(text):
    """Absaetze mit >=4 Negationen (kein/nicht/nichts/niemand)."""
    findings = []
    paragraphs = re.split(r"\n\s*\n", text)
    for idx, para in enumerate(paragraphs):
        s = para.strip()
        if not s or s.startswith("#") or s.startswith("|"):
            continue
        if s.startswith("-") or s.startswith("*"):
            continue
        c = len(NEGATION_REGEX.findall(s))
        if c >= 4:
            preview = s[:100] + ("..." if len(s) > 100 else "")
            findings.append((idx + 1, f"{c}× Negation", preview))
    return findings


def is_thalassien_kapitel(entwurf_text):
    """Heuristik: Wenn Header explizit Moragh als POV/Setting/Timeline nennt → nicht Thalassien."""
    header = "\n".join(entwurf_text.splitlines()[:40])
    if re.search(r"(POV|Setting|Timeline)[^\n]*Moragh", header, re.IGNORECASE):
        return False
    return True


# === Hauptlauf ===

def main():
    if len(sys.argv) < 2:
        print("Aufruf: python scripts/entwurfs-check.py B1-K30")
        sys.exit(1)

    kid = sys.argv[1]
    entwurf_path = REPO / "buch" / "kapitel" / f"{kid}-entwurf.md"
    if not entwurf_path.exists():
        print(f"Datei nicht gefunden: {entwurf_path}")
        sys.exit(1)

    text = entwurf_path.read_text(encoding="utf-8")

    print(f"# Entwurfs-Check: {kid}")
    print()
    print("Auto-Patterns aus `buch/_meta/entwurfs-qualitaet.md`. Findings sind Hinweise — der Autor entscheidet, was raus muss.")
    print()
    print("| # | Pattern | Treffer | Erstes Beispiel |")
    print("|---|---------|--------:|-----------------|")

    n = [0]
    total_findings = [0]

    def report(label, findings):
        n[0] += 1
        if not findings:
            print(f"| {n[0]} | {label} | 0 | — |")
            return
        total_findings[0] += len(findings)
        first = findings[0]
        if isinstance(first[2], str):
            example = f"Z. {first[0]}: {first[2]}"
        elif isinstance(first[1], dict):
            example = f"Block {first[0]}: {first[1]}"
        else:
            example = str(first)
        # Markdown-Pipes escapen
        example = example.replace("|", r"\|")
        if len(findings) > 1:
            example += f" *(+{len(findings) - 1} weitere)*"
        marker = "⚠ " if len(findings) > 0 else ""
        print(f"| {n[0]} | {marker}{label} | {len(findings)} | {example} |")

    # 1. Realweltliche Monatsnamen
    f = find_pattern(text, MONATE_REGEX) + find_pattern(text, MAI_REGEX)
    report("Realweltliche Monatsnamen", f)

    # 2. "Moragh" in Thalassien-Kapiteln (heuristisch)
    if is_thalassien_kapitel(text):
        report('"Moragh" in Thalassien-Kapitel', find_pattern(text, MORAGH_REGEX))
    else:
        n[0] += 1
        print(f'| {n[0]} | "Moragh" in Thalassien-Kapitel | – | (Moragh-Setting -> übersprungen) |')

    # 3. „nicht X, sondern Y"
    report('"nicht X, sondern Y" (Pflicht-Prüfung)', find_pattern(text, NICHT_SONDERN_REGEX))

    # 4. „halb X" Pseudo-Präzision
    report('"halb X" Pseudo-Präzision', find_pattern(text, HALB_REGEX))

    # 5. Anglizismen / Epoche-Bruch
    report("Anglizismen / Epoche-Bruch", find_pattern(text, ANGLIZISMEN_REGEX))

    # 6. Kleidungs-Anachronismen
    report("Kleidungs-Anachronismen (Jacke/Bluse)", find_pattern(text, KLEIDUNG_REGEX))

    # 7. Metrische Maße
    report("Metrische Maßeinheiten", find_pattern(text, METRISCHE_REGEX))

    # 8. Stakkato-Ketten
    report("Stakkato-Ketten (3+ Sätze < 6 W)", check_stakkato(text))

    # Bonus: Sein-Verb-Häufung
    report("Sein-Verb-Häufung (>2×/150-Wort-Block)", check_sein_verben_haeufung(text))

    # Bonus: Negations-Cluster
    report("Negations-Cluster (≥4/Absatz)", check_negation_cluster(text))

    print()
    if total_findings[0] == 0:
        print("**Status:** Alle Patterns sauber.")
    else:
        print(f"**Befunde:** {total_findings[0]} Treffer über {n[0]} Pattern. Manuell prüfen — `buch/_meta/entwurfs-qualitaet.md` für Kontext.")


if __name__ == "__main__":
    main()
