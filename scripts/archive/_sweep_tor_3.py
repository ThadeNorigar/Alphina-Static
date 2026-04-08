"""
Sweep Part 3: status.json + zeitleiste.json.
moragh-karte.json wird NICHT angefasst (Tor-Shek, Tor-Kesh sind Moragh-Ortsnamen).
"""

from pathlib import Path
import sys

REPO = Path(__file__).resolve().parent.parent.parent

SUBS = [
    # ---- buch/status.json --------------------------------------------------
    ("buch/status.json",
     '"untertitel": "Thalassien / Vael / Das Tor"',
     '"untertitel": "Thalassien / Vael / Das Portal"',
     1),
    ("buch/status.json",
     '"titel": "Das Tor"',
     '"titel": "Das Portal"',
     1),
    ("buch/status.json",
     "Ein Moragh-Einwanderer, durch das lecke Tor gekommen.",
     "Ein Moragh-Einwanderer, durch einen früheren Riss gekommen.",
     1),
    ("buch/status.json",
     "Vier Fremde, ein Tor, eine Schwelle.",
     "Vier Fremde, ein Portal, eine Schwelle.",
     1),
    ("buch/status.json",
     "Sie reden über Hände und Arbeit, nicht über das Tor.",
     "Sie reden über Hände und Arbeit, nicht über den Riss.",
     1),
    ("buch/status.json",
     "Varen schickt drei Feuer-Schemen durch das Tor — doppelt so groß wie Menschen.",
     "Varen schickt drei Feuer-Schemen durch das Portal — doppelt so groß wie Menschen.",
     1),
    ("buch/status.json",
     "Das Manuskript: vier Fremde, eine Schwelle, ein Tor unter der Stadt.",
     "Das Manuskript: vier Fremde, eine Schwelle, ein Portal unter der Stadt.",
     1),
    ("buch/status.json",
     "Das Tor, geschlossen, pulsierend. Ihre Hand darauf — das Tor weint.",
     "Der Riss, geschlossen, pulsierend. Ihre Hand darauf — der Riss weint.",
     1),
    ("buch/status.json",
     "Alphina geht in die Tunnel, allein, Farne als Kompass. Findet ihn am Tor.",
     "Alphina geht in die Tunnel, allein, Farne als Kompass. Findet ihn am Riss.",
     1),
    ("buch/status.json",
     "Elke öffnet das Tor und geht durch.",
     "Elke öffnet das Portal und geht durch.",
     1),
    ("buch/status.json",
     "Die Frequenz von etwas hinter dem Tor.",
     "Die Frequenz von etwas hinter dem Riss.",
     1),
    ("buch/status.json",
     "Vier Menschen in der Dunkelheit, Alphinas Farne leuchten grünlich. Das Tor pulsiert.",
     "Vier Menschen in der Dunkelheit, Alphinas Farne leuchten grünlich. Der Riss pulsiert.",
     1),
    ("buch/status.json",
     "Runa stolpert im letzten Moment durch. Das Tor schließt sich. Nicht von ihnen — von Varen.",
     "Runa stolpert im letzten Moment durch. Das Portal schließt sich. Nicht von ihnen — von Varen.",
     1),
    ("buch/status.json",
     '"titel": "Elke hört das Tor"',
     '"titel": "Elke hört das Portal"',
     1),
    ("buch/status.json",
     "Vael ohne die Fünf. Das Portal ist geschlossen. Esther Voss vor dem toten Tor.",
     "Vael ohne die Fünf. Das Portal ist geschlossen. Esther Voss vor dem toten Riss.",
     1),
    ("buch/status.json",
     '"titel": "Maren: Das Tor ist zu"',
     '"titel": "Maren: Das Portal ist zu"',
     1),
    ("buch/status.json",
     "Maren sucht das Tor durch das Wasser.",
     "Maren sucht den Riss durch das Wasser.",
     1),
    ("buch/status.json",
     "Die Gilden wollen das Tor schließen.",
     "Die Gilden wollen den Riss schließen.",
     1),
    ("buch/status.json",
     '"titel": "Vesper: Die Tor-Frage"',
     '"titel": "Vesper: Die Riss-Frage"',
     1),
    ("buch/status.json",
     "Die Tor-Frage: offen, geschlossen, reguliert.",
     "Die Riss-Frage: offen, geschlossen, reguliert.",
     1),

    # ---- buch/zeitleiste.json ----------------------------------------------
    ("buch/zeitleiste.json",
     '"untertitel": "Zwei Welten. Ein Tor. Zwei Zeiten."',
     '"untertitel": "Zwei Welten. Ein Riss. Zwei Zeiten."',
     1),
    ("buch/zeitleiste.json",
     '"titel": "Varen öffnet das Tor — 3 Feuer-Schemen nach Thalassien"',
     '"titel": "Varen öffnet das Portal — 3 Feuer-Schemen nach Thalassien"',
     1),
    ("buch/zeitleiste.json",
     '"titel": "Elke in ihrem Garten. Weiß nicht dass Varen das Tor öffnete."',
     '"titel": "Elke in ihrem Garten. Weiß nicht dass Varen das Portal öffnete."',
     1),
    ("buch/zeitleiste.json",
     '"detail": "Wissenschaftler verstehen das Tor. Vael ist Großstadt."',
     '"detail": "Wissenschaftler verstehen das Portal. Vael ist Großstadt."',
     1),
    ("buch/zeitleiste.json",
     '"detail": "Nicht als Tor — als Grenze die beide Seiten akzeptieren."',
     '"detail": "Nicht als Portal — als Grenze die beide Seiten akzeptieren."',
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
