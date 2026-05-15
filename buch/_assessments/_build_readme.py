#!/usr/bin/env python3
"""Generiert buch/_assessments/README.md aus kapitel-scores.json."""
import json
from pathlib import Path

BASE = Path(__file__).parent
data = json.loads((BASE / "kapitel-scores.json").read_text(encoding="utf-8"))
meta = data["meta"]
kap = data["kapitel"]

assert len(kap) == meta["anzahl_kapitel"], f"Anzahl-Mismatch: {len(kap)} != {meta['anzahl_kapitel']}"

# Aggregate
n = len(kap)
avg_council = sum(k["council"]["gesamt"] for k in kap) / n
avg_book = sum(k["book_council"]["gesamt"] for k in kap) / n
final_reif = [k["id"] for k in kap if k["council"]["verdikt"] == "FINAL-REIF"]
pflicht_total = sum(len(k["council"]["pflicht_findings"]) for k in kap)
axes = meta["council_achsen"]
axis_avg = {a: sum(k["council"]["scores"][a] for k in kap) / n for a in axes}

# Em-Dash-Befund zaehlen (haeufigster PFLICHT-Treffer)
emdash_kap = [k["id"] for k in kap if any("Em-Dash" in f["problem"] or "Gedankenstrich" in f["problem"]
              for f in k["council"]["pflicht_findings"])]

ranked = sorted(kap, key=lambda k: k["council"]["gesamt"])

lines = []
lines.append("# Kapitel-Assessment-Datensatz — Buch 1")
lines.append("")
lines.append(f"*Erstellt: {meta['erstellt']} · {n} finale Kapitel · Strukturierte Daten: `kapitel-scores.json`*")
lines.append("")
lines.append(meta["methode"])
lines.append("")
lines.append("## Aggregat")
lines.append("")
lines.append(f"- **Council-Gesamt Ø:** {avg_council:.2f} / 10")
lines.append(f"- **Book-Council-Gesamt Ø:** {avg_book:.1f} / 100")
lines.append(f"- **FINAL-REIF (Council ≥ 9.0):** {len(final_reif)} / {n} — {', '.join(final_reif) if final_reif else 'keine'}")
lines.append(f"- **Book-Council-Verdikt:** alle {n} GRENZWERTIG (70–89) — keine BESTANDEN, keine DURCHGEFALLEN")
lines.append(f"- **PFLICHT-Findings gesamt:** {pflicht_total}")
lines.append(f"- **Kapitel mit Em-Dash-PFLICHT-Befund:** {len(emdash_kap)} / {n}")
lines.append("")

sweep_notes = meta.get("sweep_notes", [])
if sweep_notes:
    lines.append("### Sweep-Notes")
    lines.append("")
    for note in sweep_notes:
        lines.append(f"- {note}")
    lines.append("")

lines.append("**Achsen-Durchschnitt (Council):**")
lines.append("")
lines.append("| " + " | ".join(axes) + " |")
lines.append("|" + "|".join(["---"] * len(axes)) + "|")
lines.append("| " + " | ".join(f"{axis_avg[a]:.1f}" for a in axes) + " |")
lines.append("")
lines.append("Schwaechste Achse systemisch: **stil_disziplin** "
             f"(Ø {axis_avg['stil_disziplin']:.1f}) — getrieben von Em-Dashes, 'Takt'-Missbrauch, Stakkato-Ketten.")
lines.append("")
lines.append("## Übersicht (Lese-Reihenfolge)")
lines.append("")
lines.append("| Kapitel | POV | Council | Verdikt | Stil | Book | Book-Verdikt | Risiko-Stimme | PFLICHT |")
lines.append("|---------|-----|--------:|---------|-----:|-----:|--------------|---------------|--------:|")
for k in kap:
    c = k["council"]
    b = k["book_council"]
    rs = b["risiko_signal"]
    verd = "✅ FINAL-REIF" if c["verdikt"] == "FINAL-REIF" else "NICHT-FINAL"
    lines.append(
        f"| {k['id']} | {k['pov']} | {c['gesamt']:.1f} | {verd} | "
        f"{c['scores']['stil_disziplin']:.1f} | {b['gesamt']:.1f} | {b['verdikt']} | "
        f"{rs['stimme']} {rs['score']} | {len(c['pflicht_findings'])} |"
    )
lines.append("")
lines.append("## Ranking Council-Gesamt (schwächste zuerst)")
lines.append("")
for k in ranked:
    lines.append(f"- **{k['council']['gesamt']:.1f}** {k['id']} ({k['pov']}) — {k['council']['verdikt']}")
lines.append("")
lines.append("## Lesehinweis")
lines.append("")
lines.append("Pro Kapitel stehen in `kapitel-scores.json`: 7 Council-Achsen-Scores, Gesamt + Verdikt, "
             "3–5 Staerken, 3–5 Schwaechen, die PFLICHT-Findings (mit Zeile + Problem) sowie das "
             "Book-Council-Rating (5 Leserinnen-Stimmen, Gesamt, Verdikt, Risiko-Signal). "
             "Der Datensatz ist eine Momentaufnahme — bei Aenderungen an einem Kapitel wird der "
             "betreffende Eintrag neu erhoben.")
lines.append("")

(BASE / "README.md").write_text("\n".join(lines), encoding="utf-8")
print(f"README.md geschrieben: {n} Kapitel, Council Ø {avg_council:.2f}, Book Ø {avg_book:.1f}, "
      f"{len(final_reif)} FINAL-REIF, {pflicht_total} PFLICHT-Findings")
