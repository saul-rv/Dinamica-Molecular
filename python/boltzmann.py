"""
boltzmann.py — Distribución de Maxwell-Boltzmann (2D)
══════════════════════════════════════════════════════

Read results_python.csv and generate:

  · boltzmann.gif        →  histogram animated 
  · boltzmann_static.png →  final results histogram

The 2D Maxwell-Boltzmann distribution for speed v is the Rayleigh distribution:

    f(v) = a · v · exp(−a · v² / 2)   con  a = 2 / <v²>

'a' is estimated directly from the accumulated data of each frame..

Execute:
    python3 boltzmann.py

Requirement: main.py must be executed first to generate results_python.csv.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import csv
import os
import sys
from collections import defaultdict

code_dir = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(code_dir, 'results_python.csv')


# Verify CSV file exists
if not os.path.exists(CSV_PATH):
    print(f"Error: not found'{CSV_PATH}'")
    print("Execute main.py first to generate the CSV file.")
    sys.exit(1)

# Read CSV 
speeds_by_time = defaultdict(list)
with open(CSV_PATH, 'r', newline='') as f:
    reader = csv.DictReader(f)
    for row in reader:
        speeds_by_time[float(row['t'])].append(float(row['speed']))
unique_times  = sorted(speeds_by_time.keys())
total_records = sum(len(v) for v in speeds_by_time.values())


# Create frames for the animation
step       = max(1, len(unique_times) // 100)
anim_times = set(unique_times[::step])

cumulative = []
frame_data = []

for t_val in unique_times:
    cumulative.extend(speeds_by_time[t_val])
    if t_val in anim_times:
        frame_data.append((t_val, np.array(cumulative, dtype=float)))

# Maxwell-Boltzmann 2D
def mb_2d(v, v2_mean):
    """Maxwell-Boltzmann in 2 dimensions (Rayleigh distribution).

    f(v) = a · v · exp(−a · v² / 2)   con  a = 2 / <v²>

    Args:
        v:       array of speed values
        v2_mean: estimated mean of v²

    Returns:
        Array values of the Maxwell-Boltzmann distribution
    """
    if v2_mean <= 0:
        return np.zeros_like(v)
    a = 2.0 / v2_mean
    return a * v * np.exp(-a * v**2 / 2)


# Gif
fig, ax = plt.subplots(figsize=(8, 5))

def update(frame_idx):
    t_val, speeds = frame_data[frame_idx]
    ax.clear()

    ax.hist(speeds, bins=20, color='tomato', edgecolor='white',
            density=True, alpha=0.80, label='Simulated data (2D)')

    v2_mean = np.mean(speeds**2)
    if v2_mean > 0:
        v_max   = speeds.max() * 1.15 + 0.01
        v_range = np.linspace(0, v_max, 200)
        ax.plot(v_range, mb_2d(v_range, v2_mean), 'b--', lw=2.2,
                label='Maxwell-Boltzmann theoretical (2D)')

    ax.set_xlabel('Speed |v|', fontsize=11)
    ax.set_ylabel('Probability density', fontsize=11)
    ax.set_title(f'Maxwell-Boltzmann distribution — t = {t_val:.2f}', fontsize=12)
    ax.legend(loc='upper right', fontsize=10)
    return []

ani      = animation.FuncAnimation(fig, update, frames=len(frame_data), blit=False)
gif_path = os.path.join(code_dir, 'boltzmann.gif')
ani.save(gif_path, writer='pillow', fps=10)
plt.close(fig)
print(f"  GIF saved: boltzmann.gif  ({len(frame_data)} frames)")


# Graphic static final values
all_speeds = np.array(cumulative, dtype=float)
v2_mean    = np.mean(all_speeds**2)
v_max      = all_speeds.max() * 1.15
v_range    = np.linspace(0, v_max, 300)

fig, ax = plt.subplots(figsize=(8, 5))
ax.hist(all_speeds, bins=25, color='tomato', edgecolor='white',
        density=True, alpha=0.80, label='Simulated data (2D)')
ax.plot(v_range, mb_2d(v_range, v2_mean), 'b--', lw=2.5,
        label='Maxwell-Boltzmann theoretical (2D)')
ax.set_xlabel('Speed |v|', fontsize=12)
ax.set_ylabel('Probability density', fontsize=12)
ax.set_title('Maxwell-Boltzmann distribution — (2D, 4 particles)', fontsize=13)
ax.legend(fontsize=11)
plt.tight_layout()
static_path = os.path.join(code_dir, 'boltzmann_static.png')
plt.savefig(static_path, dpi=120)
plt.close(fig)
print(f"  Graphic saved: boltzmann_static.png")
