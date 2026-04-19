"""
Wandelt die Vael-Küste von einem geschlossenen Halbinsel-Polygon in eine
durchgängige Polyline West→Ost um. Meer im Süden, Land im Norden.
Passt auch districts, cliff, grauwe.river und harbor_basin entsprechend an.

places, streets, distances bleiben unberührt.
"""
import json, os, sys

FILE = os.path.join(os.path.dirname(__file__), '..', 'buch', 'vael-karte.json')

# Küste: Polyline von West (x=0) nach Ost (x=1200)
# Meer südlich (hohe y), Land nördlich (niedrige y)
# Zwei Haupt-Einbuchtungen: Tidemoor-Westufer (x~380) und Hafenbecken + Grauwe-Mündung (x~550-750)
COAST = [
    [0,    540],
    [80,   545],
    [160,  538],
    [240,  548],
    [310,  562],
    [370,  580],   # Tidemoor-Westufer-Bucht beginnt
    [420,  598],
    [460,  595],
    [500,  610],
    [540,  628],
    [580,  645],   # Hafenbecken-Einlauf
    [620,  658],
    [660,  665],   # tiefste Bucht = Grauwe-Mündung
    [700,  662],
    [740,  652],
    [780,  640],
    [820,  625],
    [860,  608],
    [900,  592],   # Werft-Ostufer
    [950,  582],
    [1010, 580],
    [1080, 585],
    [1150, 590],
    [1200, 595]
]

# Klippenkante: waagerecht zwischen Ober- und Unterstadt (y ~ 370-395)
CLIFF = [
    [180, 360],
    [270, 370],
    [370, 378],
    [470, 385],
    [570, 392],
    [670, 390],
    [770, 383],
    [870, 370],
    [960, 355]
]

# Oberstadt: nördliches Plateau, oberhalb Cliff
OBERSTADT_POLY = [
    [150, 155],
    [300, 130],
    [480, 125],
    [650, 130],
    [820, 145],
    [930, 175],
    [985, 225],
    [995, 290],
    [975, 340],
    [920, 370],
    [820, 380],
    [700, 390],
    [580, 390],
    [450, 385],
    [320, 375],
    [220, 355],
    [160, 310],
    [140, 240],
    [150, 155]
]

# Unterstadt: Streifen zwischen Cliff und Küste
UNTERSTADT_POLY = [
    [200, 400],
    [300, 405],
    [420, 410],
    [540, 415],
    [660, 415],
    [780, 410],
    [880, 405],
    [950, 400],
    [1000, 430],
    [1000, 490],
    [970, 545],
    [900, 580],
    [820, 600],
    [720, 620],
    [640, 625],
    [560, 615],
    [480, 595],
    [400, 570],
    [330, 540],
    [260, 500],
    [220, 450],
    [200, 400]
]

# Grauwe: Fluss kommt von NO, mündet im Süden in der tiefsten Bucht
GRAUWE_RIVER = [
    [885, 40],
    [855, 100],
    [825, 170],
    [795, 240],
    [765, 310],
    [735, 380],
    [710, 450],
    [690, 515],
    [675, 580],
    [665, 625],
    [660, 665]    # Mündung — genau im Küsten-Tiefpunkt
]
GRAUWE_WIDTHS = [14, 18, 22, 26, 32, 38, 46, 56, 70, 88, 108]

# Hafenbecken: Wasserfläche innerhalb der Hafen-Bucht
# (liegt südlich der Unterstadt-Kante, wird vom Meer aus Küsten-Einbuchtung gespeist)
HARBOR_BASIN = []  # leer — die Küstenlinie definiert das Becken implizit

def main():
    with open(FILE, 'r', encoding='utf-8') as f:
        karte = json.load(f)

    # Nur diese Felder ändern, places/streets/distances/viewbox bleiben
    karte['scale_note'] = '1 SVG-Einheit ≈ 4 m. Meer südlich, Land nördlich. Küste als durchgängige Linie West→Ost.'
    karte['coast'] = COAST
    karte['cliff'] = CLIFF

    # Districts
    assert len(karte['districts']) == 2
    karte['districts'][0]['polygon'] = OBERSTADT_POLY
    karte['districts'][1]['polygon'] = UNTERSTADT_POLY

    # Grauwe
    karte['grauwe']['description'] = (
        'Flussmündung, brackig, 2 Ströme. Kommt aus dem Nordost-Inland, '
        'durchfließt die Stadt, mündet im Süden ins Meer (tiefste Küsteneinbuchtung).'
    )
    karte['grauwe']['river'] = GRAUWE_RIVER
    karte['grauwe']['width_map'] = GRAUWE_WIDTHS
    karte['grauwe']['harbor_basin'] = HARBOR_BASIN

    with open(FILE, 'w', encoding='utf-8') as f:
        json.dump(karte, f, ensure_ascii=False, indent=2)

    print(f"Vael-Karte aktualisiert:")
    print(f"  coast:      Polyline mit {len(COAST)} Punkten (West→Ost)")
    print(f"  cliff:      {len(CLIFF)} Punkte")
    print(f"  Oberstadt:  {len(OBERSTADT_POLY)} Punkte")
    print(f"  Unterstadt: {len(UNTERSTADT_POLY)} Punkte")
    print(f"  Grauwe:     {len(GRAUWE_RIVER)} Flusspunkte")
    print(f"  places:     {len(karte['places'])} (unverändert)")
    print(f"  streets:    {len(karte['streets'])} (unverändert)")


if __name__ == '__main__':
    main()
