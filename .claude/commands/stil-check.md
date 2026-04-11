# /stil-check — Stilprüfung und Rhythmus-Analyse

Du prüfst ein Kapitel von "Der Riss" auf Stilprobleme. Systematisch, mit Zahlen.

## Input

`$ARGUMENTS` = Pfad zur Kapitel-Datei (z.B. `buch/kapitel/02-sorel.md`)

Wenn kein Argument: frage welche Datei.

## Phase 0: Kontext laden

Lies parallel:
1. Die Kapitel-Datei
2. `buch/02-stilregeln-v2.md` — Stilregeln
3. `buch/kapitel/01-alphina.md` — Referenzton (Kapitel 1 ist der Maßstab)
4. Das VORHERIGE Kapitel (für Stil-Konsistenz)

Bestimme:
- **POV-Figur** und **Perspektive** (ALLE POVs = 3. Person nah/Präteritum)
- **Figurenstimme** aus `buch/02-stilregeln-v2.md` Figurenstimmen-Tabelle laden:
  - Max Satzlänge (Alphina ~40W, Sorel ~50W, Vesper ~20W, Maren ~35W)
  - Leitmotiv (Puls, Hände, Turm/Finger, ?)
  - Rhythmus-Erwartung

## Phase 1: Harte Zählungen (mit Grep)

Zähle mit Grep/Bash — keine Schätzungen:

| Muster | Max | Aktion wenn über Limit |
|--------|-----|----------------------|
| "nicht X — sondern Y" / "nicht X, sondern Y" | 2x pro Kapitel | Überzählige markieren |
| "wie etwas das..." / "wie ein..." Vergleiche | 4x pro Kapitel | Überzählige markieren |
| "und" als Satzverbinder (Hauptsatz und Hauptsatz) | Meldung ab >3 in einem Satz | Ketten markieren |
| Wort/Phrase die >7x vorkommt (außer Artikeln/Pronomen) | 7x | Häufung markieren |
| Markante Phrase (z.B. "dreizehn Jahre", "die Routine") | 4x | Jede über 4 markieren |
| "als hätte/wäre/könnte..." Hypothetische Konstruktionen | ~6 | Dichte-Warnung |
| Sätze über figurenspezifischem Limit | Alphina >40W, Sorel >50W, Vesper >20W, Maren >35W | Überlängen markieren |
| Sätze >60 Wörter | Meldung | Bandwurm-Kandidaten markieren (alle Figuren) |
| Satzlängen-Verteilung: KURZ (1-10W), MITTEL (11-20W), LANG (21+W) | MITTEL >20% | FINDING wenn MITTEL <15% (Register-Monotonie) |
| Begehren-Wort-Wiederholung ("Puls", "Handgelenk", "kippte", "unter dem Nabel") | 3x pro Wort | FINDING wenn >3x dasselbe Begehren-Wort |
| Geschmack in Nähe-Szenen ("schmeckte", "Geschmack", "Zunge", "Lippen", "salzig", "bitter", "süß", "Metall auf") | min. 1 in Nähe-Szene | FINDING wenn Nähe-Szene ohne Geschmacks-Referenz |

## Phase 2: Rhythmus-Analyse

Gehe das Kapitel Absatz für Absatz durch:

**1. Bandwurm-Stakkato-Balance:**
- Folgen zwei Bandwurm-Sätze (>40 Wörter) direkt aufeinander? → Finding
- Gibt es Passagen >500 Wörter ohne einen Einwortsatz oder Fragment? → Finding
- Unter Druck/Schock: bricht die Syntax? (Einwortsätze, Fragmente, Abbrüche) → Wenn nicht: Finding

**2. "und"-Ketten:**
- Sätze mit >3 "und"-Verbindungen als Hauptsatz-Reiher identifizieren
- Absätze mit >5 "und"-Verbindungen markieren
- Vergleich: wie viele "und"-Ketten hat Kapitel 1 pro 1000 Wörter vs. dieses Kapitel?

**3. Satzanfänge:**
- Gleicher Satzanfang >3x in einem Absatz? → Finding
- "Er/Sie/Ich" als Satzanfang >40% der Sätze? → Finding

## Phase 3: Stilregeln-Check

**1. Emotionen benannt statt gezeigt:**
- Suche nach: "war traurig", "fühlte Angst", "war wütend", "spürte Freude", "war nervös", "war einsam"
- Auch indirekt: "kein Schmerz, keine Angst" (benennt durch Negation)
- → Markieren. Körperreaktion stattdessen.

**2. Erklärende Nachsätze:**
- Sätze die enden mit "weil..." wo die Handlung für sich spricht
- Sätze die zusammenfassen was gerade passiert ist
- "als hätte/wäre/könnte..." Anhänge die nur das Offensichtliche erklären
- → Markieren. Braucht die Leserin das?

**3. Magie-Ankündigungen:**
- "Plötzlich geschah etwas Seltsames/Unerwartetes"
- "Etwas war anders"
- Jede Meta-Kommentierung von Magie durch den Erzähler
- → Magie passiert mitten im Alltag. Nie ankündigen.

**4. Komma-Listen (Körper- und Detail-Inventuren):**
- Suche nach Sätzen mit **3+ komma-getrennten Substantiv-Phrasen** ohne Verben dazwischen
- Besonders bei Körperbeschreibungen: *"Runde Schultern, runde Hüften, Schwärze an den Unterarmen, ein Fleck auf der Wange."* → Katalog statt Wahrnehmung
- Muster-Erkennung: Phrase + Komma + Phrase + Komma + Phrase (+ Komma + Phrase), jede Phrase ohne Verb
- Ausnahme: Stakkato-Inventur unter Druck (Vesper am Uhrwerk), wenn die POV-Figur BEWUSST zählt/katalogisiert
- → Finding. Fix-Prinzip: **Sequenz statt Inventur.** Was sieht die POV-Figur zuerst? Welches Detail fällt auf, während die beschriebene Person sich BEWEGT? Statische Listen durch Wahrnehmungs-Hierarchie ersetzen.
- Test: Kann man die Komma-Glieder in beliebiger Reihenfolge vertauschen ohne dass sich etwas ändert? Dann ist es eine Liste, keine Wahrnehmung.

**5. Name vor Einführung (Sorel-Prinzip):**
- Jeder Eigenname muss INNERHALB des Textes eingeführt werden (Dialog, Schild, eigene Schlussfolgerung)
- Der Narrator darf den Namen einer Figur NICHT benutzen bevor die POV-Figur ihn kennt
- Prüfung: Erste Erwähnung des Namens — wo erfährt die POV-Figur ihn? Wenn die Einführung NACH der ersten Erwähnung kommt → Finding
- Fix: *"Runa wischte sich die Hände..."* → *"Die Druckerin wischte sich die Hände..."* bis zur Vorstellung

**6. Dialog-Handwerk (siehe Stilregeln v2 "Dialog-Handwerk"):**

*Adverb-Tags (HARTES VERBOT, max 0):*
- Suche: `sagte (er|sie|.*) (wütend|traurig|liebevoll|dominant|befehlend|leise|laut|fröhlich|nervös|ärgerlich|ruhig|kalt|freundlich)`
- Auch: `flüsterte/murmelte/zischte + Adverb`
- → Finding. Fix: Adverb streichen, Körper zeigen oder Tag ganz weg.

*Tag-Frequenz:*
- In zusammenhängenden 2-Personen-Dialogen: max 1 Tag pro 4-6 Wechsel
- Wenn jede Replik einen Tag hat → Finding (Tempo erstickt)
- Action-Beats statt Tags wenn der Körper etwas verraten soll

*Info-Dump-Marker:*
- Suche: `wie du weisst|wie du weißt|wie ihr wisst|wie wir alle wissen|du erinnerst dich`
- → Finding. Figuren erzählen einander nicht was beide wissen.

*On-the-nose:*
- Repliken die ihr eigenes Thema direkt aussprechen ("Ich liebe dich, aber ich habe Angst vor dir.")
- Repliken die Plot-Punkte oder Motive buchstabieren
- → Finding. Subtext fehlt.

*Pause-Inflation:*
- Pausen/Schweigen pro Szene zählen
- Mehr als 2-3 bedeutungsschwere Pausen (`Stille.`, `Pause.`, `Er schwieg.`, `Sie sagte nichts.`) pro Szene → Finding (Inflation entwertet sie)

*Anonymisierungs-Test:*
- Eine Seite Dialog ohne Tags lesen — erkennt man wer spricht?
- Wenn die Stimmen nicht differenziert sind → Finding
- Vergleich: Satzlänge, Lieblingswörter, Bildfeld, wie jeder "nein" sagt

**7. Innenleben & Gedankengänge (siehe Stilregeln v2 "Innenleben"):**

*Denk-Tags (HARTES VERBOT, max 0):*
- Suche: `(sie|er) dachte|(sie|er) fragte sich|(sie|er) überlegte|(sie|er) sagte sich`
- → Finding. Im Deep POV überflüssig. Erlebte Rede stattdessen.

*Kursiv-Inflation:*
- Kursive Passagen zählen (`*...*` Markup oder bekannte Gedanken-Einwürfe)
- Max 5-6 pro Kapitel
- Kursiv NUR für Fast-Ausrufe — kurze, hammer-artige Einwürfe
- Laufendes Denken bleibt in erlebter Rede, NICHT kursiv
- Über Limit → Finding

*Flashback-Rampe (HARTES VERBOT):*
- Suche: `sie erinnerte sich, dass|er erinnerte sich an den Tag|sie dachte zurück an`
- → Finding. Erinnerung muss durch konkreten Reiz im Jetzt ausgelöst werden, nicht angekündigt.

*Prämature Ahnung (Sorel-Prinzip, HARTES VERBOT):*
- Suche: `sie wusste noch nicht, dass|er ahnte nicht, dass|niemand wusste, dass`
- → Finding. Narrator weiss nur was die Figur weiss.

*Berufslinsen-Bruch:*
- Beschreibungen prüfen: Sieht die POV-Figur durch ihre Berufslinse?
- Alphina (Botanikerin) → Wachstum/Wurzeln/Druck. KEIN Tonwert, keine Belichtung.
- Sorel (Fotograf) → Licht/Belichtung/Tonwert. KEINE Pflanzennamen.
- Vesper (Uhrmacher) → Toleranz/Passung/Mechanik. KEINE Heilkräuter.
- Maren (Schiffbauerin) → Strömung/Holz/Salz. KEINE Sterndeutung.
- Bruch → Finding.

*Direkte Emotionsbenennung im Innenleben (max 0):*
- Suche: `(sie|er) war (traurig|wütend|nervös|einsam|verzweifelt|glücklich|ängstlich)`
- Auch: `(sie|er) fühlte (Trauer|Wut|Angst|...)`
- Auch indirekt: `kein Schmerz, keine Angst`
- → Finding. Körpersymptom oder Gedanken-Fragment stattdessen.

*Navel-Gazing-Test:*
- Gedanken-Passagen prüfen: Endet sie in einem Verb der Handlung?
- Wenn die Reflexion bei sich selbst bleibt → Finding (Füllmaterial)
- Mehr als 2 Absätze reine Innensicht ohne Außenhandlung → Finding

**8. Metapher-Ökonomie (siehe Stilregeln v2 "Metapher-Ökonomie"):**
- Nach einem starken Bild/Vergleich/Metapher: prüfe ob der Folgesatz dasselbe Konzept in anderen Worten wiederholt
- Semantische Doppelung = FINDING
- Beispiel-Finding: *"Ein Nagel, der stand. Ein Nagel, der noch nicht eingetrieben war."* → zweiter Satz killt den ersten
- Manueller Check — aufmerksam Absatz für Absatz lesen, besonders nach lyrischen Passagen

**9. Register-Verteilung (siehe Stilregeln v2 "Register-Wechsel"):**
- Satzlängen-Histogramm aus Phase 1 auswerten
- Melde im Bericht: Anteil KURZ / MITTEL / LANG
- FINDING wenn MITTEL <15% (Register-Monotonie — zu viele lange Sätze, zu wenig Mittelbau)
- FINDING wenn nur 1 Register verwendet wird (alle Sätze im selben Bucket)
- Min. 2 Register pro Kapitel ist Pflicht

**10. Kontrollverlust-Check (siehe Stilregeln v2 "Kontrollverlust-Momente"):**
- Hinweis im Bericht: *"Enthält das Kapitel Kontrollverlust-Momente (Analyse stoppt, Körper übernimmt)? Council-Reviewer prüft."*
- Automatisch prüfbar: Gibt es Szenen mit körperlicher Nähe? Wenn ja → Hinweis dass min. 1 Kontrollverlust-Moment erwartet wird
- Nicht automatisch prüfbar: ob die Berufslinse im richtigen Moment versagt — das prüft der Council

**11. Begehren-Vokabular (siehe Stilregeln v2 "Begehren-Vokabular"):**
- Grep nach häufigen Begehren-Markern: "Puls", "Handgelenk", "kippte", "unter dem Nabel", "warme Hände"
- FINDING wenn >3x dasselbe Begehren-Wort im Kapitel
- Prüfe ob das Begehren-Register zum POV passt (Alphina = Invasion/Wachstum, Sorel = Licht/Bild, Vesper = Takt/Mechanik, Maren = Strömung/Drift)

**12. Geschmack in Nähe-Szenen (siehe Stilregeln v2 "Geschmack als Pflicht-Sinn"):**
- Identifiziere Szenen mit körperlicher Nähe/Berührung
- Grep nach Geschmacks-Wörtern: "schmeckte", "Geschmack", "Zunge", "Lippen", "salzig", "bitter", "süß", "Metall auf", "Salz"
- FINDING wenn Nähe-Szene ohne Geschmacks-Referenz

## Phase 3.5: Cross-POV und Aftermath

**1. Cross-POV-Vokabular:**
- Benutzt dieser POV dieselben Beschreibungen wie ein anderer POV für denselben Ort?
- Prüfe gegen `02-stilregeln-v2.md` POV-Vokabular-Tabelle
- Finding wenn identische Formulierungen für Stein, Nebel, Geruch etc.

**2. Aftermath-Pacing:**
- Nach einem Climax-Moment (Horror, Enthüllung, Gänsehaut): gibt es mindestens 3 Beats?
- Körper → Raum → Stille → Frage
- Finding wenn direkt nach dem Peak zum Kapitelende gesprungen wird

## Phase 4: Vergleich mit Referenzkapitel

Kurzer Abgleich mit Kapitel 1:
- Stimmt die Erzähldichte? (Sinne pro Absatz, spezifische Details)
- Stimmt das Tempo? (Kapitel 1 hat ~200 Wörter pro Minute Lesezeit, Pausen durch Fragmente)
- Stimmt der Figurenton? (Alphina = Kontrolle + Risse. Sorel = Stille + Hände.)

## Output: Gate-Bericht

```
## Stil-Check: [Dateiname]
POV: [Figur] | Perspektive: [Ich/3.P] | Wörter: [N]

### Harte Zählungen
| Muster | Gefunden | Limit | Status |
|--------|----------|-------|--------|
| "nicht X — sondern Y" | N | 2 | OK/ÜBER |
| "wie..." Vergleiche | N | 4 | OK/ÜBER |
| "und"-Ketten (>3 pro Satz) | N | — | Meldung |
| Wort-Häufungen (>7x) | [Wort]: Nx | 7 | OK/ÜBER |
| Bandwurm-Sätze (>60W) | N | — | Meldung |
| Satzlängen: KURZ/MITTEL/LANG | N%/N%/N% | MITTEL >20% | OK/UNTER |
| Begehren-Wort-Wiederholung | [Wort]: Nx | 3 | OK/ÜBER |
| Geschmack in Nähe-Szenen | ja/nein | min. 1 | OK/FEHLT |

### Findings

| # | Zeile | Typ | Problem | Fix-Vorschlag |
|---|-------|-----|---------|---------------|
| 1 | ~63 | UND-KETTE | 7x "und" in einem Satz | Aufbrechen: Punkte statt "und" |
| 2 | ~37 | BANDWURM | 2 Bandwürmer hintereinander, kein Stakkato | Fragment einfügen |
| 3 | ~67 | EMOTION | "kein Schmerz, keine Angst" benennt Emotionen | Nur Körperbild: "der Moment bevor man fällt" |

### Sauber
- [Was gut funktioniert — Leitmotive, Sinne, Rhythmus-Stellen die sitzen]

### Zusammenfassung
- Findings gesamt: N
- Kritisch (Harte Limits überschritten): N
- Rhythmus (und-Ketten, Bandwürmer): N
- Stil (Emotionen, Nachsätze, Ankündigungen): N

### Verdikt
**BESTANDEN** / **NICHT BESTANDEN** — [Begründung in einem Satz]
```

**NACH DEM BERICHT:**
Frage den Autor: "Bericht gelesen? Soll ich die Fixes einarbeiten, oder willst du Findings streichen/anpassen?"

**GATE: Keine Weiterarbeit ohne explizite Freigabe durch den Autor.**

## Regeln

- JEDEN Absatz prüfen. Nicht überfliegen.
- Harte Zählungen mit Grep — keine Schätzungen.
- Im Zweifel: Finding erstellen.
- Keine Fixes ohne Freigabe. Nur Bericht.
- Der Autor entscheidet was gefixt wird und was bleibt.

$ARGUMENTS
