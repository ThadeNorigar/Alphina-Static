#!/usr/bin/env python3
"""
Antislop-Check fuer Belletristik-Prosa.

Pattern-Filter (Layer 1) gegen die Top-Verstoesse aus
buch/_autor-feedback-katalog.md. Laeuft als Pre-Filter vor
jeder Block-Akzeptanz in der /ausarbeitung-Pipeline.

Usage:
    python scripts/antislop-check.py <text-file>
    python scripts/antislop-check.py - (read from stdin)

Exit codes:
    0 — Block ist sauber (alle Layer-1-Filter bestanden)
    1 — Block hat Pattern-Verstoesse, Output zeigt Findings

Pattern sind in priorisierte Kategorien strukturiert:
    PFLICHT — harte Verstoesse, immer ablehnen
    TIC     — Frequenz-/Tic-Schwellen, ablehnen wenn ueberschritten
    STIL    — Hinweise, nur Warnung
"""

import argparse
import re
import sys
from collections import Counter
from dataclasses import dataclass, field


@dataclass
class Finding:
    pattern_name: str
    category: str  # PFLICHT / TIC / STIL
    line: int
    matched_text: str
    context: str
    why: str


@dataclass
class CheckResult:
    findings: list = field(default_factory=list)
    word_count: int = 0

    def has_pflicht(self) -> bool:
        return any(f.category == "PFLICHT" for f in self.findings)

    def has_tic(self) -> bool:
        return any(f.category == "TIC" for f in self.findings)

    def passes(self) -> bool:
        return not self.has_pflicht() and not self.has_tic()


# ============================================================
# PATTERN DEFINITIONS
# ============================================================

# PFLICHT — immer ablehnen wenn Match
PFLICHT_PATTERNS = {
    "antithese_nicht_sondern": (
        re.compile(r"\bnicht\s+\w[^,.!?]{0,80}\s*(?:—|–|-|,)\s*sondern\s+", re.IGNORECASE),
        "Antithese 'nicht X, sondern Y' — Pflicht-Pruefung pro Einsatz, Default streichen",
    ),
    "antithese_nicht_kein_dash": (
        re.compile(r"\b(?:Nicht|Kein[er]?)\s+\w[^,.!?]{0,60}\s*(?:—|–)\s*\w", re.IGNORECASE),
        "Antithese-Variante 'Nicht/Kein X — Y' (Dash-Antithese)",
    ),
    "halb_x_pseudo": (
        # Generisch: 'halb' + beliebiges Substantiv. Ausnahmen: 'halb so', 'halb fuer sich' (Dialog), 'halbe Stunde' (Termin), Komposita ohne Trennung
        re.compile(r"\b(?:halbe[rsn]?|halb)\s+(?!so\b|fuer\b|für\b)[A-ZÄÖÜ][a-zäöüß]{3,}", re.UNICODE),
        "'halb X'-Pseudo-Praezision (Tic) — Default streichen, Alternativen: kurz/knapp/einen Augenblick",
    ),
    "etwas_in_koerperteil": (
        re.compile(r"\betwas\s+in\s+(?:sein|ihr|seinem|ihrem|seiner|ihrer)[a-z]*\s+(?:Brust|Nacken|Sehen|Brustkorb|R[üu]cken|Hals|Kopf|Bauch|Magen|Kehle)", re.IGNORECASE),
        "'etwas in X'-Konstruktion (Erzaehler-Glosse) — verboten",
    ),
    "anglizismus_modern": (
        re.compile(r"\b(?:scannte|scannen|scant|gescannt|gescheckt|gecheckt|setup|debug(?:gen|ging|ged)?|drift(?:en|ete)?|chargen?|fix[ed]?|cool|okay|gefixt|gefakt)\b", re.IGNORECASE),
        "Anglizismus / Epoche-Bruch — frueh-19.-Jhd Register",
    ),
    "metrische_masse": (
        re.compile(r"\b(?:Millimeter|Zentimeter|\d+\s*[kmd]?[mM]\b|Kilometer)\b"),
        "Metrische Masseinheit (Anglizismus, Epoche-Bruch)",
    ),
    "realwelt_monat": (
        re.compile(r"\b(?:Januar|Februar|M[äa]rz|April|Mai|Juni|Juli|August|September|Oktober|November|Dezember|M[äa]rzlicht|M[äa]rzwind|M[äa]rzregen|M[äa]rzluft|Augustnachmittag|Maitag|Junimorgen)\b"),
        "Realwelt-Monatsname — verboten, nur Welt-Monate (Eismond, Sturmmond, etc.)",
    ),
    "resonanz_in_prosa": (
        re.compile(r"\b(?:Resonanz|Resonanzen|Resonanzfeld|Resonanzpuls)\b"),
        "'Resonanz' in Prosa — Canon-Begriff, Figuren kennen ihn nicht",
    ),
    "schemen_in_prosa": (
        re.compile(r"\b(?:Schemen|Schemens|Schemen-)\b"),
        "'Schemen' in Prosa — Canon-Begriff, Figuren benennen es konkret (das Wesen)",
    ),
    "puls_abstrakt": (
        re.compile(r"\b(?:der|sein|ihr|ein)\s+Puls\b|\bPulsschlag\b"),
        "'Puls' als abstraktes Substantiv — Klischee. Konkrete Koerperstelle (Halsschlagader/Handgelenk/Kehle) oder konkretes Verb (pochen/schlagen)",
    ),
    "denk_tag": (
        re.compile(r"(?:dachte|fragte sich|ueberlegte|überlegte)\s*[,.]", re.IGNORECASE),
        "Denk-Tag ('sie dachte', 'er fragte sich') — verboten, erlebte Rede ist Default",
    ),
}

# TIC — Schwellen-basiert (Frequenz im Block)
TIC_PATTERNS = {
    "sein_verb_cluster": (
        re.compile(r"\b(?:lag|lagen|war|waren|stand|standen|sa[ßs]|sa[ßs]en)\b", re.IGNORECASE),
        3,  # Schwelle: mehr als 3 Treffer auf 200W = Tic
        "Default-Sein-Verb-Cluster (lag/war/stand/sass) — pro 200W max 3, Wenn ueberschritten: praezisere Verben einsetzen",
    ),
    "negation_cluster": (
        re.compile(r"\b(?:nicht|nichts|kein[er]?[srm]?[ne]?)\b", re.IGNORECASE),
        15,  # Schwelle: mehr als 15 pro 1000W = Tic
        "Negations-Cluster — max 15 pro 1000W. Pro Negation pruefen ob positiv umformulierbar.",
    ),
    "hypothetische": (
        re.compile(r"\bals\s+(?:h[äa]tte|w[äa]re|k[öo]nnte|w[üu]rde|h[äa]ttest|w[äa]rst)\b", re.IGNORECASE),
        2,  # Schwelle: mehr als 2 pro Block
        "'als haette/waere/koennte' Hypothetische — max 2 pro Block, sonst Default-Anschluss-Tic",
    ),
}

# Substantiv-Phrasen ohne Verb (heuristisch)
# Erkenne kurze Saetze, die mit Komma-getrennten Substantiv-Adjektiv-Ketten enden
def detect_substantiv_phrase_ohne_verb(text: str) -> list:
    """Findet Saetze, die wie 'X. Y, Z, A.' aussehen — also Aufzaehlungen ohne Verb."""
    findings = []
    # Markdown-Header / Frontmatter / italics-Date entfernen vor Analyse
    text_clean = re.sub(r"^#{1,6}\s+.+$", "", text, flags=re.MULTILINE)
    text_clean = re.sub(r"^\*[^*]+\*$", "", text_clean, flags=re.MULTILINE)
    text_clean = re.sub(r"^---.*?---\s*", "", text_clean, flags=re.DOTALL)
    # Saetze mit Komma-Aufzaehlung von Substantiv-Phrasen, ohne sichtbares Verb
    # Heuristik: Satz enthaelt mind. 2 Kommas + endet auf Punkt + keine Verb-Form sichtbar
    sentences = re.split(r"(?<=[.!?])\s+", text_clean)
    # Verb-Detektor: schwache Endungen + haeufige starke/unregelmaessige Verben
    verb_forms = re.compile(
        r"\b(?:"
        # Schwache Endungen
        r"[a-zäöüß]+(?:te|ten|t[en]?|en|st|e|et)|"
        # Hilfsverben
        r"war|sind|ist|waren|hat|hatten?|wird|werden|wurde[ns]?|"
        r"kann|konnten?|muss|mussten?|soll|sollten?|darf|durften?|mag|mochten?|"
        # Haeufige starke/unregelmaessige Verben Praeteritum
        r"rief|riefen|fiel|fielen|kam|kamen|ging|gingen|sah|sahen|las|lasen|"
        r"trug|trugen|fand|fanden|stand|standen|zog|zogen|hieb|hielten?|"
        r"hob|hoben|schob|schoben|riss|rissen|stieß|stießen|drueckte|drueckten|drückte|drückten|"
        r"trat|traten|wich|wichen|blieb|blieben|ließ|liessen|liefen?|lief|"
        r"saß|saßen|lag|lagen|hielt|hielten|nahm|nahmen|gab|gaben|"
        r"sprach|sprachen|schrie|schrien|trat|traten|flog|flogen|"
        r"warf|warfen|fing|fingen|brach|brachen|riss|rissen|stieß|stießen|"
        r"schlug|schlugen|wuchs|wuchsen|sank|sanken|schien|schienen|"
        r"verstand|verstanden|begann|begannen|erkannte|erkannten|"
        # Modal-Praeteritum
        r"konnte|konnten|musste|mussten|sollte|sollten|durfte|durften|wollte|wollten|"
        # Praesens haeufig
        r"sieht|geht|kommt|nimmt|gibt|liegt|steht|haelt|hält|"
        r"trifft|spricht|laeuft|läuft|faellt|fällt|"
        r"draengte|drängte|draengten|drängten"
        r")\b",
        re.IGNORECASE
    )

    for sent in sentences:
        sent_clean = sent.strip()
        if not sent_clean or len(sent_clean.split()) < 2:
            continue
        # Ignoriere Dialog (in Anfuehrungszeichen)
        if sent_clean.startswith('»') or sent_clean.startswith('„'):
            continue
        words = sent_clean.split()
        commas = sent_clean.count(",")
        # Heuristik 1: 2+ Kommas + max 12 Worte ohne Verb
        # Heuristik 2: 1+ Komma + max 8 Worte ohne Verb (kurze Adjektiv-Substantiv-Kette)
        # Heuristik 3: kein Komma + max 5 Worte ohne Verb (Substantiv-Phrase als ganzer Satz)
        if commas >= 2 and len(words) <= 12 and not verb_forms.search(sent_clean):
            findings.append(sent_clean)
        elif commas == 1 and len(words) <= 8 and not verb_forms.search(sent_clean):
            findings.append(sent_clean)
        elif commas == 0 and len(words) <= 5 and not verb_forms.search(sent_clean):
            findings.append(sent_clean)
    return findings


# Anaphern-Kaskade: 3+ aufeinanderfolgende Saetze mit gleichem Anfangswort
def detect_anaphern(text: str) -> list:
    findings = []
    sentences = re.split(r"(?<=[.!?])\s+", text)
    if len(sentences) < 3:
        return findings
    for i in range(len(sentences) - 2):
        words = []
        for j in range(3):
            sent = sentences[i + j].strip()
            if not sent:
                break
            first_word = sent.split()[0] if sent.split() else ""
            # Strip Quotes
            first_word = re.sub(r'^[„»"]', "", first_word)
            words.append(first_word.lower())
        if len(words) == 3 and words[0] == words[1] == words[2] and words[0]:
            findings.append(f"3x '{words[0]}' Anfang: {' / '.join(s.strip()[:50] for s in sentences[i:i+3])}")
    return findings


# Verb-Wiederholung im Block
def detect_verb_wiederholung(text: str) -> list:
    """Findet Verben, die mehr als 2x im Block vorkommen (Verb-Tic)."""
    findings = []
    # Sehr grobe Heuristik: extrahiere alle Verb-Endungen-Worte
    common_verbs = re.findall(r"\b([a-zäöüß]{3,12}(?:te|ten|t|en))\b", text.lower())
    counter = Counter(common_verbs)
    # Filter: ignoriere bestimmte Allerweltsworte + Eigennamen + Funktionsworte
    skip = {
        # Hilfsverben
        "war", "waren", "hat", "hatten", "ist", "sind", "wird", "werden",
        # Konjunktionen / Praepositionen
        "und", "oder", "aber", "wenn", "dann", "noch", "auch", "wie", "als",
        # Determinatoren
        "den", "dem", "des", "ein", "einen", "eine", "einer", "eines",
        # Pronomen
        "sie", "ihn", "ihm", "ihr", "ihre", "ihrem", "ihren", "ihres",
        "sein", "seine", "seinem", "seinen", "seines",
        # Adverbien
        "fast", "halb", "ganz", "etwa", "kurz", "lang", "noch", "schon", "doch",
        "mehr", "weniger", "wieder", "immer", "nie", "nun",
        # Negationen (werden separat geprueft)
        "nicht", "nichts", "kein", "keine", "keiner",
        # Hafen-/Werft-Eigennamen / Welt-Vokabular
        "maren", "alphina", "sorel", "vesper", "runa", "tohl", "varen", "tarn",
        "joran", "henrik", "halvard", "lene", "haron", "esther", "jara", "elke", "keldan", "kesper",
        "vael", "moragh", "thalassien", "grauwe", "nebelmond", "glutmond", "lichtmond", "saatmond",
        "speicher", "werft", "hafen", "kai", "schritt", "schritte", "boote", "boot", "stein",
        "wesen", "tuer", "tuere", "tag", "tage", "stunde", "stunden", "minute", "minuten",
        "hand", "haende", "fuss", "fuesse", "augen", "auge", "kopf", "bein", "bein",
    }
    for verb, count in counter.most_common(8):
        if count > 2 and verb not in skip and len(verb) >= 5:
            findings.append(f"'{verb}' kommt {count}x vor")
    return findings


# ============================================================
# CHECK FUNCTIONS
# ============================================================

def get_context(text: str, match_start: int, match_end: int, ctx_chars: int = 50) -> str:
    start = max(0, match_start - ctx_chars)
    end = min(len(text), match_end + ctx_chars)
    return text[start:end].replace("\n", " ")


def get_line_number(text: str, pos: int) -> int:
    return text[:pos].count("\n") + 1


def check_pflicht(text: str, result: CheckResult) -> None:
    for name, (pattern, why) in PFLICHT_PATTERNS.items():
        for match in pattern.finditer(text):
            ctx = get_context(text, match.start(), match.end())
            line = get_line_number(text, match.start())
            result.findings.append(Finding(
                pattern_name=name,
                category="PFLICHT",
                line=line,
                matched_text=match.group(0),
                context=ctx,
                why=why,
            ))


def check_tic(text: str, result: CheckResult, word_count: int) -> None:
    for name, (pattern, base_threshold, why) in TIC_PATTERNS.items():
        matches = list(pattern.finditer(text))
        # Schwelle skalieren je nach Pattern-Typ
        if name == "negation_cluster":
            threshold_for_block = max(1, base_threshold * word_count // 1000)
        elif name == "sein_verb_cluster":
            threshold_for_block = max(1, base_threshold * word_count // 200)
        else:
            threshold_for_block = base_threshold

        if len(matches) > threshold_for_block:
            # Erste 3 Treffer als Beispiele
            samples = []
            for match in matches[:3]:
                samples.append(match.group(0))
            result.findings.append(Finding(
                pattern_name=name,
                category="TIC",
                line=0,
                matched_text=f"{len(matches)}x (Schwelle {threshold_for_block}): " + ", ".join(samples),
                context=f"{len(matches)} Treffer in {word_count}W (Block-Limit {threshold_for_block})",
                why=why,
            ))


def check_substantiv_phrasen(text: str, result: CheckResult) -> None:
    findings = detect_substantiv_phrase_ohne_verb(text)
    for f in findings:
        result.findings.append(Finding(
            pattern_name="substantiv_phrase_ohne_verb",
            category="PFLICHT",
            line=0,
            matched_text=f[:80],
            context=f,
            why="Substantiv-Phrasen-Kette ohne Verb — Stakkato (Pattern #1)",
        ))


def check_anaphern(text: str, result: CheckResult) -> None:
    findings = detect_anaphern(text)
    for f in findings:
        result.findings.append(Finding(
            pattern_name="anaphern_kaskade",
            category="TIC",
            line=0,
            matched_text=f[:120],
            context=f,
            why="Anaphern-Kaskade 3+ Saetze mit gleichem Anfang",
        ))


def check_verb_wiederholung(text: str, result: CheckResult) -> None:
    findings = detect_verb_wiederholung(text)
    for f in findings:
        result.findings.append(Finding(
            pattern_name="verb_wiederholung",
            category="STIL",
            line=0,
            matched_text=f,
            context=f,
            why="Verb-Wiederholung >2x im Block — Verb-Praezision pruefen",
        ))


# ============================================================
# MAIN
# ============================================================

def run_checks(text: str) -> CheckResult:
    result = CheckResult()
    result.word_count = len(text.split())

    check_pflicht(text, result)
    check_tic(text, result, result.word_count)
    check_substantiv_phrasen(text, result)
    check_anaphern(text, result)
    check_verb_wiederholung(text, result)

    return result


def format_output(result: CheckResult, source: str = "") -> str:
    lines = []
    lines.append(f"=== Antislop-Check ({source or 'stdin'}) ===")
    lines.append(f"Wortzahl: {result.word_count}")
    lines.append(f"Findings: {len(result.findings)}")
    lines.append("")

    by_cat = {"PFLICHT": [], "TIC": [], "STIL": []}
    for f in result.findings:
        by_cat[f.category].append(f)

    for cat in ("PFLICHT", "TIC", "STIL"):
        if not by_cat[cat]:
            continue
        lines.append(f"--- {cat} ({len(by_cat[cat])}) ---")
        for f in by_cat[cat]:
            lines.append(f"  [{f.pattern_name}] L{f.line}: {f.matched_text}")
            lines.append(f"    Kontext: ...{f.context}...")
            lines.append(f"    -> {f.why}")
            lines.append("")

    if result.passes():
        lines.append("VERDIKT: BESTANDEN (Layer 1)")
    elif result.has_pflicht():
        lines.append("VERDIKT: NICHT BESTANDEN (PFLICHT-Verstoesse)")
    else:
        lines.append("VERDIKT: GRENZWERTIG (TIC-Schwellen ueberschritten)")

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Antislop-Check fuer Belletristik-Prosa")
    parser.add_argument("file", help="Pfad zur Text-Datei oder '-' fuer stdin")
    parser.add_argument("--quiet", action="store_true", help="Nur Exit-Code, kein Output")
    args = parser.parse_args()

    if args.file == "-":
        text = sys.stdin.read()
        source = "stdin"
    else:
        with open(args.file, "r", encoding="utf-8") as f:
            text = f.read()
        source = args.file

    result = run_checks(text)

    if not args.quiet:
        print(format_output(result, source))

    if result.has_pflicht():
        return 2
    if result.has_tic():
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
