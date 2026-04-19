"""
Fügt Topologie-Daten in buch/moragh-karte.json ein.
Liest die existierende Datei, ergänzt topology-Feld (wenn leer), schreibt zurück.
Bestehende cities/portal/coast bleiben unangetastet.

Quelle der Daten: Moragh-Topologie-Recherche (Kanon hat keine explizite Topologie,
plausible Rekonstruktion aus Fraktionen + Stadt-Verteilung + Rohstoff-Erwähnungen).
"""
import json
import os
import sys

FILE = os.path.join(os.path.dirname(__file__), '..', 'buch', 'moragh-karte.json')

# --- Formationen (Polygone) -------------------------------------------------
formations = [
    {
        "type": "granit",
        "label": "Thar-Rücken",
        "polygon": [
            [1020, 180], [1090, 170], [1170, 175], [1235, 200],
            [1270, 250], [1285, 320], [1285, 410], [1275, 490],
            [1260, 560], [1225, 605], [1175, 615], [1120, 605],
            [1080, 580], [1055, 540], [1035, 480], [1025, 410],
            [1015, 340], [1010, 270], [1020, 180]
        ]
    },
    {
        "type": "kalkstein",
        "label": "Zentrales Hochplateau",
        "polygon": [
            [560, 280], [680, 260], [800, 275], [880, 310],
            [910, 370], [895, 440], [850, 490], [770, 520],
            [680, 520], [590, 510], [510, 475], [470, 420],
            [460, 350], [490, 300], [560, 280]
        ]
    },
    {
        "type": "sandstein",
        "label": "Velmar-Schieferkamm",
        "polygon": [
            [820, 610], [870, 595], [935, 605], [985, 640],
            [1005, 685], [985, 730], [930, 760], [870, 770],
            [810, 755], [775, 720], [770, 665], [795, 625],
            [820, 610]
        ]
    },
    {
        "type": "basalt",
        "label": "Westliche Basaltküste",
        "polygon": [
            [290, 260], [340, 235], [380, 245], [395, 305],
            [380, 380], [355, 450], [330, 530], [305, 590],
            [280, 555], [275, 485], [280, 410], [285, 335],
            [290, 260]
        ]
    },
    {
        "type": "vulkanit",
        "label": "Keth-Varen — verglaste Todzone",
        "polygon": [
            [815, 400], [845, 388], [880, 395], [905, 420],
            [910, 455], [895, 480], [870, 490], [840, 485],
            [815, 465], [805, 435], [815, 400]
        ]
    },
    {
        "type": "vulkanit",
        "label": "Dulrath-Ost-Schlackefeld",
        "polygon": [
            [860, 435], [890, 430], [915, 445], [920, 465],
            [905, 480], [875, 478], [855, 465], [855, 445],
            [860, 435]
        ]
    }
]

# --- Höhenlinien (Polylines) ------------------------------------------------
# 200m = Niedrig-Plateau, 400m = Zentral, 600m = Bergketten, 800m = Spitzen
contours = [
    # 200m — Plateau-Außenrand (Küstennahe, niedriger Bereich)
    {
        "elevation": 200,
        "closed": False,
        "points": [
            [360, 200], [420, 220], [500, 230], [590, 240], [680, 250],
            [770, 260], [860, 255], [940, 240], [1010, 225], [1080, 215]
        ]
    },
    {
        "elevation": 200,
        "closed": False,
        "points": [
            [370, 650], [450, 680], [540, 695], [630, 705], [720, 695],
            [810, 680], [890, 665], [960, 645]
        ]
    },
    # 400m — Zentrales Hochplateau (Bund-Region)
    {
        "elevation": 400,
        "closed": True,
        "points": [
            [500, 310], [580, 290], [670, 295], [760, 310], [830, 340],
            [870, 390], [870, 450], [830, 495], [760, 510], [670, 505],
            [580, 490], [510, 460], [470, 410], [475, 360], [500, 310]
        ]
    },
    # 400m — Velmar-Hochland
    {
        "elevation": 400,
        "closed": True,
        "points": [
            [820, 625], [880, 615], [940, 625], [980, 660], [985, 700],
            [950, 735], [890, 745], [830, 735], [795, 705], [790, 665],
            [820, 625]
        ]
    },
    # 600m — Ost-Bergkette (Thar)
    {
        "elevation": 600,
        "closed": True,
        "points": [
            [1060, 220], [1120, 205], [1180, 215], [1225, 250], [1245, 305],
            [1250, 380], [1240, 460], [1220, 525], [1185, 570], [1135, 575],
            [1095, 555], [1070, 510], [1055, 440], [1050, 360], [1055, 285],
            [1060, 220]
        ]
    },
    # 800m — Thar-Ost-Gipfel
    {
        "elevation": 800,
        "closed": True,
        "points": [
            [1150, 260], [1195, 255], [1220, 285], [1225, 330],
            [1210, 365], [1175, 380], [1140, 370], [1120, 335],
            [1125, 295], [1150, 260]
        ]
    }
]

# --- Rohstoffe --------------------------------------------------------------
resources = [
    # Purpurstein — überall wo Quellen (unter großen Städten)
    {"type": "purpurstein", "x": 722,  "y": 389, "richness": 3},  # Orath
    {"type": "purpurstein", "x": 822,  "y": 345, "richness": 3},  # Kethmar
    {"type": "purpurstein", "x": 630,  "y": 510, "richness": 3},  # Halvaren
    {"type": "purpurstein", "x": 470,  "y": 615, "richness": 2},  # Sulmen
    {"type": "purpurstein", "x": 914,  "y": 661, "richness": 2},  # Velmar
    {"type": "purpurstein", "x": 1108, "y": 385, "richness": 2},  # Thar-Kem
    {"type": "purpurstein", "x": 1170, "y": 500, "richness": 2},  # Draveth
    {"type": "purpurstein", "x": 1080, "y": 280, "richness": 2},  # Sulkara

    # Eisen-Erz — Ost-Bergkette, zentrale Bund-Region
    {"type": "eisen", "x": 1140, "y": 300, "richness": 3},
    {"type": "eisen", "x": 1210, "y": 390, "richness": 2},
    {"type": "eisen", "x": 1085, "y": 250, "richness": 2},
    {"type": "eisen", "x": 1180, "y": 550, "richness": 2},
    {"type": "eisen", "x": 790,  "y": 400, "richness": 1},
    {"type": "eisen", "x": 560,  "y": 380, "richness": 1},

    # Kupfer — Zentral-Hochland
    {"type": "kupfer", "x": 800,  "y": 380, "richness": 2},
    {"type": "kupfer", "x": 680,  "y": 440, "richness": 1},
    {"type": "kupfer", "x": 1100, "y": 450, "richness": 1},

    # Silber — Velmar (Prestige-Metall)
    {"type": "silber", "x": 920,  "y": 670, "richness": 2},
    {"type": "silber", "x": 870,  "y": 700, "richness": 1},
    {"type": "silber", "x": 1235, "y": 430, "richness": 1},

    # Edelsteine (Quarz/Kristall + seltene Gemmen)
    {"type": "edelstein", "x": 1195, "y": 280, "richness": 2},  # Quarzadern Ost
    {"type": "edelstein", "x": 1250, "y": 350, "richness": 2},
    {"type": "edelstein", "x": 940,  "y": 645, "richness": 1},  # Velmar-Kristalle
    {"type": "edelstein", "x": 1160, "y": 360, "richness": 1},  # Kobaltschiefer-Hub

    # Kohle — Zentral-West (fossile Sediment-Schichten)
    {"type": "kohle", "x": 740, "y": 420, "richness": 2},
    {"type": "kohle", "x": 650, "y": 380, "richness": 1},
    {"type": "kohle", "x": 1120, "y": 420, "richness": 1},

    # Salz — Küsten-Salinen
    {"type": "salz", "x": 400,  "y": 660, "richness": 2},
    {"type": "salz", "x": 1240, "y": 585, "richness": 1},
    {"type": "salz", "x": 330,  "y": 480, "richness": 1},
]


def main():
    with open(FILE, 'r', encoding='utf-8') as f:
        karte = json.load(f)

    existing = karte.get('topology') or {}
    existing_contours = existing.get('contours') or []
    existing_formations = existing.get('formations') or []
    existing_resources = existing.get('resources') or []

    already_populated = bool(existing_contours or existing_formations or existing_resources)
    if already_populated and '--force' not in sys.argv:
        print(f"Topologie bereits befüllt:")
        print(f"  contours:    {len(existing_contours)}")
        print(f"  formations:  {len(existing_formations)}")
        print(f"  resources:   {len(existing_resources)}")
        print(f"Zum Überschreiben: --force")
        return

    karte['topology'] = {
        'contours': contours,
        'formations': formations,
        'resources': resources
    }

    with open(FILE, 'w', encoding='utf-8') as f:
        json.dump(karte, f, ensure_ascii=False, indent=2)

    print(f"Topologie eingefügt:")
    print(f"  contours:    {len(contours)}")
    print(f"  formations:  {len(formations)}")
    print(f"  resources:   {len(resources)}")
    print(f"  cities:      {len(karte.get('cities', []))} (unverändert)")
    print(f"  portal:      {karte.get('portal', {}).get('name', '?')} (unverändert)")
    print(f"  coast:       {len(karte.get('coast', []))} Punkte (unverändert)")


if __name__ == '__main__':
    main()
