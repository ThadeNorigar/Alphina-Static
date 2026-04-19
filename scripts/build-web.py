#!/usr/bin/env python3
"""
Build-Skript für die Website-Datenquellen.

Liest:
  buch/synopse-b{1,2,3}.md       (Plot-Synopsen pro Buch)
  buch/pov/*.md                   (Hauptfiguren-Dossiers)
  buch/nebenfiguren/*.md          (Nebenfiguren-Dossiers)

Schreibt:
  story/data/synopsen.json
  story-in-work/data/figuren.json

Jede MD-Datei hat optional einen YAML-Frontmatter-Block am Anfang (zwischen
'---'-Zeilen). Der Body wird Markdown gerendert und als HTML-String ins JSON
gepackt. So braucht der Browser keine Markdown-Library.

Aufruf: python scripts/build-web.py
"""

from __future__ import annotations

import datetime as _dt
import json
import re
import sys
from pathlib import Path
from typing import Any

import markdown
import yaml

ROOT = Path(__file__).resolve().parent.parent
BUCH = ROOT / "buch"

STORY_DATA = ROOT / "story" / "data"
WIP_DATA = ROOT / "story-in-work" / "data"

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n(.*)$", re.DOTALL)

MD = markdown.Markdown(extensions=["extra", "sane_lists"])


def render_md(text: str) -> str:
    MD.reset()
    return MD.convert(text.strip())


def parse_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    """Trennt YAML-Frontmatter vom Body. Gibt (frontmatter, body) zurück."""
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}, text
    raw_fm, body = m.group(1), m.group(2)
    try:
        fm = yaml.safe_load(raw_fm) or {}
    except yaml.YAMLError as e:
        print(f"  WARNUNG: ungültiges Frontmatter ({e})", file=sys.stderr)
        fm = {}
    return fm, body


def split_sections(body: str) -> list[dict[str, Any]]:
    """Spaltet einen MD-Body an H2-Überschriften. Alles vor der ersten H2
    wird als Intro behandelt."""
    sections: list[dict[str, Any]] = []
    current_title: str | None = None
    current_lines: list[str] = []

    def flush() -> None:
        if current_title is None and not current_lines:
            return
        body_md = "\n".join(current_lines).strip()
        if current_title is None and not body_md:
            return
        sections.append(
            {
                "title": current_title or "",
                "html": render_md(body_md) if body_md else "",
            }
        )

    for line in body.splitlines():
        if line.startswith("## "):
            flush()
            current_title = line[3:].strip()
            current_lines = []
        else:
            current_lines.append(line)
    flush()
    return sections


# ---------------------------------------------------------------------------
# Synopsen
# ---------------------------------------------------------------------------

def build_synopsen() -> dict[str, Any]:
    result: dict[str, Any] = {}
    for buch_nr in (1, 2, 3):
        path = BUCH / f"synopse-b{buch_nr}.md"
        if not path.exists():
            print(f"  (übersprungen, fehlt: {path.name})")
            continue
        text = path.read_text(encoding="utf-8")
        fm, body = parse_frontmatter(text)
        sections = split_sections(body)
        result[f"b{buch_nr}"] = {"meta": fm, "sections": sections}
        print(f"  + synopse-b{buch_nr}: {len(sections)} Abschnitte")
    return result


# ---------------------------------------------------------------------------
# Figuren
# ---------------------------------------------------------------------------

# Zusätzliche Top-Level-Figuren-Dossiers im buch/-Wurzelordner (Ebene-3-Dateien).
# Werden nur eingelesen, wenn sie explizit gelistet UND Frontmatter haben.
EXTRA_FIGUREN_FILES = [
    "11-nyr.md",
    "13-talven.md",
    "19-varen.md",
]


def _fig_meta(md_path: Path, folder_label: str, typ_default: str, pov_default: bool) -> dict[str, Any]:
    text = md_path.read_text(encoding="utf-8")
    fm, body = parse_frontmatter(text)
    # Typ aus Frontmatter gewinnt immer — auch wenn er "antagonist" oder Sonderform ist
    typ = fm.get("typ") or typ_default
    return {
        "name": fm.get("name") or md_path.stem.replace("-", " ").title(),
        "slug": fm.get("slug") or md_path.stem,
        "typ": typ,
        "pov": fm.get("pov") if "pov" in fm else pov_default,
        "ordner": fm.get("ordner") or folder_label,
        "welt": fm.get("welt") or "",
        "reihenfolge": fm.get("reihenfolge") or 0,
        "alter": fm.get("alter") or "",
        "fraktion": fm.get("fraktion") or "",
        "rolle": fm.get("rolle") or "",
        "buecher": fm.get("buecher") or [],
        "html": render_md(body),
    }


def build_figuren() -> dict[str, Any]:
    hauptfiguren: list[dict[str, Any]] = []
    nebenfiguren: list[dict[str, Any]] = []

    for folder, target, typ_default, pov_default in (
        ("pov", hauptfiguren, "hauptfigur", True),
        ("nebenfiguren", nebenfiguren, "nebenfigur", False),
    ):
        src = BUCH / folder
        if not src.exists():
            continue
        for md_path in sorted(src.glob("*.md")):
            target.append(_fig_meta(md_path, folder, typ_default, pov_default))

    for filename in EXTRA_FIGUREN_FILES:
        md_path = BUCH / filename
        if not md_path.exists():
            print(f"  (übersprungen, fehlt: {filename})")
            continue
        meta = _fig_meta(md_path, "buch", "hauptfigur", True)
        # Antagonist + Hauptfigur landen beide in Hauptfiguren-Block
        if meta["typ"] in ("hauptfigur", "antagonist"):
            hauptfiguren.append(meta)
        else:
            nebenfiguren.append(meta)

    # Deduplizieren per slug (falls eine Figur doppelt auftaucht, gewinnt der erste Eintrag)
    def dedup(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
        seen: set[str] = set()
        out: list[dict[str, Any]] = []
        for f in items:
            if f["slug"] in seen:
                print(f"  WARNUNG: doppelter Slug übersprungen: {f['slug']}")
                continue
            seen.add(f["slug"])
            out.append(f)
        return out

    hauptfiguren = dedup(hauptfiguren)
    nebenfiguren = dedup(nebenfiguren)

    hauptfiguren.sort(key=lambda f: (-(f["reihenfolge"] or 0), f["name"]))
    nebenfiguren.sort(key=lambda f: (-(f["reihenfolge"] or 0), f["name"]))

    print(f"  + {len(hauptfiguren)} Hauptfiguren, {len(nebenfiguren)} Nebenfiguren")
    return {"hauptfiguren": hauptfiguren, "nebenfiguren": nebenfiguren}


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def _json_default(o: Any) -> Any:
    if isinstance(o, (_dt.date, _dt.datetime)):
        return o.isoformat()
    raise TypeError(f"not serializable: {type(o).__name__}")


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2, default=_json_default),
        encoding="utf-8",
    )
    size_kb = path.stat().st_size / 1024
    print(f"  -> {path.relative_to(ROOT)} ({size_kb:.1f} KB)")


def main() -> int:
    print("Synopsen:")
    synopsen = build_synopsen()
    write_json(STORY_DATA / "synopsen.json", synopsen)

    print("\nFiguren:")
    figuren = build_figuren()
    write_json(WIP_DATA / "figuren.json", figuren)

    print("\nbuild-web: fertig.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
