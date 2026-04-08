"""
Einmal-Skript: Tor → Riss / Portal Sweep.

Regel:
- Riss       = dauerhaft, sickernd, dünne Stelle zwischen den Welten
- Portal     = das öffenbare 4:33-Ritual, Einweg-Durchgang
- Stadttor, reale Tore bleiben unverändert

Jede Substitution ist ein (datei, alt, neu, erwartete_anzahl)-Triple.
Das Skript liest jede Datei, prüft ob 'alt' genau erwartete_anzahl Mal vorkommt,
macht die Ersetzung, und schreibt zurück. Bei Mismatch: Fehler, kein Schreiben.
"""

from pathlib import Path
import sys

REPO = Path(__file__).resolve().parent.parent.parent

SUBS = [
    # ---- buch/00-welt.md ---------------------------------------------------
    ("buch/00-welt.md",
     "Zwei Welten. Ein Tor.",
     "Zwei Welten. Ein Riss.",
     1),
    ("buch/00-welt.md",
     "Unter Vael liegt ein Tor zwischen den Welten. Es wird von der Moragh-Seite kontrolliert.",
     "Unter Vael liegt der Riss zwischen den Welten. Er kann von der Moragh-Seite als Portal geöffnet werden.",
     1),
    ("buch/00-welt.md",
     "**Richtungsportal.** Beide Seiten können das Tor öffnen. Aber wer öffnet, kann nur in eine Richtung durchlassen: **von der öffnenden Seite auf die andere.** Moragh öffnet → Moragh-Menschen gehen nach Thalassien. Thalassien öffnet → Thalassier gehen nach Moragh. Kein Gegenverkehr. Kein Zurückgehen durch dasselbe Tor.",
     "**Richtungsportal.** Beide Seiten können den Riss als Portal öffnen. Aber wer öffnet, kann nur in eine Richtung durchlassen: **von der öffnenden Seite auf die andere.** Moragh öffnet → Moragh-Menschen gehen nach Thalassien. Thalassien öffnet → Thalassier gehen nach Moragh. Kein Gegenverkehr. Kein Zurückgehen durch dasselbe Portal.",
     1),
    ("buch/00-welt.md",
     "**Das Tor ruft NIEMANDEN.** Das Tor ist ein Mechanismus, kein Magnet. Es leckt —",
     "**Der Riss ruft NIEMANDEN.** Der Riss ist ein Mechanismus, kein Magnet. Er leckt —",
     1),
    ("buch/00-welt.md",
     "Die Standuhr verliert wirklich 4:33 (Tor-Leck).",
     "Die Standuhr verliert wirklich 4:33 (Riss-Leck).",
     1),
    ("buch/00-welt.md",
     "Es war nie das Tor. Es war Varen.",
     "Es war nie der Riss. Es war Varen.",
     1),
    ("buch/00-welt.md",
     "## Varen — der Forscher am Tor",
     "## Varen — der Forscher am Riss",
     1),
    ("buch/00-welt.md",
     "**Mächtig. GUT GENÄHRT. In Form.** Nicht ausgemergelt, nicht am Ende. Das Tor zu öffnen hat ihn Monate gekostet,",
     "**Mächtig. GUT GENÄHRT. In Form.** Nicht ausgemergelt, nicht am Ende. Das Portal zu öffnen hat ihn Monate gekostet,",
     1),
    ("buch/00-welt.md",
     "Sie finden das Manuskript, übersetzen das Ritual, öffnen das Tor. Freiwillig.",
     "Sie finden das Manuskript, übersetzen das Ritual, öffnen das Portal. Freiwillig.",
     1),
    ("buch/00-welt.md",
     "Also schickt er Agenten durch das Tor, mit dem Thalassisch das Elke ihm beigebracht hat,",
     "Also schickt er Agenten durch das Portal, mit dem Thalassisch das Elke ihm beigebracht hat,",
     1),
    ("buch/00-welt.md",
     "### Vael heilt WEIL das Tor geschlossen ist",
     "### Vael heilt weil der Riss versiegt",
     1),
    ("buch/00-welt.md",
     "Kam nach Vael als das Tor das letzte Mal offen war",
     "Kam nach Vael als das Portal das letzte Mal offen war",
     1),
    ("buch/00-welt.md",
     "**Elke van der Holt** — Bildhauerin. Resonanz: Erde/Stein. Ging durch das Tor.",
     "**Elke van der Holt** — Bildhauerin. Resonanz: Erde/Stein. Ging durch das Portal.",
     1),
    ("buch/00-welt.md",
     "Varen öffnete das Tor von der Moragh-Seite",
     "Varen öffnete das Portal von der Moragh-Seite",
     1),
    ("buch/00-welt.md",
     "öffneten die Vier das Tor von der Thalassien-Seite.",
     "öffneten die Vier das Portal von der Thalassien-Seite.",
     1),
    ("buch/00-welt.md",
     "Während Alphina vor dem Tor steht: Elke auf der anderen Seite. Sie hört das Tor. Jemand kommt.",
     "Während Alphina vor dem Portal steht: Elke auf der anderen Seite. Sie hört das Portal. Jemand kommt.",
     1),
    ("buch/00-welt.md",
     "Geht durch, schließt das Tor von innen, rettet Vael.",
     "Geht durch, schließt das Portal von innen, rettet Vael.",
     1),
    ("buch/00-welt.md",
     "Kein Lecken mehr, keine Moragh-Magie die durchsickert. Vael heilt WEIL das Tor geschlossen ist.",
     "Kein Lecken mehr, keine Moragh-Magie die durchsickert. Vael heilt weil der Riss versiegt.",
     1),
    ("buch/00-welt.md",
     "Fünf Menschen aus einer Welt ohne Magie, in einer Welt im Krieg. Das Tor ist zu.",
     "Fünf Menschen aus einer Welt ohne Magie, in einer Welt im Krieg. Das Portal ist zu.",
     1),
    ("buch/00-welt.md",
     "erste Wissenschaftler die das Tor theoretisch verstehen. Das Tor öffnet sich erneut.",
     "erste Wissenschaftler die das Portal theoretisch verstehen. Das Portal öffnet sich erneut.",
     1),
    ("buch/00-welt.md",
     "Die Quelle zwischen den Welten bleibt offen. Nicht als Tor — als Grenze die beide Seiten akzeptieren.",
     "Die Quelle zwischen den Welten bleibt offen. Nicht als Portal — als Grenze die beide Seiten akzeptieren.",
     1),
    ("buch/00-welt.md",
     "Das Tor ist der dünnste Punkt zwischen den Welten.",
     "Der Riss ist der dünnste Punkt zwischen den Welten.",
     1),
]


def run():
    errors = []
    changed = []
    for rel, alt, neu, expected in SUBS:
        path = REPO / rel
        if not path.exists():
            errors.append(f"{rel}: NICHT GEFUNDEN")
            continue
        text = path.read_text(encoding="utf-8")
        count = text.count(alt)
        if count != expected:
            errors.append(f"{rel}: erwartet {expected}x, gefunden {count}x: {alt[:60]!r}")
            continue
        new_text = text.replace(alt, neu)
        path.write_text(new_text, encoding="utf-8")
        changed.append(rel)

    print(f"OK: {len(changed)} Substitutionen erfolgreich")
    if errors:
        print(f"\nFEHLER ({len(errors)}):")
        for e in errors:
            print(f"  {e}")
        sys.exit(1)


if __name__ == "__main__":
    run()
