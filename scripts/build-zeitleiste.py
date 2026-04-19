#!/usr/bin/env python3
"""
Baut buch/zeitleiste.json komplett neu aus den SoT-Kanon-Quellen.

Schema (neu, flach):
  {
    "meta": {...},
    "typen": {...},
    "events": [  # strikt chronologisch nach tz_sort
      {
        "tz": 154, "tz_sort": 154.0, "tz_datum": "3. Nebelmond 154",
        "mz": null,
        "welt": "thalassien" | "moragh" | "synchronisation",
        "pov": "Elke",
        "buch": "B1", "kapitel": "I1",
        "leseart": "interludium" | "normal" | "rueckblende" | "vorschau",
        "titel": "...",
        "detail": "...",
        "typen": ["begegnung", "wohnort"],
        "tags": [],
        "kapitel_status": "final" | "entwurf" | "idee" | "",
        "sync": { "thalassien": "...", "moragh": "..." }  # nur bei welt="synchronisation"
      }
    ]
  }

Ankerpunkte (laut B3-ZEITLEISTE.md):
  TZ 154 (=MZ -5.5 grob) — Elke + 3 in Vael, Elkes Durchgang
  TZ 551 (=MZ 0) — B1-Start, 21. Saatmond 551
  TZ ~553 (=MZ ~1) — B1-Ende, Portalübertritt Vier + Runa
  TZ 1987 (=MZ 5) — Maren tritt durch nach Thalassien
  TZ 2153 (=MZ 10) — B3-Ende, Portal tot

Ratio: 1 Moragh-Jahr = 400 TZ-Jahre = 12 Moragh-Monate = 33.33 TZ-Jahre/MZ-Monat.

Aufruf:
  python scripts/build-zeitleiste.py           # dry-run
  python scripts/build-zeitleiste.py --apply   # schreibt zeitleiste.json
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "buch" / "zeitleiste.json"

# ---------------------------------------------------------------------------
# Konstanten / Helpers
# ---------------------------------------------------------------------------

# Roman-interne TZ-Jahreszahl: B1-Start = 551 TZ. B3-Ende = 884 TZ (551+333).
# Die B3-ZEITLEISTE.md nutzt parallel 1820–2153 als "real-world-Äquivalent";
# wir bleiben bei der Roman-internen 551er-Zählung, weil Kapitel-Header das nutzen.
TZ_B1_START = 551
MZ_PER_TZ_YEAR = 1 / 400   # Moragh-Zeit läuft langsamer
TZ_PER_MZ_MONAT = 400 / 12  # = 33.33 TZ-Jahre pro Moragh-Monat

THAL_MONATE = [
    "Eismond", "Sturmmond", "Saatmond", "Gruenmond", "Bluetenmond",
    "Lichtmond", "Glutmond", "Erntemond", "Herbstmond", "Nebelmond",
    "Frostmond", "Dunkelmond",
]
THAL_MONAT_UMLAUT = {
    "Gruenmond": "Grünmond", "Bluetenmond": "Blütenmond",
}

def thal_datum(tag: int, monat_nr: int, jahr: int) -> str:
    m = THAL_MONATE[monat_nr - 1]
    m = THAL_MONAT_UMLAUT.get(m, m)
    return f"{tag}. {m} {jahr} TZ"


def mz_to_tz(mz: float) -> float:
    """Rechnet MZ-Monat-Wert in TZ-Jahr-Äquivalent um (ab MZ 0 = TZ 551)."""
    return TZ_B1_START + mz * TZ_PER_MZ_MONAT


def tz_to_float_date(jahr: int, monat_nr: int = 1, tag: int = 1) -> float:
    """TZ als Float (jahr + monat_anteil + tag_anteil) für Sortierung."""
    tage_pro_monat = 365 / 12
    tag_im_jahr = (monat_nr - 1) * tage_pro_monat + tag
    return jahr + tag_im_jahr / 365


# ---------------------------------------------------------------------------
# Event-Typen-Katalog
# ---------------------------------------------------------------------------

TYPEN = {
    "portal":       {"label": "Portal",       "farbe": "#8b4513"},
    "begegnung":    {"label": "Begegnung",    "farbe": "#4a6a7a"},
    "erkenntnis":   {"label": "Erkenntnis",   "farbe": "#6a5080"},
    "erotik":       {"label": "Erotik",       "farbe": "#8b3a5a"},
    "schluessel":   {"label": "Schlüssel",    "farbe": "#b8860b"},
    "tod":          {"label": "Tod",          "farbe": "#6b6259"},
    "tschechow":    {"label": "Tschechow",    "farbe": "#5a7a5a"},
    "hintergrund":  {"label": "Hintergrund",  "farbe": "#555555"},
    "wohnort":      {"label": "Wohnort",      "farbe": "#7a6a4a"},
    "wissen":       {"label": "Wissen",       "farbe": "#5a6a8a"},
    "resonanz":     {"label": "Resonanz",     "farbe": "#6a8a5a"},
    "gaensehaut":   {"label": "Gänsehaut",    "farbe": "#8b6a8b"},
    "verabredung":  {"label": "Verabredung",  "farbe": "#5a8a7a"},
    "krieg":        {"label": "Krieg",        "farbe": "#8a4040"},
    "sync":         {"label": "Synchronisation", "farbe": "#c8bfb0"},
}


# ---------------------------------------------------------------------------
# Event-Sammlung
# ---------------------------------------------------------------------------

EVENTS: list[dict[str, Any]] = []


def add(ev: dict[str, Any]) -> None:
    # Default-Felder
    ev.setdefault("leseart", "normal")
    ev.setdefault("typen", [])
    ev.setdefault("tags", [])
    ev.setdefault("kapitel_status", "")
    # tz_sort = Float für Sortierung
    if "tz_sort" not in ev:
        ev["tz_sort"] = float(ev.get("tz", 0))
    EVENTS.append(ev)


# =====================================================================
# BLOCK 1 — TZ 154: Elke + drei andere in Vael (400 Jahre vor B1)
# =====================================================================

def block_tz_154() -> None:
    """I1, I2, I3 — Ankunft, Feuer-Schemen, Portal-Durchgang."""

    # I1 — Elkes Ankunft in Vael
    add({
        "tz": 154, "tz_sort": tz_to_float_date(154, 10, 1),
        "tz_datum": "1. Nebelmond 154 TZ",
        "welt": "thalassien", "pov": "Elke",
        "buch": "B1", "kapitel": "I1", "leseart": "interludium",
        "titel": "Elke kommt nach Vael — wegen Purpursteins",
        "detail": "Elke van der Holt, Bildhauerin aus dem Süden, reitet drei Tage durch dunkler werdende Wälder nach Vael. Ihr Ziel: ein Gestein, das es nirgendwo sonst gibt — Purpurstein, fast schwarz, mit schimmernden Einschlüssen. Der Händler Hendryk begleitet sie, dreht sich zweiten Tag unruhig im Sattel nach Norden um. Vael empfängt sie in Nebel, der wie ein Atmen aus dem Fels kommt.",
        "typen": ["begegnung", "wohnort"],
        "tags": ["Erste Begegnung: Vael", "Purpurstein"],
        "kapitel_status": "final",
    })

    # I2 — Keldan & Kesper & Lene, Vier Fremde, Resonanz-Anfänge
    add({
        "tz": 154, "tz_sort": tz_to_float_date(154, 11, 15),
        "tz_datum": "15. Frostmond 154 TZ · 6 Wochen in Vael",
        "welt": "thalassien", "pov": "Elke",
        "buch": "B1", "kapitel": "I2", "leseart": "interludium",
        "titel": "Vier Fremde in Vael — Keldans Eisen singt",
        "detail": "Elke trifft Keldan Rohn, den Schmied am Hafen. Sein Eisen wird zu weich, gibt nach wie Zinn. Die Esse steht auf nacktem Purpurstein, der immer warm bleibt. Aldert der Wirt bringt sie zusammen mit Kesper (Maler, Pigmente in den Falten der Knöchel) und Lene (junge Schreiberin, Dahl-Familie, wird später das Manuskript verfassen). Vier Fremde, deren Material sich anders verhält als erwartet.",
        "typen": ["begegnung", "resonanz", "tschechow"],
        "tags": ["Keldan Rohn", "Kesper Holm", "Lene Dahl", "Tschechow: Manuskript"],
        "kapitel_status": "final",
    })

    # I3 — Feuer-Schemen & Portal-Durchgang (Synchronisationspunkt!)
    add({
        "tz": 154, "tz_sort": tz_to_float_date(154, 11, 28),
        "tz_datum": "28. Frostmond 154 TZ",
        "welt": "thalassien", "pov": "Elke",
        "buch": "B1", "kapitel": "I3", "leseart": "interludium",
        "titel": "Die Nacht des grossen Feuers — Kesper bringt sein letztes Bild",
        "detail": "Erscheinungen sind anders geworden — Lene sah eine aufrechte Gestalt, Keldan zählte sieben Schemen am Hafen in einer Nacht. Kesper bringt Elke sein letztes Bild und setzt sich an ihr Bett. Terpentin, Leinöl, Indigo in den Falten. Die Schemen in der Stadt haben sich nicht mehr wie Tiere bewegt — sie sind gefolgt, geduldig, zielgerichtet.",
        "typen": ["gaensehaut", "schluessel"],
        "tags": ["Feuer-Schemen", "Tschechow: Varen-Bindung"],
        "kapitel_status": "final",
    })

    # Portal-Durchgang (Synchronisation)
    add({
        "tz": 154, "tz_sort": tz_to_float_date(154, 11, 28) + 0.01,
        "tz_datum": "28. Frostmond 154 TZ · Nacht",
        "mz": -5.5,
        "welt": "synchronisation", "pov": "Elke / Varen",
        "buch": "B1", "kapitel": "I3", "leseart": "interludium",
        "titel": "Portal-Übertritt — Elke geht durch, Varen empfängt",
        "detail": "Drei Feuer-Schemen wüten in Vael. Die Vier öffnen das Portal von der Thalassien-Seite. Kesper und Keldan sterben im Kampf. Elke tritt durch. Lene überlebt als Einzige, wird später das Manuskript schreiben. Auf der Moragh-Seite: Varen kappt die Schemen-Bindung, sobald er Elke empfangen hat — die Schemen lösen sich in Vael in Rauch auf.",
        "typen": ["portal", "tod", "schluessel"],
        "sync": {
            "thalassien": "Kesper + Keldan sterben. Lene überlebt, schreibt das Manuskript (später von Varen überschrieben).",
            "moragh": "Varen empfängt Elke. Kappt Schemen-Bindung in Vael. Beginn ihrer sechs Monate in Mar-Keth.",
        },
        "tags": ["Portal-Ritual", "Kesper tot", "Keldan tot", "Lene Überlebende"],
        "kapitel_status": "final",
    })


# =====================================================================
# BLOCK 2 — Zeitsprung ~400 Jahre (TZ 154 → TZ 551, MZ -5 → MZ 0)
# =====================================================================

def block_zeitsprung() -> None:
    """Moragh-Hintergrund zwischen Elkes Ankunft und B1-Start.
    Nur relevante Moragh-Events: Varen + Elke, Trennung, Mar-Keth-Unfall, Krieg,
    Portalforschung. Thalassien-Seite: 400 Jahre Industrialisierung."""

    # MZ -5 bis MZ -4.5 — Elke + Varen zusammen, sechs Monate
    add({
        "tz": 354, "tz_sort": 354.0,  # rund Mitte zwischen 154 und 551
        "mz": -5.0,
        "welt": "moragh", "pov": "Elke / Varen",
        "buch": "B0", "kapitel": "", "leseart": "hintergrund",
        "titel": "Elke + Varen — sechs Monate in Mar-Keth",
        "detail": "Varen (junger Velmar-Forscher, Haus Keth) und Elke leben sechs Moragh-Monate zusammen. Forschungspartnerschaft und Liebesgeschichte. Elke lehrt ihm Thalassisch, er ihr Moragh. Dann trennt sie sich — sie spürt, dass seine Forschung sie als Mittel braucht, nicht als Partnerin. Elke zieht weiter, weiß nichts von seinen späteren Plänen.",
        "typen": ["begegnung", "hintergrund"],
        "tags": ["Mar-Keth", "Haus Keth"],
    })

    # MZ -3 — Mar-Keth-Unfall, drei Quellen tot
    add({
        "tz": 400, "tz_sort": 400.0,
        "mz": -3.0,
        "welt": "moragh", "pov": "Varen",
        "buch": "B0", "kapitel": "", "leseart": "hintergrund",
        "titel": "Varens Leylinien-Experiment scheitert",
        "detail": "Varen versucht drei benachbarte Quellen unter Mar-Keth zu koppeln, um magiefreie Flächen besiedelbar zu machen. Unfall: Mar-Keth, Dulrath-Ost und Reshkol kollabieren unwiederbringlich. ~200.000 Menschen heimatlos. Velmar (Haus Keth) vertuscht intern und stößt Varen ohne öffentliche Anklage aus. Der Bund hält es für Naturkatastrophe, die Thar beschuldigen den Bund.",
        "typen": ["tod", "hintergrund"],
        "tags": ["Mar-Keth-Unfall", "drei Quellen tot", "Varen ausgestossen"],
    })

    # MZ -2.5 — Krieg beginnt
    add({
        "tz": 420, "tz_sort": 420.0,
        "mz": -2.5,
        "welt": "moragh", "pov": "",
        "buch": "B0", "kapitel": "", "leseart": "hintergrund",
        "titel": "Der Krieg beginnt — Orath vs. Thar",
        "detail": "Das Thar-Konglomerat glaubt, der Bund von Orath habe die Mar-Keth-Explosion absichtlich ausgelöst und schlägt zurück. Krieg aus Misstrauen, nicht aus Ressourcennot. Er dauert vier MZ-Jahre (~1.600 TZ). Velmar hält sich raus.",
        "typen": ["krieg", "hintergrund"],
        "tags": ["Orath-Thar-Krieg"],
    })

    # MZ -2 — Varen beginnt Portalforschung
    add({
        "tz": 450, "tz_sort": 450.0,
        "mz": -2.0,
        "welt": "moragh", "pov": "Varen",
        "buch": "B0", "kapitel": "", "leseart": "hintergrund",
        "titel": "Varen beginnt im Geheimen die Portalforschung",
        "detail": "Varen erkennt, dass tote Quellen mit Moragh-Magie allein nicht wiederzubeleben sind. Er erinnert sich an die 350 Verschwundenen vor 200 MZ-Jahren durchs Portal. Beginnt die Rekonstruktion — Druckmanipulation beherrscht er, Zeitmanipulation muss er lernen. Erste brachiale Versuche ab MZ -3 erzeugen Raumzeit-Risse.",
        "typen": ["tschechow", "hintergrund"],
        "tags": ["Portalforschung", "Tschechow: Risse in Thalassien"],
    })

    # MZ -1 — Haron Dahl entsendet
    add({
        "tz": 485, "tz_sort": 485.0,
        "mz": -1.0,
        "welt": "moragh", "pov": "Varen",
        "buch": "B0", "kapitel": "", "leseart": "hintergrund",
        "titel": "Varen entsendet Haron Dahl nach Vael",
        "detail": "Varen schickt Agenten per Portal nach Thalassien — Moragh-Geborene mit altem Thalassisch (von Elke gelernt), begleitet von gebundenen Schemen. Haron Dahl kommt als junger Mann in Vael an, lebt unter falschem Namen, baut Boote in Lenes alter Werft. Stirbt vor B1 an Moragh-Körper-Schwerkraft-Mismatch.",
        "typen": ["tschechow", "hintergrund"],
        "tags": ["Haron Dahl", "Moragh-Agenten", "Tschechow: Boot"],
    })

    # Thalassien-Synchronisation über 400 Jahre (grob)
    add({
        "tz": 540, "tz_sort": 540.0,
        "welt": "synchronisation", "pov": "",
        "buch": "", "kapitel": "", "leseart": "hintergrund",
        "titel": "Thalassien — 400 Jahre später",
        "detail": "Knapp 400 Jahre zwischen Elkes Durchgang und B1-Start. Vael hat sich industrialisiert: Gaslampen statt Öllampen, Druckpressen statt Druckstöcken, erste Dampfschiffe am Hafen, Schreibmaschinen in Kontoren. Lenes Manuskript liegt im Archiv, von Varen überschrieben. Der Botanische Garten ist gewachsen, der Steinkreis steht unverändert. Riss-Phänomene nehmen zu: Farne ohne Licht, Wasser das rückwärts fliesst, Schemen in Kellern.",
        "typen": ["sync", "hintergrund"],
        "sync": {
            "thalassien": "Industrialisierung, Vael TZ 551. Riss-Phänomene eskalieren seit Varens brachialer Portal-Aktivität (MZ -3). Das Archiv hütet Lenes (überschriebenes) Manuskript.",
            "moragh": "MZ 0. Varens Plan reift: vier Thalassier-Resonanzen nach Vael locken. Ritual, Sprachbuch, Anleitung sind durch Schemen platziert.",
        },
        "tags": ["Zeitsprung", "Industrialisierung"],
    })


# ---------------------------------------------------------------------------
# Main (Stand: nur Block 1+2 — B1/B2/B3 kommen in naechsten Iterationen)
# ---------------------------------------------------------------------------

# Erweiterte Detail-Texte fuer B1-K01..K08-Events (statt OLD-Kuerze)
# Quelle: buch/kapitel/0{1..8}-*.md (finale Kapitel-Files)
B1_DETAIL_OVERRIDES: dict[str, str] = {
    "Ein Farn dreht seinen Wedel nach Alphina":
        "Asplenium nidus am Fenster, die Erde warm wie Haut. Alle fünf Wedel schwenken ruckartig auf sie zu, als sie den Namen Vael auf dem Brief liest.",
    "Alphina wohnt in Velde":
        "Vierter Stock, Giebelhaus am Kanal, seit elf Jahren. 49 Pflanzen, die Monstera kennt ihren Weg zur Treppe. Sie nennen sie die Hexe im Vierten.",
    "Alphina: Farn dreht sich nach ihr":
        "Drei Uhr morgens, die Erde im Topf warm wie Haut. Sie testet zehnmal nach links und rechts, der Farn folgt. Kein Phototropismus, keine Zugluft. Eine Antwort.",
    "Sorel findet sein Gesicht auf einer Glasplatte aus Vael":
        "Kollodium-Nassplatte, Nummer sieben, aus einem Auktionslos Grauküste. Im Rotlicht steigt der Hafen auf, dann sein eigenes Gesicht im Dunst, ruhig und wissend.",
    "Sorel wohnt in Nachtholm":
        "Kellerwohnung in der Schluchtstadt, seit dreizehn Jahren. Basalt unter den Füssen, Rotlicht, 263 Gesichter toter Fremder an der Wand. Er schläft tags.",
    "Sorel: Sein eigenes Gesicht auf fremder Glasplatte":
        "Platte 7 aus dem Vael-Los, 1783–1791. Sein Gesicht im Nebel der Kaimauer, schärfer als der Rest. Die zweite Platte nach Falkensand — dreizehn Jahre Suche.",
    "Sorel: Hinweis Vael Lichthaus Keller":
        "Rückseite der Platte, verblasste braune Tinte, sorgfältige kleine Schrift. Drei Wörter, die ein Ziel benennen, das er nie betreten hat.",
    "Reisender Uhrmacher erzählt von der 4:33-Standuhr":
        "Grosser Fremder im Gasthaus »Zur Feder«, marineblaue Augen, Hände ohne Hornhaut. Erzählt beiläufig von einem Herrenhaus in Vael, einer Standuhr, die täglich 273 Sekunden verliert.",
    "Vesper wohnt in Karst":
        "Uhrmacherwerkstatt in der Innenlandestadt, sechsundzwanzig Uhren im Regal, jede in eigenem Tempo. Seit dreizehn Jahren keine Diagonalen mehr, nur Zahnräder.",
    "Vesper trifft den reisenden Uhrmacher":
        "Fremder Akzent, fragt nach Rubinlagern wie nach einer Landkarte. Marineblauer Blick, der misst. Setzt die Zahl 273 hinter Vespers Stirn und verschwindet spurlos in die Gasse.",
    "Maren erbt Haron Dahls Werft und das halbfertige Boot":
        "Brief des Notars. Fünf Jahre Briefwechsel, einundsechzig Briefe, nie getroffen. Werft am Wasser, Lederschürze am Haken, dreiviertel fertiger Rumpf auf Böcken.",
    "Maren: Haron ging nachts in den Garten":
        "Edric erzählt es in der Werft, zum Hobel, nicht zu ihr. Haron am Klippenrand, jede Nacht spät, nie ein Wort dazu. Feine Hände, spät gelernt, falscher Akzent.",
    "Maren: Das Boot ist dreiviertel fertig":
        "Kiel aus Eiche, Spanten aus Esche, dampfgebogen. Drei Lagen Lärche eingepasst, oben nackte Spanten. Der Knoten im Heckholz geblieben, um ihn herumgeschnitten.",
    "Alphina in Vael. Trifft Runa Kvist — Druckerin mit warmen Händen.":
        "Druckerei in der Oberstadt, Geruch von heissem Blei und Hadernpapier. Runa: kurzes dunkles Haar, Druckerschwärze an den Unterarmen, Hände so heiss, dass Alphinas Finger zurückzucken.",
    "Alphina bezieht den Anker":
        "Gasthaus in der Hafengasse, zweiter Stock, linke Tür. Drei Schritte breit, Kamin aus Purpurstein, Wochenpreis im Voraus. Das Zimmer reicht für einen Koffer und ein Notizbuch.",
    "Alphina: Schattentiere in Vael":
        "Hafengasse nach Mitternacht. Katzengross, faserige Körper aus Rauch, leuchtend schwarze Augen, sitzen an der Wand als gäbe es keine Schwerkraft. Verschwinden beim Blinzeln. Drei Stück.",
    "Sorel bezieht das Lichthaus":
        "Dreistöckiges Speichergebäude am Hafen, wie auf der Platte. Keller mit warmer Wand, der nach Fixierer riecht, obwohl leer. Ein alter Nagel sitzt genau dort, wo er die Schnur spannen wollte.",
    "Sorel: Kratzspuren am Hafenpoller":
        "Am Kai wartet eine rauchende Gestalt mit Hufen, anderthalb Köpfe grösser, mit Sorels eigenem Gesicht. Nach dem Verschwinden am Poller drei parallele Rillen, Ränder glatt verschmolzen, warm.",
    "Standuhr verliert 4:33 — reagiert auf Vesper":
        "Tidemoor-Haus am Grauwe-Ufer. Hand aufs Nussbaumgehäuse: Null Abweichung. Hand weg: 273 Sekunden wieder. Drei Durchgänge, sechs Stunden, dasselbe Ergebnis.",
    "Vesper bezieht den Anker":
        "Zweiter Stock, selbe Hafengasse wie Alphina, selbes Haus. Schmales Bett, Werkzeugrolle auf dem Tisch, Pinzetten in ihrer Reihe. Tagsüber am Tidemoor-Haus an der Standuhr.",
    "Vesper: Standuhr verliert 4:33 pro Tag":
        "Nussbaumgehäuse, Pendel einwandfrei, Ankerrad sauber, keine Verschleiss-Spur. Hundertzwanzig Halbschwünge pro Minute, jeder an der richtigen Stelle. Trotzdem 273 Sekunden Verlust.",
    "Vesper: Die Uhr reagiert auf seine Hand":
        "Handfläche aufs Gehäuse, Wärme kriecht von innen durch das Holz. Sein Puls findet einen fremden Puls. Die Abweichung verschwindet. Hand weg: 4:33. Wie ein Lebewesen, das sich an ihn schmiegt.",
    "Vesper: Heißes Wasser ohne Kessel":
        "Tidemoor-Küche nach Mitternacht. Hahn aufgedreht, siebzig Sekunden bis der Dampf steigt. Rohre am Spülstein kalt, im Keller kalt. Kein Kessel, kein Ofen, kein Brennstoff.",
    "Vesper: Kratzspuren am Kellerfenster":
        "Aus der Ecke ein Kratzen, drei Striche, Pause, drei Striche. Am Rahmen drei parallele Rillen, zwanzig Zentimeter, Kanten wie geschmolzen. Warm wie Sorels Poller. Dieselbe Hand.",
    "Boot baut sich nachts weiter — Schemen arbeiten":
        "Unter dem alten Segel versteckt, sieht Maren eine rauchende Gestalt durchs Tor gleiten. Breite Schultern, schwere Hände mit glänzenden Fingerspitzen, setzt eine Lärchenplanke ohne Hammer ein.",
    "Maren trifft Tohl Daverin":
        "Fischer, vierzig Jahre auf der Grauwe, Gesicht wie Treibholz. Sitzt jeden Morgen am Stegende. Zeigt ihr den rückwärts fliessenden Streifen: »Ich will, dass Sie's erkennen, nicht glauben.«",
    "Maren: Das Boot wächst nachts weiter":
        "Jeden Morgen eine neue Planke, fünfte Reihe Steuerbord, Lärche, warm. Naht so eng, dass der Fingernagel nicht hineinpasst. Ihr Bleistiftstrich: morgens abgeschliffen, die Lücke darunter geschlossen.",
    "Maren: Wasser fließt rückwärts in die Werft":
        "Tohl zeigt es an der Mündung: ein zehn Meter breiter Streifen läuft flussaufwärts gegen das Gefälle. Seit drei Wochen, erst nachts, jetzt auch tags. Ein Rinnsal sucht ihre Hand auf dem Werftboden.",
    "Maren: Pochen unter der Werft":
        "Ohr auf das warme Bretterholz. Tief, so tief dass sie es fühlt statt hört: einmal, Pause, einmal. Ein Herzschlag im Gestein, der ihren eigenen Puls verlangsamt, bis er im Takt liegt.",
}


# =====================================================================
# BLOCK 3 — B1 (aus OLD extrahiert, neues Schema, Thalassien-fokussiert)
# =====================================================================

def block_b1() -> None:
    """B1-Kapitel aus zeitleiste.OLD.json extrahieren, in neues Schema konvertieren.
    Filter: nur B1-Events mit relevantem Inhalt. K35/K36 sind Moragh-Events (Portal durch)."""
    old_path = ROOT / "buch" / "zeitleiste.OLD.json"
    if not old_path.exists():
        print("  WARN: zeitleiste.OLD.json fehlt — B1 wird nicht extrahiert")
        return

    old = json.loads(old_path.read_text(encoding="utf-8"))

    # Monats-Datum → TZ-Float-Mapping (B1 spielt Blütenmond bis Erntemond 551)
    # Die OLD-Events haben tz_tag (Jahrestag als int) und tz_datum-Strings.
    for m in old.get("monate", []):
        if "Buch 1" not in m.get("label", ""):
            continue
        for welt in ("thalassien", "moragh"):
            for ev in (m.get("events") or {}).get(welt) or []:
                if not isinstance(ev, dict): continue
                buch = ev.get("buch") or ""
                kap = ev.get("kapitel") or ""
                if buch != "B1": continue  # B2-Events aus der OLD raus (die kommen aus dem Agent-Block)

                tz_tag = ev.get("tz_tag") or 100  # Fallback: Tag 100 im Jahr
                tz_year = ev.get("tz") or 551
                tz_sort = float(tz_year) + (tz_tag / 365.0)

                # Skip I1/I2/I3 — die haben wir in block_tz_154 schon
                if kap in ("I1", "I2", "I3"):
                    continue
                # Skip den alten "Elke in ihrem Garten" Hintergrund-Event (zu B0 verschoben)
                t_check = ev.get("titel") or ""
                if "Elke in Dravek" in t_check or "Elke in ihrem Garten" in t_check:
                    continue
                # Skip den alten "Portal öffnet sich" Event — wird als sync-Event neu eingefuegt
                if "Portal öffnet sich" in t_check and "Fünf gehen" in t_check:
                    continue

                # tz_sort nach Plot-Reihenfolge: K01 -> 551.02, K33 -> 551.66, Portal 551.80 etc.
                # So haben wir strikte Plot-Chronologie statt unzuverlaessiger tz_tag aus OLD.
                kap_nr_match = kap.isdigit()
                if kap_nr_match:
                    k = int(kap)
                    if k <= 33:
                        tz_sort = float(tz_year) + 0.02 * k   # K01=551.02 ... K33=551.66
                    elif k == 34:
                        tz_sort = float(tz_year) + 0.78
                    elif k == 35:
                        tz_sort = float(tz_year) + 0.83
                    elif k == 36:
                        tz_sort = float(tz_year) + 0.88
                    else:
                        tz_sort = float(tz_year) + 0.02 * k
                elif kap == "ZEITSPRUNG":
                    tz_sort = float(tz_year) + 0.67  # direkt nach K33
                elif kap == "Epilog":
                    tz_sort = float(tz_year) + 0.93  # nach K36
                # Leichte Staffelung innerhalb eines Kapitels, falls mehrere Events
                tz_sort += 0.0001 * (len([x for x in EVENTS if x.get("buch")=="B1" and x.get("kapitel")==kap]))

                titel = ev.get("titel") or ""
                detail_orig = ev.get("detail") or ""
                detail = B1_DETAIL_OVERRIDES.get(titel, detail_orig)

                new_ev = {
                    "tz": tz_year,
                    "tz_sort": tz_sort,
                    "tz_datum": ev.get("datum_text") or "",
                    "welt": welt,
                    "pov": ev.get("figur") or (ev.get("pov", "").split("·")[-1].strip() if ev.get("pov") else ""),
                    "buch": "B1",
                    "kapitel": kap,
                    "leseart": "interludium" if kap.startswith("I") else "normal",
                    "titel": titel,
                    "detail": detail,
                    "typen": ev.get("typen") or [],
                    "tags": ev.get("tags") or [],
                    "kapitel_status": ev.get("kapitel_status") or "",
                }
                # MZ nur fuer Moragh-B1-Events setzen (K35/K36)
                if welt == "moragh" and kap in ("35", "36"):
                    new_ev["mz"] = 0.02 if kap == "35" else 0.04
                # kein mz fuer Thalassien-B1-Events (die MZ 3634/3635 aus OLD ist Altzaehlung, raus)
                EVENTS.append(new_ev)

    # Portal-Uebertritt B1 → B2 als Synchronisations-Event einfuegen
    add({
        "tz": 551, "tz_sort": 551.815,
        "mz": 0.01,
        "tz_datum": "Portal-Oeffnung · Ende B1 · MZ 0",
        "welt": "synchronisation", "pov": "Alphina / Vesper / Maren / Runa / Sorel",
        "buch": "B1", "kapitel": "34", "leseart": "normal",
        "titel": "Portal öffnet sich — Fünf gehen nach Moragh",
        "detail": "Am Steinkreis im Botanischen Garten: vier Resonanzen wirken zusammen, das Portal bleibt 4:33 offen. Alphina, Sorel, Vesper, Maren treten durch, Runa schlüpft als fünfte durch. In Moragh erwartet Varen sie.",
        "sync": {
            "thalassien": "Vael 551 TZ — der Steinkreis reisst die Luft auf. Zurueck bleiben Henrik im Garten, Halvard, Jara. Das Manuskript im Archiv hat seinen Zweck erfuellt.",
            "moragh": "MZ 0. Varen wartet am Moragh-Steinplatz in Dravek. Kappt seine Schemen in Vael. Die fuenf Resonanzen sind jetzt hier.",
        },
        "typen": ["portal", "schluessel"],
        "tags": ["Portal-Ritual", "4:33", "Fuenf durch"],
        "kapitel_status": "final",
    })


# =====================================================================
# BLOCK 4 — B2 (aus Agent-Output, ~29 Events)
# =====================================================================

B2_EVENTS: list[dict[str, Any]] = [
    {"mz": 0.05, "welt": "moragh", "pov": "Alphina", "buch": "B2", "kapitel": "01", "leseart": "normal",
     "titel": "Drei-Tage-Marsch zum Lichtschein",
     "detail": "Die Vier marschieren durch Moragh zum Lichtschein. Fremde Flora und Fauna, Harons Sprachbrocken passen nur halb, Runas Feuer hält Wunden warm.",
     "typen": ["begegnung", "hintergrund"],
     "tags": ["Lichtschein", "Moragh-Ankunft"]},
    {"mz": 0.1, "welt": "moragh", "pov": "Alphina", "buch": "B2", "kapitel": "01", "leseart": "normal",
     "titel": "Alphinas erster Schlaf-Hain",
     "detail": "Im Schlaf bricht der Boden um Alphina auf. Farne, Moos, Ranken in zehn Metern Radius. Sie hat nichts gewollt, kann es nicht wiederholen, nicht stoppen.",
     "typen": ["resonanz", "tschechow"],
     "tags": ["Schlaf-Hain", "Trauer als Wachstum"]},
    {"mz": 0.15, "welt": "moragh", "pov": "Vesper", "buch": "B2", "kapitel": "02", "leseart": "normal",
     "titel": "Vesper liest Moraghs Struktur",
     "detail": "Vesper kartografiert: Bäume in Spiralen, Flüsse nach Fibonacci, zwei Monde im Verhältnis 4:33. Die Sonne ist kein Stern, sondern dunkler Kern mit gleissendem Ring.",
     "typen": ["erkenntnis", "tschechow"],
     "tags": ["4:33", "Muster-Sinn"]},
    {"mz": 0.2, "welt": "moragh", "pov": "Runa", "buch": "B2", "kapitel": "04", "leseart": "normal",
     "titel": "Runas Feuer-Resonanz entdeckt",
     "detail": "Allein am Gartenrand formt Runa aus der Hand ein Messing-A. Kein Ofen, nur Hitze. Elke findet sie: schwache Feuer-Resonanz, hier ist sie mehr.",
     "typen": ["resonanz", "erkenntnis", "tschechow"],
     "tags": ["Feuer-Resonanz", "Messing-Type"]},
    {"mz": 0.3, "welt": "moragh", "pov": "Alphina", "buch": "B2", "kapitel": "07", "leseart": "normal",
     "titel": "Elke findet die Vier",
     "detail": "Die Gruppe trifft Elke van der Holt in ihrem Steingarten. Elke fragt, Alphinas Hain im Blick: »Das kostet dich nichts, oder?«",
     "typen": ["begegnung", "tschechow"],
     "tags": ["Elke", "Dravek-Garten"]},
    {"mz": 0.4, "welt": "moragh", "pov": "Maren", "buch": "B2", "kapitel": "08", "leseart": "normal",
     "titel": "Das Portal ist zu — Maren spürt die Richtung",
     "detail": "Maren spürt durchs Wasser Richtung und Abstand zum Portal. Geschlossen. Die Moragh-Seite hat eigene Mechanik. Wenn sie die Anleitung findet, kommt sie heim.",
     "typen": ["portal", "erkenntnis", "tschechow"],
     "tags": ["Portal-geschlossen", "Wasserresonanz"]},
    {"mz": 0.5, "welt": "moragh", "pov": "Alphina", "buch": "B2", "kapitel": "10", "leseart": "normal",
     "titel": "Ankunft in der Bund-Stadt",
     "detail": "Elke führt die Fünf in die Bund-Stadt. Türme aus gewachsenem Stein, Strassen die sich verschieben. Die Älteste greift Alphinas Hand zu schnell — Hoffnung, nicht Gier.",
     "typen": ["begegnung", "tschechow"],
     "tags": ["Bund-Stadt", "Hand greift"]},
    {"mz": 0.7, "welt": "moragh", "pov": "Vesper", "buch": "B2", "kapitel": "12", "leseart": "normal",
     "titel": "Talven, Drael und Nyr treten auf",
     "detail": "Talven hilft Vesper in der Bund-Bibliothek, kennt jede Karte. Drael führt die Stadt, wirkt zu informiert. Nyr erscheint später als Thar-Emissärin: »Du bist der, der Muster sieht.«",
     "typen": ["begegnung", "tschechow"],
     "tags": ["Talven", "Nyr", "Drael"]},
    {"mz": 1.25, "welt": "moragh", "pov": "Alphina", "buch": "B2", "kapitel": "15", "leseart": "normal",
     "titel": "Bund trainiert Alphina, die Farbe kippt",
     "detail": "Der Bund drängt Alphina zu Vorführungen. Tagsüber beginnt sie zu steuern. Bei Draels Druck kippt die Farbe erstmals: grün zu schwarz, rot geädert, Ranken dicht wie Drahtseile.",
     "typen": ["resonanz", "erkenntnis"],
     "tags": ["Farb-Kippe", "grün → schwarz/rot"]},
    {"mz": 2.05, "welt": "moragh", "pov": "Varen", "buch": "B2", "kapitel": "I4", "leseart": "interludium",
     "titel": "Varen beobachtet aus der Distanz",
     "detail": "Varen in seinem Quartier. Schemen berichten. Drei tote Quellen rot markiert. Er sieht, was der Bund mit Alphina macht, und wartet auf den Moment, in dem sie zu weit geht.",
     "typen": ["hintergrund", "tschechow"],
     "tags": ["Varen-POV", "Drei rote Markierungen"]},
    {"mz": 2.2, "welt": "moragh", "pov": "Alphina", "buch": "B2", "kapitel": "19", "leseart": "normal",
     "titel": "Dorf-Desaster durch Schlaf-Hain",
     "detail": "Nach einer Vorführung im Bund-Dorf schläft Alphina. Am Morgen ist das halbe Dorf überwuchert. Die Bewohner evakuieren — nicht vor den Velmar. Vor ihr.",
     "typen": ["resonanz", "erkenntnis"],
     "tags": ["Dorf überwuchert"]},
    {"mz": 2.3, "welt": "moragh", "pov": "Vesper", "buch": "B2", "kapitel": "18", "leseart": "normal",
     "titel": "Vesper geht mit Nyr zu den Thar",
     "detail": "Nyr kommt in ihrer Magitech-Bestie Kessler. Vesper entscheidet sich bewusst: die Thar benennen ihre Fehler. Keine Entführung — er geht mit, um zu verstehen.",
     "typen": ["begegnung", "erkenntnis"],
     "tags": ["Kessler", "Thar-Kem"]},
    {"mz": 2.4, "welt": "moragh", "pov": "Alphina", "buch": "B2", "kapitel": "20", "leseart": "normal",
     "titel": "Alphina und Runa küssen sich — die Welt bleibt still",
     "detail": "Nach dem Dorf-Desaster. Runa setzt sich dazu, Schulter an Schulter. Ein Kuss, ungeschickt. Keine Farne wachsen. Bei Sorel hat die Welt geblüht. Bei Runa bleibt sie still.",
     "typen": ["erotik", "erkenntnis", "tschechow"],
     "tags": ["Runa-Kuss", "Welt bleibt still"]},
    {"mz": 2.5, "welt": "moragh", "pov": "Runa", "buch": "B2", "kapitel": "14", "leseart": "normal",
     "titel": "Runas zweisprachige Druckerpresse in Halvaren",
     "detail": "Runa baut eine Presse auf — Thalassien-Lettern aus Moragh-Metall, aus der Hand geformt. Druckt Berichte, dokumentiert, sammelt. Zunächst nur für sich.",
     "typen": ["hintergrund", "tschechow"],
     "tags": ["Druckerpresse", "Halvaren"]},
    {"mz": 2.6, "welt": "moragh", "pov": "Alphina", "buch": "B2", "kapitel": "19", "leseart": "normal",
     "titel": "Talvens Hunger am Hain",
     "detail": "Am Rand von Alphinas Schlaf-Hain berührt Talven eine Ranke, konzentriert sich. Nach dreissig Sekunden Kopfschmerzen. Sein Gesicht zeigt HUNGER. Dann kocht er Frühstück, lächelt.",
     "typen": ["tschechow", "hintergrund"],
     "tags": ["Talven-Hunger", "Verräter-Setup"]},
    {"mz": 2.8, "welt": "moragh", "pov": "Alphina", "buch": "B2", "kapitel": "21", "leseart": "normal",
     "titel": "Alphina als Bund-Waffe, blühende Dornen",
     "detail": "Wochen an der Front. Wurzeln durch Stellungen, blühende schwarze Dornen als Verteidigung. Drael behandelt sie wie eine Kanone. Jeder Feind trägt Varens Gesicht.",
     "typen": ["krieg", "resonanz"],
     "tags": ["Waffe", "blühende Dornen"]},
    {"mz": 3.1, "welt": "moragh", "pov": "Alphina", "buch": "B2", "kapitel": "25", "leseart": "normal",
     "titel": "Halvara-Kel: Alphina überlädt die Quelle",
     "detail": "Bei der Thar-Siedlung Halvara-Kel drückt Alphina Wurzeln in die kleinere Quelle. Sie stirbt. Zweihundert Meter Radius verdorren in Sekunden. Schmied bricht zusammen, Kinder schreien. Sie hat es gewollt.",
     "typen": ["krieg", "tod", "erkenntnis"],
     "tags": ["Halvara-Kel", "200m-Todeszone"]},
    {"mz": 3.15, "welt": "moragh", "pov": "Talven", "buch": "B2", "kapitel": "I9", "leseart": "interludium",
     "titel": "Talvens heimliche Resonanz-Ernte",
     "detail": "In Halvaren versucht Talven heimlich Resonanz-Ernte an einem fremden Quellchen. Sein Reservoir hält einen Atemzug. Nasenbluten, Haarausfall in Büscheln, rechtes Auge milchig.",
     "typen": ["resonanz", "tschechow"],
     "tags": ["Talven-Ernte", "milchiges Auge"]},
    {"mz": 3.2, "welt": "moragh", "pov": "Alphina", "buch": "B2", "kapitel": "26", "leseart": "normal",
     "titel": "Varen fängt Alphina mit Schemen ab",
     "detail": "Als Alphina auf die grosse Quelle zielt, strömen Schemen übers Feld. Bindungsketten. Runa kämpft sich aus hundert Metern durch, wird zurückgeschlagen. Alphina wird weggetragen.",
     "typen": ["krieg", "begegnung"],
     "tags": ["Schemen-Ketten", "Runa sieht es"]},
    {"mz": 3.25, "welt": "moragh", "pov": "Varen", "buch": "B2", "kapitel": "I10", "leseart": "interludium",
     "titel": "Vier rote Markierungen",
     "detail": "Varen vor der Kartenwand. Drei alte rote Quellen — seine. Er nimmt den vierten Stift, markiert Halvara-Kel. Klein. Frisch. Ihre. Legt den Stift hin, geht zu ihr.",
     "typen": ["erkenntnis", "tschechow"],
     "tags": ["Vier rote Markierungen", "Spiegelung"]},
    {"mz": 3.3, "welt": "moragh", "pov": "Alphina", "buch": "B2", "kapitel": "28", "leseart": "normal",
     "titel": "Alphina liest die Bund-Chiffre",
     "detail": "In Varens Labor. Sie liest die abgefangene Bund-Kommunikation. Quellen-Zerstörung als koordinierte Strategie, Dutzende tote Zonen. Sie war nicht die Erste — nur die Stärkste.",
     "typen": ["erkenntnis", "wissen"],
     "tags": ["Bund-Chiffre", "systematische Zerstörung"]},
    {"mz": 3.4, "welt": "moragh", "pov": "Varen", "buch": "B2", "kapitel": "31", "leseart": "normal",
     "titel": "Varens Geständnis",
     "detail": "Mar-Keth, Dulrath-Ost, Reshkol. Sein Leylinien-Experiment, drei tote Quellen, 200.000 Heimatlose, der Krieg brach daraus hervor. »Niemand weiß es. Nur du.« Thalassische Resonanz ist azyklisch.",
     "typen": ["erkenntnis", "hintergrund"],
     "tags": ["Geständnis", "azyklische Resonanz"]},
    {"mz": 3.5, "welt": "moragh", "pov": "Alphina", "buch": "B2", "kapitel": "36", "leseart": "normal",
     "titel": "Sex mit Varen — Resonanz-Anker gesetzt",
     "detail": "Zwei Täter in einem Raum. Blühende schwarze Dornen aus Decke und Steinritzen. Varen setzt heimlich einen Resonanz-Anker in ihre Frequenz. Sie hält die Wärme für Nachglut.",
     "typen": ["erotik", "tschechow", "resonanz"],
     "tags": ["Anker", "Manipulation"]},
    {"mz": 3.55, "welt": "moragh", "pov": "Varen", "buch": "B2", "kapitel": "34", "leseart": "normal",
     "titel": "Vier-Thalassier-Liste",
     "detail": "Varen notiert eine Liste: Alphina, Vesper, Maren, Runa. Neben jedem Namen ein Resonanz-Maximum. Legt sie zwischen zwei Bücher. Kein Kommentar. Setup für B3.",
     "typen": ["tschechow", "wissen"],
     "tags": ["Vier-Thalassier-Liste", "Ritual-Setup"]},
    {"mz": 3.6, "welt": "moragh", "pov": "Maren", "buch": "B2", "kapitel": "37", "leseart": "normal",
     "titel": "Maren findet Portal-Ritual-Anleitung",
     "detail": "In der Thar-Bibliothek findet Maren die Velmar-Karte: Portal-Netzwerk, Ritual-Methode, von Moragh-Seite öffenbar. Einmal. Einweg. Sie hat genug Resonanz für den Hinweg.",
     "typen": ["portal", "wissen", "tschechow"],
     "tags": ["Velmar-Karte", "Einweg"]},
    # Sulkara-Finale — vor Maren-Portal, da gleicher MZ-Moment (kurz davor)
    {"mz": 4.98, "welt": "moragh", "pov": "Runa", "buch": "B2", "kapitel": "42", "leseart": "normal",
     "titel": "Sulkara-Finale: Alphina gegen Bund",
     "detail": "Vier-POV-Schlacht um die Nebenquelle. Runa ruft Alphinas Namen, halber Herzschlag Zögern, dann Alphinas Dornen gegen Bund-Soldaten. Vesper sieht durch Kesslers Luke: »nicht heute.«",
     "typen": ["krieg", "erkenntnis"],
     "tags": ["Sulkara", "Vier-POV"]},
    {"mz": 4.99, "welt": "moragh", "pov": "Alphina", "buch": "B2", "kapitel": "42", "leseart": "normal",
     "titel": "Alphina schlägt Talven nieder",
     "detail": "Rückzug nach Torkal. Talven kehrt mit blutigen Händen aus Elkes Garten zurück — Varens sauber gelegter Falschbeweis. Alphina schlägt ihn nieder, glaubt, er habe Elke getötet.",
     "typen": ["krieg", "tschechow"],
     "tags": ["Talven niedergeschlagen", "Falschbeweis", "B3-Setup"]},
    {"mz": 5.0, "welt": "synchronisation", "pov": "Maren", "buch": "B2", "kapitel": "38", "leseart": "normal",
     "titel": "Maren tritt durchs Portal nach 1987 TZ",
     "detail": "Maren öffnet das Portal von Moragh-Seite. Vesper und Nyr halten die Thar-Wachen 4:33 zurück. Dahinter: Thalassien 1987 TZ. Sie tritt durch.",
     "typen": ["portal", "tschechow"],
     "sync": {
        "thalassien": "Vael 1987 TZ — Gaslampen durch Elektrizität ersetzt, erste Automobile, Telefonleitungen. Maren kommt an, beginnt sofort zu dokumentieren.",
        "moragh": "Portal schliesst 4:33 später. Vesper bleibt. Die Vier sind getrennt.",
     },
     "tags": ["Portal-Durchgang", "Zeitdilatation", "1987 TZ"]},
    {"mz": 5.01, "welt": "moragh", "pov": "Runa", "buch": "B2", "kapitel": "42", "leseart": "normal",
     "titel": "Runa reisst den Namen aus dem Farn-Brief",
     "detail": "Runa in der Bund-Krankenstation, gebrochene Rippe. Zieht den Brief mit gezeichnetem Farn heraus. Reisst nur den Namen Alphina raus. Behält den Farn und »ich hab nicht aufgehört«.",
     "typen": ["erkenntnis", "tschechow"],
     "tags": ["Farn-Brief", "Entkoppelung"]},
]


# Erweiterte Detail-Texte fuer B2-Events, strikt aus Akt-Docs + Synopse extrahiert.
# Quellen: 06-09-buch2-akt*.md, synopse-b2.md, B3-ZEITLEISTE.md (B2-Ende), 00-storyline.md
B2_DETAIL_OVERRIDES: dict[str, str] = {
    "Drei-Tage-Marsch zum Lichtschein":
        "Drei Tage nach Sorels Tod marschieren Alphina, Vesper, Maren und Runa zum Lichtschein, den sie am Ende von B1 gesehen haben. Fremde Flora am eigenen Leib, Harons Sprachbrocken passen nur halb, Runas Feuer hält Wunden.",
    "Alphinas erster Schlaf-Hain":
        "Alphina schläft am Feuer ein. Im Schlaf bricht der Boden um sie auf: Gras, Farne, Moos, Ranken in einem Kreis von zehn Metern. Am Morgen ein Hain. Sie hat nichts getan, nichts gewollt, kann es nicht wiederholen, nicht stoppen.",
    "Vesper liest Moraghs Struktur":
        "Vesper kartografiert. Bäume in Spiralen, Flüsse nach Fibonacci, zwei Monde im Verhältnis 4:33 — Varens Frequenz oder Moraghs eigene. Die Sonne: kein Feuerball, ein dunkler Kern mit gleissendem Ring.",
    "Runas Feuer-Resonanz entdeckt":
        "Runa hält ihren Schmelzlöffel — das Zinn wird weich in ihrer Hand, schmilzt ohne Ofen. Sie lässt ihn fallen. Später formt sie eine Messing-Type, ein perfektes A, aus der Hand. In Vael hätte sie dafür einen Schmelzofen gebraucht.",
    "Elke findet die Vier":
        "Die Gruppe findet Elke van der Holt in ihrem Steingarten — vierhundert Jahre in Moragh, Pflanzen aus beiden Welten, Basalt den sie geformt hat. Sie legt die Hand auf Alphinas Schlaf-Hain: »Das kostet dich nichts, oder?«",
    "Das Portal ist zu — Maren spürt die Richtung":
        "Maren sucht das Portal durch das Wasser. Sie fühlt den Punkt, wo die Welt dünn wird — aber geschlossen, Stein dahinter. Die Moragh-Seite hat eine eigene Mechanik. Wenn sie die Anleitung fände, könnte sie es von hier öffnen.",
    "Ankunft in der Bund-Stadt":
        "Elke führt die Vier zwei Tage Marsch zur nächsten Bund-Stadt: gewachsene Türme, Strassen die sich verschieben, Brücken über bergauf fliessende Flüsse. Bewohner mit Purpur-, Weinrot- und schwarzen Augen. Staunen, Flüstern, zeigende Finger.",
    "Talven, Drael und Nyr treten auf":
        "Talven, dreiundzwanzig, schmaler Bibliotheks-Lehrling, bringt Vesper Tee und Reservoirkarten — hilfsbereit, schnell. Drael, Bund-Kommandant. Nyr, Thar-Emissärin in ihrer Magitech-Bestie: »Du bist der, der Muster sieht.«",
    "Bund trainiert Alphina, die Farbe kippt":
        "Alphina lernt tagsüber Kontrolle unter Bund-Meistern. Solange sie diszipliniert ist, wächst es grün. Wenn die Wut durchbricht, kippt die Farbe nach schwarz/rot, die Ranken werden dicht wie Drahtseile. Die Meister nennen es »Verunreinigung«.",
    "Varen beobachtet aus der Distanz":
        "Varen schickt Schemen als Späher. Sie berichten: die Thalassier sind beim Bund angekommen. An seiner Wand drei tote Quellen rot markiert, auf einer zweiten Karte Bund-Truppenbewegungen, die auf weitere Quellen zielen. »Sie kommen.«",
    "Dorf-Desaster durch Schlaf-Hain":
        "Bund-Vorführung in einem Dorf drei Stunden von der Stadt. Alphina pflanzt tagsüber einen Baum in zehn Minuten. Nachts im Gasthaus schläft sie. Am Morgen ist das halbe Dorf überwuchert — Farne durch Fenster, Moos über Dächer. Die Bewohner evakuieren vor ihr.",
    "Vesper geht mit Nyr zu den Thar":
        "Nyr überzeugt Vesper: »Jedes System hat Fehler. Die Thar benennen ihre.« Er geht mit ihr zu den Thar — bewusste Wahl, nicht Entführung. Er will verstehen, nicht kämpfen, sich weder vom Bund noch von Alphinas Rache instrumentalisieren lassen.",
    "Alphina und Runa küssen sich — die Welt bleibt still":
        "Nacht auf dem Dach, zwei Monde. Runas Schulter an Alphinas, Wärme ohne Feuer-Resonanz. Sie küssen sich — ungeschickt, zu schnell. Keine Farne wachsen. Bei Sorel hat die Welt geblüht. Bei Runa ist sie still. Beides macht ihr Angst.",
    "Runas zweisprachige Druckerpresse in Halvaren":
        "Runa gründet eine kleine Druckerei in Halvaren — Moragh-Papier, thalassische Lettern, die sie in Moragh-Metall aus der Hand gegossen hat. Sie druckt zweisprachige Flugblätter, dokumentiert, was der Bund-Älteste nicht verbreiten will.",
    "Talvens Hunger am Hain":
        "Als alle den Schlaf-Wald anstarren, berührt Talven am Rand eine Ranke. Sein mittelmässiges Reservoir reicht für ein schwebendes Steinchen; nach dreissig Sekunden Kopfschmerzen. Sein Blick auf den Hain — Hunger, einen Moment lang, bevor er wieder lächelt.",
    "Alphina als Bund-Waffe, blühende Dornen":
        "Alphina an der Front: Wurzeln reissen durch Stellungen, Bäume wachsen als Barrikaden, Dornenhecken als Verteidigung. Drael behandelt sie wie eine Kanone — Ziel, feuern, nachladen. Jeder Feind trägt Varens Gesicht. Der Hass ist produktiv, der Hass hat Struktur.",
    "Halvara-Kel: Alphina überlädt die Quelle":
        "Drael zeigt ihr eine kleinere Nebenquelle — »Sparen hundert Leben.« Alphina drückt Wurzeln tiefer als je zuvor, spürt das pulsierende Herz, überlädt. Die Quelle stirbt. Radius zweihundert Meter: Bäume verdorren, ein Schmied bricht zusammen, Kinder schreien. Sie hat es gewollt.",
    "Talvens heimliche Resonanz-Ernte":
        "Talven versucht heimlich eine kleine Resonanz-Ernte an einem fremden Quellchen. Sein Reservoir hält einen Atemzug, dann Nasenbluten, Haarausfall in Büscheln, das rechte Auge milchig. Horror-Disproportion: Alphina tötet im Nebenbei, was Talven fast das Leben kostet.",
    "Varen fängt Alphina mit Schemen ab":
        "Als Alphina zur grossen Quelle zielt, strömen Schemen über das Schlachtfeld. Bindungsketten legen sich um ihre Handgelenke. Ihre Pflanzen versuchen zu wachsen — Varens Magie hält. Runa sieht es aus hundert Metern, kämpft, tötet Dutzende Schemen, wird zurückgeschlagen.",
    "Vier rote Markierungen":
        "Varens Quartier, kein Gefängnis — ein Labor. An der Wand Karten: vier tote Quellen, rot markiert. Drei alt, verblasst, mit Notizen in Moragh — seine. Eine frisch, klein, an der Position der Thar-Siedlung. Ihre. Dieselbe Tat, verschiedene Gründe.",
    "Alphina liest die Bund-Chiffre":
        "Varen hat abgefangene Bund-Kommunikation entschlüsselt. Alphina liest: Quellen-Zerstörung als koordinierte Kriegsstrategie, Dutzende tote Zonen, zehn weitere Ziele geplant — sechshundert Menschen, achthundert. Sie war nicht die Erste. Nur die Stärkste.",
    "Varens Geständnis":
        "Varen in altem Thalassisch, langsam, ohne Rechtfertigung: drei Reservoir-Quellen — Mar-Keth, Dulrath-Ost, Reshkol. Leylinien-Experiment, Kettenreaktion, zweihunderttausend heimatlos, Kriegsausbruch. »Niemand weiss es. Nur du.« Auf Alphinas Frage nach Sorel: »Weil dein Hass Treibstoff brauchte.«",
    "Sex mit Varen — Resonanz-Anker gesetzt":
        "Gewachsen aus geteilter Schuld. Dornen aus Boden, Steinritzen, Decke — schwarz, scharf, dicht. Keine Farne, keine Zärtlichkeit: Kontrolle durch Erkenntnis. Varen setzt heimlich einen Bindungs-Anker in ihrer Frequenz. Sie spürt Wärme an der Wirbelsäule, hält sie für Orgasmus-Nachwirkung.",
    "Vier-Thalassier-Liste":
        "Varen an seinem Arbeitstisch. Eine Liste, klein zwischen zwei Büchern versteckt: vier Namen — Alphina, Vesper, Maren, Runa. Neben jedem Namen eine Zahl. Resonanz-Maximum. Das, was sie für das Ritual geben müssten. Kein Kommentar. Kein Zögern.",
    "Maren findet Portal-Ritual-Anleitung":
        "In der Thar-Bibliothek findet Maren alte Moragh-Karten des Portal-Netzwerks und die Methode: wie man das Portal von Moragh-Seite öffnet, nicht durch Wasser, durch das Ritual. Gespiegelt zu Vael. Sie HAT Resonanz — für den Hinweg Moragh nach Thalassien reicht es. Einweg.",
    "Sulkara-Finale: Alphina gegen Bund":
        "Sulkara, dreizehntausend Bewohner. Der Bund greift mit Ersatz-Magiern die Nebenquelle an. Varen und Alphina kommen als dritte Partei zur Reparatur — Schemen-Vorhut, Umleitung des Überladungsstosses. Ein Baum schiesst zehn Meter hoch, fällt um. Die Quelle lebt.",
    "Alphina schlägt Talven nieder":
        "Beim Rückzug nach Torkal kehrt Talven mit blutigen Händen aus Elkes Garten zurück — Varens Falschbeweis, sauber gelegt. Alphina schlägt Talven nieder, glaubt, er habe Elke getötet. Setup Buch 3.",
    "Maren tritt durchs Portal nach 1987 TZ":
        "Maren öffnet das Portal am Steinplatz nahe der Thar-Kontrolle. Vesper und Nyr halten Wachen für 4:33 zurück. Die Luft reisst auf: Thalassien, aber 1987 TZ. Gaslampen durch Elektrizität ersetzt, Automobile statt Kutschen. Sie tritt durch. Das Portal schliesst sich.",
    "Runa reisst den Namen aus dem Farn-Brief":
        "Bund-Krankenstation, Schnittwunden, gebrochene Rippe. Runa zieht den Brief mit gezeichnetem Farn aus der Tasche — »Alphina. Ich hab nicht aufgehört.« Sie reisst nur den Namen »Alphina« heraus. Den Rest des Briefes, den Farn, die Worte, behält sie.",
}


def block_b2() -> None:
    """B2-Events einfuegen. MZ wird in tz_sort umgerechnet, tz = gerundete TZ-Aequivalenz.
    Detail-Text wird aus B2_DETAIL_OVERRIDES geholt (strikt aus Akt-Docs extrahiert)."""
    for e in B2_EVENTS:
        mz = e["mz"]
        tz_aequiv = mz_to_tz(mz)
        new_ev = dict(e)
        # Override Detail wenn vorhanden
        titel = new_ev.get("titel", "")
        if titel in B2_DETAIL_OVERRIDES:
            new_ev["detail"] = B2_DETAIL_OVERRIDES[titel]
        new_ev["tz"] = round(tz_aequiv)
        new_ev["tz_sort"] = tz_aequiv
        new_ev["tz_datum"] = f"MZ {mz:.2f} · TZ {round(tz_aequiv)}"
        new_ev.setdefault("kapitel_status", "idee")
        EVENTS.append(new_ev)


# =====================================================================
# BLOCK 5 — B3 (aus B3-ZEITLEISTE.md, strukturiert)
# =====================================================================

# Aus B3-ZEITLEISTE.md direkt abgeleitet. MZ in Moragh-Monaten seit B1-Start.
# Thalassien-Zeitpunkte in TZ-Zahlen (aus B3-ZEITLEISTE, dort "Thalassien-Zeit" Spalte).
B3_EVENTS: list[dict[str, Any]] = [
    # === Akt I ===
    {"mz": 5.5, "welt": "moragh", "pov": "Alphina", "buch": "B3", "kapitel": "41", "leseart": "normal",
     "titel": "Alphina + Varen in Torkal — erste Quellen-Reparatur (Halvara-Kel)",
     "detail": "Drei Wochen nach Sulkara. Sie reisen zur toten Quelle Halvara-Kel, legen die Hände auf den ausgelaugten Fels. Ein Puls, ein Zucken, Pochen — Alphina lacht erstmals seit Sorels Tod. Der Anker zwischen ihren Schulterblättern zieht Überschuss in Varens Speicher.",
     "typen": ["resonanz", "tschechow"],
     "tags": ["Torkal", "Halvara-Kel", "Anker-zieht"]},
    {"mz": 5.55, "welt": "moragh", "pov": "Vesper", "buch": "B3", "kapitel": "42", "leseart": "normal",
     "titel": "Vesper analysiert Expedition-Sensoren",
     "detail": "Vesper in Thar-Kem über Aufklärungsdaten. Bodentemperatur-Anomalien am Steinplatz, Sensoren, die er nicht kennt. Etwas kommt durch — Thar-Kommandantin legt seinen Bericht ungelesen auf den Stapel.",
     "typen": ["erkenntnis", "tschechow"],
     "tags": ["Expedition-Warnung", "Thar-Kommandantin"]},
    {"mz": 5.7, "welt": "moragh", "pov": "Runa", "buch": "B3", "kapitel": "43", "leseart": "normal",
     "titel": "Runa in Halvaren — Drael-Beobachtung",
     "detail": "Runa druckt weiter zweisprachige Flugblätter in Halvaren. Drael besucht abends zu höflichem Tee, der nie getrunken wird. Sie sammelt Material gegen ihn.",
     "typen": ["hintergrund"],
     "tags": ["Halvaren", "Drael-Gegner"]},
    {"mz": 5.75, "welt": "thalassien", "pov": "Maren", "buch": "B3", "kapitel": "I7", "leseart": "rueckblende",
     "titel": "I7 — Maren gründet die Schwellenforschungsgesellschaft",
     "detail": "Rückblick auf Vael 1990 TZ. Maren mit drei Mitgliedern im Dachgeschoss der Werft: »Dann warten wir Jahrzehnte.« Gründung der späteren staatlich finanzierten Institution.",
     "typen": ["schluessel", "hintergrund"],
     "tags": ["Schwellenforschungsgesellschaft", "Vael 1990"]},
    {"mz": 5.8, "welt": "moragh", "pov": "Talven", "buch": "B3", "kapitel": "44", "leseart": "normal",
     "titel": "Talven verteilt Resonanz, Held-Aufstieg",
     "detail": "Talven in Halvaren. Fieber sinkt unter seiner Hand, ein alter Rufer formt für eine Minute eine Lichtkugel. Seine Hände werden kalt. Nachts findet er ein schwarz gebundenes Velmar-Handbuch unter seiner Tür.",
     "typen": ["resonanz", "tschechow"],
     "tags": ["Held-Aufstieg", "Bindungs-Handbuch"]},
    {"mz": 5.85, "welt": "moragh", "pov": "Alphina", "buch": "B3", "kapitel": "45", "leseart": "normal",
     "titel": "Zweite Quellen-Reparatur (Mar-Keth)",
     "detail": "Mar-Keth pulsiert wieder, schwach aber sichtbar. Alphina fühlt Heilung, Varen notiert still den Frequenzwert in seinem Notizbuch. Sie glaubt ihm.",
     "typen": ["resonanz", "tschechow"],
     "tags": ["Mar-Keth", "Reparatur-Fassade"]},
    {"mz": 5.9, "welt": "thalassien", "pov": "Tyra", "buch": "B3", "kapitel": "46", "leseart": "normal",
     "titel": "Erste Expedition kommt durchs Portal — 2020 TZ",
     "detail": "Tyra Halvard und vierzehn Forscher treten durch den Steinkreis. Wissenschaftliche Expedition, keine militärische. Die Moragh-Welt ist anders als die Schriften beschreiben.",
     "typen": ["portal", "begegnung"],
     "sync": {
        "thalassien": "Vael 2020 TZ. Institut schickt Expedition 1 los, 15 Forscher.",
        "moragh": "Am Steinplatz treffen sie auf erste Thar-Patrouille. Keine Verluste, aber Spannung.",
     },
     "tags": ["Expedition 1", "Tyra Halvard", "2020 TZ"]},
    {"mz": 5.95, "welt": "moragh", "pov": "Vesper", "buch": "B3", "kapitel": "47", "leseart": "normal",
     "titel": "Thar erobert Ankunftsstadt",
     "detail": "Die Thar-Kommandantin reagiert endlich, erobert die Stadt am Steinplatz, nimmt Expedition 1 ein — misstraut, verhört, trennt sie von der Welt. Vesper fordert Kooperation, wird abgewiesen.",
     "typen": ["krieg", "begegnung"],
     "tags": ["Expedition-gefangen"]},
    {"mz": 6.2, "welt": "moragh", "pov": "Alphina", "buch": "B3", "kapitel": "48", "leseart": "normal",
     "titel": "Dritte Quellen-Reparatur (Dulrath-Ost) — Reparaturen verblassen",
     "detail": "Dulrath-Ost pulsiert, aber schon Halvara-Kel erlischt wieder. Varen nickt: einzelne Injektion halte nicht, man müsse wiederkommen. Alphina schluckt die Erklärung. Ihr Schlaf-Hain in Torkal welkt an den Rändern.",
     "typen": ["resonanz", "erkenntnis"],
     "tags": ["Reparatur-Fassade bröckelt", "Anker leckt"]},
    # === Akt II ===
    {"mz": 6.5, "welt": "moragh", "pov": "Varen", "buch": "B3", "kapitel": "51", "leseart": "normal",
     "titel": "Varen entdeckt das Ritual — vier Thalassier-Opfer",
     "detail": "Varen in der Moragh-Sprachbuch-Bibliothek. Er findet die alte Velmar-Ritualform: vier Thalassier-Resonanzen, absorbiert durch einen Binder, dauerhafte preisfreie Magie. Legt die Liste wieder zwischen die Bücher.",
     "typen": ["wissen", "tschechow"],
     "tags": ["Ritual entdeckt"]},
    {"mz": 6.55, "welt": "thalassien", "pov": "Tyra", "buch": "B3", "kapitel": "I13", "leseart": "rueckblende",
     "titel": "I13 — Tyra Halvard + Team vor dem Aufbruch",
     "detail": "Rückblende Vael 2019 TZ. Tyra mit ihren vierzehn Kollegen vor dem Durchgang. Abschied, Koffer, Vorträge, Familien, Witze. Eine Nacht vor dem Portal. Institut füttert Hoffnung.",
     "typen": ["hintergrund"],
     "tags": ["Expedition 1 Start", "Vael 2019"]},
    {"mz": 6.6, "welt": "moragh", "pov": "Tyra", "buch": "B3", "kapitel": "52", "leseart": "normal",
     "titel": "Erste Expedition scheitert blutig",
     "detail": "Expedition 1 kooperiert nicht unter Thar-Gefangenschaft. Fluchtversuch, elf tot, zwei verschwunden. Tyra und ein Geologe fliehen nach Westen. Marsk stirbt an Pilzvergiftung. In Tyras Ohren beginnt ein Summen.",
     "typen": ["tod", "krieg"],
     "tags": ["Expedition 1 scheitert", "Tyra allein"]},
    {"mz": 6.7, "welt": "moragh", "pov": "Varen", "buch": "B3", "kapitel": "53", "leseart": "normal",
     "titel": "Varen manipuliert Orath-Älteste zur Verwüster-Beschwörung",
     "detail": "Anonymer Brief an Kelmaris Verask, als Bund-Informant signiert: Verwüster-Vergeltung. Orath beschwört. Varen öffnet das Portal selbst — niemand sonst kann es.",
     "typen": ["tschechow", "wissen"],
     "tags": ["Kelmaris Verask", "Portal-Öffnung durch Varen"]},
    {"mz": 6.75, "welt": "synchronisation", "pov": "Maren", "buch": "B3", "kapitel": "I8", "leseart": "normal",
     "titel": "Verwüster-Angriff auf Vael — Maren stirbt",
     "detail": "Der Steinkreis in Vael reisst auf, drei rauchige Gestalten brechen durch die Glasfront des Instituts. Maren, achtzig, mit versagendem Herz, flüstert gegen die Wand: »Ich habe sie hergeschickt.« Die fünfzehnjährige Syra Halvard schreibt abends in ihr Notizbuch — beim nächsten Mal werde es eine Armee sein.",
     "typen": ["tod", "portal", "schluessel"],
     "sync": {
        "thalassien": "Vael 2037 TZ. Institut-Aussengebäude zerstört. Maren stirbt im Angesicht der Verwüster.",
        "moragh": "Varen bleibt für Öffnungsdauer am Steinplatz. Niemand sieht ihn. Die Älteste hält es für Bund-Angriff.",
     },
     "tags": ["Maren tot", "Syra Halvard 15", "2037 TZ"]},
    {"mz": 7.0, "welt": "moragh", "pov": "Alphina", "buch": "B3", "kapitel": "54", "leseart": "normal",
     "titel": "Varen präsentiert Alphina das »heroische« Ritual",
     "detail": "Varen stellt das Ritual als Zukunftsopfer vor — sich selbst als ersten Brennenden. Alphina hört Hoffnung und zweifelt nur leise. Der Anker zieht sie zu seiner Lesart.",
     "typen": ["wissen", "erkenntnis"],
     "tags": ["Ritual-Fassade"]},
    {"mz": 7.05, "welt": "moragh", "pov": "Alphina", "buch": "B3", "kapitel": "55", "leseart": "normal",
     "titel": "Alphinas Drei-Sätze-Absage bei Runa",
     "detail": "Alphina reist nach Halvaren zu Runa, bietet ihr an, selbst zu sehen. Runa hart und klar: »Du riechst nach ihm. Du sprichst wie er. Ich glaube dir nicht.« Vierter Satz, leiser: »Ich habe keinen Platz an seinem Tisch.«",
     "typen": ["begegnung", "erkenntnis"],
     "tags": ["Drei-Sätze-Absage", "vierter Satz"]},
    {"mz": 7.2, "welt": "moragh", "pov": "Vesper", "buch": "B3", "kapitel": "56", "leseart": "normal",
     "titel": "Vesper bekommt Temporal-KI-Helm",
     "detail": "Thar eigene Forschung. Vesper sieht durch den Helm den Resonanz-Anker zwischen Alphinas Schulterblättern — als Leuchtlinie. Er beginnt, das Ritual-Kalkül zu entschlüsseln.",
     "typen": ["tschechow", "wissen"],
     "tags": ["Temporal-KI-Helm"]},
    {"mz": 7.3, "welt": "moragh", "pov": "Talven", "buch": "B3", "kapitel": "57", "leseart": "normal",
     "titel": "Talvens Radikalisierung — Blutmagie und Schemen-Binden",
     "detail": "Talven öffnet das Velmar-Handbuch, zieht das erste Blut. Schemen weichen ihm zögernd aus. Baut Kristall-Batterien. Niemand fragt, wohin er sein Blut verliert.",
     "typen": ["resonanz", "tschechow"],
     "tags": ["Blutmagie", "Schemen-Binden", "Grenzüberschreitung"]},
    {"mz": 7.35, "welt": "moragh", "pov": "Varen", "buch": "B3", "kapitel": "58", "leseart": "normal",
     "titel": "Elke wird ermordet",
     "detail": "Ein aufgeladener Schemen betritt Elkes Haus in Dravek. Sie wehrt sich. Der Schemen tötet in der Küche, trägt sie in den Garten, platziert sie auf der Bank. Nimmt den Basalt-Splitter-Anhänger, findet das Maren-Dokument nicht.",
     "typen": ["tod", "schluessel"],
     "tags": ["Elke tot", "Küche", "Basalt-Splitter"]},
    {"mz": 7.4, "welt": "moragh", "pov": "Alphina", "buch": "B3", "kapitel": "59", "leseart": "normal",
     "titel": "Alphina verdächtigt Talven",
     "detail": "Alphina findet Elke im Garten. Zwei Tage später öffnet sie Talvens Schrank, findet das schwarz gebundene Handbuch, einen Zettel in seiner Schrift: »Morgen Abend. Dravek. Elke.« Varens gefälschte Falle steht.",
     "typen": ["erkenntnis", "tschechow"],
     "tags": ["Talven-Verdacht", "Falschbeweise"]},
    {"mz": 7.45, "welt": "moragh", "pov": "Vesper", "buch": "B3", "kapitel": "60", "leseart": "normal",
     "titel": "Vesper findet erstes Velmar-Dokument",
     "detail": "In der Thar-Bibliothek unter Expeditions-Notizen findet Vesper ein altes Velmar-Dokument — Ritual-Fragmente, vier Resonanzen, Name-Rechengröße. Er beginnt zu verstehen.",
     "typen": ["wissen", "tschechow"],
     "tags": ["Velmar-Dokument"]},
    # === Akt III ===
    {"mz": 7.5, "welt": "moragh", "pov": "Vesper", "buch": "B3", "kapitel": "61", "leseart": "normal",
     "titel": "Vesper entschlüsselt das Ritual-Kalkül",
     "detail": "Vesper zeigt Alphinas Resonanz als Rechengröße. Symptome: Wärme an der Wirbelsäule nach Reparatur-Sitzungen, Müdigkeit, Ziehen bei Entfernung. Alphina kennt alle drei.",
     "typen": ["erkenntnis", "wissen"],
     "tags": ["Ritual-Kalkül"]},
    {"mz": 7.55, "welt": "thalassien", "pov": "Syra", "buch": "B3", "kapitel": "I9", "leseart": "rueckblende",
     "titel": "I9 — Junge Syra Halvard + Kelvar Velkan, Institut-Wandel",
     "detail": "Parallel Vael 2080 TZ. Syra Halvard (15) trifft den jungen Kelvar Velkan (25) im Institut. Nach Marens Tod Eroberungs-Doktrin. Zwei Generationen nach Maren, Ton hat gekippt.",
     "typen": ["hintergrund"],
     "tags": ["Syra Halvard", "Kelvar Velkan", "2080 TZ"]},
    {"mz": 7.7, "welt": "moragh", "pov": "Alphina", "buch": "B3", "kapitel": "63", "leseart": "normal",
     "titel": "Alphina findet das Ritual-Dokument in Varens Quartier",
     "detail": "Sie wartet, bis Varen schläft, sprengt mit Wurzeln ein Schloss im Schreibtisch. Findet Ritual-Buch, Liste, am Rand in seiner Handschrift: »Die Trauer macht sie stärker. Sorels Nutzen liegt im Sterben.«",
     "typen": ["erkenntnis", "schluessel"],
     "tags": ["Sorels Nutzen im Sterben"]},
    {"mz": 7.75, "welt": "moragh", "pov": "Alphina", "buch": "B3", "kapitel": "64", "leseart": "normal",
     "titel": "Alphina liest den Maren-Brief — zweite Erkenntnis",
     "detail": "Über Elkes Hinweis »Unter dem Stein, wo nichts wächst« findet Alphina das Velmar-Dokument, Marens Notizen. Zweite Erkenntnis: Maren wusste es schon, bevor sie ging.",
     "typen": ["erkenntnis", "tschechow"],
     "tags": ["Maren-Brief", "Unter dem Stein"]},
    {"mz": 7.8, "welt": "moragh", "pov": "Alphina", "buch": "B3", "kapitel": "65", "leseart": "normal",
     "titel": "Alphina verlässt Varen — ohne Drama",
     "detail": "Sie legt das Blatt zurück, legt sich neben Varen, atmet, rechnet. Morgens verlässt sie Torkal ohne Drama. Der Anker zieht, aber sie bleibt auch.",
     "typen": ["erkenntnis"],
     "tags": ["Anker bleibt, sie bleibt auch"]},
    {"mz": 7.9, "welt": "moragh", "pov": "Runa", "buch": "B3", "kapitel": "66", "leseart": "normal",
     "titel": "Runa läuft aus dem Bund über",
     "detail": "Drael belügt Runa über die Expedition-Gefahr. Sie enttarnt ihn mit einer Drael-Dokumentmappe, bekommt eine Stunde Fliehen, läuft in die freie Stadt Kolmen.",
     "typen": ["begegnung", "erkenntnis"],
     "tags": ["Drael enttarnt", "Kolmen"]},
    {"mz": 7.95, "welt": "moragh", "pov": "Tyra", "buch": "B3", "kapitel": "67", "leseart": "normal",
     "titel": "Tyra Halvard erreicht Alphinas Gruppe",
     "detail": "In Kolmen steht Tyra an Alphinas Tür. Schall-Resonanz: Stille-Zonen, Schemen-Fernsprecher. Zwei kleine Schemen werden Fernsprecher — Alphina hört Tyras Stimme aus dem Garten und lacht das erste Mal echt seit Monaten.",
     "typen": ["begegnung", "tschechow"],
     "tags": ["Tyra-Fernsprecher", "Schall-Resonanz"]},
    {"mz": 8.0, "welt": "thalassien", "pov": "Syra", "buch": "B3", "kapitel": "I14", "leseart": "rueckblende",
     "titel": "I14 — Halvard + Velkan planen Expedition 2",
     "detail": "Parallel Vael 2110 TZ. Resonanz-Modulator im Test. Biotech-Bodymod-Soldaten. Halvard (jetzt 45) und Velkan (55) sprechen von »Befreiung der Weltenkreuzung«. Sprache klingt nach Krieg.",
     "typen": ["hintergrund", "krieg"],
     "tags": ["Expedition 2 Plan", "Resonanz-Modulator"]},
    {"mz": 8.05, "welt": "moragh", "pov": "Alphina", "buch": "B3", "kapitel": "68", "leseart": "normal",
     "titel": "Wiederbegegnung Alphina–Runa",
     "detail": "In Kolmen. Alphina weint. Runa bleibt hart und klar, dann berührt sie ihre Hand: »Aber ich stehe. Wenn es zählt.«",
     "typen": ["begegnung", "erkenntnis"],
     "tags": ["Versöhnung"]},
    {"mz": 8.1, "welt": "moragh", "pov": "Nyr", "buch": "B3", "kapitel": "69", "leseart": "normal",
     "titel": "Nyr verlässt die Thar",
     "detail": "Unbehagen über Zivilisten-als-Schild-Befehle. Kessler ist ihr, nicht der Kommandantin. Sie fährt nachts aus Thar-Kem, verabschiedet sich von Vesper friedlich, bietet Beistand an.",
     "typen": ["begegnung", "erkenntnis"],
     "tags": ["Nyr-Austritt", "Reiter-Bindung absolut"]},
    {"mz": 8.3, "welt": "moragh", "pov": "Alphina", "buch": "B3", "kapitel": "70", "leseart": "normal",
     "titel": "Alphina tötet Talven — Fehlurteil",
     "detail": "Alphina konfrontiert Talven. Die drei Fälschungen wirken. Dornen durchs Brustbein. Sein Satz: »Ich hätte es irgendwann wirklich gekonnt.« Er stirbt. Die Wahrheit bleibt bei Varen.",
     "typen": ["tod", "krieg"],
     "tags": ["Talven tot", "Fehlurteil"]},
    {"mz": 8.55, "welt": "synchronisation", "pov": "Kessler/Kelvar", "buch": "B3", "kapitel": "71", "leseart": "normal",
     "titel": "Zweite Expedition kommt durch — 2500 Soldaten, 2120 TZ",
     "detail": "Modulator 72 Stunden aktiv. Expedition 2: 2500 Soldaten, Biotech-Bodymod, stockwerkshohe Killermaschinen. General Kelvar Velkan führt. In zwei Moragh-Wochen fällt Bund-Grenzgebiet, eine freie Stadt ist erobert.",
     "typen": ["portal", "krieg", "schluessel"],
     "sync": {
        "thalassien": "Vael 2120 TZ. Institut schickt grossen Zug, Hymnen und Propaganda. Kein Weg zurück im Plan.",
        "moragh": "Steinplatz-Gebiet wird Militärzone. Moragh-Flüchtlinge strömen nach Westen.",
     },
     "tags": ["Expedition 2", "2500 Soldaten", "2120 TZ", "Kelvar Velkan"]},
    {"mz": 8.8, "welt": "moragh", "pov": "Drael", "buch": "B3", "kapitel": "72", "leseart": "normal",
     "titel": "Notbündnis Orath + Thar",
     "detail": "Drael und die Thar-Kommandantin treffen sich persönlich. Jahrelange Feindschaft, jetzt gemeinsamer Feind. Vesper wird Stratege des Bündnisses — erstes Bündnis in vier Jahren Krieg.",
     "typen": ["begegnung", "krieg"],
     "tags": ["Notbündnis"]},
    # === Akt IV ===
    {"mz": 9.2, "welt": "thalassien", "pov": "Kelvar", "buch": "B3", "kapitel": "I16", "leseart": "rueckblende",
     "titel": "I16 — Expedition 2 Aufbruch aus Vael",
     "detail": "Rückblende zum Start der Invasion. Vael 2120 TZ. Die Portal-Maschine wird aktiviert. Hymne, Flaggen, Kessels Abschiedsrede: »Wir holen uns die Welt zurück, die man uns genommen hat.«",
     "typen": ["hintergrund", "krieg"],
     "tags": ["Expedition 2 Aufbruch"]},
    {"mz": 9.25, "welt": "moragh", "pov": "Varen", "buch": "B3", "kapitel": "73", "leseart": "normal",
     "titel": "Varen versammelt seinen Zirkel — Einladung",
     "detail": "Zwanzig bis dreissig Anhänger, Velmar-Fragmente, Bund-Überläufer. Varen schickt eine Einladung an Alphina und Vesper: Duell-Ort, Duell-Zeit, Duell-Regeln. Er weiss, sie kommen.",
     "typen": ["begegnung", "tschechow"],
     "tags": ["Duell-Einladung"]},
    {"mz": 9.4, "welt": "moragh", "pov": "Runa", "buch": "B3", "kapitel": "74", "leseart": "normal",
     "titel": "Parallel-Schlacht beginnt — Runa + Nyr in Kessler",
     "detail": "Bündnis vs. Expedition vor Dulrath-Ost. Runa + Nyr in Kessler gegen Expeditions-Drohnen. Iven (17, Moragh-Elektrizitäts-Resonanz) lahmt Expeditions-Elektronik mit einem Störsender-Ritual, zahlt mit dem Körper.",
     "typen": ["krieg", "resonanz"],
     "tags": ["Iven", "Parallel-Schlacht", "Kessler im Kampf"]},
    {"mz": 9.5, "welt": "moragh", "pov": "Alphina", "buch": "B3", "kapitel": "75", "leseart": "normal",
     "titel": "Duell Alphina + Vesper vs. Varen — Beginn",
     "detail": "Drei Kapitel, etwa 15.000 Wörter. Varen in seinem Ring. Alphina und Vesper. Varen löst den Anker über seine Frequenz aus — Alphinas Dornen wachsen unter ihrer Haut. Vespers Schemen-Angriff zielt auf seinen Temporal-Helm.",
     "typen": ["krieg", "schluessel"],
     "tags": ["Duell", "Anker-Bruch"]},
    {"mz": 9.55, "welt": "moragh", "pov": "Vesper", "buch": "B3", "kapitel": "76", "leseart": "normal",
     "titel": "Vespers linker Unterarm zerkocht",
     "detail": "Ein aufgeladener Varen-Schemen fasst Vespers linken Unterarm. Haut spannt, bleibt unversehrt, Fleisch innen kocht. Er kämpft weiter mit der rechten Hand.",
     "typen": ["tod", "krieg"],
     "tags": ["Vesper-Arm-Verlust"]},
    {"mz": 9.6, "welt": "moragh", "pov": "Alphina", "buch": "B3", "kapitel": "77", "leseart": "normal",
     "titel": "Varens Register-Bruch + Reveal",
     "detail": "Drei Finger von Alphinas linker Hand explodieren in eigenen Dornen. Varen: »Kleine naive Alphina. Du warst sauberer zu lesen als Sorel. Ich habe dich nie angesehen. Nur deinen Frequenzwert.« Später: »Sie starb in der Küche.« Noch später, leise: »Garten.«",
     "typen": ["erkenntnis", "tod", "schluessel"],
     "tags": ["Register-Bruch", "Frequenzwert", "Küche", "Garten"]},
    {"mz": 9.65, "welt": "moragh", "pov": "Alphina", "buch": "B3", "kapitel": "77", "leseart": "normal",
     "titel": "Alphina gibt Varen den Todesstoss",
     "detail": "Mit verbleibenden zwei Fingern und Dornen. Kein Pathos, keine Rede. Varens letztes Wort: »Garten.« Sie versteht erst, dass er Elke meinte, als sie ihre Finger im Gras liegen sieht.",
     "typen": ["tod", "schluessel"],
     "tags": ["Varen tot", "Letztes Wort Garten"]},
    {"mz": 9.8, "welt": "synchronisation", "pov": "Alphina", "buch": "B3", "kapitel": "78", "leseart": "normal",
     "titel": "Portal-Finale — Expedition 2 startet zweite Durchgangs-Welle, Alphina kollabiert die Quelle",
     "detail": "Expedition aktiviert Modulator für zweite Welle. Stockwerkshohe Killermaschinen beginnen durchzutreten. Tausende Moragh-Tote beim Durchbruch. Alphina überlädt die Portal-Quelle mit Wachstum — Solo-Akt, Stufe 10. Quelle kollabiert beidseitig. Eine Maschine wird halbiert, Teil in jeder Welt.",
     "typen": ["portal", "tod", "schluessel"],
     "sync": {
        "thalassien": "Vael 2153 TZ. Alle Magie permanent weg. Farne stehen still, Steinkreis kalt, Institut wird zur Ruine einer überholten Wissenschaft.",
        "moragh": "Portal-Quelle tot. Portal endgültig zu. Expedition 2 in Moragh gestrandet, Rest in Thalassien ohne Rückweg.",
     },
     "tags": ["Portal tot", "Magie weg", "2153 TZ"]},
    {"mz": 9.9, "welt": "moragh", "pov": "Vesper", "buch": "B3", "kapitel": "79", "leseart": "normal",
     "titel": "Ruhezeit — Vesper amputiert, Gruppe erholt sich",
     "detail": "Vesper-Amputation mit Runas Feuer-Klinge. Drei Finger Alphinas sind verloren. Kessler liegt auf dem Schlachtfeld zurück, Nyr trauert. Die Gruppe rastet eine Moragh-Woche, zählt die Toten.",
     "typen": ["hintergrund", "tod"],
     "tags": ["Amputation", "Ruhezeit"]},
    {"mz": 10.0, "welt": "moragh", "pov": "Alphina", "buch": "B3", "kapitel": "80", "leseart": "normal",
     "titel": "Alphina + Vesper — BDSM-Annäherung",
     "detail": "Nach Wochen des Schweigens eine Nacht bei Kerzenlicht. Vesper als Dom, geduldig, reflektiert. Alphina erstmals Sub — durch Scham über ihre Varen-Zeit. Blühende Dornen ruhig, mit Blüten.",
     "typen": ["erotik", "begegnung"],
     "tags": ["BDSM-Annäherung", "Sub-Alphina"]},
    {"mz": 10.05, "welt": "thalassien", "pov": "", "buch": "B3", "kapitel": "I15", "leseart": "vorschau",
     "titel": "I15 — Kind in Vael berührt den Farn",
     "detail": "Thalassien 2155+. Ein Kind im Botanischen Garten legt die Hand an den alten Farn, der einst auf Alphina reagierte. Nichts passiert. Der Farn ist Pflanze, nur Pflanze.",
     "typen": ["hintergrund"],
     "tags": ["Magie weg", "Farn still"]},
    {"mz": 10.1, "welt": "moragh", "pov": "Alle", "buch": "B3", "kapitel": "EP", "leseart": "normal",
     "titel": "Epilog Halvek-Mar — vier Narbige + Tyra",
     "detail": "Halvek-Mar, Küstenstadt im Westen. Alphina (drei Finger fehlen, Farne wachsen wieder grün), Vesper (amputiert, Uhren bauen mit Prothese), Runa und Nyr (Kessler als zivile Arbeitsbestie im Hafen), Tyra (Moragh-Heimat, Schall-Resonanz). Stille. Meer. Narben. Keine Heimkehr.",
     "typen": ["hintergrund", "schluessel"],
     "tags": ["Halvek-Mar", "Epilog", "Narbige"]},
]


def block_b3() -> None:
    for e in B3_EVENTS:
        mz = e["mz"]
        tz_aequiv = mz_to_tz(mz)
        new_ev = dict(e)
        new_ev["tz"] = round(tz_aequiv)
        new_ev["tz_sort"] = tz_aequiv
        new_ev["tz_datum"] = f"MZ {mz:.2f} · TZ {round(tz_aequiv)}"
        new_ev.setdefault("kapitel_status", "idee")
        EVENTS.append(new_ev)


# =====================================================================
# BLOCK 6 — Monats-Sync-Punkte (nach jedem vollen Moragh-Monat)
# =====================================================================

def inject_monats_sync() -> None:
    """Fügt nach jedem vollen Moragh-Monat (MZ 1.0, 2.0, ..., 10.0) einen
    Synchronisations-Event ein, der die Thalassien-Zeitlage zu diesem Moment skizziert.
    Nur für den Zeitraum ab B2-Start (MZ > 0)."""
    monats_sync_texte: dict[int, tuple[int, str]] = {
        1:  (584, "Vael 584 TZ — die Vier fehlen, Halvard registriert ihr Verschwinden. Schemen-Aktivität lässt nach."),
        2:  (618, "Vael 618 TZ — 67 Jahre später (keiner lebt mehr, der die Vier kannte). Das Archiv in Vael existiert noch, Lenes Manuskript samt Varens Ergänzungen."),
        3:  (651, "Vael 651 TZ — 100 Jahre nach B1. Erste Automobile, Telegraph am Hafen. Schwellenforschung eine Randnotiz der Uni."),
        4:  (684, "Vael 684 TZ — 133 Jahre nach B1. Industrialisierung, Eisenbahn, erste Fabriken im Süden."),
        5:  (1987, "Vael 1987 TZ — Maren tritt durchs Portal ein. Gaslampen durch Elektrizität ersetzt, Automobile, Telefonleitungen. Beginnt zu dokumentieren."),
        6:  (2020, "Vael 2020 TZ — Schwellenforschungsgesellschaft ist staatliches Institut. Expedition 1 bricht auf."),
        7:  (2053, "Vael 2053 TZ — 16 Jahre nach Marens Tod. Eroberungs-Doktrin. Institut bewaffnet sich."),
        8:  (2087, "Vael 2087 TZ — Biotech-Bodymod-Programm beginnt. Junge Syra Halvard wird Forschungsleiterin."),
        9:  (2120, "Vael 2120 TZ — Expedition 2 bricht auf. 2500 Soldaten. General Kelvar Velkan führt."),
        10: (2153, "Vael 2153 TZ — Portal kollabiert. Alle Magie permanent weg. Institut wird Ruine."),
    }
    for mz_month, (tz_year, text) in monats_sync_texte.items():
        tz_aequiv = mz_to_tz(mz_month)
        add({
            "tz": round(tz_aequiv),
            "tz_sort": tz_aequiv + 0.0001,  # minimal nach Events im gleichen Monat
            "mz": float(mz_month),
            "tz_datum": f"MZ {mz_month}.0 · TZ {tz_year}",
            "welt": "synchronisation",
            "pov": "",
            "buch": "", "kapitel": "", "leseart": "normal",
            "titel": f"Sync — Ende Moragh-Monat {mz_month}",
            "detail": text,
            "typen": ["sync"],
            "tags": [f"MZ-Monat {mz_month}", f"TZ {tz_year}"],
            "kapitel_status": "",
        })


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def build() -> dict[str, Any]:
    block_tz_154()
    block_zeitsprung()
    block_b1()
    block_b2()
    block_b3()
    inject_monats_sync()

    # Sortiere strikt nach tz_sort
    EVENTS.sort(key=lambda e: (e["tz_sort"], e.get("mz") or 0))

    return {
        "meta": {
            "titel": "Der Riss — Zeitleiste",
            "untertitel": "Eine Welt, ein Riss, zwei Zeiten — chronologisch",
            "beschreibung": (
                "Strikte Chronologie nach Thalassien-Jahr (TZ). Moragh-Events erscheinen "
                "an ihrer TZ-Äquivalenz-Position (1 Moragh-Monat = 33,33 TZ-Jahre). "
                "Interludien sind chronologisch einsortiert, ihr Lesekontext im Roman "
                "steht im Feld 'buch/kapitel/leseart'."
            ),
            "zeitrechnung": {
                "tz_null": "Erfindung des Uhrwerks",
                "mz_null": "Besiedelung von Moragh (Portal-Ankerpunkt)",
                "verhaeltnis": "1 Moragh-Jahr = 400 TZ-Jahre = 12 MZ-Monate",
                "ankerpunkt": "B1-Start = 21. Saatmond 551 TZ = MZ 0",
            },
            "schema_version": 2,
        },
        "typen": TYPEN,
        "events": EVENTS,
    }


def main() -> int:
    apply = "--apply" in sys.argv
    data = build()
    print(f"Events gesamt: {len(data['events'])}")
    print("\nErste 10 Events (chronologisch):")
    for e in data["events"][:10]:
        print(f"  [TZ {e['tz']:5}] [{e['welt']:16}] [{e.get('buch', ''):3}-{e.get('kapitel', ''):4}] {e['titel'][:65]}")

    if apply:
        OUT.write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        print(f"\n(geschrieben: {OUT.relative_to(ROOT)})")
    else:
        print("\nDry-run. Für tatsaechliches Schreiben: --apply")
        print("HINWEIS: B1, B2, B3, Sync-Monate fehlen noch (TODO).")

    return 0


if __name__ == "__main__":
    sys.exit(main())
