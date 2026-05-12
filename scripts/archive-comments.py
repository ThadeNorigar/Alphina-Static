#!/usr/bin/env python3
"""Backup aller Online-Kommentare in buch/_archiv/.

Holt alle Kommentare (entwurf + final, include_resolved=true) ueber alle Kapitel
aus buch/status.json und speichert sie als JSON + lesbare Markdown-Datei nach
buch/_archiv/online-kommentare-<datum>.{json,md}.

Aufruf:
    python scripts/archive-comments.py
    python scripts/archive-comments.py --dry-run

Hinweis: das eigentliche Leeren der DB passiert serverseitig auf adrianphilipp.de
(siehe docs/superpowers/plans/2026-05-12-ratings.md fuer den DELETE-Endpoint).
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATUS_FILE = ROOT / "buch" / "status.json"
ARCHIV_DIR = ROOT / "buch" / "_archiv"

API_BASE = "https://alphina.net/api/comments"
ADMIN_KEY = "21c7ef896af35a6ce31b79c1f712b94a4f1d523b911de20e"


def slug_for(kap_id: str) -> str:
    """B1-K17 -> '17', B1-KI3 -> 'I3'. Wir bekommen hier die rohen Keys aus status.json."""
    if kap_id.startswith("I"):
        return kap_id
    try:
        return str(int(kap_id))
    except ValueError:
        return kap_id


def fetch(url: str) -> list[dict]:
    req = urllib.request.Request(url, headers={"X-User-Id": ADMIN_KEY})
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
            return payload if isinstance(payload, list) else []
    except urllib.error.HTTPError as e:
        print(f"  HTTP {e.code} fuer {url}", file=sys.stderr)
        return []
    except Exception as e:
        print(f"  Fehler fuer {url}: {e}", file=sys.stderr)
        return []


def collect_kapitel_ids(status: dict) -> list[str]:
    ids: list[str] = []
    for buch_key in ("buch1", "buch2", "buch3"):
        buch = status.get(buch_key) or {}
        for kid in (buch.get("kapitel") or {}).keys():
            ids.append(kid)
    return ids


def fetch_all(kap_ids: list[str]) -> list[dict]:
    # Slugs koennen ueber Buecher hinweg kollidieren (B1-K17 und B2-K17 -> "17").
    # Wir fetchen daher pro Slug nur einmal und dedupen ueber id.
    slugs: list[str] = []
    seen_slug: set[str] = set()
    for kid in kap_ids:
        s = slug_for(kid)
        if s not in seen_slug:
            seen_slug.add(s)
            slugs.append(s)

    out: list[dict] = []
    seen_ids: set = set()
    for slug in slugs:
        for modus in ("entwurf", "final"):
            url = f"{API_BASE}?kapitel={slug}&modus={modus}&include_resolved=true"
            data = fetch(url)
            new = []
            for c in data:
                cid = c.get("id")
                if cid is not None and cid in seen_ids:
                    continue
                if cid is not None:
                    seen_ids.add(cid)
                c.setdefault("modus", modus)
                new.append(c)
            if new:
                print(f"  slug={slug} ({modus}): {len(new)} Kommentare")
            out.extend(new)
    return out


def write_markdown(comments: list[dict], path: Path) -> None:
    by_kap: dict[str, dict[str, list[dict]]] = {}
    for c in comments:
        kap = c.get("kapitel_id") or "?"
        modus = c.get("modus") or "?"
        by_kap.setdefault(kap, {}).setdefault(modus, []).append(c)

    lines: list[str] = []
    lines.append(f"# Online-Kommentare — Archiv vom {date.today().isoformat()}")
    lines.append("")
    lines.append(f"Gesamt: **{len(comments)}** Kommentare aus **{len(by_kap)}** Kapiteln.")
    lines.append("")
    lines.append("Quelle: `GET https://alphina.net/api/comments?include_resolved=true` mit Admin-Key.")
    lines.append("")

    for kap in sorted(by_kap.keys()):
        for modus in sorted(by_kap[kap].keys()):
            items = sorted(
                by_kap[kap][modus],
                key=lambda c: (c.get("absatz_idx", 0), c.get("created_at", "")),
            )
            lines.append(f"## {kap} — {modus} ({len(items)})")
            lines.append("")
            for c in items:
                idx = c.get("absatz_idx", "?")
                anker = (c.get("absatz_text") or "").strip()
                if len(anker) > 100:
                    anker = anker[:100] + "…"
                created = c.get("created_at", "")
                text = (c.get("text") or "").strip()
                resolved = c.get("resolved_status") or c.get("resolved_at") or ""
                meta_bits = [f"#{c.get('id', '?')}", created]
                if resolved:
                    meta_bits.append(f"resolved={resolved}")
                lines.append(f"- **Absatz {idx}** — _{anker}_  ({' · '.join(meta_bits)})")
                for line in text.splitlines():
                    lines.append(f"    > {line}")
                lines.append("")

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="nur abrufen, nichts schreiben")
    args = parser.parse_args()

    if not STATUS_FILE.exists():
        print(f"FEHLER: {STATUS_FILE} nicht gefunden", file=sys.stderr)
        return 1

    status = json.loads(STATUS_FILE.read_text(encoding="utf-8"))
    kap_ids = collect_kapitel_ids(status)
    print(f"Hole Kommentare fuer {len(kap_ids)} Kapitel …")
    comments = fetch_all(kap_ids)
    print(f"Gesamt: {len(comments)} Kommentare.")

    if args.dry_run:
        print("Dry-Run — nichts geschrieben.")
        return 0

    ARCHIV_DIR.mkdir(parents=True, exist_ok=True)
    stamp = date.today().isoformat()
    json_path = ARCHIV_DIR / f"online-kommentare-{stamp}.json"
    md_path = ARCHIV_DIR / f"online-kommentare-{stamp}.md"

    json_path.write_text(json.dumps(comments, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_markdown(comments, md_path)

    print(f"Geschrieben: {json_path.relative_to(ROOT)}")
    print(f"Geschrieben: {md_path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
