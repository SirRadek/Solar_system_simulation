from vpython import label, mag, mag2
from parameters import SimulationState

# Vytvoření popisku, který je na začátku neviditelný, bez rámečku, s mírným posunem a průhledností
popup = label(visible=False, box=False, xoffset=-50, yoffset=50, font='sans', opacity=0.4)

def update_labels(state: SimulationState):
    obj = state.obj  # Získání aktuálního objektu ze stavu simulace
    if not hasattr(obj, "pos"):
        popup.visible = False  # Pokud objekt nemá atribut 'pos' (pozice), popisek skryj
        return
    r0mag = mag(obj.pos)  # Výpočet vzdálenosti objektu od počátku (středu souřadnic)
    if r0mag < 1:
        popup.visible = False  # Pokud je objekt moc blízko (méně než 1 km), popisek skryj
        return
    # Nastavení pozice popisku k objektu
    popup.pos = obj.pos
    # Sestavení textu popisku s informací o poloměru a vzdálenosti objektu
    popup.text = f"Object\nRadius: {getattr(obj, 'radius', 0)} km\nDistance: {int(round(r0mag))} km"
    popup.visible = True  # Zviditelnění popisku
