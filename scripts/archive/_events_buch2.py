"""
Buch 2 — Schluesselereignisse in zeitleiste.json einpflegen.

Verteilung auf monate[]:
  monat[11] MZ Monat 1   — Akt I (Kap 1-10 + I1, I2)          fremde Welt, Trauer
  monat[12] MZ Monat 2   — Akt II (Kap 11-20 + I3, I4)        Fraktionen, Lernen
  monat[13] MZ Monat 3   — Akt III (Kap 21-30 + I10, I11)     Schlachtfeld, Gefangenschaft
  monat[14] MZ Monat 4+  — Akt IV (Kap 31-42 + I12)           Getrennt, Maren nach Thalassien

Kapitel-Nummern sind Buch-2-intern (1-42). Um Kollisionen mit Buch 1 zu vermeiden,
praefixieren wir Kap-Nummern mit "B2-". Das verhindert dass stand.py --buch buch1 sie
aus Versehen aufsammelt.
"""

import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
ZEITLEISTE = REPO / "buch" / "zeitleiste.json"


def ev(kap, typen, titel, pov=None, welt="moragh", **kwargs):
    """Event-Builder. welt = 'thalassien' oder 'moragh' (fuer die monate[]-Zuordnung)."""
    e = {
        "tz": None,  # noch kein TZ da Moragh-Zeit
        "mz": None,
        "kapitel": f"B2-{kap}",
        "typen": typen,
        "titel": titel,
    }
    if pov:
        e["pov"] = pov
    e.update(kwargs)
    e["_welt"] = welt  # internal marker fuer die monat-Zuordnung
    return e


# =============================================================================
# BUCH 2 — AKT I: Fremde Welt (monat[11], MZ Monat 1)
# =============================================================================

AKT1 = [
    ev("01", ["schlüssel"],
       "Alphinas erster Trauer-Hain in Elkes Garten — unbewusst im Schlaf",
       pov="B2 Kap 1 · Alphina", mz=0.1,
       detail="Die Trauer kommt nicht als Gefuehl, sondern als Wachstum. Im Schlaf bricht der Boden auf — ein Hain von zehn Metern. Alphina kann nichts wiederholen, nichts stoppen.",
       tags=["Schluesselereignis: Trauer als Resonanz"]),

    ev("02", ["erkenntnis"],
       "Vesper sieht die Struktur von Moragh: Fibonacci, 4:33, zwei Monde",
       pov="B2 Kap 2 · Vesper", mz=0.15,
       detail="Die Baeume in Spiralen, Fluesse Fibonacci, Monde im 4:33-Verhaeltnis. Die Sonne: ein dunkler Kern mit gleissendem Ring. Kein Stern.",
       tags=["Erkenntnis: Moragh-Struktur"]),

    ev("03", ["erkenntnis"],
       "Maren fuehlt Moragh-Wasser — es fliesst bergauf und formt Mulden",
       pov="B2 Kap 3 · Maren", mz=0.2),

    ev("04", ["erkenntnis", "tschechow"],
       "Runa formt Moragh-Metall mit blossen Haenden — Feuer-Resonanz in Moragh stark",
       pov="B2 Kap 4 · Runa", mz=0.25,
       tags=["Tschechow: Runas warme Haende"]),

    ev("07", ["begegnung", "erkenntnis"],
       "Elke: 'Das kostet dich nichts, oder?' — Kern-Frage der Ungerechtigkeit",
       pov="B2 Kap 7 · Alphina", mz=0.4,
       figuren=["Alphina", "Elke"],
       detail="Elke sieht Alphinas Hain. 'Das hast du in einer Nacht getan. Das kostet dich nichts, oder?' Alphinas Antwort: 'Nein.' Elkes Gesicht: zwischen Neid und Angst.",
       tags=["Tschechow: Ungerechtigkeit als Kernthema"]),

    ev("08", ["erkenntnis"],
       "Maren sucht das Portal durchs Wasser — findet es, aber geschlossen",
       pov="B2 Kap 8 · Maren", mz=0.45,
       tags=["Tschechow: Maren sucht den Rueckweg"]),

    ev("09", ["erkenntnis"],
       "Elke zu Runa: 'Hier bist du mehr' — Runas Feuer-Resonanz erkannt",
       pov="B2 Kap 9 · Runa", mz=0.5,
       figuren=["Runa Kvist", "Elke"]),

    ev("10", ["schlüssel"],
       "Die Gilden-Stadt empfaengt die Fuenf — die Aelteste greift Alphinas Hand",
       pov="B2 Kap 10 · Alphina", mz=0.6,
       detail="Tuerme die gewachsen sind, Strassen die sich verschieben. Die Aelteste: 'Ihr seid sicher hier.' Alphinas Hain hat sich herumgesprochen. Waffe.",
       tags=["Schluesselereignis: Ankunft Gilden-Stadt"]),
]


# =============================================================================
# BUCH 2 — AKT II: Die Fraktionen (monat[12], MZ Monat 2)
# =============================================================================

AKT2 = [
    ev("12", ["begegnung", "tschechow"],
       "Vesper trifft Talven in der Gilden-Bibliothek",
       pov="B2 Kap 12 · Vesper", mz=1.1,
       figuren=["Vesper", "Talven"],
       intensitaet="fluechtig",
       detail="Talven, 23, bringt die Reservoir-Karten aus dem Suedarchiv. Hilfsbereit, schnell, der Typ der Probleme loest bevor man sie ausspricht.",
       tags=["Erste Begegnung: Talven", "Tschechow: Talvens Hunger"]),

    ev("15", ["schlüssel"],
       "Die Gilden-Aelteste bietet Alphina Schutz — fuer Kriegsdienst",
       pov="B2 Kap 15 · Alphina", mz=1.3,
       detail="Die Binder ruecken vor. Die Gilden brauchen Alphinas Resonanz. Talven fluestert die Nuancen — und sein Gesicht zeigt fuer einen Moment Hunger.",
       tags=["Schluesselereignis: Erstes Gilden-Angebot"]),

    ev("16", ["erotik"],
       "Alphina und Runa: erster Kuss auf dem Dach",
       pov="B2 Kap 16 · Alphina", mz=1.4,
       figuren=["Alphina", "Runa Kvist"],
       intensitaet="bekannt",
       detail="Zwei Menschen die nicht wissen was sie tun. Bei Sorel hat die Welt geblueht — bei Runa ist sie still. Die Stille macht Angst.",
       tags=["Beziehung: Alphina + Runa"]),

    ev("18", ["begegnung", "schlüssel"],
       "Nyr trifft Vesper — Thar-Emissaerin ueberzeugt ihn",
       pov="B2 Kap 18 · Vesper", mz=1.5,
       figuren=["Vesper", "Nyr"],
       intensitaet="fluechtig",
       detail="Nyr kommt in ihrer Magitech-Bestie Kessler. 'Jedes System hat Fehler. Die Thar benennen ihre.' Vesper geht mit ihr — bewusste Wahl, nicht Entfuehrung.",
       tags=["Erste Begegnung: Nyr", "Schluesselereignis: Vesper zu den Thar"]),

    ev("19", ["schlüssel", "tschechow"],
       "Das Dorf-Desaster — Alphinas Schlaf-Wald verschluckt ein halbes Dorf",
       pov="B2 Kap 19 · Alphina", mz=1.6,
       detail="Tagsueber kontrolliert, nachts unkontrolliert. Die Dorfbewohner evakuieren — nicht vor den Bindern, vor IHR. Talven sieht den Hain und sein Hunger waechst.",
       tags=["Schluesselereignis: Schlaf-Wald als Waffe sichtbar"]),

    ev("20", ["schlüssel"],
       "Alphina wird zur Bund-Waffe — Angriff auf Quellen beginnt",
       pov="B2 Kap 20 · Alphina", mz=1.8,
       detail="Der Bund setzt Alphina offensiv ein. Wurzeln durch feindliche Stellungen. Alphina hoert auf Fragen zu stellen. Der Hass auf Varen fuehlt sich produktiv an.",
       tags=["Schluesselereignis: Alphina als Waffe"]),
]


# =============================================================================
# BUCH 2 — AKT III: Das Schlachtfeld (monat[13], MZ Monat 3)
# =============================================================================

AKT3 = [
    ev("21", ["hintergrund"],
       "Alphina an der Front — Wochen als Bund-Waffe",
       pov="B2 Kap 21 · Alphina", mz=2.1),

    ev("25", ["schlüssel", "tod"],
       "Alphina zerstoert eine Reservoir-Quelle — ABSICHTLICH — Wendepunkt des Romans",
       pov="B2 Kap 25 · Alphina", mz=2.3,
       detail="Draels Befehl, Alphinas Druecken. Wurzeln bis zum Quellen-Kern. Die Quelle stirbt. Ein Kreis aus totem Land, 200m Radius. Vierhundert Menschen ohne Magie. Sie wollte es. Sie drueckt auf die naechste.",
       tags=["Schluesselereignis: Erste absichtliche Quellen-Zerstoerung", "Tod: Reservoir-Quelle"]),

    ev("26", ["schlüssel"],
       "Varen schlaegt zu — Alphina in Ketten, Runa sieht es aus der Ferne",
       pov="B2 Kap 26 · Alphina", mz=2.35,
       detail="Varens Schemen stroemen ueber das Schlachtfeld. Bindungsmagie-Ketten um Alphinas Handgelenke. Runa kaempft — toetet Dutzende Schemen mit brennenden Haenden. Wird zurueckgeschlagen.",
       tags=["Schluesselereignis: Alphina gefangen"]),

    ev("27", ["erkenntnis"],
       "Varen zeigt Alphina die vier toten Quellen an der Wand — drei seine, eine ihre",
       pov="B2 Kap 27 · Alphina", mz=2.4,
       detail="Varens Quartier ist kein Gefaengnis, sondern ein Labor. 'Die Quelle die du getoetet hast — sie hat eine Siedlung von vierhundert Menschen versorgt.' Die Ketten klirren nicht mehr.",
       tags=["Erkenntnis: Vierhundert", "Schluesselereignis: Varens Karten"]),

    ev("28", ["erkenntnis", "schlüssel"],
       "Die Wahrheit sickert: Der Bund zerstoert Quellen systematisch",
       pov="B2 Kap 28 · Alphina", mz=2.5,
       detail="Abgefangene Bund-Kommunikation. Nicht Draels Improvisation — PLAN. Alphina war nicht die Erste. Nur die Staerkste. Ihr Selbstbild zerbricht.",
       tags=["Erkenntnis: Bund-Wahrheit"]),

    ev("29", ["schlüssel"],
       "Runa beim Bund, erkennt die Wahrheit — plant Alphinas Befreiung",
       pov="B2 Kap 29 · Runa", mz=2.55,
       detail="Dokumentation zu gross um ignoriert zu werden. Runa brennt Loecher in den Tisch. Weiss nicht dass Alphina bereits wechselt.",
       tags=["Tschechow: Runa als Chronistin"]),
]


# =============================================================================
# BUCH 2 — AKT IV: Neue Fronten (monat[14], MZ Monat 4+)
# =============================================================================

AKT4 = [
    ev("31", ["erkenntnis", "schlüssel"],
       "Varens Gestaendnis: Sein Experiment hat drei Quellen zerstoert und den Krieg ausgeloest",
       pov="B2 Kap 31 · Alphina", mz=3.1,
       detail="'Niemand weiss es. Nur du.' Thalassische Resonanz als Herzschrittmacher fuer tote Quellen — der einzige Weg zur Reparatur.",
       tags=["Schluesselereignis: Varens Gestaendnis"]),

    ev("32", ["erkenntnis"],
       "Alphinas Schuld-Spiegelung — sie ist die Frau die den Krieg fuehrt",
       pov="B2 Kap 32 · Alphina", mz=3.15,
       detail="Drei Quellen (Unfall) + eine Quelle (absichtlich). Wer ist schlimmer? Alphinas Selbstbild broeckelt.",
       tags=["Erkenntnis: Selbstbild zerbricht"]),

    ev("35", ["erotik", "schlüssel"],
       "Alphina und Varen: Sex, Dornen statt Farne — zwei Taeter die sich erkennen",
       pov="B2 Kap 35 · Alphina", mz=3.3,
       figuren=["Alphina", "Varen"],
       intensitaet="intim",
       detail="Gewachsen aus geteilter Schuld, nicht aus Anziehung. Kontrolle durch Erkenntnis. Dornen wachsen durch Stein. Die Ketten auf dem Boden — sie hat sie irgendwann gebrochen.",
       tags=["Erotik: Alphina + Varen", "Tschechow: Dornen statt Farne"]),

    ev("36", ["schlüssel"],
       "Alphina wechselt die Seite — Verbuendete, nicht Gefangene",
       pov="B2 Kap 36 · Alphina", mz=3.35,
       detail="Sie vergibt Varen Sorels Tod NICHT. Aber sie steht auf seiner Seite. Ihre Resonanz kann Quellen reparieren. Das ist Zweck, nicht Vergebung.",
       tags=["Schluesselereignis: Alphina wechselt Seite"]),

    ev("37", ["schlüssel"],
       "Runa beim Bund — erkennt dass der Befreiungsplan sinnlos ist",
       pov="B2 Kap 37 · Runa", mz=3.4,
       detail="Nicht weil er nicht funktioniert — weil die Seite fuer die sie kaempft die falsche ist. Runa verlaesst den Bund.",
       tags=["Schluesselereignis: Runa verlaesst Bund"]),

    ev("38", ["portal", "schlüssel"],
       "Maren findet den Rueckweg — Portal-Ritual fuer die Moragh-Seite",
       pov="B2 Kap 38 · Vesper+Maren", mz=3.5,
       detail="Thar-Bibliothek, alte Karten. Maren hat genug Resonanz fuer den Hinweg Moragh→Thalassien. Nicht fuer den Rueckweg. Vesper bleibt, sie geht. Der Abschied: 'Ich weiss.'",
       tags=["Portal", "Schluesselereignis: Maren findet Rueckweg"]),

    ev("39", ["schlüssel"],
       "Maren in Thalassien ~1910 — gestrandet, gruendet die Schwellenforschungsgesellschaft",
       pov="B2 Kap 39 · Maren", welt="thalassien", mz=3.55,
       detail="Die Welt hat sich veraendert — Elektrizitaet, Automobile. Vael ist Industriestadt. Der Steinkreis: vergessen. Maren gruendet in Halvards Namen die Schwellenforschungsgesellschaft.",
       tags=["Schluesselereignis: Maren gestrandet in 1910"]),

    ev("I12", ["tschechow"],
       "Talven verteilt geerntete Resonanz — beide Augen werden milchig",
       pov="B2 I12 · Talven", mz=3.6,
       detail="Talven ist Moragh-Held. Verteilt geerntete Resonanz aus Alphinas Schlaf-Spuren an die Armen. Seine Augen wolkig, Haare duenner, Naegel bruechig. Er laechelt: 'Es geht mir gut.'",
       tags=["Tschechow: Talven zerfaellt"]),

    ev("40", ["schlüssel"],
       "Runa zum Thar-Konglomerat — zu ihren Bedingungen",
       pov="B2 Kap 40 · Runa", mz=3.7,
       detail="Nicht wegen Kael — trotz Kael. Die Thar haben Ehrlichkeit ueber ihre Brutalitaet. Die Druckerin wird Schmiedin. 'Nuetzlich' ist das Wort das sie hoert.",
       tags=["Schluesselereignis: Runa zu den Thar"]),

    ev("42", ["hintergrund"],
       "Ende Buch 2: Alle getrennt, alle gebrochen",
       pov="B2 Kap 42 · Alle", mz=3.9,
       detail="Alphina+Varen (Verbuendete). Runa beim Konglomerat. Vesper+Nyr bei den Thar. Maren gestrandet in Thalassien. Talven, Gilden-Held, milchige Augen.",
       tags=["Epilog Buch 2"]),
]


# =============================================================================
# MAIN
# =============================================================================

def assign_mz(event):
    """Entferne internal _welt marker; bereinige das Event."""
    e = {k: v for k, v in event.items() if not k.startswith("_")}
    return e


def main():
    with open(ZEITLEISTE, encoding="utf-8") as f:
        z = json.load(f)

    # Akt -> monat Zuordnung
    akt_monat = {
        1: 11,
        2: 12,
        3: 13,
        4: 14,
    }

    groups = [
        (1, AKT1),
        (2, AKT2),
        (3, AKT3),
        (4, AKT4),
    ]

    added_total = 0
    for akt_num, events in groups:
        monat = z["monate"][akt_monat[akt_num]]
        existing_keys = set()
        for bucket in ("thalassien", "moragh"):
            for e in monat["events"].get(bucket, []):
                existing_keys.add((e.get("kapitel"), e.get("titel")))

        for raw in events:
            welt = raw["_welt"]
            clean = assign_mz(raw)
            key = (clean["kapitel"], clean["titel"])
            if key in existing_keys:
                continue
            monat["events"].setdefault(welt, [])
            monat["events"][welt].append(clean)
            existing_keys.add(key)
            added_total += 1

    with open(ZEITLEISTE, "w", encoding="utf-8") as f:
        json.dump(z, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print(f"OK: {added_total} Buch-2-Events hinzugefuegt")
    for akt_num, events in groups:
        m_idx = akt_monat[akt_num]
        m = z["monate"][m_idx]
        thal = len(m["events"].get("thalassien", []))
        mor = len(m["events"].get("moragh", []))
        print(f"  Akt {akt_num} -> monat[{m_idx}] ({m.get('label','-')})  thal={thal}  mor={mor}")


if __name__ == "__main__":
    main()
