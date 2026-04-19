#!/usr/bin/env python3
"""
Einmaliges Migrations-Skript: fügt YAML-Frontmatter in bestehende Figuren-Dossiers ein.

Greift NICHT in den Body ein. Wenn Frontmatter bereits existiert, wird die Datei
übersprungen (idempotent).

Felder:
  - name:      aus erster H1-Zeile extrahiert (bis " — ")
  - slug:      aus Dateiname
  - typ:       aus Ordner (pov/ → hauptfigur, nebenfiguren/ → nebenfigur)
  - pov:       true für pov/, false für nebenfiguren/
  - reihenfolge: manuell sortierbar über Override-Map unten

Detail-Felder (welt, fraktion, alter, rolle) werden leer gelassen und können
nach Bedarf händisch ergänzt werden.
"""

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
BUCH = ROOT / "buch"

# Manuelle Reihenfolge-Hints für Sortierung auf der Website (höher = prominenter).
# Ungenannte Figuren bekommen Reihenfolge 0.
REIHENFOLGE = {
    "alphina": 100, "sorel": 95, "vesper": 90, "maren": 85,
    "runa": 80, "elke": 75, "varen": 70,
    "nyr": 65, "talven": 60,
    "iven": 55, "tyra-halvard": 50, "syra-halvard": 45,
    "drael": 40, "kelvar-velkan": 35,
}

# Welt-Zuordnung (thalassien | moragh | beide) soweit bekannt.
WELT = {
    "alphina": "beide", "sorel": "beide", "vesper": "beide", "maren": "beide",
    "runa": "beide", "elke": "beide",
    "varen": "moragh", "nyr": "moragh", "talven": "moragh",
    "drael": "moragh", "iven": "moragh",
    "syra-halvard": "thalassien", "tyra-halvard": "beide",
    "kelvar-velkan": "thalassien",
    "henrik": "thalassien", "haron-dahl": "thalassien", "lene-dahl": "thalassien",
    "edric-dahl": "thalassien", "jara": "thalassien",
    "brel": "moragh", "detrik": "moragh", "draven-keth": "moragh",
    "irenna-torven": "moragh", "kalm": "moragh", "kovik": "moragh",
    "kvarn": "moragh", "liran": "moragh", "mira": "moragh", "miran": "moragh",
    "morrek": "moragh", "ormek": "moragh", "perrin-halde": "moragh",
    "sefra-varn": "moragh", "thassir-kol": "moragh", "tohl": "moragh",
    "vela": "moragh", "vesh": "moragh",
    "keldan-rohn": "thalassien", "kesper-holm": "thalassien",
}

HAS_FRONTMATTER = re.compile(r"^---\s*\n", re.MULTILINE)
H1 = re.compile(r"^#\s+(.+?)\s*$", re.MULTILINE)


def extract_name(text: str, slug: str) -> str:
    """Extrahiert den Figurnamen aus der H1-Zeile."""
    m = H1.search(text)
    if not m:
        return slug.replace("-", " ").title()
    title = m.group(1)
    # "POV — Alphina Fenne" → "Alphina Fenne"
    # "Alphina Fenne — POV-Dossier" → "Alphina Fenne"
    # "Brel — Nebenfigur" → "Brel"
    # "Haron Dahl — Nebenfigur (verstorben vor B1)" → "Haron Dahl"
    parts = re.split(r"\s+[—–-]{1,}\s+", title, maxsplit=1)
    if parts[0].strip().lower() == "pov":
        return parts[1].split("—")[0].split("(")[0].strip() if len(parts) > 1 else slug
    return parts[0].split("(")[0].strip()


def build_frontmatter(slug: str, folder: str, name: str) -> str:
    typ = "hauptfigur" if folder == "pov" else "nebenfigur"
    pov = folder == "pov"
    welt = WELT.get(slug, "")
    reihenfolge = REIHENFOLGE.get(slug, 0)

    lines = [
        "---",
        f"name: {name}",
        f"slug: {slug}",
        f"typ: {typ}",
        f"pov: {str(pov).lower()}",
        f"ordner: {folder}",
    ]
    if welt:
        lines.append(f"welt: {welt}")
    if reihenfolge:
        lines.append(f"reihenfolge: {reihenfolge}")
    # Leere Felder als Platzhalter, vom Autor zu füllen:
    lines.append("# alter:")
    lines.append("# fraktion:")
    lines.append("# rolle:")
    lines.append("# buecher: [1, 2, 3]")
    lines.append("---")
    return "\n".join(lines) + "\n\n"


def process_folder(folder_name: str) -> None:
    folder = BUCH / folder_name
    for md in sorted(folder.glob("*.md")):
        text = md.read_text(encoding="utf-8")
        if text.lstrip().startswith("---"):
            print(f"  skip (hat schon Frontmatter): {md.name}")
            continue
        slug = md.stem
        name = extract_name(text, slug)
        fm = build_frontmatter(slug, folder_name, name)
        md.write_text(fm + text, encoding="utf-8")
        print(f"  + {md.name}  ->  name='{name}'")


def main() -> int:
    if not BUCH.exists():
        print(f"FEHLER: {BUCH} nicht gefunden", file=sys.stderr)
        return 1
    print("POV-Dossiers:")
    process_folder("pov")
    print("\nNebenfiguren:")
    process_folder("nebenfiguren")
    return 0


if __name__ == "__main__":
    sys.exit(main())
