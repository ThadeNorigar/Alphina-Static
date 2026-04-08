"""
Sweep Part 4 (final): 09-entwurf.md + alle Szenenplaene + die 3 verpassten Tors-Genitive.

IGNORIERT (per User-Anweisung):
  - Alle finalen Kapitel 1-8 + I1 und deren entwurf.md/szene*.md Dateien
  - Alle realen Tore (Stadttor, Werft-Tor, Garten-Tor, Pfoertnerhaus)
  - moragh-karte.json (Tor-Shek, Tor-Kesh sind Moragh-Ortsnamen)
  - szenen/17-01.md (Gartentor, Vesper kommt "durch das Tor" zum Garten)
  - szenen/40-02.md (Werft-Tor)
"""

from pathlib import Path
import sys

REPO = Path(__file__).resolve().parent.parent.parent

SUBS = [
    # ---- Verpasste Tors-Genitive in bereits bearbeiteten Dateien ---------
    ("buch/00-welt.md",
     "Verstärkt sich in der Nähe des Tors.",
     "Verstärkt sich in der Nähe des Risses.",
     1),
    ("buch/05-akt4.md",
     "Vespers Analyse läuft parallel: die 4:33 — es war nie die Frequenz des Tors. Es war Varens Signatur.",
     "Vespers Analyse läuft parallel: die 4:33 — es war nie die Frequenz des Risses. Es war Varens Signatur.",
     1),
    ("buch/status.json",
     "4:33 war nie die Frequenz des Tors — sondern Varens Signatur.",
     "4:33 war nie die Frequenz des Risses — sondern Varens Signatur.",
     1),

    # ---- buch/kapitel/09-entwurf.md --------------------------------------
    ("buch/kapitel/09-entwurf.md",
     "Erde-warm, Tor-warm, jetzt Stein-warm",
     "Erde-warm, Riss-warm, jetzt Stein-warm",
     1),
    ("buch/kapitel/09-entwurf.md",
     "Runa schlüpft durch das Tor",
     "Runa schlüpft durch das Portal",
     1),

    # ---- buch/szenen/ — alphabetisch -------------------------------------
    ("buch/szenen/11-02.md",
     "Das Tor unter Vael, geschlossen, aber leckend.",
     "Der Riss unter Vael, geschlossen, aber leckend.",
     1),

    ("buch/szenen/16-02.md",
     "wie Moragh-Luft die durch ein leckendes Tor sickert",
     "wie Moragh-Luft die durch einen leckenden Riss sickert",
     1),

    # 17-01 BLEIBT: "Zuletzt Vesper, durch das Tor" = Gartentor

    ("buch/szenen/18-01.md",
     "*Das Tor. Die Schwelle. Was darunter wartet.*",
     "*Das Portal. Die Schwelle. Was darunter wartet.*",
     1),

    ("buch/szenen/18-02.md",
     "Resonanz. Tunnel unter der Stadt. Ein Tor. Eine andere Welt.",
     "Resonanz. Tunnel unter der Stadt. Ein Portal. Eine andere Welt.",
     1),
    ("buch/szenen/18-02.md",
     "Die Bildhauerin geht durch. Die anderen schließen das Tor.",
     "Die Bildhauerin geht durch. Die anderen schließen das Portal.",
     1),
    ("buch/szenen/18-02.md",
     "*Wenn das Tor sich wieder öffnet.",
     "*Wenn das Portal sich wieder öffnet.",
     1),

    ("buch/szenen/19-01.md",
     "Der Stein der nachgibt. Ein Tor unter der Stadt.",
     "Der Stein der nachgibt. Ein Portal unter der Stadt.",
     1),

    ("buch/szenen/23-02.md",
     "Manuskript von 1423. Vier Fremde, ein Tor, eine Schwelle.",
     "Manuskript von 1423. Vier Fremde, ein Portal, eine Schwelle.",
     1),

    ("buch/szenen/24-02.md",
     "Die Frequenz des Tors, dachte er,",
     "Die Frequenz des Risses, dachte er,",
     1),

    ("buch/szenen/27-03.md",
     "# Kap 27, Szene 3 — Maren: Das Tor",
     "# Kap 27, Szene 3 — Maren: Der Riss",
     1),
    ("buch/szenen/27-03.md",
     "Das Tor war geschlossen — kein Tor aus Holz oder Metall, sondern aus etwas Dichtem, Schimmerndem,",
     "Der Riss war geschlossen — keine Wand aus Holz oder Metall, sondern aus etwas Dichtem, Schimmerndem,",
     1),
    ("buch/szenen/27-03.md",
     "Das Tor weinte.",
     "Der Riss weinte.",
     1),

    ("buch/szenen/28-03.md",
     "# Kap 28, Szene 3 — Alphina: Am Tor",
     "# Kap 28, Szene 3 — Alphina: Am Riss",
     1),
    ("buch/szenen/28-03.md",
     "Er kniet vor dem Tor, Kamera auf dem Stativ,",
     "Er kniet vor dem Riss, Kamera auf dem Stativ,",
     1),
    ("buch/szenen/28-03.md",
     "Das Tor schimmert hinter ihm, pulsierend,",
     "Der Riss schimmert hinter ihm, pulsierend,",
     1),
    ("buch/szenen/28-03.md",
     "und sein Gesicht im Schimmer des Tors ist müde",
     "und sein Gesicht im Schimmer des Risses ist müde",
     1),
    ("buch/szenen/28-03.md",
     "Das Tor pocht hinter uns.",
     "Der Riss pocht hinter uns.",
     1),

    ("buch/szenen/30-01.md",
     "# Kap 30, Szene 1 — Sorel: Am Tor",
     "# Kap 30, Szene 1 — Sorel: Am Riss",
     1),
    ("buch/szenen/30-01.md",
     "Das Tor pulsierte hinter ihm, warm, das Schimmern warf Muster",
     "Der Riss pulsierte hinter ihm, warm, das Schimmern warf Muster",
     1),
    ("buch/szenen/30-01.md",
     "Das Pochen des Tors füllte die Stille,",
     "Das Pochen des Risses füllte die Stille,",
     1),
    ("buch/szenen/30-01.md",
     "Im Schimmer des Tors sah der Junge",
     "Im Schimmer des Risses sah der Junge",
     1),

    ("buch/szenen/30-02.md",
     "Das Tor pochte hinter ihnen, stärker als zuvor,",
     "Der Riss pochte hinter ihnen, stärker als zuvor,",
     1),

    ("buch/szenen/31-03.md",
     "Die vier am Tor. Unten, im tiefsten Punkt der Tunnel,",
     "Die vier am Riss. Unten, im tiefsten Punkt der Tunnel,",
     1),
    ("buch/szenen/31-03.md",
     "Das Tor pulsiert, stärker als letzte Woche,",
     "Der Riss pulsiert, stärker als letzte Woche,",
     1),
    ("buch/szenen/31-03.md",
     "die Intervalle enger, das Tor drückt.",
     "die Intervalle enger, der Riss drückt.",
     1),
    ("buch/szenen/31-03.md",
     "durch den Boden, durch den Stein, zum Tor.",
     "durch den Boden, durch den Stein, zum Riss.",
     1),
    ("buch/szenen/31-03.md",
     "vier Menschen die einander ansehen und wissen. Das Tor pocht.",
     "vier Menschen die einander ansehen und wissen. Der Riss pocht.",
     1),

    ("buch/szenen/32-01.md",
     "nach unten, zum Stein, zum Tunnel, zum Tor.",
     "nach unten, zum Stein, zum Tunnel, zum Riss.",
     1),

    ("buch/szenen/32-04.md",
     "langsam, rückwärts, Richtung Tunnel, Richtung Tor.",
     "langsam, rückwärts, Richtung Tunnel, Richtung Riss.",
     1),

    ("buch/szenen/33-02.md",
     "Das Tor. Zwei Pfeiler aus schwarzem Basalt,",
     "Der Riss. Zwei Pfeiler aus schwarzem Basalt,",
     1),

    ("buch/szenen/33-03.md",
     "Vesper und Maren sind weitergegangen, zum Tor.",
     "Vesper und Maren sind weitergegangen, zum Riss.",
     1),

    ("buch/szenen/34-03.md",
     "Das Tor schloss sich. Stein auf Stein, lautlos,",
     "Das Portal schloss sich. Stein auf Stein, lautlos,",
     1),
    ("buch/szenen/34-03.md",
     "Maren legte die Hand auf den Stein wo das Tor gewesen war.",
     "Maren legte die Hand auf den Stein wo das Portal gewesen war.",
     1),
    ("buch/szenen/34-03.md",
     "Der Stein war kalt hinter ihm. Kein Tor mehr. Kein Zurück.",
     "Der Stein war kalt hinter ihm. Kein Portal mehr. Kein Zurück.",
     1),

    ("buch/szenen/35-01.md",
     "Er hatte geglaubt, 4:33 sei die Frequenz des Tors —",
     "Er hatte geglaubt, 4:33 sei die Frequenz des Risses —",
     1),
    ("buch/szenen/35-01.md",
     "Und dann sah er es: 4:33 war nicht die Frequenz des Tors.",
     "Und dann sah er es: 4:33 war nicht die Frequenz des Risses.",
     1),

    ("buch/szenen/39-03.md",
     "allein, vor einer Wand aus Basalt die gestern noch ein Tor war.",
     "allein, vor einer Wand aus Basalt die gestern noch ein Portal war.",
     1),

    # 40-02 BLEIBT: "Maren schob das Tor auf" = Werft-Tor

    ("buch/szenen/40-03.md",
     "sie war in einen Tunnel gegangen, durch ein Tor, in eine andere Welt.",
     "sie war in einen Tunnel gegangen, durch ein Portal, in eine andere Welt.",
     1),

    ("buch/szenen/40-04.md",
     "Sorel ist tot. Das Tor ist zu. Thalassien liegt auf der anderen Seite",
     "Sorel ist tot. Das Portal ist zu. Thalassien liegt auf der anderen Seite",
     1),

    ("buch/szenen/I4-01.md",
     "Ihr Gesicht, korrekt. Dahinter: das Tor. Genau so, wie Lene es beschrieben hat,",
     "Ihr Gesicht, korrekt. Dahinter: der Riss. Genau so, wie Lene es beschrieben hat,",
     1),

    ("buch/szenen/I5-01.md",
     "Drei Formen kommen durch das Tor — nicht von der Thalassien-Seite, von Moragh.",
     "Drei Formen kommen durch das Portal — nicht von der Thalassien-Seite, von Moragh.",
     1),

    ("buch/szenen/I5-02.md",
     "darunter die Tunnel, darunter das Tor. Sie drückt.",
     "darunter die Tunnel, darunter der Riss. Sie drückt.",
     1),
    ("buch/szenen/I5-02.md",
     "Nahe am Tor — da wo die Magie durch die Ritzen sickert —",
     "Nahe am Riss — da wo die Magie durch die Ritzen sickert —",
     1),
    ("buch/szenen/I5-02.md",
     "In Thalassien stimmt das. Aber nahe am Tor,",
     "In Thalassien stimmt das. Aber nahe am Riss,",
     1),

    ("buch/szenen/I7-01.md",
     "Die Vier kämpfen sich zum Steinkreis durch — Elke will das Tor öffnen.",
     "Die Vier kämpfen sich zum Steinkreis durch — Elke will das Portal öffnen.",
     1),
    ("buch/szenen/I7-01.md",
     "Der Fels gibt nach, wie immer, aber diesmal drückt sie tiefer. Das Tor öffnet sich —",
     "Der Fels gibt nach, wie immer, aber diesmal drückt sie tiefer. Das Portal öffnet sich —",
     1),

    ("buch/szenen/I9-01.md",
     "Sie kannte diesen Rhythmus. Das Tor. Seit Wochen still,",
     "Sie kannte diesen Rhythmus. Der Riss. Seit Wochen still,",
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
