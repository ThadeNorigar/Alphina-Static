const fs = require("fs");
const data = JSON.parse(fs.readFileSync("buch/zeitleiste.json", "utf8"));
let fixes = 0;

// Kapitel-Details: knappe Kernhandlung, was den Plot treibt
const kapDetails = {
  "15": {
    titel: "Schemen-Eskalation, Runa sammelt Sichtungen",
    detail: "Alphina im Garten bei Tag. Schemen-Tiere haeufiger, aggressiver. Runa sammelt Sichtungen fuer Flugblaetter. Alphina sieht Sorel am Steg — registriert ihn, sagt nichts.",
    tags: ["Tschechow: Schemen-Eskalation", "Setup: Alphina+Sorel"]
  },
  "16": {
    titel: "Sorels Steg-Fotos zeigen Alphina hinter ihm",
    detail: "Sorel fotografiert den Steg. Auf jeder Platte steht Alphina — hinter ihm, obwohl sie nicht dort war. Seine Resonanz projiziert sie. Er erkennt es nicht als Resonanz.",
    tags: ["Tschechow: Steg-Fotos feuern in K25", "Resonanz: Licht-Projektion"]
  },
  "19": {
    titel: "Vesper bringt Maren die reparierte Schiffsuhr zur Werft",
    detail: "Saegemehl, Tee auf Holzkisten. Arm-Beruehrung. Erster ehrlicher Austausch ueber das Unmoegliche — Standuhr, Boot, Schemen. Zweites Treffen nach K14.",
    tags: ["Beziehung: Vesper+Maren vertieft"]
  },
  "20": {
    titel: "Maren zeigt Vesper Harons Zettel — gemeinsam ins Archiv",
    detail: "Maren zeigt Vesper den Zettel aus Harons Werkstatt (frueher gefunden). Vesper: Das gehoert ins Stadtarchiv. Esther Voss erkennt Handschrift, holt 400-jaehriges Manuskript. Jara schiebt Vesper wortlos zweiten Folianten zu. Maren sieht es.",
    tags: ["Schluesselereignis: Manuskript gefunden", "Tschechow: Jara weiss mehr"]
  },
  "23": {
    titel: "VERDACHT: Bruecken-Kap ohne neuen Beat",
    detail: "Sorel nach der Dunkelkammer. Innerer Monolog, Platten entwickeln. Kein neuer Plot-Beat. EMPFEHLUNG: Streichen, Sorels Reflexion als Einstieg in K25 integrieren.",
    tags: ["Audit: Streichen oder in K25"]
  },
  "25": {
    titel: "Alphina findet die Steg-Fotos — Grenzverletzung",
    detail: "Alphina entdeckt Sorels Platten mit ihr drauf. Bruch: Du hast mich genommen ohne zu fragen. Sorel schweigt drei Sekunden zu lang. Sie geht. Tschechow aus K16 feuert.",
    tags: ["Tschechow feuert: Steg-Fotos", "Bruch: Alphina+Sorel"]
  },
  "26": {
    titel: "VERDACHT: Gleicher Bruch wie K25 + Schem-Beruehrung",
    detail: "Alphina durchsucht Sorels Sachen, findet Nachtholm-Platte. Schem beruehrt ihre Wange (Varens Hand durch die Welten). EMPFEHLUNG: Schem-Beat in K25 integrieren, K26 mit K25 zusammenlegen.",
    tags: ["Audit: Mit K25 zusammenlegen", "Tschechow: Varens Beruehrung"]
  },
  "27": {
    titel: "VERDACHT: Dom/Sub-Vertiefung ohne Plot-Funktion",
    detail: "Vesper und Maren: zweite Nacht. Einziger neuer Beat: Miniatur-Steinkreis im Tidemoor-Keller. EMPFEHLUNG: Steinkreis-Beat in K28 einbauen, K27 streichen.",
    tags: ["Audit: Streichen, Beat in K28"]
  },
  "28": {
    titel: "Maren folgt dem Wasser zum Steinkreis",
    detail: "Wasser fuehrt Maren zum Botanischen Garten. Harons zweite Kiste mit Moragh-Phrase. Maren findet den Steinkreis selbst — ohne Vespers Karte, ohne Alphinas Farne.",
    tags: ["Schluesselereignis: Maren findet Steinkreis", "Haron-Enthuelllung"]
  },
  "29": {
    titel: "Alphina findet Sorel am Riss — Versoehnung",
    detail: "Alphina geht zum Steinkreis. Sorel ist dort. Purpurstein reagiert auf beide gleichzeitig. Versoehnung ohne Worte — sie legt die Hand auf den Stein, er legt seine daneben.",
    tags: ["Beziehungs-Wende: Alphina+Sorel", "Steinkreis reagiert auf Resonanzen"]
  },
  "30": {
    titel: "VERDACHT: Uhren stehen still — wiederholt K28",
    detail: "Alle Uhren in Vael stehen gleichzeitig. Haron-Briefe (aus K28). Marens emotionaler Zusammenbruch. EMPFEHLUNG: Uhren-Stillstand als Szene in K32, Rest streichen.",
    tags: ["Audit: Beat in K32 integrieren"]
  },
  "31": {
    titel: "Schemen greifen an — Runas Haende gluehen",
    detail: "Erstmals aggressiver Schemen-Angriff. Haendler stirbt. Thar-Schemen entdeckt (andere Bauart). Runas Haende gluehen — fuenfte Resonanz (Feuer). Sie ist keine Zuschauerin.",
    tags: ["Eskalation: Schemen toeten", "Tschechow: Runa = fuenfte Resonanz"]
  },
  "32": {
    titel: "Vespers grosse Erkenntnis: 4:33 = Varens Atem",
    detail: "Vesper legt Drifttabelle neben Marens Gezeiten neben Runas Flugblatt-Chronologie neben Halvards Verletzungsprotokolle. Alles folgt demselben Takt. 4:33 ist nicht die Frequenz des Risses — es ist die Frequenz von etwas DAHINTER. Jemand atmet.",
    tags: ["Schluesselereignis: 4:33 = Varens Signatur"]
  },
  "33": {
    titel: "Letzte Nacht in Vael — Entscheidung zum Durchgang",
    detail: "Vesper und Jara haben das Ritual uebersetzt. Die Vier entscheiden sich. Runa bittet dazuzubleiben: Ich komme mit.",
    tags: ["Schluesselereignis: Entscheidung Portal"]
  },
  "34": {
    titel: "Sorel haelt Alphinas Hand — der Garten blueht",
    detail: "Steinkreis, Nacht vor dem Ritual. Sorel haelt zum ersten Mal ihre Hand UNGEBETEN. Darf ich? Kontrolle faellt. Die ganze Hoehle blueht. Runa folgt unbemerkt.",
    tags: ["Tschechow feuert: Darf ich?", "Beziehung: Alphina+Sorel Zaertlichkeit"]
  },
  "39": {
    titel: "VERDACHT: Elke-Treffen — evtl. mit K38 zusammenlegen",
    detail: "Maren POV. Elke findet die Gruppe. Altes Thalassisch. Zeitdilatation-Erkenntnis. EMPFEHLUNG: Pruefen ob K38+K39 ein Kapitel sein koennen (Elke als Cliffhanger).",
    tags: ["Audit: Pruefen ob mit K38 zusammenlegbar"]
  },
  "40": {
    titel: "VERDACHT: Trauer/Hass — bereits in K37 transportiert",
    detail: "Alphinas Trauer wird Hass. Dornen statt Farne. Racheschwur. EMPFEHLUNG: Als letzte Szene in K38 integrieren. Dornenwachstum als Schlussbild staerker als eigenes Kapitel.",
    tags: ["Audit: In K38 integrieren"]
  },
  "I4": {
    titel: "VERDACHT: Redundant zu I3",
    detail: "Varen beobachtet weiter durch Schemen. Die Vierte ist die Richtige. EMPFEHLUNG: In I3 integrieren. Ein Interludium reicht fuer Varen als Beobachter.",
    tags: ["Audit: In I3 integrieren"]
  },
  "I6": {
    titel: "VERDACHT: Atmosphaere ohne Plot-Funktion",
    detail: "Elke und Kaspar Intimszene. Beide sterben/verschwinden in I7. EMPFEHLUNG: Streichen, emotionaler Einsatz als Absatz zu Beginn von I7.",
    tags: ["Audit: Streichen, Absatz in I7"]
  }
};

function walk(obj) {
  if (Array.isArray(obj)) { obj.forEach(walk); return; }
  if (obj && typeof obj === "object") {
    if (obj.kapitel && kapDetails[obj.kapitel]) {
      const d = kapDetails[obj.kapitel];
      // Only update if current detail is a placeholder
      if (!obj.detail || obj.detail.length < 80 || obj.detail.startsWith("Alphina im Garten") || obj.detail.startsWith("Sorel fotografiert")) {
        obj.titel = d.titel;
        obj.detail = d.detail;
        obj.tags = d.tags;
        fixes++;
      }
    }
    Object.values(obj).forEach(walk);
  }
}
walk(data);

fs.writeFileSync("buch/zeitleiste.json", JSON.stringify(data, null, 2), "utf8");
try {
  JSON.parse(fs.readFileSync("buch/zeitleiste.json", "utf8"));
  console.log(fixes + " Kapitel-Details aktualisiert. JSON valid.");
} catch (e) {
  console.log("ERROR: " + e.message);
}
