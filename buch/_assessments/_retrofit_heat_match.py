#!/usr/bin/env python3
"""Retrofit: aktualisiert Heat-Achsen-Werte (strikt nach Canon-Definition) +
berechnet Kern-Gesamt (6 Achsen) + Heat-Match als Diagnose-Flag.

Verdikt-Politik (revidiert 2026-05-18):
- FINAL nur aus Kern (6 monotone Achsen, Schwelle 9.0)
- Heat-Match ist Diagnose-Flag (OK/Knapp/Miss), nicht verdikts-bestimmend
- Heat-Miss triggert Refit-Empfehlung, blockiert aber nicht Final-Status
- Trauer/Plot/Epilog-Kapitel koennen jetzt sauber FINAL werden

Heat-Definition (Canon `01-autorin-stimme.md` §11):
  0-1: keine               (Plot, Kampf, Archiv, Dialog)
  2-3: leise               (Blickwechsel, Waerme ohne Beruehrung)
  4-6: commercial          (Kuss, Koerper-Masse, Heat spuerbar)
  7-9: explizit nicht-BDSM (Sex auf der Seite, Alphina/Sorel)
  8-10: explizit BDSM      (Vesper/Maren, Réage-Disziplin)
"""
import json
from pathlib import Path

BASE = Path(__file__).parent
fp = BASE / "kapitel-scores.json"
data = json.loads(fp.read_text(encoding="utf-8"))

# Heat-Ist neu erhoben (strikte Definition, Welle A-D + 4 bereits korrekt)
HEAT_IST = {
    "B1-K01": 1.0, "B1-K02": 0.5, "B1-K03": 0.5, "B1-K04": 1.0, "B1-I1": 0.0,
    "B1-K05": 2.0, "B1-K06": 0.5, "B1-K07": 2.5, "B1-K08": 1.0, "B1-I2": 0.0,
    "B1-K09": 2.5, "B1-K10": 1.0, "B1-K11": 2.5, "B1-K12": 3.5, "B1-K13": 3.5,
    "B1-K14": 4.0, "B1-K15": 1.5, "B1-K16": 4.5, "B1-K17": 4.5, "B1-K18": 3.5,
    "B1-K19": 2.5, "B1-K20": 3.0, "B1-K21": 9.0, "B1-K22": 3.5, "B1-K23": 5.0,
    "B1-K24": 2.0, "B1-K25": 7.0, "B1-K26": 2.0, "B1-K27": 9.0, "B1-K27_5": 8.0,
    "B1-K28": 1.5, "B1-K29": 2.0, "B1-K30": 2.0, "B1-K31": 0.5, "B1-K32": 1.0,
    "B1-K33": 1.5, "B1-K34": 1.0, "B1-K35": 9.0, "B1-K36": 5.0, "B1-I3": 1.5,
    "B1-K37": 1.5, "B1-K38": 2.0, "B1-K39": 2.0, "B1-K40": 1.0,
}

# Heat-Soll basierend auf Plan/Genre-Erwartung pro Kapitel-Typ
# (Soll = was das Kapitel laut Bogen-Plan an Heat braucht; nicht zwingend = Ist)
HEAT_SOLL = {
    "B1-K01": 2,    # Hook Alphina, etwas Begehren plausibel
    "B1-K02": 1,    # Sorel-Eroeffnung Plot
    "B1-K03": 1,    # Vesper-Eroeffnung
    "B1-K04": 1,    # Maren-Eroeffnung
    "B1-I1":  0,    # Origin-Vignette
    "B1-K05": 2,    # Ankunft mit Runa-Funke
    "B1-K06": 1,    # Sorel-Schemen-Plot
    "B1-K07": 3,    # Vesper, BDSM-Vorgriff
    "B1-K08": 2,    # Maren-Schemen
    "B1-I2":  0,    # Origin-Vignette
    "B1-K09": 3,    # Resonanz-Touch
    "B1-K10": 2,    # Sorel-Erkennung Alphina
    "B1-K11": 3,    # Vesper-Alphina-Begegnung
    "B1-K12": 4,    # A/S-Schwelle
    "B1-K13": 3,    # Sorel-Naehe-Beats
    "B1-K14": 4,    # Maren-Begehren commercial
    "B1-K15": 2,    # Steinkreis-Plot
    "B1-K16": 4,    # Sorel-imaginierte Akt-Platte
    "B1-K17": 5,    # Maren/Vesper-Schwelle
    "B1-K18": 4,    # Vesper-Dom-Begehren
    "B1-K19": 3,    # Action mit Naehe-Subtext
    "B1-K20": 3,    # V/M-Bridge
    "B1-K21": 9,    # erster Sex A/S
    "B1-K22": 3,    # Plot mit V/M-Heat
    "B1-K23": 5,    # Kuss + Sex-ausblende
    "B1-K24": 2,    # Archiv-Plot mit Spur
    "B1-K25": 6,    # Runa-Solo-Sex (Heat-Echo)
    "B1-K26": 3,    # Council mit V/M-Mikro
    "B1-K27": 9,    # V/M-Vollszene
    "B1-K27_5": 8,  # V/M-Bruecke
    "B1-K28": 2,    # Solo-Untersuchung
    "B1-K29": 2,    # Brueckentag
    "B1-K30": 3,    # Bett + Action
    "B1-K31": 1,    # Trauma-Solo
    "B1-K32": 1,    # Plot
    "B1-K33": 2,    # Solo-Forschung
    "B1-K34": 2,    # Planung mit Halte-Beat
    "B1-K35": 9,    # V/M-Vollszene
    "B1-K36": 5,    # erster Kuss A/S
    "B1-I3":  1,    # Tod-Ritus
    "B1-K37": 2,    # Action Riss
    "B1-K38": 2,    # Trauer/Tod
    "B1-K39": 2,    # Trauer
    "B1-K40": 1,    # Vael-Epilog
}

# Heat-Begruendungen aus Re-Erhebung (Subagent-Output)
HEAT_BEGRUENDUNG = {
    "B1-K01": "Plot-Aufbruch um Pflanzen-Resonanz; Laris-Erinnerung mit Hand auf Bauch ist Abwehr/Schliessung, nicht Begehren.",
    "B1-K02": "Doppelgaenger-Schock in der Dunkelkammer, keinerlei Naehe-Register oder Begehren.",
    "B1-K03": "Werkstatt, Varen-Begegnung, 4:33-Raetsel; kein Koerper- oder Naehe-Register.",
    "B1-K04": "Ankunft an Werft, Edric-Vorstellung sachlich, Thessa-Rueckblick ist Flucht vor Naehe, kein Begehren.",
    "B1-I1":  "Origin-Vignette Steinkreis 154 n. Chr.; reine Plot/Welt-Exposition ohne Naehe-Register.",
    "B1-K05": "Runa-Begegnung in der Druckerei: Fingerberuehrung beim Muenz-Uebergeben, Runas Hitze, Kribbeln in Alphinas Hand als dezenter Funke.",
    "B1-K06": "Schemen-Encounter am Poller, Plot/Horror; kein Begehren oder Koerper-Naehe-Register.",
    "B1-K07": "Magd-Imago kniend mit Tuch ueber Augen (BDSM-Vorgriff), Streifen am Arm, Fingerspitzen auf Vespers Handflaeche — Begehren angedeutet, kein Vollzug.",
    "B1-K08": "Schemen-Arbeit unterm Segel; Koerper-Hellwachheit ist Magie-Resonanz, kein Naehe-/Begehren-Register.",
    "B1-I2":  "Origin-Vignette Keldans Glocke; Handwerks-Wunder, keinerlei Naehe-Register.",
    "B1-K09": "Runas Fingerspitzen am inneren Handgelenk ('eine Stelle, die ein Mensch nicht beilaeufig beruehrte'), warme Haut durchscheinend — leise queere Anziehung angedeutet.",
    "B1-K10": "Plot-/Magie-Kapitel: Sorel entdeckt Platte 14, fotografische Spurensuche, Verbrennung — kein Begehrensregister, nur fixierte Aufmerksamkeit auf Alphinas Bild.",
    "B1-K11": "Erste lange Begegnung Vesper/Alphina im Tuerrahmen: Daumen streift Schwiele, 'keine Absicht. Oder eine, die keiner zugeben wollte' — Waerme angedeutet, kein Touch-Register.",
    "B1-K12": "Alphinas Hand auf Sorels Knie, 'Ziehen tief im Bauch, gegen den Atem', Hand-Heilung am Verband — deutliches Begehren ohne Kuss/Koerper-Masse.",
    "B1-K13": "Alphina nimmt Sorels Hand im Gaslicht, Daumen auf Brandstelle, Mantelstoff streift Mantelstoff in der Gasse — sinnliche Naehe-Beats, ohne expliziten Kuss.",
    "B1-K14": "Marens Koerper bei Vespers Blick: harter Zug unterm Nabel, Waerme in Oberschenkel-Innenseiten und Handgelenk-Adern — explizites koerperliches Begehren, kein Touch.",
    "B1-K15": "Plot-Kapitel (Schemen, Runa-Bericht, Mittelpunkt-Enthuellung); Sorel-Begegnung am Steg ist Schweigen/Abkehr, kurz 'Waerme in den Handflaechen'.",
    "B1-K16": "Sorels imaginierte Akt-Platte von Alphina (Brustwarze, Huefte, Licht ueber Schluesselbein) — auf der Seite ausgemalte Begehrens-Komposition als Scham/Bekenntnis, kein realer Akt.",
    "B1-K17": "Maren stellt sich Vespers Fingerkuppen an ihrer Sehne vor, Waerme tiefer in Becken — deutliches BDSM-Sub-Begehren imaginiert.",
    "B1-K18": "Vespers Bild von Marens kniender Pose, Glut 'reglos in seinem Becken' — Dom-Begehren angedeutet, primaer Plot-Gespraech mit Sorel.",
    "B1-K19": "Action-/Magie-Kapitel dominiert; Heat nur in Mikro-Beats: Alphinas Koerper erkennt Sorel vor ihr, Sorels Hand bleibt nach dem Wegreissen kurz am Arm 'ohne Druck'.",
    "B1-K20": "V/M-Bridge-Beats ohne Sex: Vespers 'Schlaues Maedchen' loest Atem unter den Schluesselbeinen aus, Salz auf Marens Oberlippe, seine Schulter neben ihrer ohne Beruehrung.",
    "B1-K21": "Alphina/Sorel-Erstsex auf der Seite: Mund am Hals, Hand am Oberschenkel, Penetration, Orgasmus mit Farnen-Manifestation aus Wand, Aftercare auf Mantel; Yarros/Réage-Anatomie ohne BDSM.",
    "B1-K22": "Pflanzen-Plot dominiert; V-Heat erst am Ende: Maren schnuert enger 'wusste, dass sie das fuer ihn tat', Pochen in Innenseiten der Schenkel, Mund trocken.",
    "B1-K23": "Magie-Uebung mit erotischer Aufladung, dann offenes 'Ich will dich', Kuss mit Zunge, Mieder-Schnur wird geloest; Sex selbst ausgeblendet (Yarros-Ton).",
    "B1-K24": "Archiv-Plot-Kapitel; Heat nur als Spur: Unterarm streift seinen am Krug, Hand in Sorels Manteltasche auf der Gasse.",
    "B1-K25": "Runa masturbiert allein in der Druckerei mit Alphina-Fantasie auf der Seite: feucht, Orgasmus mit Heat-Echo-Brand am Werktisch; explizit-soloszenisch.",
    "B1-K26": "Council-Plot-Kapitel; Heat nur in zwei Mikro-Beats am Anfang: Druck hinter Vespers Hosenbund beim Anblick Marens, Daumen entlang ihres Lederriemens.",
    "B1-K27": "V/M-Vollszene Réage-Disziplin: Anweisungs-Strip vor dem Tisch, Hand am Geschlecht, Orgasmus ueber dem Tisch, Schlucken der feuchten Finger, 'braves Maedchen', Aftercare.",
    "B1-K27_5": "V/M-Power-Exchange-Bridge ohne Vollszene: Schachturm-Uebergabe als Konsens-Ritual, geheimes Saum-Fach im Wollrock; explizites Begehrens-Bild ohne Vollzug.",
    "B1-K28": "Solo-Untersuchung mit Schemen-Begegnung; nur Eroeffnung (schlafender Vesper) und Schluss (Anlehnen an seinen warmen Ruecken, 'Waerme, die nichts wollte') als leise Naehe-Beats.",
    "B1-K29": "Kurzes Begehren-Bild zu Beginn (Bogen ihrer Huefte) und am Ende stilles Liegen bei Alphina mit Hand am Brustbein; sonst Magie-Test und Schemen-Horror.",
    "B1-K30": "Eroeffnung intim im Bett (Alphinas Hand auf Brustbein) und Schluss-Geste, aber Schutz-/Liebes-Register ohne Begehren, dazwischen Angriffs-Set-Piece.",
    "B1-K31": "Reines Trauma-/Erkenntnis-Solo nach Jorans Tod; kein Naehe-Register, nur Wut, Wut-Magie und Vorbereitung des Aufbruchs.",
    "B1-K32": "Hafen-Plot und Tag-Schemen-Angriff; nur winziger Schluss-Beat im Flur ('Waerme unter dem Schluesselbein, einmal, kurz, vorbei') beim Wiedersehen mit Sorel.",
    "B1-K33": "Solo-Forschung und Pendel-Magie; am Morgen liegt Marens Daumen auf seinem Unterarm — zaertlich-vertraut ohne Begehren.",
    "B1-K34": "Planungs-Meeting der Vier; Alphina/Sorel am Ende angekleidet im Bett, leiser Halte-Beat, sonst reines Plot/Logistik-Kapitel.",
    "B1-K35": "V/M-Vollszene mit Schachturm-Ritual, Augenbinde, Hanf-Stricken an vier Pfosten, Mandeloel, Edging und Penetration; Réage-Disziplin auf der Seite.",
    "B1-K36": "Erster Kuss Alphina/Sorel im Steinkreis mit 'Darf ich?'-Geste, weichem Oeffnen der Lippen, Heat-Echo als Farn-Wachstum — commercial spuerbar.",
    "B1-I3":  "Kurze zaertliche Geste (Hand auf Kespers Hand), danach reines Feuer-/Ritus-/Todes-Set-Piece am Steinkreis ohne Begehren.",
    "B1-K37": "Action/Riss-Sprung-Kapitel; kein Begehren-Register, nur Plot-Eskalation und Cliffhanger mit Varens Hand unter Alphinas Kinn.",
    "B1-K38": "Sorels Tod und Alphinas Verlust; Varens Halsgriff hat Klinik-Touch ohne Power-Exchange, kein Begehren-Akt.",
    "B1-K39": "Trauer-zu-Auftrag; Beerdigung mit Wurzel-Magie, kein Naehe-/Begehren-Register.",
    "B1-K40": "Drei Verlust-Vignetten in Vael (Jara/Edric/Tarn); kein Naehe-/Begehren-Register, reine Ghost-Presence-Atmosphaere.",
}

KERN_ACHSEN = ["sog", "plot_charakter", "stil_disziplin", "pov_schaerfe", "verstaendlichkeit", "tschechow"]
KERN_SCHWELLE = 9.0


def heat_match(soll: float, ist: float) -> float:
    return max(0.0, round(10.0 - 2.0 * abs(soll - ist), 1))


def heat_flag(match: float) -> str:
    if match >= 7.0:
        return "OK"
    if match >= 5.0:
        return "Knapp"
    return "Miss"


def verdikt_neu(kern: float) -> str:
    return "FINAL" if kern >= KERN_SCHWELLE else "NICHT-FINAL"


fehlend = []
for k in data["kapitel"]:
    if k["id"] not in HEAT_IST:
        fehlend.append(k["id"])
        continue
    # Heat-Ist updaten (alte Werte aus Methoden-Drift ersetzen)
    k["council"]["scores"]["heat"] = HEAT_IST[k["id"]]
    # Optional: Begruendung als Side-Info
    if k["id"] in HEAT_BEGRUENDUNG:
        k["council"]["heat_begruendung"] = HEAT_BEGRUENDUNG[k["id"]]

    scores = k["council"]["scores"]
    kern_werte = [scores[a] for a in KERN_ACHSEN]
    kern_gesamt = round(sum(kern_werte) / len(kern_werte), 2)
    soll = HEAT_SOLL[k["id"]]
    ist = HEAT_IST[k["id"]]
    hm = heat_match(soll, ist)
    flag = heat_flag(hm)
    vd = verdikt_neu(kern_gesamt)
    k["council"]["kern_gesamt"] = kern_gesamt
    k["council"]["heat_soll"] = soll
    k["council"]["heat_match"] = hm
    k["council"]["heat_flag"] = flag
    k["council"]["verdikt_neu"] = vd
    # Alte Pseudo-Felder von vorherigem Retrofit-Lauf entfernen
    for old in ("verdikt_neu_grund", "verdikt_strukturell", "verdikt_note"):
        k["council"].pop(old, None)

if fehlend:
    raise SystemExit(f"FEHLER: Heat-Ist fehlt fuer: {fehlend}")

# Meta updaten
meta = data["meta"]
meta["heat_ist_quelle"] = "2026-05-18 Re-Erhebung Welle A-D (strikte Definition nach 01-autorin-stimme.md §11)"
meta["heat_soll_map"] = HEAT_SOLL
meta["heat_match_formel"] = "max(0, 10 - 2 * |heat_soll - heat_ist|)"
meta["heat_flag_schwellen"] = {
    "OK": "match >= 7.0",
    "Knapp": "5.0 <= match < 7.0",
    "Miss": "match < 5.0  → Refit-Empfehlung, kein Final-Blocker",
}
meta["verdikt_neu_schwelle"] = "FINAL wenn kern_gesamt >= 9.0 (6-Achsen-Mittel: sog/plot/stil/pov/verstaendlichkeit/tschechow)"
meta["kern_achsen"] = KERN_ACHSEN
meta["heat_politik"] = "Heat ist Diagnose-Achse, nicht Final-Blocker. Heat-Miss triggert Refit-Empfehlung, blockt aber nicht den Final-Status."

n = len(data["kapitel"])
final_n = sum(1 for k in data["kapitel"] if k["council"]["verdikt_neu"] == "FINAL")
nicht_final_n = n - final_n
heat_ok = sum(1 for k in data["kapitel"] if k["council"]["heat_flag"] == "OK")
heat_knapp = sum(1 for k in data["kapitel"] if k["council"]["heat_flag"] == "Knapp")
heat_miss = sum(1 for k in data["kapitel"] if k["council"]["heat_flag"] == "Miss")

# Auch der Final-Reif-Liste folgendes hinzufuegen
final_ids = [k["id"] for k in data["kapitel"] if k["council"]["verdikt_neu"] == "FINAL"]
heat_miss_in_final = [k["id"] for k in data["kapitel"] if k["council"]["verdikt_neu"] == "FINAL" and k["council"]["heat_flag"] == "Miss"]

meta["aggregate_neu"] = {
    "final": final_n,
    "nicht_final": nicht_final_n,
    "final_ids": final_ids,
    "kern_gesamt_avg": round(sum(k["council"]["kern_gesamt"] for k in data["kapitel"]) / n, 2),
    "heat_match_avg": round(sum(k["council"]["heat_match"] for k in data["kapitel"]) / n, 2),
    "heat_flags": {"OK": heat_ok, "Knapp": heat_knapp, "Miss": heat_miss},
    "final_mit_heat_miss": heat_miss_in_final,
}

fp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Retrofit OK: {n} Kapitel.")
print(f"  Kern Ø: {meta['aggregate_neu']['kern_gesamt_avg']}")
print(f"  Heat-Match Ø: {meta['aggregate_neu']['heat_match_avg']}")
print(f"  FINAL: {final_n}  NICHT-FINAL: {nicht_final_n}")
print(f"  Heat-Flags: OK={heat_ok}  Knapp={heat_knapp}  Miss={heat_miss}")
if heat_miss_in_final:
    print(f"  Hinweis: FINAL mit Heat-Miss → {heat_miss_in_final}")
