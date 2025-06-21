import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.cm import get_cmap
from matplotlib.colors import Normalize
import cartopy.crs as ccrs
import cartopy.io.img_tiles as cimgt

# Function to input wind vector (correcting for 'from' direction)
def input_vector(name):
    V_kmph = float(input(f"{name} wind speed (in km/h): "))
    theta_deg = float(input(f"{name} azimuth θ (degrees from east, counterclockwise): "))
    phi_deg = float(input(f"{name} elevation φ (in degrees): "))

    # Convert speed to m/s and angles to radians
    V = V_kmph * (1000 / 3600)
    theta = math.radians((theta_deg + 180) % 360)
    phi = math.radians(phi_deg)

    u = V * math.cos(phi) * math.cos(theta)
    v = V * math.cos(phi) * math.sin(theta)
    w = V * math.sin(phi)
    return (u, v, w)

# --- Inputs ---
region_name = input("Enter region name: ")
center_lon = float(input("Enter region center longitude (e.g., 80.0): "))
center_lat = float(input("Enter region center latitude (e.g., 25.0): "))

print("\nEnter wind data for 4 cardinal directions:")
V_north = input_vector("North")
V_south = input_vector("South")
V_east  = input_vector("East")
V_west  = input_vector("West")#54.78° S, 88.80° E

dx_km = float(input("\ndx (east-west spacing in km): "))
dy_km = float(input("dy (north-south spacing in km): "))
dx = dx_km * 1000
dy = dy_km * 1000

# Extract components
uN, vN, _ = V_north
uS, vS, _ = V_south
uE, vE, _ = V_east
uW, vW, _ = V_west

# Vorticity calculation
du_dy = (uN - uS) / (2 * dy)
dv_dx = (vE - vW) / (2 * dx)
omega_z = dv_dx - du_dy
omega_str = f"{omega_z:.6e} s⁻¹"

# Weather interpretation
if omega_z > 0.0001:
    report = f"ωz = {omega_str} → High positive vorticity → Possible cyclone, tornado, or turbulence."
    color = 'red'
elif 0.00001 < omega_z <= 0.0001:
    report = f"ωz = {omega_str} → Moderate vorticity → Rain, thunderstorms, or frontal activity."
    color = 'orange'
elif -0.00001 <= omega_z <= 0.00001:
    report = f"ωz = {omega_str} → Near-zero vorticity → Calm or stable weather conditions."
    color = 'green'
else:
    report = f"ωz = {omega_str} → Negative vorticity → Clear skies, high-pressure zones likely."
    color = 'blue'

# Net wind vector
u = (uN + uS + uE + uW) / 4
v = (vN + vS + vE + vW) / 4

# --- Satellite Map Setup ---
tiler = cimgt.QuadtreeTiles()
zoom = 8
fig = plt.figure(figsize=(12, 8))
ax = plt.axes(projection=tiler.crs)
ax.set_extent([center_lon - 2, center_lon + 2, center_lat - 2, center_lat + 2])
ax.add_image(tiler, zoom)

# Wind vector arrow (with fix for scalar inputs)
ax.quiver(np.array([center_lon]), np.array([center_lat]),
          np.array([u]), np.array([v]),
          scale=50, color='white', label='Wind Flow',
          transform=ccrs.PlateCarree())

# Location marker as a pin and label
ax.scatter(center_lon, center_lat, color=color, s=150, edgecolor='black',
           marker='v', label='Location 📍', transform=ccrs.PlateCarree(), zorder=5)

# 📍 Region name label
ax.text(center_lon, center_lat + 0.2, f"📍 {region_name}", fontsize=13,
        fontweight='bold', color='white', ha='center', transform=ccrs.PlateCarree())

# Weather report
plt.figtext(0.5, 0.01, f"Weather Report for {region_name}: {report}",
            ha='center', fontsize=12, wrap=True, color='black',
            bbox=dict(facecolor='white', alpha=0.8, boxstyle="round"))

plt.title("Satellite View - Wind Flow and Weather Condition", fontsize=15)
plt.legend(loc='upper right')

# --- Particle Wind Animation ---
num_particles = 200
lon_min, lon_max = center_lon - 2, center_lon + 2
lat_min, lat_max = center_lat - 2, center_lat + 2

# Randomly initialized particle positions
particles_lon = np.random.uniform(lon_min, lon_max, num_particles)
particles_lat = np.random.uniform(lat_min, lat_max, num_particles)

# Particle velocity initialized to zero (no initial speed)
particles_u = np.zeros(num_particles)
particles_v = np.zeros(num_particles)

# Add turbulence factor to velocities
turbulence_factor = 0.05  # Controls the strength of random turbulence
wind_speed = math.sqrt(u**2 + v**2)
speed_scale = 0.0002

# Set particle initial velocities in the wind direction
particles_u = u + turbulence_factor * np.random.randn(num_particles)  # Small random deviation
particles_v = v + turbulence_factor * np.random.randn(num_particles)

# Normalizing the wind's effect
particles_u *= speed_scale
particles_v *= speed_scale

# Particle color normalization for visual effect
norm = Normalize(vmin=0, vmax=20)
cmap = get_cmap('plasma')
color = cmap(norm(wind_speed))

# Scatter plot for particles
particles = ax.scatter(particles_lon, particles_lat, s=2, color=color,
                       transform=ccrs.PlateCarree(), label='Wind Particles')

def update_particles(frame):
    global particles_lon, particles_lat, particles_u, particles_v
    
    # Update positions with velocity, including random perturbation
    particles_lon += particles_u
    particles_lat += particles_v

    # Introduce random fluctuation (turbulence) for each step
    particles_u += turbulence_factor * np.random.randn(num_particles)
    particles_v += turbulence_factor * np.random.randn(num_particles)

    # Boundary conditions (particles re-entering the map after moving out)
    out_of_bounds = (particles_lon < lon_min) | (particles_lon > lon_max) | \
                    (particles_lat < lat_min) | (particles_lat > lat_max)
    
    particles_lon[out_of_bounds] = np.random.uniform(lon_min, lon_max, np.sum(out_of_bounds))
    particles_lat[out_of_bounds] = np.random.uniform(lat_min, lat_max, np.sum(out_of_bounds))

    # Update particle positions
    particles.set_offsets(np.c_[particles_lon, particles_lat])
    return particles,

# Create the animation
ani = FuncAnimation(fig, update_particles, frames=200, interval=50, blit=False)

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()
