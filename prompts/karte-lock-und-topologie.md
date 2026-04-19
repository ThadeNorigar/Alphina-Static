# Prompt für separate Claude-Session: Karten-Editor Lock + Topologie-Ansicht

Kopiere den folgenden Block in eine neue Session mit Claude Code im Projektverzeichnis
`C:\Users\micro\StudioProjects\Alphina-Static`.

---

## Prompt

Ich arbeite am Karten-Editor für die Moragh-Welt der Trilogie „Der Riss".
Die Karte ist jetzt inhaltlich fixiert — bitte baue zwei Features ein, die beide
die **bestehende Architektur** (`moragh-server.py` + `moragh-editor.html` + `buch/moragh-karte.json`)
minimal-invasiv erweitern.

### Kontext (Stand, bitte erst verifizieren)

- Editor-HTML: `moragh-editor.html` (im Projekt-Root)
- Server: `moragh-server.py` (Port 8090, GET/POST `/data`, schreibt `buch/moragh-karte.json`)
- Aktuelle Datenstruktur in `buch/moragh-karte.json`:
  `{ cities: [{x, y, name, size, faction}...], portal: {x, y, name}, coast: [[x, y]...] }`
- Die Karte ist inhaltlich abgeschlossen (Städte, Fraktionen, Küstenlinie, Portal in Dravek).
- Kein Breaking-Change am bestehenden Format. Neue Felder **additiv**.

### Aufgabe 1 — Schreibschutz (Lock)

**Ziel:** Der Editor darf Stadt-Positionen, Namen, Größen, Fraktionen, Küstenpunkte
und Portal-Position **standardmäßig nicht verändern**. Ein sichtbarer Entsperren-Knopf
schaltet die Bearbeitung frei.

**Verhalten:**
- Beim Laden ist der Zustand **gesperrt** — alle Bearbeitungs-Interaktionen (Drag,
  Klick-zum-Hinzufügen, Fraktions-Buttons, Löschen, Küsten-Editor) sind deaktiviert
  oder zeigen beim Versuch einen kurzen Hinweis („Karte ist gesperrt — oben rechts entsperren").
- Oben rechts ein Knopf: **`🔒 Gesperrt`** (Standard) / **`🔓 Entsperrt`** (nach Klick).
- Im entsperrten Zustand funktioniert der Editor wie bisher.
- Beim Entsperren eine sanfte Bestätigungs-Abfrage („Karte jetzt bearbeiten? Änderungen
  werden automatisch gespeichert.").
- Zustand wird **nicht** persistiert — bei Neuladen ist wieder `gesperrt`.
- Der Ansichtsmodus (Zoom, Pan, Hover, Tooltip) ist **immer** aktiv, auch im Lock.

**Implementationshinweis:** Es reicht ein `locked = true` Flag, das in den entsprechenden
Event-Handlern und im Auto-Save (`save()` in der `moragh-editor.html` bei ~Zeile 773)
früh aussteigt, wenn `locked`. Fraktions-Buttons deaktivieren per `disabled` oder
per CSS `pointer-events: none`.

### Aufgabe 2 — Topologie-Ansicht (separat)

**Ziel:** Eine zweite, umschaltbare Ebene zeigt **Höhenlinien, Gesteinsformationen
und Rohstoffvorkommen**, ohne die bestehende Städte-Ansicht zu überdecken oder zu zerstören.

**Umschaltung:**
- Oben rechts (neben Lock-Knopf) ein Ansichts-Umschalter:
  - `Politisch` (Standard, aktuell)
  - `Topologie`
- Bei `Topologie` werden Städte/Fraktionsfarben **stark zurückgenommen** (dünnere Linien,
  halbe Deckkraft) — sie bleiben als Orientierung sichtbar, treten aber in den Hintergrund.
- Die Topologie-Schicht erscheint darüber: Höhenlinien (dünne Konturen in Grautönen),
  Gesteinsformationen (farbig getönte Flächen), Rohstoff-Marker (kleine Symbole).

**Datenstruktur-Erweiterung für `buch/moragh-karte.json`:**

```json
{
  "cities": [...],
  "portal": {...},
  "coast": [...],
  "topology": {
    "contours": [
      { "elevation": 100, "points": [[x, y], ...], "closed": true }
    ],
    "formations": [
      { "type": "granit" | "basalt" | "sandstein" | "kalkstein" | "vulkanit",
        "polygon": [[x, y], ...],
        "label": "optional name" }
    ],
    "resources": [
      { "type": "eisen" | "kupfer" | "silber" | "salz" | "kohle" | "edelstein" | "purpurstein",
        "x": x, "y": y,
        "richness": 1-3 }
    ]
  }
}
```

**Editor-Tools für Topologie (nur im entsperrten Zustand):**
- Höhenlinien zeichnen: Polyline-Werkzeug, Höhe angeben.
- Formation zeichnen: Polygon-Werkzeug, Typ wählen.
- Rohstoff platzieren: Klick, Typ wählen, Ergiebigkeit 1–3.
- Löschen: Klick auf existierendes Element mit Entfernen-Modifier.

**Farbpalette (Vorschlag, kann variiert werden):**
- Granit: warmgrau
- Basalt: dunkel anthrazit
- Sandstein: ocker
- Kalkstein: hellbeige
- Vulkanit: rötlich-dunkelbraun
- Höhenlinien: grau, dünn, alle 100m eine Hauptlinie, alle 20m eine Nebenlinie
- Rohstoff-Symbole: kleine Icons mit Typ-Initiale (z.B. `Fe`, `Cu`, `Ag`, `S`, `K`, `◇`, `P`)

**Wichtig:**
- Politische Ansicht bleibt bei Re-Laden und beim Wechsel **intakt**.
- Topologie-Daten werden über denselben `/data`-Endpunkt gespeichert — Server muss
  das zusätzliche Feld persistieren (sollte mit dem generischen `json.dump`
  aus `moragh-server.py` automatisch klappen, aber bitte testen).

### Akzeptanzkriterien

1. Neu-Laden der Seite → Karte ist gesperrt. Keine versehentliche Bewegung möglich.
2. Entsperren-Knopf → Bestätigung → Bearbeitung funktioniert wie vorher.
3. Umschalter Politisch / Topologie → saubere Layer-Trennung, keine Darstellungs-Fehler.
4. Topologie-Daten in `buch/moragh-karte.json` werden persistiert und beim Neuladen wieder
   korrekt angezeigt.
5. Existierende Daten (cities, portal, coast) werden **nicht verändert**.

### Out of Scope

- Generieren von Beispiel-Topologie-Daten (mache ich selbst in der Session).
- Welt-spezifische Welt-Lore (Granit-Vorkommen in Orath etc.) — separat.
- Deploy / Build — lokal reicht.

### Start-Check vor Implementierung

1. Lies `moragh-server.py` und `moragh-editor.html` vollständig.
2. Lies die ersten 200 Zeilen von `buch/moragh-karte.json`, um die aktuelle Struktur
   und Größenordnung zu sehen.
3. Starte den Server (`python moragh-server.py`) und öffne `http://localhost:8090/`
   zum manuellen Testen während der Entwicklung.

Berichte Fortschritt kompakt, frage nur, wenn du zwischen zwei unklaren Wegen wählen musst.
Deutsch durchgehend, Umlaute korrekt, keine ae/oe/ue-Ersetzungen.
