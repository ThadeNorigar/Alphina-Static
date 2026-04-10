const fs = require("fs");
const data = JSON.parse(fs.readFileSync("buch/zeitleiste.json", "utf8"));
let fixes = 0;

function walk(obj, fn) {
  if (Array.isArray(obj)) { obj.forEach(o => walk(o, fn)); return; }
  if (obj && typeof obj === "object") { fn(obj); Object.values(obj).forEach(o => walk(o, fn)); }
}

// === 1. K01-K07 DATE FIXES ===
const dateFixes = {
  "01": { tag: 80, datum: "21. Maerz" },
  "02": { tag: 80, datum: "21. Maerz" },
  "03": { tag: 83, datum: "24. Maerz" },
  "04": { tag: 83, datum: "24. Maerz" },
  "05": { tag: 83, datum: "24. Maerz" },
  "06": { tag: 86, datum: "27. Maerz" },
  "07": { tag: 87, datum: "28. Maerz" }
};
walk(data, obj => {
  if (obj.kapitel && dateFixes[obj.kapitel] && obj.tz_tag !== undefined) {
    const f = dateFixes[obj.kapitel];
    if (obj.tz_tag !== f.tag) { obj.tz_tag = f.tag; obj.datum_text = f.datum; fixes++; }
  }
});

// === 2. ALPHINA LEBT ===
walk(data, obj => {
  if (obj.titel === "Alphina stirbt") {
    obj.titel = "Alphina lebt";
    obj.detail = "Kein Opfertod. Die Pflanzen wachsen weiter. Die Quelle bleibt offen.";
    obj.typen = ["schluessel"];
    obj.tags = ["Schluesselereignis"];
    fixes++;
  }
});

// === 3. KAMINFEUER VERSCHOBEN ===
walk(data, obj => {
  if (obj.titel && obj.titel.includes("Kaminfeuer ohne Brennstoff") && obj.kapitel === "05") {
    obj.titel = "Alphina: Kaminfeuer ohne Brennstoff (verschoben)";
    obj.tz_tag = null; obj.datum_text = null; obj.stufe = "offen";
    obj.detail = "War fuer K05 geplant, nicht eingebaut. Spaeteres Alphina-Kapitel.";
    fixes++;
  }
});

// === 4. K14 ORT + TITEL ===
walk(data, obj => {
  if (obj.kapitel === "14" && obj.ort && obj.ort.includes("Uhrmacher")) {
    obj.ort = "Gasthof Anker, Schankraum (Vespers gemieteter Arbeitstisch)";
    fixes++;
  }
  if (obj.titel && obj.titel.includes("Uhrengesch")) {
    obj.titel = obj.titel.replace(/Uhrengesch[aä]ft/g, "Anker");
    fixes++;
  }
});

// === 5. VAREN EXPERIMENT MOTIV ===
walk(data, obj => {
  if (obj.titel === "Varens Leylinien-Experiment scheitert" && obj.detail) {
    obj.detail = obj.detail.replace(
      /um Kapazit.t zu erh.hen \(Motiv: .berbev.lkerung\)/,
      "um magiefreie Flaechen besiedelbar zu machen (Motiv: Expansion der bewohnbaren Zonen)"
    );
    fixes++;
  }
});

// === 6. KRIEGSGRUND ===
walk(data, obj => {
  if (obj.titel && obj.titel.includes("Der Krieg beginnt") && obj.detail && obj.detail.includes("verbleibende")) {
    obj.detail = "Ausloeser: Das Thar-Konglomerat glaubt, der Bund von Orath habe die Explosion absichtlich ausgeloest. Es gibt genug Quellen -- der Krieg beginnt aus Misstrauen und Vergeltung, nicht aus Ressourcenknappheit. Dauert 4 MZ-Jahre (= ~1.600 TZ). Die Fuenf erfahren in Buch 2 zunaechst die Konglomerat-Version.";
    fixes++;
  }
});

// === 7. ELKE VERLAESST VAREN ===
walk(data, obj => {
  if (obj.titel === "Elke verl\u00e4sst Varen") {
    obj.detail = "Persoenliche Gruende: will nicht zurueck nach Vael, spuert dass seine Forschung sie als Mittel braucht. Weiss NICHT von den zerstoerten Quellen. Er macht weiter. Allein.";
    fixes++;
  }
});

// === 8. VAREN RUECKHOLUNG ===
walk(data, obj => {
  if (obj.titel && obj.titel.includes("Varen plant die R\u00fcckholung")) {
    obj.detail = "Elke hat ihn verlassen. Varen glaubt: Resonanz-Magie ohne Quelle ist die Loesung. Er kann nicht selbst durchs Portal ohne sich die Rueckkehr zu verbauen. Schickt menschliche Agenten (Moragh-geboren) mit klarem Auftrag + gebundene Schemen als Helfer (Agenten koennen kein Handwerk). Schemen erledigen praktische Arbeit. Ueber Schemen-Bindung sammelt Varen diffuse Informationen.";
    fixes++;
  }
});

// === 9. WOCHENZAEHLUNG KONVENTION ===
if (data.meta && data.meta.schema) {
  data.meta.schema._wochenzaehlung = "Konvention: Ankunftstag = Tag 1. Fixe Kapitel (1-14, I1, I2) sind Source of Truth.";
  fixes++;
}

// === 10. K19 DETAIL FIX ===
walk(data, obj => {
  if (obj.kapitel === "19" && obj.detail && obj.detail.includes("Karton")) {
    obj.detail = "Maren zeigt Vesper den Zettel aus Harons Werkstatt (schon frueher gefunden). Vesper: Das gehoert ins Stadtarchiv. Gemeinsam hin. Esther Voss erkennt eine Handschrift, holt das 400-jaehrige Manuskript. Jara schiebt Vesper wortlos einen zweiten Folianten zu. Maren sieht es. Marens Gedanken von K14 kommen zurueck, schaerfer.";
    fixes++;
  }
  if (obj.kapitel === "19" && obj.detail && obj.detail.includes("acht-Stein")) {
    obj.detail = obj.detail.replace("acht-Stein", "sieben-Stein");
    fixes++;
  }
});

// === 11. K19/K20 SWAP ===
walk(data, obj => {
  if (obj.kapitel === "19" && obj.tz_tag === 168) {
    obj.tz_tag = 171; obj.datum_text = "20. Juni"; fixes++;
  }
  if (obj.kapitel === "20" && obj.tz_tag === 171) {
    obj.tz_tag = 165; obj.datum_text = "14. Juni"; fixes++;
  }
});

// === 12. ADD MAGIE-SICKERN EVENT ===
walk(data, obj => {
  if (Array.isArray(obj)) {
    for (let i = 0; i < obj.length; i++) {
      if (obj[i] && obj[i].titel && obj[i].titel.includes("Varen plant die R\u00fcckholung")) {
        if (!obj[i + 1] || !obj[i + 1].titel || !obj[i + 1].titel.includes("Portaltaetigkeit")) {
          obj.splice(i + 1, 0, {
            tz: 354, mz: -0.42,
            titel: "Verstaerkte Portaltaetigkeit -- Magie sickert nach Thalassien",
            detail: "Durch Varens Agenten+Schemen entstehen groessere Risse im Gewebe. Magie sickert staerker nach Thalassien. Passiveffekte nehmen zu. Resonanz-Faehigkeiten der Fuenf entwickeln sich unbewusst.",
            typen: ["hintergrund", "tschechow"],
            tags: ["Hintergrund: Magie-Sickern", "Tschechow: Resonanz-Entwicklung"]
          });
          fixes++;
        }
        break;
      }
    }
  }
});

// === 13. K41 FIX ===
walk(data, obj => {
  if (obj.kapitel === "41") {
    obj.titel = "Vael ohne die Fuenf -- Varens Spuren verschwinden";
    obj.detail = "Schemen verschwinden schlagartig. Was Varen angezettelt hat hoert auf. Aber kleinere Anomalien BLEIBEN: Wasser fliesst ungewoehnlich, Uhren gehen wieder falsch, Tidemoor-Uhr kaputt, Farne im Garten wachsen weiter. Riss-Quelle sickert weiter. Halvard schreibt seinen Bericht -- sachlich, praezise, das einzige schriftliche Zeugnis. Jara archiviert Runas Flugblaetter. Das Boot wartet, drei Viertel fertig.";
    fixes++;
  }
});

// === 14. MOVE K35-K38 FROM BUCH 2 TO BUCH 1 ===
let moraghEventsToMove = [];
for (const monat of data.monate || []) {
  if (monat.buch && monat.buch.includes("Buch 2")) {
    if (monat.events && monat.events.moragh) {
      const keep = [];
      for (const ev of monat.events.moragh) {
        if (ev.kapitel && ["35", "36", "38", "39"].includes(ev.kapitel)) {
          moraghEventsToMove.push(ev);
        } else if (ev.titel && ev.titel.includes("Alphinas Trauer")) {
          moraghEventsToMove.push(ev);
        } else {
          keep.push(ev);
        }
      }
      monat.events.moragh = keep;
      // Move Halvard to K41 (already in Buch 1)
      if (monat.events.thalassien) {
        monat.events.thalassien = monat.events.thalassien.filter(
          ev => !(ev.titel && ev.titel.includes("Halvard"))
        );
      }
    }
  }
}

// Fix moved events
for (const ev of moraghEventsToMove) {
  if (ev.titel && ev.titel.includes("Varen begegnet")) {
    ev.kapitel = "36"; ev.pov = "Kap 36 - Alphina";
  }
  if (ev.titel && ev.titel.includes("Sorel stirbt")) {
    ev.kapitel = "36";
  }
  if (ev.titel && ev.titel.includes("Elke findet")) {
    ev.kapitel = "38";
    ev.detail = "Elke tritt aus dem Dunkel. 1423er Thalassisch. Ihr seid nicht die Ersten. Sie kennt Varen -- war seine Geliebte. Cliffhanger: Buch 1 endet hier.";
    ev.tags = ["Schluesselereignis: Buch 1 Cliffhanger", "Erste Begegnung: Die Gruppe + Elke"];
  }
}

// Add K37 (new)
moraghEventsToMove.push({
  tz: 551, mz: 0, kapitel: "37",
  typen: ["schluessel"],
  titel: "Flucht nach Sorels Tod -- Alphina stumm, die anderen verwundet",
  pov: "Kap 37 - Maren",
  tz_tag: 274, datum_text: "1. Oktober -- Moragh",
  detail: "Maren POV. Alphinas Zorn-Explosion hat alle verletzt: Maren (Dornen in Wade), Vesper (Wurzel trifft Schulter), Runa (Brombeeren, Schnitte). Alphina ist stumm, Narbe entlang der Wirbelsaeule. Varen geflohen. Zwei Monde am Himmel. Kein Rueckweg.",
  tags: ["Schluesselereignis: Nachwirkung"]
});

// Insert into Buch 1 portal month (where Elke's garden event is)
for (const monat of data.monate || []) {
  if (monat.events && monat.events.moragh) {
    if (monat.events.moragh.some(e => e.titel && e.titel.includes("Elke in ihrem Garten"))) {
      monat.events.moragh.push(...moraghEventsToMove);
      fixes += moraghEventsToMove.length;
      break;
    }
  }
}

// === 15. REMOVE OLD-FORMAT DUPLICATES ===
function removeDupes(obj) {
  if (Array.isArray(obj)) {
    for (let i = obj.length - 1; i >= 0; i--) {
      const e = obj[i];
      if (e && e.kapitel && e.titel && !e.tz_tag && !e.detail) {
        const hasRich = obj.some(o => o !== e && o.kapitel === e.kapitel && o.tz_tag && o.titel);
        if (hasRich) { obj.splice(i, 1); fixes++; }
      }
    }
    obj.forEach(o => removeDupes(o));
  } else if (obj && typeof obj === "object") {
    Object.values(obj).forEach(o => removeDupes(o));
  }
}
removeDupes(data);

// === 16. BUCH 1/2 BOUNDARY ===
for (const monat of data.monate || []) {
  if (monat.sync && monat.sync.label && monat.sync.label.includes("Portal")) {
    monat.sync.label = "Portal -- Die Fuenf nach Moragh. BUCH 1 ENDET mit Elke-Cliffhanger (K38).";
    fixes++;
  }
  if (monat.buch && monat.buch.includes("Buch 2") && !monat.buch.includes("beginnt NACH")) {
    monat.buch = "Buch 2: Das Auge (beginnt NACH Elke-Treffen)";
    fixes++;
    break;
  }
}

// === WRITE ===
fs.writeFileSync("buch/zeitleiste.json", JSON.stringify(data, null, 2), "utf8");
console.log("Applied " + fixes + " fixes");
try {
  JSON.parse(fs.readFileSync("buch/zeitleiste.json", "utf8"));
  console.log("JSON valid");
} catch (e) {
  console.log("ERROR: " + e.message);
}
