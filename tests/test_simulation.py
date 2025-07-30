# tests/test_simulation.py
from planets import planet_list, sun_texture, stars_texture, death_star_texture, saturn_ring_texture, uranus_ring_texture
from moons import moon_list
import os

def test_planet_textures():
    for planet in planet_list:
        assert os.path.exists(planet.texture), f"Missing texture: {planet.texture}"

def test_special_textures():
    for tex in [sun_texture, stars_texture, death_star_texture, saturn_ring_texture, uranus_ring_texture]:
        assert os.path.exists(tex), f"Missing texture: {tex}"

def test_moon_textures():
    for moon in moon_list:
        assert os.path.exists(moon.texture), f"Missing texture: {moon.texture}"

def run_all_tests():
    test_planet_textures()
    test_special_textures()
    test_moon_textures()
    print("All texture tests passed!")

if __name__ == "__main__":
    run_all_tests()
