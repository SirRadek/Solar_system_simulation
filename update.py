"""
Funkce pro aktualizaci pozic planet a měsíců v simulaci sluneční soustavy.
Kompatibilní s dataclass-based SimulationState a objekty planet/měsíců.
"""

from vpython import vector, sin, cos, norm, scene
from typing import Any
from spaceship import ship
from numpy import arccos, clip

def update_planet(planetlist: list, t: float, dt: float, n: int):
    """
    Aktualizuje pozici, dráhu (trail) a rotaci planety v simulaci.
    :param planetlist: List [sphere, orbit_coords, timescale, a, tilt, spin]
    :param t: Aktuální čas simulace
    :param dt: Délka časového kroku simulace
    :param n: Počet bodů na oběžné dráze
    """
    # Nastavení nové pozice planety podle předpočítané orbity a simulovaného času
    planetlist[0].pos = vector(*planetlist[1][:, (int(-t / planetlist[2])) % n])
    # Přidání nové pozice do dráhy planety (trail)
    planetlist[0].trail.append(
        pos=planetlist[0].pos,
        retain=int(1.5e-9 * planetlist[3] ** 1.55 / dt)  # Délka stopy (závisí na velikosti a rychlosti)
    )
    # Rotace planety kolem vlastní osy (pro efektní otáčení textury)
    planetlist[0].rotate(
        angle=planetlist[5] * dt,
        axis=vector(-sin(planetlist[4]), cos(planetlist[4]), 0)
    )
    return 0

def update_moon(moonlist: list, t: float, dt: float, n: int):
    """
    Aktualizuje pozici, dráhu (trail) a rotaci měsíce v simulaci.
    :param moonlist: List [sphere, planet_coords, moon_coords, planet_timescale, moonscale, tilt, spin, lock]
    :param t: Aktuální čas simulace
    :param dt: Délka časového kroku simulace
    :param n: Počet bodů na oběžné dráze
    """
    # Pozice měsíce je součet aktuální pozice planety a aktuálního bodu na dráze měsíce
    moonlist[0].pos = vector(*(
        moonlist[1][:, (int(-t / moonlist[3])) % n] +
        moonlist[2][:, (int(-t / moonlist[4])) % n]
    ))

    # Simulace slapové synchronizace (tidal locking) a rotace
    # Výpočet dvou po sobě jdoucích vektorů rychlostí pro určení úhlu rotace
    vel_vect0 = vector(
        *(moonlist[2][:, (int(-(t + dt) / moonlist[4])) % n] -
          moonlist[2][:, (int(-(t) / moonlist[4])) % n])
    )
    vel_vect1 = vector(
        *(moonlist[2][:, (int(-(t + 2 * dt) / moonlist[4])) % n] -
          moonlist[2][:, (int(-(t + dt) / moonlist[4])) % n])
    )
    v0n = norm(vel_vect0)
    v1n = norm(vel_vect1)
    try:
        cx = clip(v0n.dot(v1n), -1.0, 1.0)
        d1 = arccos(cx)
    except ImportError:
        # Pokud není numpy, úhel se nenastaví (mělo by být výjimečné)
        d1 = 0

    # Rotace měsíce (slapová synchronizace nebo klasická rotace)
    moonlist[0].rotate(
        angle=d1 * moonlist[7],  # moonlist[7] == lock (True/False/float)
        axis=vector(-sin(moonlist[5]), cos(moonlist[5]), 0)
    )
    return 0

def update_all_bodies(state):
    # Update planet a měsíců
    for planet in state.planets:
        update_planet(planet, state.t, state.dt, state.n)
    for moon in state.moons:
        update_moon(moon, state.t, state.dt, state.n)
    # Aktualizace prstenců
    if hasattr(state, "saturn_ring") and hasattr(state, "planets"):
        state.saturn_ring.pos = state.planets[6][0].pos
    if hasattr(state, "uranus_ring") and hasattr(state, "planets"):
        state.uranus_ring.pos = state.planets[7][0].pos
    # Fake obloha vždy na center
    if hasattr(state, "stars"):
        state.stars.pos = scene.camera.pos

def update_spaceship(state):
    s, v, a, predraw = ship(state.s0, state.v0, state.a0, state.dt, state.spaceship, state.predraw)
    state.s0, state.v0, state.a0, state.predraw = s, v, a, predraw
