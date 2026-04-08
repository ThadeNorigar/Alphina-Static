"""
Sweep Part 2: Aktpläne + Storyline.
Jede Substitution muss genau 1x matchen — sonst Fehler.
"""

from pathlib import Path
import sys

REPO = Path(__file__).resolve().parent.parent.parent

SUBS = [
    # ---- buch/00-storyline.md --------------------------------------------
    ("buch/00-storyline.md",
     "Zwei Welten. Ein Tor.",
     "Zwei Welten. Ein Riss.",
     1),
    ("buch/00-storyline.md",
     "**Akt IV — Das Tor**",
     "**Akt IV — Das Portal**",
     1),

    # ---- buch/02-akt1.md (nur 1 Treffer, in der Tschechow-Tabelle) -------
    ("buch/02-akt1.md",
     "| Runas warme Hände | Alphina registriert es (Kap 9) | Akt IV — Feuer/Hitze-Resonanz. Runa geht durch das Tor |",
     "| Runas warme Hände | Alphina registriert es (Kap 9) | Akt IV — Feuer/Hitze-Resonanz. Runa geht durch das Portal |",
     1),

    # ---- buch/03-akt2.md --------------------------------------------------
    ("buch/03-akt2.md",
     "Beschreibt vier Fremde, ein Tor, eine Schwelle.",
     "Beschreibt vier Fremde, ein Portal, eine Schwelle.",
     1),
    ("buch/03-akt2.md",
     "Reden. Nicht über das Tor, nicht über die Anomalien.",
     "Reden. Nicht über den Riss, nicht über die Anomalien.",
     1),
    ("buch/03-akt2.md",
     "Varen schickt drei Feuer-Schemen durch das Tor —",
     "Varen schickt drei Feuer-Schemen durch das Portal —",
     1),

    # ---- buch/04-akt3.md --------------------------------------------------
    ("buch/04-akt3.md",
     "Die Vier kämpfen sich zum Steinkreis durch — Elke will das Tor öffnen, auf die andere Seite.",
     "Die Vier kämpfen sich zum Steinkreis durch — Elke will das Portal öffnen, auf die andere Seite.",
     1),
    ("buch/04-akt3.md",
     "Elke öffnet das Tor von der Thalassien-Seite und geht durch.",
     "Elke öffnet das Portal von der Thalassien-Seite und geht durch.",
     1),
    ("buch/04-akt3.md",
     "Nicht die Frequenz des Tors. Die Frequenz von etwas dahinter.",
     "Nicht die Frequenz des Risses. Die Frequenz von etwas dahinter.",
     1),
    ("buch/04-akt3.md",
     "sie wird sie nicht los. Nicht durch Flucht. Nur durch das Tor.",
     "sie wird sie nicht los. Nicht durch Flucht. Nur durch das Portal.",
     1),
    ("buch/04-akt3.md",
     '| "Du hast mich genommen ohne zu fragen" | Kap 25 | Akt IV — Am Tor hält Sorel ihre Hand. Diesmal fragt er |',
     '| "Du hast mich genommen ohne zu fragen" | Kap 25 | Akt IV — Am Portal hält Sorel ihre Hand. Diesmal fragt er |',
     1),
    ("buch/04-akt3.md",
     "| Runas glühende Hände | Kap 31 | Akt IV — Feuer/Hitze-Resonanz. Runa folgt den Vier durch das Tor |",
     "| Runas glühende Hände | Kap 31 | Akt IV — Feuer/Hitze-Resonanz. Runa folgt den Vier durch das Portal |",
     1),

    # ---- buch/05-akt4.md --------------------------------------------------
    ("buch/05-akt4.md",
     "# Akt IV — Das Tor (Seite 680–900, ~56.000 Wörter, Kap 34–41 + I8, I9)",
     "# Akt IV — Das Portal (Seite 680–900, ~56.000 Wörter, Kap 34–41 + I8, I9)",
     1),
    ("buch/05-akt4.md",
     "**Varen ist GUT GENÄHRT. In Form. MÄCHTIG.** Aus allen Fraktionen ausgestoßen. Forscher, kein Soldat. Das Tor zu öffnen hat ihn Monate gekostet,",
     "**Varen ist GUT GENÄHRT. In Form. MÄCHTIG.** Aus allen Fraktionen ausgestoßen. Forscher, kein Soldat. Das Portal zu öffnen hat ihn Monate gekostet,",
     1),
    ("buch/05-akt4.md",
     "| Fisch der nach Metall stinkt | I9 — Thar-Späher. Metall-Geruch. Die wussten vom Tor |",
     "| Fisch der nach Metall stinkt | I9 — Thar-Späher. Metall-Geruch. Die wussten vom Riss |",
     1),
]


def run():
    errors = []
    changed = 0
    for rel, alt, neu, expected in SUBS:
        path = REPO / rel
        if not path.exists():
            errors.append(f"{rel}: NICHT GEFUNDEN")
            continue
        text = path.read_text(encoding="utf-8")
        count = text.count(alt)
        if count != expected:
            errors.append(f"{rel}: erwartet {expected}x, gefunden {count}x: {alt[:70]!r}")
            continue
        new_text = text.replace(alt, neu)
        path.write_text(new_text, encoding="utf-8")
        changed += 1
    print(f"OK: {changed}/{len(SUBS)} Substitutionen erfolgreich")
    if errors:
        print(f"\nFEHLER ({len(errors)}):")
        for e in errors:
            print(f"  {e}")
        sys.exit(1)


if __name__ == "__main__":
    run()
