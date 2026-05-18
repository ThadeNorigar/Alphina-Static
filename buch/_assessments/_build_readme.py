#!/usr/bin/env python3
"""Generiert buch/_assessments/README.md aus kapitel-scores.json (Schema v2)."""
import json
from pathlib import Path

BASE = Path(__file__).parent
data = json.loads((BASE / "kapitel-scores.json").read_text(encoding="utf-8"))
meta = data["meta"]
kap = data["kapitel"]

assert len(kap) == meta["anzahl_kapitel"], f"Anzahl-Mismatch: {len(kap)} != {meta['anzahl_kapitel']}"

n = len(kap)
KERN_ACHSEN = meta.get("kern_achsen", ["sog", "plot_charakter", "stil_disziplin", "pov_schaerfe", "verstaendlichkeit", "tschechow"])

# Aggregate
avg_kern = sum(k["council"]["kern_gesamt"] for k in kap) / n
avg_heat_match = sum(k["council"]["heat_match"] for k in kap) / n
avg_book = sum(k["book_council"]["gesamt"] for k in kap) / n
final = [k for k in kap if k["council"]["verdikt_neu"] == "FINAL"]
final_ids = [k["id"] for k in final]
nicht_final = [k for k in kap if k["council"]["verdikt_neu"] == "NICHT-FINAL"]
pflicht_total = sum(len(k["council"]["pflicht_findings"]) for k in kap)

axis_avg = {a: sum(k["council"]["scores"][a] for k in kap) / n for a in KERN_ACHSEN}
heat_avg = sum(k["council"]["scores"]["heat"] for k in kap) / n
heat_flags = {"OK": 0, "Knapp": 0, "Miss": 0}
for k in kap:
    heat_flags[k["council"]["heat_flag"]] += 1

ranked = sorted(kap, key=lambda k: k["council"]["kern_gesamt"])

lines = []
lines.append("# Kapitel-Assessment-Datensatz — Buch 1")
lines.append("")
lines.append(f"*Erstellt: {meta['erstellt']} · Update: {meta.get('updated', '?')} · {n} Kapitel · Schema v2 (Heat als Diagnose-Achse) · Strukturierte Daten: `kapitel-scores.json`*")
lines.append("")
lines.append("Pro Kapitel ein Subagent (Opus): Council-Assessment (7 Achsen 0-10, davon 6 Kern + 1 Heat als Diagnose) + Book-Council-Rating (5 Leserinnen-Archetypen, Marktfaehigkeit 0-100).")
lines.append("")
lines.append("## Schema v2 — Verdikt-Politik")
lines.append("")
lines.append(f"- **Kern-Score** = Mittel ueber {len(KERN_ACHSEN)} monotone Achsen: `{' / '.join(KERN_ACHSEN)}`")
lines.append("- **FINAL** wenn `kern_gesamt >= 9.0`")
lines.append("- **Heat-Match** = `max(0, 10 - 2 * |heat_soll - heat_ist|)` — Diagnose-Achse, kein Final-Blocker")
lines.append("- **Heat-Flag:** OK (Match ≥ 7) · Knapp (5 ≤ Match < 7) · Miss (Match < 5) → triggert Refit-Empfehlung")
lines.append("- Heat-Definition strikt nach `01-autorin-stimme.md` §11: 0-1 keine, 2-3 leise, 4-6 commercial, 7-9 explizit, 8-10 explizit BDSM")
lines.append("")
lines.append("## Aggregat")
lines.append("")
lines.append(f"- **Kern-Score Ø:** {avg_kern:.2f} / 10")
lines.append(f"- **Heat-Match Ø:** {avg_heat_match:.2f} / 10")
lines.append(f"- **Heat-Score Ø (Ist):** {heat_avg:.2f} / 10 — strikte Definition")
lines.append(f"- **Book-Council-Gesamt Ø:** {avg_book:.1f} / 100")
lines.append(f"- **FINAL (Kern ≥ 9.0):** {len(final)} / {n} — {', '.join(final_ids)}")
lines.append(f"- **NICHT-FINAL:** {len(nicht_final)} / {n}")
lines.append(f"- **Heat-Flags:** OK {heat_flags['OK']} · Knapp {heat_flags['Knapp']} · Miss {heat_flags['Miss']}")
lines.append(f"- **PFLICHT-Findings gesamt:** {pflicht_total}")
lines.append("")

sweep_notes = meta.get("sweep_notes", [])
if sweep_notes:
    lines.append("### Sweep-Notes")
    lines.append("")
    for note in sweep_notes:
        lines.append(f"- {note}")
    lines.append("")

lines.append("**Achsen-Durchschnitt:**")
lines.append("")
lines.append("| " + " | ".join(KERN_ACHSEN + ["heat (ist)"]) + " |")
lines.append("|" + "|".join(["---"] * (len(KERN_ACHSEN) + 1)) + "|")
lines.append("| " + " | ".join(f"{axis_avg[a]:.1f}" for a in KERN_ACHSEN) + f" | {heat_avg:.1f} |")
lines.append("")
weakest_axis = min(KERN_ACHSEN, key=lambda a: axis_avg[a])
lines.append(f"Schwaechste Kern-Achse systemisch: **{weakest_axis}** (Ø {axis_avg[weakest_axis]:.1f}).")
lines.append("")

lines.append("## Übersicht (Lese-Reihenfolge)")
lines.append("")
lines.append("| Kapitel | POV | Kern | Verdikt | Stil | Heat (Ist/Soll) | Match | Flag | Book | Risiko | PFLICHT |")
lines.append("|---------|-----|-----:|---------|-----:|----------------:|------:|------|-----:|--------|--------:|")
for k in kap:
    c = k["council"]
    b = k["book_council"]
    rs = b["risiko_signal"]
    verd = "✅ FINAL" if c["verdikt_neu"] == "FINAL" else "NICHT-FINAL"
    flag_marker = {"OK": "✓", "Knapp": "~", "Miss": "✗"}[c["heat_flag"]]
    lines.append(
        f"| {k['id']} | {k['pov']} | {c['kern_gesamt']:.2f} | {verd} | "
        f"{c['scores']['stil_disziplin']:.1f} | {c['scores']['heat']:.1f} / {c['heat_soll']} | "
        f"{c['heat_match']:.1f} | {flag_marker} {c['heat_flag']} | "
        f"{b['gesamt']:.1f} | {rs['stimme']} {rs['score']} | {len(c['pflicht_findings'])} |"
    )
lines.append("")

lines.append("## Ranking Kern-Score (schwächste zuerst)")
lines.append("")
for k in ranked:
    c = k["council"]
    flag = c["heat_flag"]
    flag_note = "" if flag == "OK" else f" · Heat-{flag}"
    lines.append(f"- **{c['kern_gesamt']:.2f}** {k['id']} ({k['pov']}) — {c['verdikt_neu']}{flag_note}")
lines.append("")

lines.append("## FINAL-Liste (Kern ≥ 9.0)")
lines.append("")
final_sorted = sorted(final, key=lambda k: -k["council"]["kern_gesamt"])
for k in final_sorted:
    c = k["council"]
    lines.append(f"- **{c['kern_gesamt']:.2f}** {k['id']} ({k['pov']}) · Heat {c['scores']['heat']:.1f}/{c['heat_soll']} (Match {c['heat_match']})")
lines.append("")

lines.append("## Lesehinweis")
lines.append("")
lines.append("Pro Kapitel stehen in `kapitel-scores.json`: 7 Council-Achsen-Scores (6 Kern + Heat), Kern-Gesamt + Verdikt-neu, "
             "Heat-Soll/Ist/Match/Flag, 3–5 Staerken, 3–5 Schwaechen, die PFLICHT-Findings (mit Zeile + Problem) sowie das "
             "Book-Council-Rating (5 Leserinnen-Stimmen, Gesamt, Verdikt, Risiko-Signal). "
             "Heat-Achse ist Diagnose, nicht Verdikt — Heat-Miss triggert Refit-Empfehlung, blockt aber nicht Final-Status. "
             "Der Datensatz ist eine Momentaufnahme — bei Aenderungen an einem Kapitel wird der betreffende Eintrag neu erhoben.")
lines.append("")

(BASE / "README.md").write_text("\n".join(lines), encoding="utf-8")
print(f"README.md geschrieben: {n} Kapitel, Kern Ø {avg_kern:.2f}, Heat-Match Ø {avg_heat_match:.2f}, "
      f"{len(final)} FINAL, {pflicht_total} PFLICHT-Findings")
