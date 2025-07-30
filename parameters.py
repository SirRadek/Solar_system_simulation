from vpython import vector, color, curve, sphere, box, cylinder, scene
from planets import planet_list, death_star_texture, saturn_ring_texture, uranus_ring_texture
from moons import moon_list
from inceptor import planet_ini, moon_ini
from constants import *

class SimulationState:
    def __init__(self):
        self.running: bool = True
        self.ScaleUp: int = SCALE_UP
        self.t: float = 0
        self.dt: float = 1
        self.n: int = N_ORBIT_COORDINATES
        self.f: int = VPYTHON_SIM_RATE

        # Vytvoření všech planet
        self.planets = [planet_ini(planet, self.n, self.ScaleUp) for planet in planet_list]
        # Vytvoření měsíců
        self.moons = [moon_ini(moon, self.planets, self.n, self.ScaleUp) for moon in moon_list]

        self.sw_lbl = False
        self.lbl_off = False
        self.ship_mode = False
        self.predraw = False
        self.u = SUN_GRAVITATIONAL_PARAMETER
        self.am = ACCELERATION_INCREMENT
        self.n_pred = 801
        self.t_pred = 200000
        self.times = None

        # Kosmická loď
        self.spaceship = sphere(
            radius=100000,
            trail=curve(color=color.white),
            texture=death_star_texture,
            color=vector(0.5, 0.5, 0.5)
        )
        self.s0 = vector(3e+7, -2e+6, 2e+8)
        self.v0 = vector(1000, 0, 0)
        self.a0 = vector(0, 0, 0)
        self.heading = vector(1, 0, 0)  # Výchozí směr (x-ová osa)
        self.maneuver_mode = False  # výchozí vypnutý mód
        # --- Pozadí – automatické přepínání poloměru podle vzdálenosti kamery ---

        self.stars = sphere(
            pos=scene.camera.pos,
            radius= 3503443661 * (-1),
            texture="textures/stars_milky_way.jpg",
            opacity=1  # Neprůhledné
        )
        # Žádné přepínání statusu a žádné negativní poloměry

        self.obj = self.planets[0]  # Výchozí objekt

        # Saturnův prstenec
        self.saturn_ring = cylinder(
            pos=self.planets[5][0].pos,
            axis=vector(0, 1, 0),
            radius=self.planets[5][0].radius + 90000 * self.ScaleUp,
            length=0.7 * self.ScaleUp,
            texture=saturn_ring_texture
        )
        # Uranův prstenec
        self.uranus_ring = cylinder(
            pos=self.planets[6][0].pos,
            axis=vector(0, 1, 0),
            radius=self.planets[6][0].radius + 35000 * self.ScaleUp,
            length=0.7 * self.ScaleUp,
            texture=uranus_ring_texture
        )