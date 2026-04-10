const fs = require("fs");
const data = JSON.parse(fs.readFileSync("buch/zeitleiste.json", "utf8"));
const status = JSON.parse(fs.readFileSync("buch/status.json", "utf8"));
let fixes = 0;

// POV mapping from status.json
const povMap = {};
for (const [id, ch] of Object.entries(status.buch1.kapitel)) {
  povMap[id] = ch.pov || ch.titel || '';
}

// 1. Add pov field to all events that lack it
function walk(obj) {
  if (Array.isArray(obj)) { obj.forEach(walk); return; }
  if (obj && typeof obj === "object") {
    if (obj.kapitel && !obj.pov && povMap[obj.kapitel]) {
      obj.pov = "Kap " + obj.kapitel + " - " + povMap[obj.kapitel];
      fixes++;
    }
    Object.values(obj).forEach(walk);
  }
}
walk(data);

// 2. Find which kapitel have events
const hasEvents = new Set();
function collect(obj) {
  if (Array.isArray(obj)) { obj.forEach(collect); return; }
  if (obj && typeof obj === "object") {
    if (obj.kapitel) hasEvents.add(obj.kapitel);
    Object.values(obj).forEach(collect);
  }
}
collect(data);

// 3. Missing chapters — create minimal entries
// Dates from aktplan/status for missing chapters
const missingDefs = {
  "15": { tag: 148, datum: "28. Mai", pov: "Alphina", detail: "Alphina im Garten bei Tag und am Steg. Resonanz-Beobachtungen vertiefen sich." },
  "16": { tag: 152, datum: "1. Juni", pov: "Sorel", detail: "Sorel fotografiert den Steg. Die Platten zeigen mehr als er sehen will." },
  "27": { tag: 210, datum: "29. Juli", pov: "Vesper", detail: "Vesper und Maren: Vertiefung. Dom/Sub-Dynamik etabliert sich." },
  "30": { tag: 232, datum: "20. August", pov: "Vesper", detail: "Die Uhren in Vael stehen. Alle gleichzeitig. Vesper weiss warum." },
  "39": { tag: 276, datum: "3. Oktober -- Moragh", pov: "Maren", detail: "Moragh: Die fremde Stadt. Maren orientiert sich." },
  "40": { tag: 276, datum: "3. Oktober -- Moragh", pov: "Alphina", detail: "Alphina begegnet Elke. Cliffhanger Buch 1." },
  "I1": { tag: null, datum: null, pov: "Elke", detail: "Nebelmond 154. Elke kommt nach Vael. Bildhauerin aus dem Sueden.", moragh: false, interludium: true },
  "I2": { tag: null, datum: null, pov: "Elke", detail: "Frostmond 154. Keldan trifft Elke. Sechs Wochen in Vael.", moragh: false, interludium: true },
  "I3": { tag: null, datum: null, pov: "Varen", detail: "Varen beobachtet die Vier durch die Schemen. Erste Einschaetzung.", moragh: true, interludium: true },
  "I4": { tag: null, datum: null, pov: "Varen", detail: "Die Schemen berichten. Varen justiert seinen Plan.", moragh: true, interludium: true },
  "I5": { tag: null, datum: null, pov: "Manuskript", detail: "Das gefaelschte Manuskript. Varens Koeder fuer die Vier.", moragh: false, interludium: true },
  "I6": { tag: null, datum: null, pov: "Varen", detail: "Varen wartet. Geduld als Waffe.", moragh: true, interludium: true },
  "I7": { tag: null, datum: null, pov: "Elke", detail: "Elke in Moragh. Rueckblick.", moragh: true, interludium: true },
  "I8": { tag: null, datum: null, pov: "Lene/Elke", detail: "Lene schreibt auf was passiert ist. Elke geht durch das Portal.", moragh: false, interludium: true },
};

// Find the Buch 1 thalassien events array (monate[12])
const b1Month = data.monate.find(m => m.buch && m.buch.includes("Buch 1"));
if (!b1Month) { console.log("ERROR: Buch 1 month not found"); process.exit(1); }

for (const [kapId, def] of Object.entries(missingDefs)) {
  if (hasEvents.has(kapId)) continue;

  const ev = {
    tz: 551,
    mz: 0,
    kapitel: kapId,
    typen: ["hintergrund"],
    titel: povMap[kapId] || def.pov,
    pov: "Kap " + kapId + " - " + def.pov,
    buch: "B1",
    kapitel_status: status.buch1.kapitel[kapId]?.status || "szenenplan",
    detail: def.detail
  };
  if (def.tag) { ev.tz_tag = def.tag; ev.datum_text = def.datum; }

  // Interludien and Moragh events go to moragh array, rest to thalassien
  if (def.moragh) {
    b1Month.events.moragh.push(ev);
  } else {
    b1Month.events.thalassien.push(ev);
  }
  console.log("Added K" + kapId + " (" + def.pov + ")");
  fixes++;
}

// 4. Re-sort thalassien by tz_tag
b1Month.events.thalassien.sort((a, b) => {
  const ta = a.tz_tag || 9999;
  const tb = b.tz_tag || 9999;
  if (ta !== tb) return ta - tb;
  const ka = parseInt(a.kapitel) || 999;
  const kb = parseInt(b.kapitel) || 999;
  return ka - kb;
});

// 5. Re-sort moragh by tz_tag
b1Month.events.moragh.sort((a, b) => {
  const ta = a.tz_tag || 9999;
  const tb = b.tz_tag || 9999;
  if (ta !== tb) return ta - tb;
  const ka = parseInt(a.kapitel) || 999;
  const kb = parseInt(b.kapitel) || 999;
  return ka - kb;
});

fs.writeFileSync("buch/zeitleiste.json", JSON.stringify(data, null, 2), "utf8");
try {
  JSON.parse(fs.readFileSync("buch/zeitleiste.json", "utf8"));
  console.log("\n" + fixes + " fixes. JSON valid.");
} catch (e) {
  console.log("ERROR: " + e.message);
}
