#!/usr/bin/env python3
"""
Kuerzt ueberlange Event-Details in zeitleiste.json auf zeitleisten-gerechte Laenge
(~200-280 Zeichen statt 400-1277). Die vollstaendigen Plot-Details gehoeren in
Kapitel-Dossiers / Szenen-Plaene — in der Zeitleiste reicht der Beat-Kern.

Matcht Events ueber Titel (eindeutig). Wenn ein Titel nicht gefunden wird,
bricht das Skript ab mit einer Warnung — kein stilles Ueberschreiben.

Aufruf:
  python scripts/shorten-events.py           # dry-run (zeigt Diff)
  python scripts/shorten-events.py --apply
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
JSON_PATH = ROOT / "buch" / "zeitleiste.json"

# Key = Event-Titel (exakt). Value = neue Detail-Version (Plot-Beat, 1-3 Saetze).
SHORTENED: dict[str, str] = {
    "Varens Leylinien-Experiment scheitert":
        "Varen versucht drei Quellen unter Mar-Keth zu koppeln, um magiefreie Flaechen besiedelbar zu machen. Unfall: Mar-Keth, Dulrath-Ost und Reshkol kollabieren unwiederbringlich, ~200.000 Menschen heimatlos. Velmar vertuscht und stoesst Varen ohne Anklage aus. Der Bund haelt es fuer Naturkatastrophe, die Thar beschuldigen den Bund.",

    "Der Krieg beginnt — Orath vs. Thar vs. Velmar":
        "Drei MZ-Monate nach der Quellen-Explosion. Die Thar glauben an einen Bund-Angriff und schlagen zurueck — Krieg aus Misstrauen, nicht aus Ressourcennot. Dauert vier MZ-Jahre (~1.600 TZ). Velmar haelt sich raus, verhandelt mit der Thar. Die Vier erfahren in Buch 2 nur die Konglomerat-Version.",

    "Varen beginnt die Portalforschung":
        "Ein Jahr nach Kriegsbeginn. Varen erkennt: tote Quellen sind mit Moragh-Magie allein nicht wiederzubeleben. Er erinnert sich an die 350 Verschwundenen vor 200 MZ durchs Portal. Beginnt im Geheimen mit der Rekonstruktion — Druckmanipulation kennt er, Zeitmanipulation muss er lernen. Erste brachiale Versuche.",

    "Vesper erkennt: der Takt in der Brust hält":
        "Beim zweiten Besuch legt Vesper der Tidemoor-Uhr nicht nur die Hand auf, sondern gibt ihr den Ankerhemmungs-Takt aus der eigenen Brust vor: 'Behalte diesen Schlag.' Seitdem laeuft sie rein. Am Abend bestaetigt sich's: Kvarns Taschenuhr laeuft nach 90 Minuten Welle-Arbeit ebenfalls null Drift. Tschechow: aktive Uebertragung haelt.",

    "Alphina und Vesper finden sich":
        "Alphina klopft, fragt nach der 4:33-Standuhr. Vesper erzaehlt zum ersten Mal vor einem anderen Menschen vom aktiven Takt-Geben an der Tidemoor-Uhr. Alphina kontert mit den Farnen an der Nordmauer und dem Stein im Steinkreis. Beide benennen zwei Modi: Geben und Hoeren. Vesper zeigt die Ring-Karte. Alphina identifiziert den Mittelpunkt sofort als den Steinkreis im Botanischen Garten. Verabredung fuer morgen halb zehn am gruenen Tor.",

    "Kvarns Uhr läuft rein — Vesper erkennt sich selbst als Punkt":
        "Nach Alphinas Abgang laeuft Kvarns Taschenuhr ohne weiteres Zutun rein. Vesper erkennt: der Takt wandert vom Resonator ins Material, sobald Kontakt und innerer Takt zusammenfallen — bei Tidemoor als Befehl, bei Kvarn als stille Anwesenheit. Notizbuch: 'Ich bin der achtzehnte Punkt. Zwei Tueren weiter, die neunzehnte.' Die Vier werden selbst Quellen.",

    "Sorel: Alphina auf jeder Platte (Projektion ohne Erkenntnis)":
        "Sorel entwickelt alte Platten (Kai, Oberstadt, Nachtholm) und sieht Alphina auf fast jeder — im Hintergrund, auch auf Aufnahmen aus der Zeit vor ihrem Kennenlernen. Die Haende-Platte aus K12 ist unmoeglich scharf. Er erklaert sich's mit 'die Kamera sieht etwas', versteht nicht: es ist seine eigene unbewusste Licht-Resonanz, geformt von Obsession. Versteckt die Platten in einer Schublade.",

    "Sorel entdeckt seine Resonanz — belichtet Platten durch Gedanken":
        "Sorel schliesst eigene Fehler aus, testet eine unbelichtete Platte. Ein Bild erscheint. Dann erkennt er sich selbst auf der Platte beim Entwickeln. Paranoia, dann Daemmerung. Bewusster Test: er stellt sich das Bild vor, nach dem er sich seit Wochen sehnt. Die Platte zeigt Alphina. Sehnsucht kippt in Vertrauensbruch.",

    "Vesper bringt Maren die Schiffsuhr — erster ehrlicher Austausch über das Unmoegliche":
        "Vesper bringt die Schiffsuhr zur Werft — weil er sie sehen will, nicht weil die Uhr es verlangt. Maren fragt nach der Standuhr, er erzaehlt offen. Sie zeigt wortlos den Tee-Strudel: Waerme ohne Erschoepfung, keine Kosten. Vesper starrt eine Sekunde zu lang. Marens BDSM-Wahrnehmung schaerft sich an seiner wartenden Art. Vesper: 'sie muss Alphina kennenlernen.' Verabschiedet sich.",

    "Sorel sucht Vesper — zwei Maenner legen Puzzleteile zusammen":
        "Sorel sucht Vesper aus eigenem Antrieb auf: Schemen-Angriff K10, Brandwunde, Alphinas Heilung K12/13, Platten ohne Kamera K16 (er verschweigt das letzte Bild). Vesper bringt: Uhren-Drift, Grundfrequenz 4:33, Marens Tee-Strudel. Beide reden ueber Alphina — unabhaengig voneinander haben sie etwas an ihr beobachtet. Setup fuer das Garten-Treffen in K19.",

    "Alle vier im Garten — erster Kampf gegen einen Waechter-Schemen":
        "Vespers arrangiertes Treffen. Alle vier erstmals zusammen. Ein Riss oeffnet sich — Waechter-Schemen (3-4m, tierisch-humanoid). Maren wird an der Schulter verletzt. Vesper verlangsamt den Schemen unabsichtlich. Sorel buendelt Licht — wird geschluckt, zieht Alphina instinktiv weg (Hand an Schulter, Setup fuer K21 und K36). Dann flutet er diffuses Raumlicht. Alphina schickt Wurzeln durch die Beine des verlangsamten Schemens, Vesper beschleunigt sie. Der Koerper loest sich in Rauch auf. Alle vier erschoepft, aber sie fuehlen sich maechtig — das macht sie in Moragh unvorsichtig. Varen hat beobachtet und bekommen was er wollte.",

    "Maren bringt Vesper Harons Symbolblatt — gemeinsam ins Archiv":
        "Maren hat Harons Symbolblatt seit K08 — eine Steinkreis-Zeichnung. Nach dem Kampf in K19 erkennt sie den Kreis wieder, bringt es zu Vesper: 'Ich kann das nicht lesen. Du schon.' Im Archiv assistiert sie ihm freiwillig — sortiert, reicht Seiten, arbeitet ihm zu. Es macht sie ruhig. Vesper bemerkt es, sagt nichts. Esther Voss erkennt den Namen Dahl in einem Register. Jara im Hintergrund hoert alles. Das Manuskript wird erst K23 gefunden — hier nur der Faden.",

    "Alphina und Sorel: Dunkelkammer — Enthuuellung, Gestaendnis, erste intime Szene":
        "Alphina findet neunzehn Platten von sich in der Dunkelkammer — aus Winkeln, die sie nie eingenommen hat, zuletzt nackt. Sorel kommt rein, luegt nicht: 'Ich begehre dich. Seit dem Steg. Seit dem Garten. Ich wollte nicht aufhoeren.' Ihr Koerper erinnert sich an K19 (seine Hand an ihrer Schulter). Handgelenke-Callback. Farne wachsen durch die Kellerwaende. Danach: Du statt Sie, nicht als Entscheidung, als Tatsache. Er sagt etwas Beilaeufiges, Zukuenftiges — ein Versprechen, das er nicht weiss, dass er gibt.",

    "Nachbrenner: fremde Pflanze in Vael, der Riss sickert unkontrolliert":
        "Tage nach dem Kampf. Maren findet in der Werft eine Pflanze aus der Fuge zwischen Holzboden und Steinmauer — genau dort, wo in K08 das Wasser rueckwaerts hereinsickerte. Flache Blaetter, falsche Jahreszeit, kein Thalassien-Gewaechs. Alphina erkennt sie nicht. Der Riss sickert ohne Varens Zutun. Hafenwasser waermer als es sein sollte.",

    "Vesper + Maren: erste Dom/Sub-Nacht im Archiv":
        "Spaet, die anderen schlafen. Maren hilft bei Uebersetzungen aus dem Moragh-Sprachbuch. Vesper legt die Hand auf ihre Schulter um auf eine Zeile zu zeigen — dieselbe Geste wie K19, aber ohne Verband, ohne Ausrede. Er nimmt sie nicht weg, sie bewegt sich nicht. Er gibt ihr wenig Bewegungsspielraum, und sie entdeckt: das ist der Zustand, in dem ihr Kopf aufhoert zu laufen. Danach schlaeft sie sofort ein.",

    "3 Monate: Sprache lernen, unkontrollierte Risse eskalieren":
        "Die Gruppe lernt die Moragh-Sprache aus dem Sprachbuch. Vesper uebersetzt systematisch, die anderen ueben. Wenig Magie-Training — sie trauen sich nach K19 nicht. Risse eskalieren: Moragh-Flora in Mauerritzen, Hafenwasser nach fremdem Salz, Nebel dreimal die Woche, die Grauwe fliesst regelmaessig rueckwaerts. Alphina und Sorel: parallel, kuehl, professionell. Vesper und Maren: schweigend, praezise, ohne Benennung.",

    "Vael ohne die Fünf -- Varens Spuren verschwinden":
        "Schemen verschwinden schlagartig — Varens Inszenierungen enden. Aber kleinere Anomalien bleiben: Wasser fliesst ungewoehnlich, Uhren gehen falsch, Tidemoor-Uhr kaputt, Farne im Garten wachsen weiter. Die Riss-Quelle sickert weiter. Halvard schreibt seinen Bericht — das einzige schriftliche Zeugnis. Jara archiviert Runas Flugblaetter. Das Boot wartet, drei Viertel fertig.",

    "Bund-Stadt — die Älteste greift Alphinas Hand":
        "Elke fuehrt die Vier zur Bund-Stadt (zwei Tage Marsch). Menschen mit Augen in Farben, die es in Thalassien nicht gibt: Purpur, Weinrot, Schwarz. Die Aelteste erkennt Alphinas Wald-Potential — der Schlaf-Hain hat sich herumgesprochen. 'Ihr seid sicher hier.' Alphinas Haut kribbelt. Die Pflanzen im Aeltesten-Garten drehen sich alle gleichzeitig nach ihr. Akt-I-Schluss — Bund-Hof als Tschechow fuer Akt II.",
}


def main() -> int:
    apply = "--apply" in sys.argv

    z = json.loads(JSON_PATH.read_text(encoding="utf-8"))

    found: set[str] = set()
    missing: list[str] = []
    size_before = 0
    size_after = 0
    diffs: list[tuple[str, int, int]] = []

    for mi, m in enumerate(z["monate"]):
        for welt in ("thalassien", "moragh"):
            for ei, ev in enumerate(m.get("events", {}).get(welt, [])):
                if not isinstance(ev, dict):
                    continue
                titel = ev.get("titel", "")
                if titel in SHORTENED:
                    old = ev.get("detail", "")
                    new = SHORTENED[titel]
                    diffs.append((titel, len(old), len(new)))
                    size_before += len(old)
                    size_after += len(new)
                    found.add(titel)
                    if apply:
                        ev["detail"] = new

    for titel in SHORTENED.keys():
        if titel not in found:
            missing.append(titel)

    print(f"Gefunden:  {len(found)} / {len(SHORTENED)}")
    if missing:
        print(f"FEHLEND:   {len(missing)}")
        for m in missing:
            print(f"   !!! {m!r}")
        return 1

    print(f"Groesse:   {size_before} -> {size_after}  (-{size_before - size_after} chars)")
    print()
    for titel, old, new in sorted(diffs, key=lambda x: -x[1]):
        print(f"   {old:5} -> {new:3}  {titel[:65]}")

    if apply:
        JSON_PATH.write_text(
            json.dumps(z, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        print(f"\n(geschrieben: {JSON_PATH.relative_to(ROOT)})")
    else:
        print("\nDry-run. Fuer tatsaechliches Schreiben: --apply")

    return 0


if __name__ == "__main__":
    sys.exit(main())
