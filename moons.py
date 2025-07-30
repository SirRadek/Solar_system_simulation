from dataclasses import dataclass
from math import pi
from typing import List

@dataclass
class Moon:
    a: float
    e: float
    inclination: float
    right_ascension: float
    mean_anomaly: float
    radius: float
    tilt: float
    spin: float
    texture: str
    period: float
    planet_name: str
    planet_num: int
    tidal_lock: int

ScaleMoon = 300

moon_list: List[Moon] = [
    Moon(384399 * 50., 0.0549, (-23.4 + 5.145) * pi / 180., -pi / 2., 0., 1737.1, 0.02691995838, 2 * pi / 708.7341666667, "textures/moon.jpg", 27.321, "Earth", 3, 1),
    Moon(9376 * 1000, 0.0151, 0, -pi / 2, 0., 11.2667 * 10, 0., 0, "textures/moon.jpg", 0.31891023, "Mars", 4, 1),
    # ... (doplníš z původního souboru dle potřeby)
]
