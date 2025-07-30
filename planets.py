# planets.py
from dataclasses import dataclass
from math import pi
from typing import List

@dataclass
class Planet:
    a: float  # Semimajor axis [km]
    e: float  # Eccentricity
    inclination: float  # Inclination [rad]
    right_ascension: float  # Longitude of ascending node [rad]
    mean_anomaly: float  # Mean anomaly [rad]
    radius: float  # Radius [km]
    tilt: float  # Axial tilt [rad]
    spin: float  # Rotation period [rad/hour]
    texture: str  # Texture file path
    name: str

planet_list: List[Planet] = [
    Planet(742000.0, 0.0001, 7.25 * pi / 180, 0.0, 0.0, 696340.0 / 20, 7.25 * pi / 180, 2 * pi / 587.28, "textures/sun.jpg", "Sun"),
    Planet(57909050., 0.205630, 7 * pi / 180., 0.8436854966, 3.0507657193, 2439.7, 0.1 * pi / 180., 2 * pi / 4222.6, "textures/mercury.jpg", "Mercury"),
    Planet(108208000., 0.0067, 3.39 * pi / 180., 1.3381895772, 0.8746717546, 6051.8, 177 * pi / 180., -2 * pi / 2802., "textures/venus.jpg", "Venus"),
    Planet(149598261., 0.01671123, 0., 0., 6.2398515744, 6371., 23 * pi / 180., 2 * pi / 24., "textures/earth.jpg", "Earth"),
    Planet(227939100., 0.093315, 1.85 * pi / 180., 0.8676591934, 0.3378329113, 3389.5, 25 * pi / 180., 2 * pi / 24.66, "textures/mars.jpg", "Mars"),
    Planet(778547200., 0.048775, 1.31 * pi / 180., 1.7504400393, 0.3284360586, 69911., 3 * pi / 180., 2 * pi / 9.93, "textures/jupiter.jpg", "Jupiter"),
    Planet(1433449370., 0.055723219, 2.49 * pi / 180., 1.98, 5.5911055356, 58232., 27 * pi / 180., 2 * pi / 10.66, "textures/saturn.jpg", "Saturn"),
    Planet(2876679082., 0.044405586, 0.77 * pi / 180., 1.2908891856, 2.4950479462, 25362., 98 * pi / 180., -2 * pi / 17.24, "textures/uranus.jpg", "Uranus"),
    Planet(4503443661., 0.011214269, 1.77 * pi / 180., 2.3001058656, 4.6734206826, 24622., 30 * pi / 180., 2 * pi / 16.11, "textures/neptune.jpg", "Neptune")
]

# Special textures
stars_texture = "textures/stars_milky_way.jpg"
death_star_texture = "textures/death_star.jpg"
saturn_ring_texture = "textures/saturn_ring.png"
uranus_ring_texture = "textures/uranus_ring.png"
