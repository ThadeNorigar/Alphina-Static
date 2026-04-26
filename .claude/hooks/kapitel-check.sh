#!/usr/bin/env bash
# Läuft als PostToolUse auf Write|Edit.
# Prüft Kapitel-Dateien auf:
#   1. "Resonanz" — Canon-Verstoß (Figuren benennen Fähigkeiten konkret).
#   2. Plot-Snippet-Drift — bei Status lektorat/final: text-Feld in status.json
#      auffrischen, falls Änderung den Plot berührt.
#   3. Deploy-Reminder.
#
# Input: JSON auf stdin mit tool_input.file_path.
# Output: Warnungen/Reminder auf stderr. Nie blockieren (exit 0).

input=$(cat)
f=$(echo "$input" | jq -r '.tool_input.file_path // .tool_response.filePath // empty' 2>/dev/null)

# Pfad-Separatoren normalisieren (Git Bash auf Windows kann beide)
f_norm="${f//\\//}"

# Nur bei Kapitel-Dateien unter buch/kapitel/*.md weiterarbeiten
case "$f_norm" in
  */buch/kapitel/*.md) ;;
  *) exit 0 ;;
esac

# Archiv-Pfade ignorieren
case "$f_norm" in
  */buch/kapitel/_archiv*) exit 0 ;;
  */buch/kapitel/legacy/*) exit 0 ;;
esac

basename=$(basename "$f_norm")

# 1) Resonanz-Canon-Check (gilt für alle Kapitel-Files)
if [ -f "$f_norm" ]; then
  hits=$(grep -Ein 'Resonanz|resonant' "$f_norm" 2>/dev/null)
  if [ -n "$hits" ]; then
    echo "" >&2
    echo "⚠️  Canon-Verstoß: 'Resonanz' in ${basename}" >&2
    echo "   Regel: Figuren benennen Fähigkeiten konkret (Wachstum, Licht, Zeit, Wasser)." >&2
    echo "   Fundstellen:" >&2
    echo "$hits" | sed 's/^/     /' >&2
    echo "" >&2
  fi
fi

# 2) Plot-Snippet-Check (nur bei finaler Prosa, nicht bei Entwurf/Handoff/Backup)
skip_status_check=""
case "$basename" in
  *-entwurf.md|*-handoff.md|*-plot-lock.md|*.backup.md|*-prework.md|*-handoff-lektorat.md)
    skip_status_check=1
    ;;
esac

kid=""
if [ -z "$skip_status_check" ]; then
  if [[ "$basename" =~ ^B[0-9]+-K([0-9]+)- ]]; then
    kid="${BASH_REMATCH[1]}"
  elif [[ "$basename" =~ ^B[0-9]+-(I[0-9]+)- ]]; then
    kid="${BASH_REMATCH[1]}"
  elif [[ "$basename" =~ ^(I[0-9]+)- ]]; then
    kid="${BASH_REMATCH[1]}"
  elif [[ "$basename" =~ ^([0-9]{2})- ]]; then
    kid="${BASH_REMATCH[1]}"
  fi
fi

if [ -n "$kid" ]; then
  # Projekt-Root aus Datei-Pfad ableiten
  status_file="${f_norm%/buch/kapitel/*}/buch/status.json"
  if [ -f "$status_file" ]; then
    info=$(jq -r --arg kid "$kid" '
      [.buch1, .buch2, .buch3]
      | map(select(. != null and (.kapitel[$kid] // null) != null) | .kapitel[$kid])
      | .[0] // empty
      | "\(.status // "")\(.text // "")"
    ' "$status_file" 2>/dev/null)

    if [ -n "$info" ]; then
      state="${info%%$'\x01'*}"
      text="${info#*$'\x01'}"
      case "$state" in
        final)
          preview="${text:0:300}"
          if [ -n "$text" ] && [ "${#text}" -gt 300 ]; then
            preview="${preview}…"
          fi
          echo "" >&2
          echo "📝 Plot-Snippet-Check — Kapitel $kid (Status: $state) wurde editiert." >&2
          if [ -n "$text" ]; then
            echo "   Aktuelles text-Feld in buch/status.json:" >&2
            echo "" >&2
            echo "   $preview" >&2
            echo "" >&2
          else
            echo "   ⚠ text-Feld ist leer in buch/status.json." >&2
            echo "" >&2
          fi
          echo "   → Falls Plot, Datum oder POV durch diese Änderung berührt wurde:" >&2
          echo "     Feld kapitel.$kid.text in buch/status.json nachziehen." >&2
          echo "" >&2
          ;;
      esac
    fi
  fi
fi

# 3) Deploy-Reminder (gilt für alle Kapitel-Files)
echo "📦 Kapitel geändert: commit + git push für Deploy nicht vergessen." >&2
exit 0
