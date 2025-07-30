from vpython import sphere, curve, color, vector
from planets import Planet
from moons import Moon
from raphson import orbit
from constants import DIST_SCALE


def planet_ini(planet: Planet, n: int, scale_up: float):
    a = planet.a  # Velká poloosa dráhy planety [km]
    tilt = planet.tilt  # Sklon rotační osy planety [rad]
    timescale = (a / 149598261.0) ** 1.5  # Časový poměr oběhu vůči Zemi (pomocné pro simulaci)
    spin = 365.25 * 24 * planet.spin / n  # Rychlost rotace planety (úhel/počet kroků)

    # Výpočet bodů na oběžné dráze planety
    coord = orbit(
        planet.mean_anomaly,  # Střední anomálie [rad]
        planet.e,  # Excentricita dráhy
        a,  # Velká poloosa [km]
        planet.inclination,  # Sklon dráhy [rad]
        planet.right_ascension,  # Délka vzestupného uzlu [rad]
        n  # Počet bodů (kroků) na dráze
    )

    # Výpočet počáteční pozice planety (převedeno na měřítko modelu)
    initial_pos = vector(
        coord[0, 0] * DIST_SCALE,
        coord[1, 0] * DIST_SCALE,
        coord[2, 0] * DIST_SCALE
    )

    # Vytvoření koule reprezentující planetu
    celestial = sphere(
        radius=planet.radius * scale_up,  # Poloměr planety (v modelu)
        texture=planet.texture,  # Textura planety (obrázek)
        pos=initial_pos,  # Počáteční pozice planety
        make_trail=False,  # Bez kreslení dráhy za pohybu
        trail=curve(color=color.white)  # Objekt pro případné kreslení dráhy (zatím neaktivní)
    )
    celestial.rotate(angle=tilt, axis=vector(0, 0, 1))  # Počáteční natočení planety (sklon osy)

    # Vrací: objekt planety, souřadnice dráhy, časovou škálu, velkou poloosu, sklon, spin
    return [celestial, coord, timescale, a, tilt, spin]


# Podobné pro měsíc (moon)
def moon_ini(moon: Moon, planets, n: int, scale_up: float):
    tilt = moon.tilt  # Sklon rotační osy měsíce [rad]
    moonscale = moon.period / 365.25  # Poměr oběžné doby měsíce k roku
    spin = 365 * 24 * moon.spin / n  # Rychlost rotace měsíce (úhel/počet kroků)
    lock = moon.tidal_lock  # Je měsíc vázán slapovou silou? (True/False)

    # Získání objektu planety, kolem které měsíc obíhá
    planet_obj = planets[moon.planet_num][0] if isinstance(planets[moon.planet_num], list) else planets[moon.planet_num]
    planet_inclination = getattr(planet_obj, "inclination", 0.0)  # Sklon dráhy planety
    planet_coords = planets[moon.planet_num][1] if isinstance(planets[moon.planet_num],
                                                              list) else None  # Body dráhy planety
    planet_timescale = planets[moon.planet_num][2] if isinstance(planets[moon.planet_num],
                                                                 list) else None  # Časová škála planety

    # Výpočet bodů dráhy měsíce
    mooncoord = orbit(
        moon.mean_anomaly,  # Střední anomálie měsíce
        moon.e,  # Excentricita dráhy měsíce
        moon.a,  # Velká poloosa měsíce
        planet_inclination + moon.inclination,  # Celkový sklon dráhy (planeta + měsíc)
        moon.right_ascension,  # Délka vzestupného uzlu měsíce
        n  # Počet bodů na dráze
    )

    # Výpočet počáteční pozice měsíce (vůči aktuální pozici planety)
    initial_pos = vector(
        mooncoord[0, 0] + planet_obj.pos.x,
        mooncoord[1, 0] + planet_obj.pos.y,
        mooncoord[2, 0] + planet_obj.pos.z
    )

    # Vytvoření koule reprezentující měsíc
    celestial = sphere(
        radius=moon.radius * scale_up,  # Poloměr měsíce v modelu
        texture=moon.texture,  # Textura měsíce (obrázek)
        pos=initial_pos,  # Počáteční pozice měsíce
        make_trail=False  # Bez kreslení dráhy
    )

    # Vrací: objekt měsíce, body dráhy planety, body dráhy měsíce, časovou škálu planety, poměr oběhu, sklon, spin, zámek rotace
    return [celestial, planet_coords, mooncoord, planet_timescale, moonscale, tilt, spin, lock]
