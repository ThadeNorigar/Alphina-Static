#!/usr/bin/env python3
"""
Ersetzt ae/oe/ue/ss-Substitute durch echte Umlaute und ß in Kanon-Dateien.

Sicher: arbeitet mit einer Whitelist aus echten deutschen Wörtern — Substrings
in Fremdwörtern wie 'Europa', 'Ouvertüre', 'Bauen' werden nicht getroffen.

Aufruf:
  python scripts/fix-umlaute.py           # dry-run (zeigt was sich ändern würde)
  python scripts/fix-umlaute.py --apply   # schreibt tatsächlich
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Zieldateien: JSON + MD, aber keine Code-Dateien
TARGETS = [
    ROOT / "buch" / "zeitleiste.json",
    ROOT / "buch" / "status.json",
    ROOT / "scripts" / "build-zeitleiste.py",
    ROOT / "buch" / "zeitleiste.OLD.json",
]

# Whitelist: kleingeschrieben oder großgeschrieben, Wortgrenzen mit \b
# Kleinschreibung → ersetze in beiden Casings (match-case preserve).
WORDS = {
    # ae -> ä
    "aeltest": "ältest", "aelteste": "älteste", "aeltesten": "ältesten",
    "aendert": "ändert", "aenderung": "änderung",
    "aergert": "ärgert", "aerger": "ärger",
    "haende": "hände", "haenden": "händen",
    "maedchen": "mädchen",
    "maechtig": "mächtig",
    "naechst": "nächst", "naechsten": "nächsten", "naechste": "nächste",
    "naeh": "näh", "naehe": "nähe",
    "naemlich": "nämlich",
    "spaet": "spät", "spaeter": "später",
    "staerker": "stärker", "staerke": "stärke", "staerkste": "stärkste",
    "staendig": "ständig",
    "truebe": "trübe", "trueber": "trüber",
    "waere": "wäre", "waeren": "wären",
    "waehlen": "wählen", "waehlt": "wählt",
    "waeg": "wäg", "waege": "wäge",
    "waermt": "wärmt", "waerme": "wärme", "waermer": "wärmer",
    "erwaehnt": "erwähnt", "erwaehnung": "erwähnung",
    "gespraech": "gespräch", "gespraeche": "gespräche", "gespraeches": "gespräches",
    "wuetend": "wütend",
    "toetet": "tötet", "toeten": "töten",
    "oeffnet": "öffnet", "oeffnen": "öffnen", "oeffnung": "öffnung",
    "zerstoert": "zerstört", "zerstoerung": "zerstörung",
    "haeufig": "häufig", "haeufiger": "häufiger",
    "traege": "träge",
    "taeglich": "täglich",
    "haendler": "händler",
    "eraeugen": "eräugen",
    # oe -> ö
    "koennen": "können", "koenne": "könne", "koennte": "könnte", "koennten": "könnten",
    "oeffentlich": "öffentlich",
    "moeglich": "möglich", "moechte": "möchte", "moegen": "mögen", "moege": "möge",
    "hoert": "hört", "hoeren": "hören", "hoere": "höre", "hoerte": "hörte",
    "loesung": "lösung", "loest": "löst", "loesen": "lösen",
    "roeten": "röten", "roete": "röte",
    "stoerung": "störung", "stoert": "stört",
    "schoen": "schön", "schoene": "schöne", "schoener": "schöner",
    "goetter": "götter", "goettin": "göttin",
    "floete": "flöte",
    # ue -> ü
    "fuer": "für", "fuers": "fürs",
    "ueber": "über", "ueberall": "überall",
    "muessen": "müssen", "muesse": "müsse", "muesste": "müsste",
    "rueck": "rück", "rueckkehr": "rückkehr", "rueckzug": "rückzug",
    "rueckwaerts": "rückwärts",
    "uebersetzt": "übersetzt", "uebersetzen": "übersetzen", "uebersetzung": "übersetzung",
    "uebergangs": "übergangs", "uebergang": "übergang",
    "ueberpruef": "überpruf", "ueberprueft": "überprüft",
    "ueberraschend": "überraschend", "ueberraschung": "überraschung",
    "bruecke": "brücke", "bruecken": "brücken",
    "gluehen": "glühen", "glueht": "glüht", "gluehte": "glühte", "gluehend": "glühend",
    "gefuehl": "gefühl", "gefuehle": "gefühle",
    "fuehlen": "fühlen", "fuehlt": "fühlt", "fuehlte": "fühlte",
    "fuehren": "führen", "fuehrt": "führt", "fuehrte": "führte", "gefuehrt": "geführt",
    "huebsch": "hübsch",
    "kuehl": "kühl", "kuehlt": "kühlt",
    "ruecksicht": "rücksicht",
    "tuer": "tür", "tueren": "türen",
    "spueren": "spüren", "spuert": "spürt", "spuerte": "spürte",
    "gruende": "gründe", "grund": "grund", "gruendet": "gründet",
    "ruecken": "rücken",
    "pruefen": "prüfen", "prueft": "prüft",
    "muede": "müde", "muedigkeit": "müdigkeit",
    "uebt": "übt", "ueben": "üben",
    "kuenstler": "künstler", "kuenstlich": "künstlich",
    "wuerde": "würde", "wuerden": "würden",
    "buerger": "bürger", "buergerlich": "bürgerlich",
    "puenktlich": "pünktlich",
    "fuenf": "fünf", "fuenfzig": "fünfzig", "fuenfte": "fünfte",
    "truebe": "trübe",
    "duenn": "dünn", "duenne": "dünne",
    "gruen": "grün", "gruene": "grüne", "gruener": "grüner",
    "gruendlich": "gründlich",
    "ruecksprache": "rücksprache",
    "nuetzlich": "nützlich",
    "fluestert": "flüstert", "fluestern": "flüstern", "fluesterte": "flüsterte",
    "fluegel": "flügel",
    "schluessel": "schlüssel",
    "enthuellung": "enthüllung", "enthuellt": "enthüllt", "enthuellen": "enthüllen",
    "huelle": "hülle",
    "buehne": "bühne",
    "sueden": "süden", "suedlich": "südlich",
    "ruestung": "rüstung",
    "stroemen": "strömen", "stroemt": "strömt",  # oe
    "fuenfte": "fünfte",
    "selbstueberschaetzung": "selbstüberschätzung",
    "selbstueber": "selbstüber",
    # ss -> ß (vorsichtig: nur bei bekannten Wörtern, NICHT bei Neuschreibung wie "dass", "Fluss")
    "weiss": "weiß", "weisst": "weißt", "weissen": "weißen", "weisse": "weiße", "weisser": "weißer",
    "strasse": "straße", "strassen": "straßen",
    "fluesse": "flüsse",
    "grusz": "gruß",
    "blosz": "bloß",
    "gross": "groß", "grosse": "große", "grosser": "großer", "grosses": "großes", "groessere": "größere", "groesser": "größer", "groessten": "größten", "grossen": "großen",
    "fliessen": "fließen", "fliesst": "fließt", "floss": "floss",
    "heiss": "heiß", "heisst": "heißt", "heisse": "heiße",
    "aussen": "außen", "draussen": "draußen",
    # Nachtraege
    "koerper": "körper", "koerperlich": "körperlich", "koerpers": "körpers",
    "luegt": "lügt", "luegen": "lügen", "lueg": "lüg",
    "aufhoeren": "aufhören", "aufhoert": "aufhört",
    "beilaeufig": "beiläufig", "beilaeufiges": "beiläufiges", "beilaeufigen": "beiläufigen",
    "zukuenftig": "zukünftig", "zukuenftige": "zukünftige", "zukuenftiges": "zukünftiges", "zukuenftigen": "zukünftigen",
    "fuehlsam": "fühlsam",
    "ankuendig": "ankündig", "ankuendigt": "ankündigt", "ankuendigung": "ankündigung",
    "hueft": "hüft", "huefte": "hüfte", "hueften": "hüften",
    "ruecklings": "rücklings",
    "juenger": "jünger", "juengere": "jüngere", "juengst": "jüngst",
    "stoesst": "stößt", "stossen": "stoßen",
    "prueft": "prüft", "geprueft": "geprüft",
    "ruehrt": "rührt", "ruehren": "rühren", "ruehrung": "rührung",
    "huellt": "hüllt", "verhuellen": "verhüllen", "enthuellen": "enthüllen",
    "ungeduld": "ungeduld",  # kein Umlaut
    "muendlich": "mündlich", "muendung": "mündung",
    "uebung": "übung", "uebungen": "übungen",
    "ueblich": "üblich", "ueblicherweise": "üblicherweise",
    "uebrig": "übrig", "uebrigens": "übrigens",
    "fluegel": "flügel", "fluegelschlag": "flügelschlag",
    "buecher": "bücher",
    "verruecken": "verrücken", "verrueckt": "verrückt",
    "stueck": "stück", "stuecke": "stücke", "stuecken": "stücken",
    "zuegel": "zügel", "zueugel": "zügel",
    "buend": "bünd", "buendig": "bündig", "buendel": "bündel", "buendelt": "bündelt",
    "zwei": "zwei", "zweifel": "zweifel",  # kein Umlaut
    # extra oe
    "moerder": "mörder", "moerdern": "mördern",
    "foerder": "förder", "foerdert": "fördert",
    "toedlich": "tödlich",
    "groesseren": "größeren", "groesseres": "größeres", "grosses": "großes",
    "verstoert": "verstört", "verstoerung": "verstörung",
    "stoert": "stört",
    "goetterbote": "götterbote",
    # ß statt ss Zusatz
    "grossmutter": "großmutter", "grossvater": "großvater",
    "strassenrand": "straßenrand",
}


def preserve_case(match: str, replacement: str) -> str:
    """Übernimmt Case des Matches (Haende -> Hände, haende -> hände, HAENDE -> HÄNDE)."""
    if match.isupper():
        return replacement.upper()
    if match[0].isupper():
        return replacement[0].upper() + replacement[1:]
    return replacement


def build_pattern(wordlist: dict[str, str]) -> re.Pattern[str]:
    # Sortiert nach Länge absteigend, damit 'aelteste' vor 'aelt' greift
    keys = sorted(wordlist.keys(), key=lambda k: -len(k))
    # Wort-Grenze am Anfang, Wort-Fortsetzung erlaubt am Ende
    # (so dass 'fuer' in 'fueren' NICHT greift, aber 'koennen' in 'koennte' nicht doppelt)
    # Wir matchen das ganze Wort-Muster + optionale Endung? Nein — wir matchen nur den Stamm
    # und überlassen den Rest. Aber dann "fuer" matcht in "fuere" — bad.
    # Safer: \bWORD(?=\W|$) — also nur wenn das Muster eine Wortgrenze danach hat.
    # Das heißt wir müssen alle Wortformen listen. Das habe ich oben gemacht.
    # Wortgrenzen: ascii-sicher.
    pat = r"\b(" + "|".join(re.escape(k) for k in keys) + r")\b"
    return re.compile(pat, re.IGNORECASE)


def fix_text(text: str, pattern: re.Pattern[str], wordlist: dict[str, str]) -> tuple[str, list[tuple[str, str]]]:
    changes: list[tuple[str, str]] = []

    def repl(m: re.Match[str]) -> str:
        matched = m.group(0)
        lower_key = matched.lower()
        if lower_key not in wordlist:
            return matched
        new = preserve_case(matched, wordlist[lower_key])
        if new != matched:
            changes.append((matched, new))
        return new

    new_text = pattern.sub(repl, text)
    return new_text, changes


def main() -> int:
    apply = "--apply" in sys.argv
    pattern = build_pattern(WORDS)

    total_changes = 0
    for path in TARGETS:
        if not path.exists():
            print(f"  (fehlt: {path.relative_to(ROOT)})")
            continue
        text = path.read_text(encoding="utf-8")
        new_text, changes = fix_text(text, pattern, WORDS)
        unique = {}
        for a, b in changes:
            unique.setdefault(a, b)
        print(f"\n{path.relative_to(ROOT)}: {len(changes)} Ersetzungen ({len(unique)} unique)")
        for a, b in sorted(unique.items()):
            print(f"  {a!r:30} -> {b!r}")
        total_changes += len(changes)

        if apply and new_text != text:
            path.write_text(new_text, encoding="utf-8")
            print(f"  (geschrieben)")

    print(f"\nGesamt: {total_changes} Ersetzungen")
    if not apply:
        print("Dry-run. Für tatsächliches Schreiben: --apply")
    return 0


if __name__ == "__main__":
    sys.exit(main())
