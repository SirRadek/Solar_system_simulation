# key_control.py
from numpy.random._examples.cffi.extending import state
from vpython import scene, label, vector, norm, cross, rate, mag
from parameters import ACCELERATION_INCREMENT
from wx import Exit
from math import sin, cos

lbl = label(text="    Simulation is paused. \n Press any key to continue.", visible=False, box=False)
pressed_keys = set()
latest_key = [None]
last_mouse_move = {'x': 0, 'y': 0}
last_mouse_pick = [None]

def rotate_vector(v, axis, angle_rad):
    axis = norm(axis)
    return v * cos(angle_rad) + cross(axis, v) * sin(angle_rad) + axis * (axis.dot(v)) * (1 - cos(angle_rad))

def keydown(evt):
    pressed_keys.add(evt.key)
    latest_key[0] = evt.key

def keyup(evt):
    pressed_keys.discard(evt.key)

def on_mouse_move(evt):
    try:
        last_mouse_move['x'] += evt.event.movementX
        last_mouse_move['y'] += evt.event.movementY
    except AttributeError:
        pass

def on_click(evt):
    last_mouse_pick[0] = scene.mouse.pick

scene.bind('keydown', keydown)
scene.bind('keyup', keyup)
scene.bind('mousemove', on_mouse_move)
scene.bind('click', on_click)

def handle_keyboard_and_mouse(state):
    key = latest_key[0]
    latest_key[0] = None

    # Myš: úhel pohledu lodi (pouze v režimu lodi)
    if getattr(state, "ship_mode", False):
        sensitivity = 0.003
        dx = last_mouse_move['x']
        dy = last_mouse_move['y']
        last_mouse_move['x'] = 0
        last_mouse_move['y'] = 0
        if not hasattr(state, "heading"):
            state.heading = vector(1, 0, 0)
        if abs(dx) > 0 or abs(dy) > 0:
            heading = state.heading
            heading = rotate_vector(heading, vector(0, 1, 0), -dx * sensitivity)  # YAW
            right = cross(heading, vector(0, 1, 0)).norm()
            heading = rotate_vector(heading, right, -dy * sensitivity)            # PITCH
            state.heading = heading.norm()

    # Manévrovací mód: [shift] = rychlejší akcelerace
    maneuver = 'shift' in pressed_keys or 'shiftleft' in pressed_keys or 'shiftright' in pressed_keys
    speed = ACCELERATION_INCREMENT * (20 if maneuver else 1)

    # 3D akcelerace lodi pouze šipkami
    if getattr(state, "ship_mode", False):
        acc = vector(0, 0, 0)
        heading = getattr(state, "heading", vector(1, 0, 0))
        upvec = vector(0, 1, 0)
        rightvec = cross(heading, upvec).norm()

        if 'up' in pressed_keys or 'up arrow' in pressed_keys:
            acc += speed * heading
        if 'down' in pressed_keys or 'down arrow' in pressed_keys:
            acc -= speed * heading
        if 'left' in pressed_keys or 'left arrow' in pressed_keys:
            acc -= speed * rightvec
        if 'right' in pressed_keys or 'right arrow' in pressed_keys:
            acc += speed * rightvec
        if 'page up' in pressed_keys:
            acc += speed * upvec
        if 'page down' in pressed_keys:
            acc -= speed * upvec
        state.a0 = acc

    # Ostatní klávesy (pauza, přepínání módů, trail...)
    if key is not None:
        if key == 'q' and 1 <= state.dt < 125:
            state.dt += 2
        elif key == 'q' and state.dt <= 0.95:
            state.dt += 0.05
        elif key == 'a' and state.dt > 1:
            state.dt -= 2
        elif key == 'a' and 0.2 < state.dt <= 1:
            state.dt -= 0.05
        elif key == ('esc', 'escape'):
            Exit()
        elif key == 'p':
            lbl.visible = True
            lbl.pos = scene.center
            import time
            while latest_key[0] is None:
                rate(100)
                time.sleep(0.01)
            latest_key[0] = None
            lbl.visible = False
        elif key == 'l':
            state.sw_lbl = not state.sw_lbl
            state.lbl_off = not state.lbl_off
        elif key == 's':
            state.ship_mode = not state.ship_mode
            state.a0 = vector(0, 0, 0)
            state.sw_lbl = True
            if not hasattr(state, "heading") or state.heading.mag < 1e-6:
                state.heading = vector(1, 0, 0)
            if state.ship_mode:
                # Kamera přesně na loď, na střed scény
                scene.center = state.spaceship.pos
                # Kamera orbit: 10x poloměr za lodí ve směru pohledu
                dist = 10 * state.spaceship.radius
                scene.camera.pos = state.spaceship.pos - dist * state.heading
                scene.camera.axis = dist * state.heading
            else:
                if hasattr(state.obj, "pos"):
                    scene.center = state.obj.pos
        elif key == 't':
            # Vypínání/zapínání trailů všech planet
            for p in getattr(state, "planets", []):
                if hasattr(p[0], "make_trail"):
                    p[0].make_trail = not p[0].make_trail
                    if not p[0].make_trail:
                        p[0].clear_trail()
        elif key == '0':
            state.a0 = vector(0, 0, 0)

    # Výběr objektu myší (pokud nejsme v módu lodi)
    if last_mouse_pick[0] and not getattr(state, "ship_mode", False):
        picked = last_mouse_pick[0]
        if picked is not None and hasattr(picked, "pos"):
            if picked is not state.stars:
                state.obj = picked
        last_mouse_pick[0] = None

    # Kamera (vždy v centru lodi v módu lodi)
    if getattr(state, "ship_mode", False):
        scene.center = state.spaceship.pos
        # Kamera sleduje loď a otáčí se kolem ní, vzdálenost lze měnit kolečkem myši
        direction = -getattr(state, "heading", vector(1, 0, 0))
        dist = mag(scene.camera.pos - scene.center)
        if dist < 2 * state.spaceship.radius:
            dist = 10 * state.spaceship.radius  # defaultně větší vzdálenost
        scene.camera.pos = state.spaceship.pos + direction * dist
        scene.camera.axis = -direction * dist
    elif hasattr(state.obj, "pos"):
        scene.center = state.obj.pos
