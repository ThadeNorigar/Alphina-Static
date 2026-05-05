#!/usr/bin/env python3
"""
Replace 'YYYY TZ' (Y >= 1500) → 'YYYY UZ' in allen Plot-Files.

Drift-Hintergrund: Aktpläne und Dossiers benutzen historisch 'YYYY TZ' für
UZ-Welt-Jahre (1987 TZ = 1987 UZ). Mit der Konversions-Klärung
2026-05-05 (1 MZ-Monat = 33 TZ-Jahre) sind das eindeutig UZ-Werte.

Sicherheits-Constraints:
- Min-Y = 1500 → schützt echte TZ-Daten (154 TZ, 551 TZ etc.)
- Negative-Lookahead (?!-) → schützt 'TZ-Jahre' (Differenz-Einheit)
- Word-Boundary \b → schützt vor false positives in IDs etc.

Usage:
    python scripts/fix_tz_to_uz.py            # dry-run
    python scripts/fix_tz_to_uz.py --apply    # in-place
"""

import argparse
import os
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
BUCH_DIR = REPO_ROOT / "buch"

# Pattern: vier-stellige Zahl >= 1500, gefolgt von einem oder mehreren
# Whitespace-Zeichen, dann 'TZ' als ganzes Wort (nicht 'TZ-Jahre').
# Akzeptiert auch ' TZ)', ' TZ.', ' TZ,' etc. — alles außer '-'.
PATTERN = re.compile(r'\b(\d{4})(\s+)TZ\b(?!-)')

# Files überspringen
SKIP_PATTERNS = [
    "_archiv",       # Archiv ist unangetastet
    ".OLD.json",     # Backups
    "review/figuren-check-2026-04-22.md",  # Edge-Cases manuell
]


def replace_match(m: re.Match) -> str:
    """Pattern-Match → ersetzter String. Nur wenn Y >= 1500."""
    year = int(m.group(1))
    if year < 1500:
        return m.group(0)  # unverändert
    sep = m.group(2)
    return f"{year}{sep}UZ"


def process_file(path: Path) -> tuple[int, list[tuple[int, str, str]]]:
    """Returns (n_changes, list of (line_no, before, after))."""
    try:
        with path.open(encoding="utf-8") as f:
            content = f.read()
    except (UnicodeDecodeError, PermissionError):
        return 0, []

    changes = []
    new_content = []
    last_end = 0
    line_no = 1
    n = 0
    for m in PATTERN.finditer(content):
        year = int(m.group(1))
        if year < 1500:
            continue
        # Berechne Zeilen-Nr
        line_no = content[: m.start()].count("\n") + 1
        # Kontext extrahieren
        line_start = content.rfind("\n", 0, m.start()) + 1
        line_end = content.find("\n", m.end())
        if line_end == -1:
            line_end = len(content)
        line_text = content[line_start:line_end]
        new_line = PATTERN.sub(replace_match, line_text)
        if new_line != line_text:
            # Sample für Bericht
            changes.append((line_no, line_text.strip()[:90], new_line.strip()[:90]))
            n += 1

    new_content_str = PATTERN.sub(replace_match, content)
    return (1 if new_content_str != content else 0), changes


def collect_files() -> list[Path]:
    files = []
    for ext in ("*.md", "*.json"):
        for p in BUCH_DIR.rglob(ext):
            rel = p.relative_to(REPO_ROOT).as_posix()
            if any(skip in rel for skip in SKIP_PATTERNS):
                continue
            files.append(p)
    return files


def main() -> int:
    ap = argparse.ArgumentParser(description="Replace 'YYYY TZ' (Y>=1500) → 'YYYY UZ'")
    ap.add_argument("--apply", action="store_true",
                    help="In-place schreiben (sonst dry-run)")
    args = ap.parse_args()

    files = collect_files()
    total_files_changed = 0
    total_changes = 0
    samples_per_file = {}

    for path in files:
        try:
            with path.open(encoding="utf-8") as f:
                content = f.read()
        except (UnicodeDecodeError, PermissionError):
            continue

        # Zähle Vorkommen
        matches = [m for m in PATTERN.finditer(content) if int(m.group(1)) >= 1500]
        if not matches:
            continue

        new_content = PATTERN.sub(replace_match, content)
        if new_content == content:
            continue

        rel = path.relative_to(REPO_ROOT).as_posix()
        total_files_changed += 1
        total_changes += len(matches)

        # Sample: erste 3 Treffer mit Kontext
        samples = []
        for m in matches[:3]:
            year = int(m.group(1))
            line_start = content.rfind("\n", 0, m.start()) + 1
            line_end = content.find("\n", m.end())
            if line_end == -1: line_end = len(content)
            line_text = content[line_start:line_end].strip()
            line_no = content[: m.start()].count("\n") + 1
            new_line = PATTERN.sub(replace_match, line_text)
            samples.append((line_no, year, line_text[:90], new_line[:90]))
        samples_per_file[rel] = (len(matches), samples)

        if args.apply:
            with path.open("w", encoding="utf-8") as f:
                f.write(new_content)

    # Report
    print(f"=== TZ → UZ Replace-Report ===")
    print(f"Files mit Treffern:  {total_files_changed}")
    print(f"Gesamt-Treffer:      {total_changes}")
    print()

    for rel, (n, samples) in sorted(samples_per_file.items()):
        print(f"--- {rel} ({n} Treffer) ---")
        for line_no, year, before, after in samples:
            print(f"  Z.{line_no}  {year} TZ → {year} UZ")
            print(f"    vor:  {before}")
            print(f"    nach: {after}")
        if n > 3:
            print(f"  ... und {n - 3} weitere")
        print()

    if args.apply:
        print(f"✓ {total_files_changed} Files geschrieben.")
    else:
        print(f"[dry-run] Nichts geschrieben. Mit --apply erneut ausführen.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
