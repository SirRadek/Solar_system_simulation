from vpython import rate
from graphics import setup_scene
from key_control import handle_keyboard_and_mouse
from info import update_labels
from parameters import SimulationState
from update import update_all_bodies, update_spaceship  # Import obou funkcí


def main():
    # Inicializace simulace a všech objektů
    state = SimulationState()
    # Nastavení grafické scény a kamery podle rozměrů obrazovky a preferencí
    setup_scene(state)

    # Hlavní smyčka simulace – běží, dokud není state.running == False
    while state.running:
        rate(state.f)  # Ovládá rychlost animace (počet snímků za sekundu)

        # Zpracování vstupu z klávesnice a myši (ovládání, pauza, výběr objektu)
        handle_keyboard_and_mouse(state)

        if state.ship_mode:
            # V režimu lodi: aktualizuj loď i všechny ostatní objekty (pokud chceš hýbat vším)
            update_spaceship(state)
            # Pokud chceš aby planety běžely zároveň s lodí, nech i update_all_bodies
            update_all_bodies(state)
        else:
            # Jinak se aktualizují všechny planety, měsíce, prstence atd.
            update_all_bodies(state)

        # Aktualizace popisků a informací na scéně (názvy planet, údaje, vzdálenosti apod.)
        update_labels(state)

        # Posun simulovaného času o jeden krok vpřed (t je „časová osa“ simulace)
        state.t += state.dt

if __name__ == "__main__":
    main()  # Spuštění hlavního programu
