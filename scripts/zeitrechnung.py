#!/usr/bin/env python3
"""
zeitrechnung.py — Konverter zwischen UZ, TZ (Thalassien) und MZ (Moragh).

Canon (buch/zeitleiste.json.meta.zeitrechnung):

  TZ (Thalassien):
    24 h/Tag, 12 Monate/Jahr, 365 Tage/Jahr (Gregorianisch).
    Monate: Eismond=Januar, Sturmmond=Februar, Saatmond=März,
    Grünmond=April, Blütenmond=Mai, Lichtmond=Juni, Glutmond=Juli,
    Erntemond=August, Herbstmond=September, Nebelmond=Oktober,
    Frostmond=November, Dunkelmond=Dezember.
    TZ 0 = Erfindung des Uhrwerks = ~1269 UZ.

  MZ (Moragh):
    26 h/Tag (Eigenrotation).
    8 Tage/Woche (Gor-Umlauf, Roter Mond).
    36 Tage/Monat = 4,5 Wochen (Nyr-Umlauf, Bleicher Mond).
    8 Monate/Jahr = 288 Tage (Orbit um das "Auge").
    Doppelflut alle 72 Tage.
    Monate:
      1 Torash  (Bogenwende,   Licht)
      2 Ashral  (Glutzeit,     Licht)
      3 Keldath (Doppelflut,   Licht)
      4 Reshvan (Ernteschluss, Licht)
      5 Dravon  (Dämmerfall,   Dunkel)
      6 Gormath (Rotmond,      Dunkel)
      7 Nyrath  (Bleichmond,   Dunkel)
      8 Shelkam (Tiefnacht,    Dunkel)
    MZ 0 = Besiedelung Moragh = TZ-Jahr -1.453.449 (absoluter Nullpunkt).

  Kopplung (Canon, User-bestätigt 2026-05-05):
    1 MZ-Monat = 33 TZ-Jahre.
    1 MZ-Jahr  = 264 TZ-Jahre (8 Monate × 33).
    (Frühere 400er-Faustregel stammte aus 12-Monats-Kalender und ist überholt.)
    Umrechnung erfolgt auf Jahresebene mit Bruchteilen.

  Anker:
    21. Saatmond 551 TZ = 21. März 1820 UZ = 1. Torash 3635 MZ (B1-Start).
    Ganz Buch 1 spielt in MZ 3635, Monat 1 (Torash), Tag 1.

Usage:
    python scripts/zeitrechnung.py uz 2026-04-22
    python scripts/zeitrechnung.py tz "22. Blütenmond 551"
    python scripts/zeitrechnung.py mz "14. Dravon 3635"
    python scripts/zeitrechnung.py tz 551-5-22
"""

from __future__ import annotations
import argparse
import datetime as _dt
import io
import re
import sys

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

# --- TZ-Canon (Gregorianisch + thalassische Monatsnamen) -----------------

TZ_MONATE = [
    "Eismond", "Sturmmond", "Saatmond", "Grünmond",
    "Blütenmond", "Lichtmond", "Glutmond", "Erntemond",
    "Herbstmond", "Nebelmond", "Frostmond", "Dunkelmond",
]
TZ_MONATE_LOWER = {m.lower(): i + 1 for i, m in enumerate(TZ_MONATE)}
for _m, _i in list(TZ_MONATE_LOWER.items()):
    _alt = _m.replace("ü", "ue").replace("ö", "oe").replace("ä", "ae")
    if _alt != _m:
        TZ_MONATE_LOWER[_alt] = _i

# TZ-Jahr ↔ UZ-Jahr: Jahresoffset
TZ_UZ_OFFSET = 1269  # TZ 0 = UZ ~1269

# --- MZ-Canon ------------------------------------------------------------

MZ_MONATE = [
    ("Torash",  "Bogenwende",   "Licht"),
    ("Ashral",  "Glutzeit",     "Licht"),
    ("Keldath", "Doppelflut",   "Licht"),
    ("Reshvan", "Ernteschluss", "Licht"),
    ("Dravon",  "Dämmerfall",   "Dunkel"),
    ("Gormath", "Rotmond",      "Dunkel"),
    ("Nyrath",  "Bleichmond",   "Dunkel"),
    ("Shelkam", "Tiefnacht",    "Dunkel"),
]
MZ_MONATE_LOWER = {m[0].lower(): i + 1 for i, m in enumerate(MZ_MONATE)}
for _m, _i in list(MZ_MONATE_LOWER.items()):
    _alt = _m.replace("ä", "ae")
    if _alt != _m:
        MZ_MONATE_LOWER[_alt] = _i

MZ_STUNDEN_PRO_TAG = 26
MZ_TAGE_PRO_WOCHE = 8
MZ_TAGE_PRO_MONAT = 36
MZ_MONATE_PRO_JAHR = 8
MZ_TAGE_PRO_JAHR = MZ_TAGE_PRO_MONAT * MZ_MONATE_PRO_JAHR  # 288

# --- Kopplung TZ ↔ MZ ----------------------------------------------------

# Canon (User-bestaetigt 2026-05-05):
# 1 MZ-Monat = 33 TZ-Jahre. Bei 8 MZ-Monaten/MZ-Jahr ergibt sich:
# 1 MZ-Jahr = 264 TZ-Jahre.
# (Aelterer Wert "1 MZ-Jahr = 400 TZ-Jahre" stammt aus 12-Monats-Kalender —
# der Kalender ist auf 8 Monate reduziert worden, das Verhaeltnis 33:1 ist
# die kanonisch gefuehrte Plot-Konversion und gewinnt.)
TZ_JAHRE_PRO_MZ_MONAT = 33
TZ_JAHRE_PRO_MZ_JAHR = TZ_JAHRE_PRO_MZ_MONAT * MZ_MONATE_PRO_JAHR  # 264

# Anker: B1-Start = 21. Saatmond 551 TZ = 1. Torash 3635 MZ
# Daraus folgt: MZ_0 in TZ-Jahren =
#   551.21858 - 3635.00055 * 264 = -959'439.79
# (im Vergleich zum frueheren -1.453.449 mit 400er Faktor).
_B1_TZ_FLOAT_FIX = 551 + (
    (_dt.date(551 + 1269, 3, 21) - _dt.date(551 + 1269, 1, 1)).days
) / 365.0
_B1_MZ_FLOAT_FIX = 3635 + (
    0 * 36 + 0 + 4 / 26
) / (8 * 36)  # 1. Torash 3635, 04h
MZ_NULL_IN_TZ_JAHR = _B1_TZ_FLOAT_FIX - _B1_MZ_FLOAT_FIX * TZ_JAHRE_PRO_MZ_JAHR

# --- UZ ↔ TZ (Gregorianisch) ---------------------------------------------

def uz_zu_tz_datum(dt: _dt.datetime) -> tuple[int, int, int, int, int]:
    """UZ-datetime -> (TZ-Jahr, Monat 1-12, Tag, Stunde, Minute)."""
    return (dt.year - TZ_UZ_OFFSET, dt.month, dt.day, dt.hour, dt.minute)

def tz_zu_uz_datum(jahr: int, monat: int, tag: int, stunde: int = 0, minute: int = 0) -> _dt.datetime:
    """TZ-Datum -> UZ-datetime (Gregorianisch)."""
    return _dt.datetime(jahr + TZ_UZ_OFFSET, monat, tag, stunde, minute)

# --- TZ: Jahr + Tag-Index --------------------------------------------------

def tz_tag_des_jahres(jahr: int, monat: int, tag: int) -> int:
    """Liefert den 1-basierten Tag im Jahr (Gregorianisch)."""
    return (_dt.date(jahr + TZ_UZ_OFFSET, monat, tag) -
            _dt.date(jahr + TZ_UZ_OFFSET, 1, 1)).days + 1

def tz_jahr_ist_schaltjahr(jahr: int) -> bool:
    y = jahr + TZ_UZ_OFFSET
    return (y % 4 == 0 and y % 100 != 0) or (y % 400 == 0)

def tz_tage_pro_jahr(jahr: int) -> int:
    return 366 if tz_jahr_ist_schaltjahr(jahr) else 365

# --- TZ ↔ MZ (Jahresebene, 400:1) -----------------------------------------

def tz_zu_mz_jahresanteil(tz_jahr: int, monat: int, tag: int, stunde: int = 0) -> float:
    """TZ-Datum -> MZ-Jahr als float (Jahr + Bruchteil innerhalb MZ-Jahr)."""
    tz_jahr_float = tz_jahr + (tz_tag_des_jahres(tz_jahr, monat, tag) - 1) / tz_tage_pro_jahr(tz_jahr)
    tz_jahr_float += stunde / (tz_tage_pro_jahr(tz_jahr) * 24)
    tz_jahre_seit_mz0 = tz_jahr_float - MZ_NULL_IN_TZ_JAHR
    return tz_jahre_seit_mz0 / TZ_JAHRE_PRO_MZ_JAHR

def mz_jahresanteil_zu_datum(mz_jahr_float: float) -> tuple[int, int, int, int]:
    """MZ-Jahr-Float -> (MZ-Jahr, Monat 1-8, Tag 1-36, Stunde 0-25)."""
    jahr = int(mz_jahr_float) if mz_jahr_float >= 0 else int(mz_jahr_float) - (1 if mz_jahr_float != int(mz_jahr_float) else 0)
    rest = mz_jahr_float - jahr  # [0, 1)
    tag_des_jahres_float = rest * MZ_TAGE_PRO_JAHR  # 0-288
    tag_im_jahr = int(tag_des_jahres_float)  # 0-287
    monat_idx, tag_im_monat = divmod(tag_im_jahr, MZ_TAGE_PRO_MONAT)
    stunde_float = (tag_des_jahres_float - tag_im_jahr) * MZ_STUNDEN_PRO_TAG
    stunde = int(stunde_float)
    return jahr, monat_idx + 1, tag_im_monat + 1, stunde

def mz_zu_jahresanteil(jahr: int, monat: int, tag: int, stunde: int = 0) -> float:
    """MZ-Datum -> MZ-Jahr als float."""
    if not (1 <= monat <= MZ_MONATE_PRO_JAHR):
        raise ValueError(f"MZ-Monat muss 1-{MZ_MONATE_PRO_JAHR} sein, war {monat}")
    if not (1 <= tag <= MZ_TAGE_PRO_MONAT):
        raise ValueError(f"MZ-Tag muss 1-{MZ_TAGE_PRO_MONAT} sein, war {tag}")
    if not (0 <= stunde < MZ_STUNDEN_PRO_TAG):
        raise ValueError(f"MZ-Stunde muss 0-{MZ_STUNDEN_PRO_TAG - 1} sein, war {stunde}")
    tag_im_jahr = (monat - 1) * MZ_TAGE_PRO_MONAT + (tag - 1)
    tag_float = tag_im_jahr + stunde / MZ_STUNDEN_PRO_TAG
    rest = tag_float / MZ_TAGE_PRO_JAHR
    return jahr + rest

def mz_zu_tz(mz_jahr_float: float) -> float:
    """MZ-Jahr-Float -> TZ-Jahr-Float (als Jahresbruchteil)."""
    tz_jahre_seit_mz0 = mz_jahr_float * TZ_JAHRE_PRO_MZ_JAHR
    return MZ_NULL_IN_TZ_JAHR + tz_jahre_seit_mz0

def tz_jahr_float_zu_datum(tz_jahr_float: float) -> tuple[int, int, int, int]:
    """TZ-Jahr-Float -> (Jahr, Monat 1-12, Tag, Stunde)."""
    jahr = int(tz_jahr_float) if tz_jahr_float >= 0 else int(tz_jahr_float) - (1 if tz_jahr_float != int(tz_jahr_float) else 0)
    rest = tz_jahr_float - jahr
    tage_im_jahr = tz_tage_pro_jahr(jahr)
    tag_des_jahres_float = rest * tage_im_jahr
    tag_des_jahres = int(tag_des_jahres_float) + 1  # 1-basiert
    stunde = int((tag_des_jahres_float - int(tag_des_jahres_float)) * 24)
    # Konvertiere tag_des_jahres in Monat/Tag via Gregorianisch
    basis = _dt.date(jahr + TZ_UZ_OFFSET, 1, 1)
    datum = basis + _dt.timedelta(days=tag_des_jahres - 1)
    return jahr, datum.month, datum.day, stunde

# --- Parser / Formatter ---------------------------------------------------

def parse_uz(s: str) -> _dt.datetime:
    s = s.strip()
    m = re.match(r"^(\d{4})-(\d{1,2})-(\d{1,2})(?:\s+(\d{1,2}):(\d{2}))?$", s)
    if m:
        y, mo, d = int(m.group(1)), int(m.group(2)), int(m.group(3))
        hh = int(m.group(4)) if m.group(4) else 0
        mm = int(m.group(5)) if m.group(5) else 0
        return _dt.datetime(y, mo, d, hh, mm)
    m = re.match(r"^(\d{1,2})[./](\d{1,2})[./](\d{4})(?:\s+(\d{1,2}):(\d{2}))?$", s)
    if m:
        d, mo, y = int(m.group(1)), int(m.group(2)), int(m.group(3))
        hh = int(m.group(4)) if m.group(4) else 0
        mm = int(m.group(5)) if m.group(5) else 0
        return _dt.datetime(y, mo, d, hh, mm)
    raise ValueError(f"UZ-Datum nicht erkannt: '{s}'. Nutze YYYY-MM-DD oder DD.MM.YYYY")

def parse_tz(s: str) -> tuple[int, int, int, int]:
    s = s.strip()
    m = re.match(r"^(\d+)\.\s*([A-Za-zÄÖÜäöüß]+)\s+(-?\d+)(?:(?:,\s*|\s+)(\d{1,2})(?::(\d{2}))?)?$", s)
    if m:
        tag = int(m.group(1))
        monat_name = m.group(2).lower()
        jahr = int(m.group(3))
        stunde = int(m.group(4)) if m.group(4) else 0
        monat = TZ_MONATE_LOWER.get(monat_name)
        if monat is None:
            raise ValueError(f"TZ-Monatsname unbekannt: '{m.group(2)}'. Muss einer von {TZ_MONATE} sein.")
        return jahr, monat, tag, stunde
    m = re.match(r"^(-?\d+)-(\d+)-(\d+)(?:\s+(\d{1,2}))?$", s)
    if m:
        return int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4)) if m.group(4) else 0
    raise ValueError(f"TZ-Datum nicht erkannt: '{s}'. Nutze '22. Blütenmond 551' oder '551-5-22'.")

def parse_mz(s: str) -> tuple[int, int, int, int]:
    s = s.strip()
    m = re.match(r"^(\d+)\.\s*([A-Za-zÄÖÜäöüß]+)\s+(-?\d+)(?:(?:,\s*|\s+)(\d{1,2}))?$", s)
    if m:
        tag = int(m.group(1))
        monat_name = m.group(2).lower()
        jahr = int(m.group(3))
        stunde = int(m.group(4)) if m.group(4) else 0
        monat = MZ_MONATE_LOWER.get(monat_name)
        if monat is None:
            raise ValueError(f"MZ-Monatsname unbekannt: '{m.group(2)}'. Muss einer von {[n for n,_,_ in MZ_MONATE]} sein.")
        return jahr, monat, tag, stunde
    m = re.match(r"^(-?\d+)-(\d+)-(\d+)(?:\s+(\d{1,2}))?$", s)
    if m:
        return int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4)) if m.group(4) else 0
    raise ValueError(f"MZ-Datum nicht erkannt: '{s}'. Nutze '14. Dravon 3635' oder '3635-5-14'.")

_UZ_WOCHENTAGE = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]
_UZ_MONATE_NAME = ["Januar","Februar","März","April","Mai","Juni","Juli","August","September","Oktober","November","Dezember"]

def fmt_uz(dt: _dt.datetime) -> str:
    return f"{dt.year:04d}-{dt.month:02d}-{dt.day:02d} {dt.hour:02d}:{dt.minute:02d} ({_UZ_WOCHENTAGE[dt.weekday()]}, {dt.day}. {_UZ_MONATE_NAME[dt.month - 1]} {dt.year})"

def fmt_tz(jahr: int, monat: int, tag: int, stunde: int) -> str:
    mname = TZ_MONATE[monat - 1] if 1 <= monat <= 12 else f"Monat?{monat}"
    return f"{tag}. {mname} {jahr} TZ, {stunde:02d}:00"

def fmt_mz(jahr: int, monat: int, tag: int, stunde: int) -> str:
    if 1 <= monat <= MZ_MONATE_PRO_JAHR:
        mname, bedeutung, halb = MZ_MONATE[monat - 1]
        return f"{tag}. {mname} {jahr} MZ, {stunde:02d}h/26 · Monat {monat}/8 ({bedeutung}, {halb}-Halbjahr)"
    return f"MZ {jahr}-{monat}-{tag}"

# --- Modul-API: alle drei Systeme aus einer Eingabe -----------------------

B1_ANKER_TZ_FLOAT = 551 + (
    (_dt.date(551 + TZ_UZ_OFFSET, 3, 21) - _dt.date(551 + TZ_UZ_OFFSET, 1, 1)).days
) / 365.0


def parse_eingabe(system: str, datum_str: str) -> tuple[float, tuple[int, int, int, int] | None]:
    """Parst Eingabe in {uz,tz,mz} und liefert (tz_jahr_float, optional originale_tz_tuple)."""
    if system == "uz":
        dt = parse_uz(datum_str)
        tz_y, tz_m, tz_d, tz_h, _ = uz_zu_tz_datum(dt)
        tz_float = tz_y + (tz_tag_des_jahres(tz_y, tz_m, tz_d) - 1) / tz_tage_pro_jahr(tz_y)
        tz_float += tz_h / (tz_tage_pro_jahr(tz_y) * 24)
        return tz_float, (tz_y, tz_m, tz_d, tz_h)
    if system == "tz":
        y, m, d, h = parse_tz(datum_str)
        tz_float = y + (tz_tag_des_jahres(y, m, d) - 1) / tz_tage_pro_jahr(y)
        tz_float += h / (tz_tage_pro_jahr(y) * 24)
        return tz_float, (y, m, d, h)
    if system == "mz":
        y, m, d, h = parse_mz(datum_str)
        mz_float = mz_zu_jahresanteil(y, m, d, h)
        tz_float = mz_zu_tz(mz_float)
        # Robustifizierung gegen Float-Rundung
        tz_float += 0.5 / (365 * 24)
        return tz_float, None
    raise ValueError(f"Unbekanntes Zeitsystem: {system}. Nutze uz/tz/mz.")


def konvertiere_alle(system: str, datum_str: str) -> dict:
    """Konvertiert ein Datum in alle drei Systeme.

    Returns dict mit Keys:
      uz_iso          ISO-Datum-String (UZ)
      uz_text         "21. März 1820" (UZ)
      tz_text         "21. Saatmond 551 TZ" (TZ)
      mz_text         "1. Torash 3635 MZ" (MZ)
      uz_jahr_float   Float-Jahr (UZ)
      tz_jahr_float   Float-Jahr (TZ)
      mz_jahr_float   Float-Jahr (MZ, absolut)
      delta_b1_jahre  TZ-Jahre Differenz zum B1-Anker (21. Saatmond 551)
      delta_b1_tage   TZ-Tage Differenz zum B1-Anker
    """
    tz_float, originale_tz = parse_eingabe(system, datum_str)
    if originale_tz is not None:
        tz_y, tz_m, tz_d, tz_h = originale_tz
    else:
        tz_y, tz_m, tz_d, tz_h = tz_jahr_float_zu_datum(tz_float)

    uz_dt = tz_zu_uz_datum(tz_y, tz_m, tz_d, tz_h)
    mz_float = tz_zu_mz_jahresanteil(tz_y, tz_m, tz_d, tz_h)
    mz_y, mz_m, mz_d, mz_h = mz_jahresanteil_zu_datum(mz_float)

    uz_jahr_float = uz_dt.year + (uz_dt.timetuple().tm_yday - 1) / 365.0

    return {
        "uz_iso": uz_dt.strftime("%Y-%m-%d"),
        "uz_text": f"{uz_dt.day}. {_UZ_MONATE_NAME[uz_dt.month - 1]} {uz_dt.year}",
        "tz_text": f"{tz_d}. {TZ_MONATE[tz_m - 1]} {tz_y} TZ",
        "mz_text": f"{mz_d}. {MZ_MONATE[mz_m - 1][0]} {mz_y} MZ",
        "uz_jahr_float": uz_jahr_float,
        "tz_jahr_float": tz_float,
        "mz_jahr_float": mz_float,
        "delta_b1_jahre": tz_float - B1_ANKER_TZ_FLOAT,
        "delta_b1_tage": (tz_float - B1_ANKER_TZ_FLOAT) * 365.0,
        # Roh-Tupel für Detail-Verarbeitung
        "uz_dt": uz_dt,
        "tz_tuple": (tz_y, tz_m, tz_d, tz_h),
        "mz_tuple": (mz_y, mz_m, mz_d, mz_h),
    }


# --- CLI-Ausgabe ----------------------------------------------------------

def konvertiere_und_drucke(tz_jahr_float: float,
                           quelle_label: str,
                           quelle_tz: tuple[int, int, int, int] | None = None) -> None:
    """Vollständiger Output für interaktive CLI-Verwendung."""
    if quelle_tz is not None:
        tz_y, tz_m, tz_d, tz_h = quelle_tz
    else:
        tz_y, tz_m, tz_d, tz_h = tz_jahr_float_zu_datum(tz_jahr_float)
    uz = tz_zu_uz_datum(tz_y, tz_m, tz_d, tz_h)
    mz_float = tz_zu_mz_jahresanteil(tz_y, tz_m, tz_d, tz_h)
    mz_y, mz_m, mz_d, mz_h = mz_jahresanteil_zu_datum(mz_float)

    print(f"Quelle:  {quelle_label}")
    print()
    print(f"  UZ:  {fmt_uz(uz)}")
    print(f"  TZ:  {fmt_tz(tz_y, tz_m, tz_d, tz_h)}")
    print(f"  MZ:  {fmt_mz(mz_y, mz_m, mz_d, mz_h)}")
    print()
    print(f"  Intern:  TZ-Jahr-Float = {tz_jahr_float:.6f}  |  MZ-Jahr-Float = {mz_float:.6f}")

    delta_tz = tz_jahr_float - B1_ANKER_TZ_FLOAT
    delta_tz_tage = delta_tz * tz_tage_pro_jahr(551)
    print(f"  Zum B1-Anker (21. Saatmond 551 TZ):  {delta_tz:+.4f} TZ-Jahre  ({delta_tz_tage:+.1f} TZ-Tage)")


def drucke_tabelle(zeilen: list[tuple[str, str, str]]) -> None:
    """zeilen = Liste von (label, system, datum_str). Druckt 3-Achsen-Tabelle."""
    # Header
    print(f"{'Event':<48} {'UZ':<22} {'TZ':<26} {'MZ':<24}")
    print("-" * 122)
    for label, system, datum in zeilen:
        try:
            r = konvertiere_alle(system, datum)
            uz_s = r["uz_text"]
            tz_s = r["tz_text"]
            mz_s = r["mz_text"]
        except (ValueError, KeyError) as e:
            uz_s = tz_s = mz_s = f"<ERR: {e}>"
        print(f"{label[:47]:<48} {uz_s:<22} {tz_s:<26} {mz_s:<24}")


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("system", nargs="?", choices=["uz", "tz", "mz"],
                    help="Quell-Zeitsystem des Eingabedatums.")
    ap.add_argument("datum", nargs="?",
                    help="Datum, z.B. '2026-04-22' oder '22. Blütenmond 551' oder '14. Dravon 3635'.")
    ap.add_argument("--batch", metavar="FILE",
                    help="Datei mit 'label|system|datum' pro Zeile, druckt Tabelle.")
    args = ap.parse_args()

    if args.batch:
        zeilen = []
        with open(args.batch, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                parts = line.split("|")
                if len(parts) != 3:
                    print(f"WARN: Zeile hat nicht 3 Felder: {line}", file=sys.stderr)
                    continue
                zeilen.append((parts[0].strip(), parts[1].strip(), parts[2].strip()))
        drucke_tabelle(zeilen)
        return 0

    if not args.system or not args.datum:
        ap.error("Brauche system + datum (oder --batch).")

    try:
        tz_float, quelle_tz = parse_eingabe(args.system, args.datum)
    except ValueError as e:
        print(f"FEHLER: {e}", file=sys.stderr)
        return 1

    konvertiere_und_drucke(tz_float, f"{args.system.upper()} {args.datum}", quelle_tz=quelle_tz)
    return 0


if __name__ == "__main__":
    sys.exit(main())
