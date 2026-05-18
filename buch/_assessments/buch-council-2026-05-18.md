# /buch-council — Buch 1 (Der Riss) · Bogen-Verdict

*Lauf: 2026-05-18 · Modus: key · 5 Personas parallel · 24 Schluesselkapitel · ~93k Woerter pro Persona*

**Kontext:** Buch 1 ist fertig (168.337 Woerter, 673 Seiten, 43 Kapitel + Epilog). Erster Buch-Level-Council nach K40 final. Ziel: pruefen, wo das Buch Markt-Promise einloest und wo nicht.

**Wichtige Korrektur am Lauf:** In den Subagent-Prompts wurde Alphina/Sorel faelschlicherweise als BDSM-Top/Bottom gerahmt. Korrekt laut `00-positioning.md` Abschnitt 3.2: *"sie fuehrt, er hat Grenzen — aus Charakter, nicht BDSM"*. Konsequenzen unten in Abschnitt "Korrektur".

---

## 1. Master-Tabelle

| Stimme    | Score | Drop-Off | Top-Staerke               | Top-Schwaeche                | Buy B2 |
|-----------|-------|----------|---------------------------|------------------------------|--------|
| LINA      | 86 %  | nirgends (knapp K11/K26/K33) | K12 Bank · K21 Dunkelkammer · K39 Begraebnis | K26 Krisensitzung · K33 zweite Pendel-Nacht · K17 Maren-Einfuehrung | **Ja** |
| NORA      | 82 %  | nirgends (knapp K33→K34) | K21 Dunkelkammer · K35 V/M-BDSM · K38 Varen+Sorels Tod | K26/K33/K34 drei Recherche-Runden · Magie-Demo-Wiederholungen · Sorel zu hoeflich | **Ja** |
| MEIKE     | 84 %  | nirgends (ueberflog K27_5) | K01 Eroeffnung · K10 Platte 14 · K30 Hafenangriff | K38 Varen zu kurz · K23/K27_5 Heat-Stau ohne Welt-Druck · K26 Council-Reihum | **Ja** |
| VICTORIA  | 84 %  | nirgends (knapp K38/K39) | K27_5 Karst-Gestaendnis · K35 Akt selbst · K33 Pendel-Skalierung | K11 zu beilaeufiger Dom-Anker · K17 Magie kapert BDSM-Funken · K21 Top nicht koerperlich vollzogen *[hinfaellig — siehe Korrektur]* | **Ja** |
| KAYA      | 78 %  | nirgends (knapp K11/K15) | K38 Sorel-Tod · K39 Trauer-zu-Auftrag · K30 Hafenangriff | K11 Setz-Kasten-Schicht · K26 Council ohne Angst · K34 Vorbereitung ohne Bruch | **Ja** |
| **Durchschnitt** | **82,8 %** | — | — | — | **5/5** |

**Niedrigste Stimme:** KAYA mit 78 % — Haerte-Register ist das Risiko-Signal.
**Status:** GRENZWERTIG (≥75 % UND ≥3/5 Buy) — 7 % unter dem 90 %-Gate fuer BESTANDEN.
**Bemerkenswert:** 0/5 Drop-Offs. Niemand ist ausgestiegen, alle haben Buch 2 gekauft.

---

## 2. Korrektur (Alphina/Sorel-Framing)

In den Persona-Subagent-Prompts wurde Alphina als "weibliche Top" und Sorel als "maennlicher Bottom" beschrieben. Das ist BDSM-Vokabular auf eine Charakter-Beziehung gepfropft. Positioning 3.2 sagt explizit: *"Emotionaler Kern: sie fuehrt, er hat Grenzen — aus Charakter, nicht BDSM."*

**Hinfaellig:**
- VICTORIAs zentrale K21-Kritik (*"konventionell vollzogen, Top/Bottom im Bett nicht eingeloest"*) — falsche Pramisse. Das Versprechen war nie "Top im Bett". Ihr K21-Punkt faellt.
- Ursprueglich vorgeschlagener Top-Fix #2 (K21 — Alphina als Top physisch lesbar machen) — gestrichen.

**Unberuehrt:**
- LINA, NORA, MEIKE, KAYA: keine hat BDSM-Brille auf A/S angelegt. Verdicts stehen.
- VICTORIAs Hauptkritik (1 vollexplizite Vesper/Maren-Szene auf 78k Woerter, K11 zu beilaeufig, K17 Magie kapert BDSM-Funken) — alle unabhaengig vom Fehler, bleibt stehen.
- VICTORIAs Score 84 % wahrscheinlich stabil (Hauptkritik betrifft V/M-Linie, nicht A/S-Linie).

**Empfehlung:** CLAUDE.md "Sie dominiert, er hat Grenzen" → "Sie fuehrt, er hat Grenzen — aus Charakter" anziehen, damit der Fehlpfad nicht wieder passiert.

---

## 3. Konvergenz-Befunde (≥3 Stimmen einig)

### Konvergente Staerken

- **K38–K39 Sorels Tod + Alphinas Trauer-zu-Auftrag** — LINA · NORA · KAYA. Drei sehr unterschiedliche Register loben dasselbe: keine Pose, koerperlich, mit Folge.
- **K21 Dunkelkammer-Sex (A/S Heat-Probe)** — LINA · NORA · MEIKE. Heat-Sweet-Spot, dunkel-explicit-emotional.
- **K35 Vesper/Maren-BDSM-Vollszene** — NORA · VICTORIA · KAYA. Réage-Disziplin sitzt; auch NORA und KAYA, die nicht primaer BDSM-Leserinnen sind, nennen die Szene als Bogen-Staerke.
- **K30 Hafenangriff (Joran-Tod, Runas Brand)** — MEIKE · KAYA. Konvergenz 2/5, aber stark gewichtet: einzige Stelle wo Vael unter Druck steht.

### Konvergente Luecken

- **Council-/Tabellen-Stau K26 + K33 + K34** — LINA · NORA · MEIKE · KAYA (**4/5!**). Drei aufeinanderfolgende Recherche-/Synthese-Sitzungen ohne Reibung am Tisch. **Klarstes Markt-Signal des Laufs.**
- **Akt I zu langsam** — NORA · VICTORIA · KAYA (3/5).
- **Akt IV zu kurz/schnell** — LINA · VICTORIA · KAYA (3/5).
- **Sorel-Figur unterentwickelt zwischen K23 und K38** — NORA · VICTORIA · LINA (teilweise). NORA: "stirbt als Stativ-Traeger". LINA: "eine einzige stille Szene fehlt".
- **Runa zu spaet innen** — LINA · NORA · MEIKE. Entscheidung mitzugehen passiert off-stage (K34 Tuer-Lauschen).
- **Varen zu kurz und zu spaet** — MEIKE · NORA (2/5, beide nachdruecklich). Antagonist traegt 38 Kapitel Erwartung und loest sie nicht ein.

---

## 4. Top-4-Fixes (priorisiert)

*Urspruenglich 5 — Fix #2 nach Korrektur gestrichen.*

1. **[MITTEL-GROSS] Council-Diet K26/K33/K34** — drei Recherche-Sitzungen auf zwei reduzieren ODER mit Reibung am Tisch aufladen. Konvergenz 4/5. **Hoechster Hebel.** Erwartete Wirkung: +3–5 % Durchschnitt.

2. **[MITTEL] Stille Alphina/Sorel-Szene zwischen K23 und K29 einfuegen.** LINA-Forderung. Loest Sorel-zu-Stativ-Problem (NORA, VICTORIA) und macht Sorels Tod in K38 haerter. Erwartete Wirkung: +2–3 %.

3. **[MITTEL-GROSS] Runa-Innen-Beat zwischen K34 und K38.** LINA + NORA + MEIKE. Eine kurze Runa-POV-Sequenz, in der sie SELBST entscheidet, mitzugehen — nicht draussen vor der Tuer. Erwartete Wirkung: +1–2 %.

4. **[MITTEL-GROSS] Varen frueher anschattieren.** MEIKE + NORA. Entweder einen einzelnen K-IV-Beat einbauen (Brief, Schemen-Spur, Zeichen) der Varens Stimme/Methode anteased, oder seinen K38-Auftritt verlaengern und koerperlich eskalieren. Erwartete Wirkung: +2–3 %.

**Bonus:** Akt IV insgesamt zu kurz (3 Personas). Wenn das Buch nicht mehr wachsen soll (168k → 225k Ziel), ist die natuerliche Stelle dafuer hier.

---

## 5. Akt-Verteilung — Verdict

| Akt | Kap | Woerter | Anteil | Verdict |
|-----|-----|---------|--------|---------|
| I   | 15  | 64.154  | **38 %** | **zu lang** (3/5: NORA, VICTORIA, KAYA) — klassisches Akt-I-Ziel ~25 % |
| II  | 10  | 35.278  | 21 %     | OK |
| III | 12  | 40.987  | 24 %     | OK strukturell — K26 zu fett |
| IV  | 7   | 27.918  | **17 %** | **zu kurz** (3/5: LINA, VICTORIA, KAYA) — Tor-Finale + Epilog gepresst |

**Diagnose:** Vorne dehnt sich das Buch in vier POV-Einfuehrungen, hinten wird der Uebertritt + Trauerbogen + B2-Setup in 7 Kapiteln gepresst. Eine Verschiebung von ~5–8 % von Akt I nach Akt IV wuerde das Bogen-Gleichgewicht herstellen, ohne die Gesamt-Wortzahl wesentlich zu verschieben.

---

## 6. Interludien-Verteilung — Verdict

Aktuell alle 3 in Akt I (I1 nach K4, I2 nach K8, I3 nach K12). **Moragh ist zwischen K12 und K38 — 26 Kapitel, 100k Woerter — unsichtbar.**

MEIKE: *"Moragh selbst bekommt nur zwei Kapitel; ich will MEHR Welt-mit-Zaehnen drueben."*
LINA: I3 *"wirkt mehr Funktion als Figur, emotional nicht."*

**Empfehlung:**
- I1 bleibt (nach K4)
- I2 bleibt (nach K8)
- **I3 wandert in Akt III** (z.B. nach K27 oder K30) — gleicher Inhalt, andere Position bringt Moragh kurz vor Tor-Uebertritt ins Bewusstsein
- **Optional ein neues I4** zwischen Akt III und IV (Varen-Schatten / Moragh-Welt vor Tor) — wuerde Top-Fix #4 und MEIKEs Welt-Mangel zugleich loesen

---

## 7. Kapitel-Plan

**Legende:** ✅ behalten · ✂️ Mikro-Edit · 🔧 mittlerer Umbau · 🏗️ grosser Umbau / Streichung / Neu · ⚪ nicht direkt im Council geprueft (Behalten-Default)

### Akt I — Diaet-Kandidat

| Kap | POV | W | Aktion | Quelle | Aufwand |
|-----|-----|---|--------|--------|---------|
| K01 | Alphina | 4.2k | ✅ behalten | MEIKE: Hook sitzt | — |
| K02 | Sorel | 3.8k | ⚪ Default behalten | — | — |
| K03 | Vesper | 3.4k | ⚪ Default behalten | — | — |
| K04 | Maren | 4.2k | ⚪ Default behalten | — | — |
| I1  | Elke | 2.7k | ✂️ Elke koerperlich-greifbarer (1-2 Koerperbeats statt Welt-Inventar) | LINA: "verliere Elke nach I2" | Mikro |
| K05 | Alphina | 4.4k | ⚪ Default behalten | — | — |
| K06 | Sorel | 3.4k | ⚪ Default behalten | — | — |
| K07 | Vesper | 2.9k | ⚪ Default behalten | — | — |
| K08 | Maren | **5.4k** | 🔧 laengstes Akt-I-Kapitel — auf 4.5k straffen (Akt-I-Diaet) | KAYA: "vier POVs brav eingefuehrt" | Mittel |
| I2  | Elke/Keldan | 1.6k | ✂️ wie I1 | LINA | Mikro |
| K09 | Alphina | **7.9k** | ✂️ Buch-laengstes Kapitel — auf 7k straffen | LINA/MEIKE loben, aber lang | Mikro-Mittel |
| K10 | Sorel | 6.7k | ✅ behalten | LINA + MEIKE: Staerke | — |
| K11 | Vesper | 6.7k | 🔧 **Uhren-/Tabellen-Anteil straffen + Vesper-Koerperdruck einbauen** (Dom-Vektor-Signal staerker) | LINA/KAYA/VICTORIA — 3/5 schwach | Mittel |
| K12 | A+S | 5.4k | ✅ behalten | LINA: "schoenste Stunde im Buch" | — |
| I3  | Elke | 1.5k | 🏗️ **nach Akt III verschieben** (z.B. nach K27) — Inhalt bleibt, Position aendert sich | MEIKE Moragh-Mangel, LINA "funktional aber emotional schwach" | Gross (Verschiebung) |

**Akt-I-Diaet-Summe:** ~−2.5k Woerter aus K8, K9, K11 + I3-Verschiebung.

### Akt II — solide, gezielte Fixes

| Kap | POV | W | Aktion | Quelle | Aufwand |
|-----|-----|---|--------|--------|---------|
| K13 | Sorel | 3.3k | ✅ behalten | LINA: Teil der starken Sequenz | — |
| K14 | Maren | 3.3k | ⚪ Default behalten | — | — |
| K15 | Alphina | 2.5k | 🔧 **Schemen-Folge muss Konsequenz haben** (jetzt zu folgenlos), oder Szene verdichten | LINA "fast gestiegen", KAYA "nichts kostet" | Mittel |
| K16 | Sorel | 4.0k | ⚪ Default behalten | — | — |
| K17 | Maren | 2.9k | 🔧 **Tee-Magie-Demo zuruecknehmen** — Maren-Wollen und BDSM-Funken vor die Magie | LINA + NORA + VICTORIA — 3/5 schwach | Mittel |
| K18 | Vesper | 3.6k | ⚪ Default behalten | — | — |
| K19 | Alle  | 4.4k | ⚪ Default behalten | — | — |
| K20 | Maren | 3.6k | ⚪ Default behalten | — | — |
| K21 | Alphina | 4.0k | ✅ behalten | LINA + NORA: Staerke | — |
| K22 | Maren | 3.5k | ✅ behalten | LINA: "macht Maren begehrenswert" | — |

### Akt III — Council-Diet kritisch

| Kap | POV | W | Aktion | Quelle | Aufwand |
|-----|-----|---|--------|--------|---------|
| K23 | Alphina | 2.3k | ✅ behalten | — | — |
| **NEU** | A+S | ~2k | 🏗️ **Stille A/S-Szene einfuegen** zwischen K23 und K26 — Fruehstueck / Hafen / Pflanze, kein Plot | LINA explizit + macht K38 haerter | Mittel |
| K24 | Alphina | 4.0k | ⚪ Default behalten | — | — |
| K25 | Runa | 2.0k | ⚪ Default behalten | — | — |
| K26 | Vesper | **6.3k** | 🏗️ **Council-Diet:** auf ~4k kuerzen + Reibung am Tisch | **4/5:** LINA + NORA + MEIKE + KAYA | **Gross** |
| K27 | Maren | 4.1k | ⚪ Default behalten | — | — |
| **NEU optional** | — | ~1.5k | 🏗️ **I3 hier einsetzen** (verschoben aus Akt I) | MEIKE: Moragh-Mangel | Mittel (Verschiebung) |
| K27_5 | Vesper | 3.3k | ✅ behalten | NORA + VICTORIA: Karst-Gestaendnis Staerke | — |
| K28 | Maren | 3.5k | ⚪ Default behalten | — | — |
| K29 | Sorel | 2.0k | ✅ behalten | LINA: Sorel allein im Dunkel | — |
| K30 | Sorel | 3.4k | ✅ behalten | MEIKE + KAYA: Hafenangriff = Staerke | — |
| K31 | Runa | 2.7k | ⚪ Default behalten | — | — |
| K32 | Alphina | 3.5k | ⚪ Default behalten | — | — |
| K33 | Vesper | 3.7k | 🔧 **zweite Pendel-Nacht straffen** oder mit gekuerztem K26 zusammenfuehren | LINA + NORA: Recherche-Stau | Mittel |

### Akt IV — Aufbau-Kandidat

| Kap | POV | W | Aktion | Quelle | Aufwand |
|-----|-----|---|--------|--------|---------|
| **NEU optional** | — | ~2k | 🏗️ **I4 einfuegen** — Moragh mit Varen-Schatten als Vorbereitung Tor | MEIKE + Top-Fix #4 | Mittel |
| K34 | Alle | **5.3k** | 🏗️ **Vorbereitungsabend mit Bruch laden** + **Runa-Innen-Beat einbauen** | NORA + MEIKE + KAYA + LINA/MEIKE (Runa) — 4/5 | **Gross** |
| **NEU optional** | A+S | ~1.5k | 🏗️ **Gewaehlter A/S-Uebergang zwischen K34 und K35** — Pendant zur M/V-Nacht | LINA explizit | Mittel |
| K35 | Maren | 3.0k | ✅ behalten | NORA + VICTORIA + KAYA: Réage-Disziplin sitzt | — |
| K36 | Alphina | 3.1k | ⚪ Default behalten | — | — |
| K37 | Runa | 4.8k | ⚪ Default behalten — ggf. Runa-Innen-Beat hier statt K34 | — | — |
| K38 | Alphina | 5.4k | 🔧 **Varen-Auftritt verlaengern + koerperlich eskalieren** — kein "spricht-flieht" | MEIKE + NORA — 2/5, nachdruecklich | Mittel-Gross |
| K39 | Alphina | 3.7k | ✅ behalten | LINA + KAYA: Trauer-zu-Auftrag = Staerke | — |
| **NEU optional** | — | ~2k | 🏗️ **Akt-IV-Aftermath** zwischen K39 und K40 — kollektive Stille | KAYA: "Welt muesste laenger nachbluten" | Mittel |
| K40 | Multi | 2.7k | ✅ behalten | LINA: "Schluss traegt" | — |

---

## 8. Wortzahl-Effekt

| Bereich | Δ Woerter |
|---------|-----------|
| Akt I Diaet (K8, K9, K11 straffen, I3 verschieben) | −2.5k |
| K26 Council-Diet (auf 4k + Reibung) | −2.3k |
| K33 straffen | −1k |
| K34 Vorbereitung mit Bruch + Runa-Innen | +1k |
| K38 Varen verlaengern | +1.5k |
| NEU stille A/S-Szene Akt III | +2k |
| NEU A/S-Uebergang Akt IV (optional) | +1.5k |
| NEU Akt-IV-Aftermath (optional) | +2k |
| NEU I4 Moragh/Varen (optional) | +2k |
| **GESAMT** | **+4 bis +5k** |

Buch waechst von 168k auf ~173k — naeher am Yarros-Korridor (Fourth Wing 170k). Ziel 225k bleibt nur erreichbar, wenn zusaetzlich Akt II oder III um neue Plot-Szenen erweitert wird (nicht Council-empfohlen, muesste aus Story-Bedarf kommen).

---

## 9. Bearbeitungs-Reihenfolge

1. **K26 zuerst** (4/5-Konvergenz, hoechster Hebel, groesster Aufwand)
2. **K11 + K17 + K15 parallel** (drei Mittel-Fixes, jeweils 3/5-Konvergenz, voneinander unabhaengig)
3. **K34 + Runa-Innen-Beat** (4/5-Konvergenz, ein groesserer Umbau)
4. **K38 Varen-Verlaengerung**
5. **K33-Straffung** (kleiner Mittel-Fix nach K26)
6. **Stille A/S-Szene Akt III einfuegen**
7. **Akt-I-Diaet** (K8/K9 straffen, I3 verschieben) — am Ende, weil reine Kuerzung
8. **Optionale Neu-Szenen** (I4, A/S-Uebergang Akt IV, Aftermath) je nach Zeit/Lust

---

## 10. Voll-Verdicts pro Persona

### LINA — Romantasy (Score 86)

**Drop-Off:** nirgends — aber dreimal nah dran: K11 (zwei POVs reden ueber Uhren und Pendel, ich habe gewartet, wann endlich jemand jemanden anfasst), K26 (Tabellen-Sitzung — ich verstehe, dass ihr das braucht, ich will trotzdem Haende und Haut), K33 (zweite Pendel-Theorie hintereinander). Drangeblieben wegen Sorel/Alphina und weil ich Maren und Vesper gerochen habe, lange bevor sie sich angefasst haben.

**Genre-Promise:**
- eingeloest: Slow-Burn Romantasy mit Koerperbeats (gehalten ab K10) · First Touch → First Time → Second Time gestaffelt (K12 Knie → K15 Steg → K21 Dunkelkammer → K23 Ausblende — Yarros/Maas-Treppe) · BDSM als gewaehlte Praxis (K27_5/K35 Réage/Reisz-Niveau) · Frauen-Agency · Dark-Atmosphaere die traegt
- nicht eingeloest: Magie wird mir zu oft erklaert statt erlebt (K11, K26, K33, K34) · Runa als halbe Figur · Vael nach Akt I weniger gerochen

**Pacing-Bogen:** zu langsam K11 + K15 + K17 (drei Aufbau-Kapitel ohne Kipp) und K26 + K33 (zwei Tabellen-Sessions auf eine reduzieren) · genau richtig K12 → K13 → K15 → K21 (beste Sequenz im Buch) · zu schnell K30 → K34 → K38 (acht Tage Buch-Zeit; brauche eine Nacht zwischen K34 und K38) · K38 → K39 → K40 genau richtig hart

**Top-Stelle:** K12 Bank — *"Ihre rechte Hand ruhte auf ihrem Knie. Ihre linke ruhte auf seinem, auf seinem Knie, warm durch den Hosenstoff. Er hatte erst spaet bemerkt, wann sie sie dorthin gelegt hatte."*

**Romance-Promise:** Sorel-Bogen sauber serviert. Treppe Slow-Burn → First Touch → First Time explizit → Second Time mit Ausblende → Riss/Tod → Anfang der emotionalen Reparatur sitzt. Swoon-Momente genug. Sorels Tod traegt emotional, weil Kiesel-Tschechow gespielt + Alphina stumm trauert und dann jagt (Witwen-Wut, nicht Witwen-Weinen). Was fehlt: eine einzige stille Szene zwischen K23 und K30, in der die zwei einfach nur leben.

**Buy B2:** Ja — Sorel ist tot und ich will Alphina mit dem Kiesel in der Tasche durch Varens Welt jagen sehen.

### NORA — Dark Romance (Score 82)

**Drop-Off:** nirgends, knapp — aber zwischen K33 und K34 hat das Buch mich fast verloren mit "noch eine Tabellen-Session, noch ein Drei-Spalten-Bogen".

**Genre-Promise:**
- eingeloest: Power-Dynamik weiblich-fuehrt-maennlich ohne Klischee · Réage-Niveau BDSM (K35) · Dark Atmosphaere · Toter-Liebhaber-Bogen mit Wumms · K21 hot/weird/dark
- nicht eingeloest: SCHAERFE IM DIALOG (reden wie Forschungsseminar) · Antagonist (Varen 2 Seiten in K38, sofort interessantester Mann) · Sex-Frequenz (zwei volle Szenen + K23-Soft in 24 Kapiteln)

**Power-Dynamik:** Haelt ueber alle Akte — groesste Leistung des Buchs. Alphina dominiert Sorel von erster Beruehrung bis letzter (sie zieht IHN zu sich in K21, sie entscheidet K23, sie heilt, sie waehlt das Tempo). Vesper/Maren halten Réage-Disziplin. ABER: Frauen werden in Akt III von Recherche geschoben, nicht von Wollen. Erst K38/K39 kaempft Alphina wirklich. Schaerfe im Dialog fehlt durchgehend — niemand provoziert, alle konsensorientiert.

**Buy B2:** Ja — Sorels Tod, Alphinas "wir vernichten ihn" und Varen haben mich gehakt, aber wehe B2 hat wieder drei Tabellen-Sessions.

### MEIKE — Dark Fantasy (Score 84)

**Drop-Off:** Nirgends, bei K27_5 ueberflogen (pures BDSM-Setup, nicht mein Register).

**Genre-Promise:**
- eingeloest: Vael HAT Zaehne — Purpurstein, Tor, Wesen die sich aus dem Schatten "schaelen" und Joran von hinten toeten. Eigenes Magie-System mit koerperlichen Konsequenzen. Cross-POV-Vokabular haelt. Sorel-Prinzip diszipliniert durchgehalten. K1 ist Hook wie er sein muss
- nicht eingeloest: Varen kommt zu spaet und zu kurz · Welt Moragh erst zwei Kapitel vor Schluss da

**Welt-mit-Zaehnen:** Vael hat Zaehne, sehr eigene (Purpurstein, Wetterfahne, rueckwarts fliessende Grauwe, 46 Kanaele, Tidemoor-Uhr 4:33, suesser Stein-Geruch). Wo es generisch wird: Wesen-Beschreibungen in K34 (Inventur-Szene rutscht in Standard-Demon-Vokabular). POV-Disziplin haelt. Gruppen-Dynamik im Tor-Finale nicht konstruiert. Aber Moragh selbst bekommt nur zwei Kapitel; will MEHR Welt-mit-Zaehnen drueben.

**Buy B2:** Ja — wegen Sorels Tod und Runas Tuer-Klopfen. Muss wissen wer Varen ist und ob Alphinas "vernichten" haelt.

### VICTORIA — BDSM (Score 84)

**Drop-Off:** Nirgends hart. Knappste Stelle K38–K39 (Moragh-Uebertritt + Sorels Tod) — BDSM-Linie und Romance bricht kollektiv ab.

**Genre-Promise:**
- eingeloest: Réage-Klinik in BDSM-Linie ernsthaft getroffen (Material mit Funktion benannt) · Power-Exchange mit GRUND (K27_5 Karst-Gestaendnis = Reisz-Niveau) · Aftercare zentral (K35 Wasser, Mandeloel-Massage, koerperliches Halten) · Symbol-Protokoll (Schachturm im Saum) = Réage-rein · Heat-Korridor sauber (kein Vulgaer-Slip)
- nicht eingeloest: K17 Tee-Drehung kapert BDSM-Spannung · K35 ist einzige vollexplizite V/M-Szene auf 78k Woerter · Maren-POV-Hingabe meist ueber Erinnerung statt szenischer Echtzeit · ~~A/S Top/Bottom~~ *[hinfaellig — siehe Korrektur]*

**BDSM-Linie:** Vesper/Maren ist die ernsthafteste BDSM-Linie in deutschsprachiger Dark Romantasy seit Jahren — Material konsistent ueber 5 Monate Diegese, Aftercare bewusst und koerperlich, Psychologie warum Vesper Dom ist und warum Maren submittet steht in Werk-Praxis und Karst-Gestaendnis. Réage-Boden getroffen, mehrfach. Aber: EINE vollexplizite Szene auf den ganzen Bogen ist zu wenig — bei Primaer- und Sekundaerlinie haette ich von jeder zwei Vollszenen erwartet.

**Buy B2:** Ja — wenn V/M mit etablierter Disziplin weitergefuehrt wird und Heat-Frequenz steigt; seltene Stimme im deutschen Markt.

### KAYA — Dystopie/Grimdark (Score 78)

**Drop-Off:** Nirgends, zweimal nah dran: K11 (siebzehn Uhren, vier Tabellen-Versionen, kein Koerper) und K15 (Schemen-Folge, die nichts kostet).

**Genre-Promise:**
- eingeloest: Sorel-Tod brutal, koerperlich, ohne literary-Vorhang (K38) · Joran-Tod als kalter Kollateralschaden · Alphinas Knien neben kalter Hand (K39) · Vespers Frost-im-Knochen (K30) bleibt · schwarze Blueten aus Sorels Brust als Grabmal = Bild
- nicht eingeloest: 80% des Buchs Romantasy + Tee-und-Tabellen · Vael nicht als bedrohte Stadt erlebt · Halvards Patienten als Listen statt Koerper · fuer 800-Seiten-Buch zu wenig Druck auf Ueberlebenden vor Uebertritt

**Haerte-Probe:** Sorel-Tod ehrlichste Stelle im Buch (kein moralischer Schutz, kein letztes Wort). Folge in K39 (Hand auf kalter Hand, Koerper-Steifheit, Kiesel-Transfer) und ansatzweise K35 (M/V als Festhalten vor Aufbruch). Wo geduckt: ganze Vael-Stadt vor dem Tor. Joran off-stage, Wesen tun fast nichts, Halvards Patienten Aktenzeichen. Genuegt mir Buch 1 als Dystopie-Probe? Nicht ganz. Romantasy mit echtem Tod im Finale — und Tod erkauft viel. B2 muss liefern: Krieg, Tote als Tote, Varen mit Gewicht.

**Buy B2:** Ja — wegen K38/K39 und Maren/Sorel; aber B2 muss Haerte zur Norm machen, nicht Ausnahme.
