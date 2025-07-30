
# Solar System Simulation 🌌

An interactive 3D simulation of the Solar System built with Python.

## 🧭 Overview

This project visualizes the Sun and planets of the Solar System in a dynamic 3D scene. Users can:

* Rotate, zoom in/out, and explore the Solar System in real time
* Observe planets orbiting the Sun and rotating around their own axes
* Switch between realistic and simplified scales (if implemented)

**Note:** Some scaling and orbital details are visually simplified for clarity and performance—this project is intended for educational and illustrative purposes, not for scientific accuracy.

## 🔧 Technologies

* **Three.js** – for 3D rendering (WebGL)
* HTML/CSS for layout and styling
* Vanilla JavaScript (ES6+) for simulation logic

## 🚀 Getting Started

1. **Clone the repository:**

   ```bash
   git clone https://github.com/SirRadek/Solar_system_simulation.git
   cd Solar_system_simulation
   ```

2. **Run locally:**

   * Open `index.html` directly in your web browser (Chrome/Firefox recommended).
   * *(Optional, if using a local server—e.g. for modules/assets)*
     If you use [live-server](https://www.npmjs.com/package/live-server) or similar:

     ```bash
     npm install
     npm start
     ```

     Then open `http://localhost:3000` in your browser.

## 🎮 Controls

| Action          | How to Use                                |
| --------------- | ----------------------------------------- |
| Rotate scene    | Left mouse button drag                    |
| Zoom in/out     | Mouse wheel or right mouse button drag    |
| View orbits     | Toggle orbit visualization (if available) |
| Change speed    | Slider or control panel (if implemented)  |
| Pause animation | Pause button or keyboard shortcut         |

*Adapt these to reflect your app’s actual controls.*

## 📂 Folder Structure

```
Solar_system_simulation/
├── index.html
├── css/
│   └── styles.css
├── js/
│   ├── scene.js
│   ├── planet.js
│   └── controls.js
├── assets/
│   ├── textures/
│   └── models/
└── README.md
```

*Adjust file/folder names to match your project structure!*

## 🎨 Data Sources & Credits

* Orbital and planetary data: Wikipedia and NASA datasets
* Textures: Public domain or credited sources (see `/assets/textures`)
* Inspired by various open-source solar system visualizations

## 🛠️ Possible Improvements

* Add moons (e.g. Earth’s Moon, Jupiter’s Io, etc.)
* More accurate elliptical orbits and axial tilts
* Asteroids, comets, and Kuiper Belt objects
* UI for simulation speed, scaling, or toggling planet info

