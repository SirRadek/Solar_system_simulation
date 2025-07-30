from vpython import scene, vector
import tkinter as tk

from parameters import SCALE_UP
from planets import planet_list

def setup_scene(state):
    # Získání rozlišení obrazovky pomocí tkinter
    root = tk.Tk()
    screen_width = root.winfo_screenwidth()   # Šířka obrazovky [pixely]
    screen_height = root.winfo_screenheight() # Výška obrazovky [pixely]
    root.destroy()
    # Nastavení velikosti okna scény (90% šířky a 80% výšky obrazovky)
    scene.width, scene.height = screen_width * 0.9, screen_height * 0.8
    # Nastavení ambientního (rozptýleného) světla na maximum (bílá)
    scene.ambient = vector(0.8, 0.8, 0.8)
    # Nastavení směru, kterým se kamera dívá
    scene.forward = vector(2, -1, -2)  # Toto určuje, z jakého směru kamera sleduje scénu
    # Vypnutí automatického škálování (pohled se automaticky nepřizpůsobuje tělesům)
    scene.autoscale = True
    # Nastavení měřítka scény (jak se reálné rozměry převádějí do okna)
    scene.scale = (1e-7, 1e-7, 1e-7)
    # Nastavení zorného pole kamery (větší číslo = širší úhel pohledu)
    scene.fov = 1.2
    scene.center = vector(0, 0, 0)
    scene.range = 1 * planet_list[7].a

    # --- ZDE můžeš nastavit počátek kamery a centrum pohledu ---
    # Počátek kamery určuje, kolem jakého bodu kamera "otáčí scénu" (střed simulace)
    # Defaultně je scene.center = vector(0, 0, 0), tj. střed souřadného systému
    # Pokud chceš například střed na Slunci (nebo kdekoliv jinde), přidej například:
    # scene.center = vector(0, 0, 0)  # Střed simulace (např. souřadnice Slunce)
    # Nebo pokud máš objekt Sun v SimulationState: scene.center = state.sun.pos

    # Další možné parametry kamery (volitelné):
    # scene.range = 1e9   # "Zoom" – velikost prostoru, který kamera vidí kolem centra
    # scene.up = vector(0, 1, 0)  # Směr "nahoru" v okně (defaultně Y)

    # Další parametry či pohyb kamery lze nastavit zde

# --- Konec funkce ---
