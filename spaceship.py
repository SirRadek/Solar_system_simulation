


def ship(s, v, a, dt, spaceship, predraw):
    v += a * dt
    s += v * dt
    spaceship.pos = s
    try:
        spaceship.trail.append(pos=s, retain=2000)
    except AttributeError:
        pass
    return s, v, a, predraw

