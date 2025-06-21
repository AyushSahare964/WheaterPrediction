🌪️ Wind Flow & Vorticity Visualizer

This Python project visualizes wind flow on a satellite map using wind inputs from the four cardinal directions. It calculates vorticity (ωz) to interpret weather conditions and shows animated particles simulating airflow.

🔍 Key Features
🌍 User-defined region on a satellite map

🧭 Wind input from North, South, East, and West

🌀 Calculates vertical vorticity (ωz)

📊 Interprets weather (e.g., cyclone, calm, high-pressure)

✨ Animated particles for wind movement

📍 Color-coded weather marker on map

📘 Concept: Vorticity
Vorticity (ωz) measures rotation in wind flow:

swift
Copy
Edit
ωz = (∂v/∂x) - (∂u/∂y)
It helps identify cyclones (positive), calm/stable zones (near-zero), and high-pressure areas (negative).

🛠️ Usage
Run the script:

bash
Copy
Edit
python wind_vorticity_visualizer.py
Input:

Region name, latitude & longitude

Wind speed (km/h), azimuth (θ), elevation (φ) for N, S, E, W

Grid spacing (dx, dy)

View:

Net wind vector and particles animation

Weather report based on vorticity

📦 Requirements

pip install matplotlib numpy cartopy
👨‍💻 Author
Created by Ayush Sahare
Inspired by real-time weather dynamics and fluid rotation concepts.
