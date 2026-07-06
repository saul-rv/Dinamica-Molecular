import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd
import os
import sys

codeDir = os.path.dirname(os.path.abspath(__file__))

if len(sys.argv) > 1:
    csvPath = os.path.join(codeDir, sys.argv[1])
else:
    csvPath = os.path.join(codeDir, 'results_python.csv')

if not os.path.exists(csvPath):
    print(f"Error: '{csvPath}' not found")
    sys.exit(1)

data = pd.read_csv(csvPath)

unique_times = data['t'].unique()
speeds_by_time = data.groupby('t')['speed'].apply(list).to_dict()

anim_times = unique_times[::10] 

cumulative = []
frame_data = []

for t_val in unique_times:
    cumulative.extend(speeds_by_time[t_val])
    if t_val in anim_times:
       frame_data.append((t_val, np.array(cumulative, dtype=float)))

# Animation
fig, ax = plt.subplots(figsize=(8, 5))

def update(frame_idx):
    t_val, speeds = frame_data[frame_idx]
    ax.clear()

    ax.hist(speeds, bins=20, color='tomato', edgecolor='white',
            density=True, alpha=0.80, label='Simulated data (2D)')

    ax.set_xlabel('Speed |v|', fontsize=11)
    ax.set_ylabel('Probability density', fontsize=11)
    ax.set_title(f'Distribución de las velocidades — t = {t_val:.2f}', fontsize=12)
    ax.legend(loc='upper right', fontsize=10)

ani = animation.FuncAnimation(fig, update, frames=len(frame_data), blit=False)
gif_path = os.path.join(codeDir, 'boltzmann.gif')
ani.save(gif_path, writer='pillow', fps=10)
plt.close(fig)
print(f"  GIF saved: boltzmann.gif  ({len(frame_data)} frames)")

# Final Speed Distribution
fig, ax = plt.subplots(figsize=(8, 5))

ax.hist(data['speed'],
        bins=25, color='tomato', edgecolor='white',
        density=True, alpha=0.80, label='Simulated data (2D)')
ax.set_xlabel('Rapidez |v|', fontsize=12)
ax.set_ylabel('Densidad de Probabilidad', fontsize=12)
ax.set_title('Distribución de rapideces final', fontsize=13)
ax.legend(fontsize=11)
plt.tight_layout()

static_path = os.path.join(codeDir, 'boltzmann_static.png')
plt.savefig(static_path, dpi=120)
plt.close(fig)
print(f"  Graphic saved: boltzmann_static.png")

# X Position Histogram
fig, ax = plt.subplots(figsize=(8, 5))

ax.hist(data['x'], bins=20, color='steelblue', edgecolor='white', density=True)
ax.set_xlabel('Posición en el eje x', fontsize=12)
ax.set_ylabel('Densidad de Probabilidad', fontsize=12)
ax.set_title('Histograma de posiciones en x de los centros de los discos', fontsize=13)
ax.set_xlim(0, 1)
plt.tight_layout()

pos_x_path = os.path.join(codeDir, 'histogram_pos_x.png')
plt.savefig(pos_x_path, dpi=120)
plt.close(fig)
print("  Histograma guardado: histogram_pos_x.png")
