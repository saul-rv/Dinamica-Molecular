from particle import Particle
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import csv
import glob
import shutil
from PIL import Image

code_dir = os.path.dirname(os.path.abspath(__file__))


def distance(particle1, particle2):
    '''Returns the distance between 2 particles

    Args:
        particle1: First particle
        particle1: Second particle
    '''
    return np.sqrt((particle1.posX-particle2.posX)**2
                  +(particle1.posY-particle2.posY)**2)


def colision(particle1, particle2):
    '''Modifies the velocity of 2 colliding particles

    The calculation is based on the equation found in:
    https://en.wikipedia.org/wiki/Elastic_collision#Two-dimensional_collision_with_two_moving_objects
    It additionally verifies that the particles are moving towards each other, and otherwise does not
    modify their velocities

    Args:
        particle1: First particle whose velocity to modify
        particle1: Second particle whose velocity to modify
    '''
    a = (particle1.velX-particle2.velX)*(particle1.posX-particle2.posX) \
        + (particle1.velY-particle2.velY)*(particle1.posY-particle2.posY)
    if a>0: return
    b = (particle1.posX-particle2.posX)**2 + (particle1.posY-particle2.posY)**2

    particle1.velX -= (particle1.posX-particle2.posX)*a/b
    particle1.velY -= (particle1.posY-particle2.posY)*a/b
    particle2.velX -= (particle2.posX-particle1.posX)*a/b
    particle2.velY -= (particle2.posY-particle1.posY)*a/b


def save_frame(particles, t, frame_num, output_dir=None):
    '''Saves the current system state as a PNG image.

    Draws each particle as a colored circle with a velocity arrow.

    Args:
        particles:  List of Particle objects
        t:          Current simulation time
        frame_num:  Frame index (used for filename ordering)
        output_dir: Folder where PNG files will be saved
    '''
    if output_dir is None:
        output_dir = os.path.join(code_dir, 'frames')
    colors = ['green', 'orange', 'red', 'blue', 'purple', 'cyan']

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect('equal')
    ax.set_title(f't = {t:.2f}', fontsize=14)
    ax.set_facecolor('#f5f5f5')

    for index, p in enumerate(particles):
        circle = plt.Circle((p.posX, p.posY), p.radius,
                             color=colors[index % len(colors)], alpha=0.85)
        ax.add_patch(circle)

        vel = np.sqrt(p.velX**2 + p.velY**2)
        if vel > 1e-9:
            scale = p.radius / vel
            ax.annotate('',
                        xy=(p.posX + scale*p.velX, p.posY + scale*p.velY),
                        xytext=(p.posX, p.posY),
                        arrowprops=dict(arrowstyle='->', color='black', lw=2))

    os.makedirs(output_dir, exist_ok=True)
    plt.tight_layout()
    plt.savefig(f'{output_dir}/frame_{frame_num:05d}.png', dpi=80)
    plt.close()

# Clear previous frames
frames_dir = os.path.join(code_dir, 'frames')
if os.path.exists(frames_dir):
    shutil.rmtree(frames_dir)

t = 0
tf = 20
dt = 0.02
particles = [Particle([0.25,0.25]), Particle([0.75,0.75]),
             Particle([0.25,0.75]), Particle([0.75,0.25])]
x_register = [p.posX for p in particles]

# Register data for CSV
records = [(0.0, idx+1, p.posX, p.posY, p.velX, p.velY,
            np.sqrt(p.velX**2 + p.velY**2))
           for idx, p in enumerate(particles)]

frame_num = 0
save_frame(particles, t, frame_num)

while (t <= tf):
    t += dt
    for p in particles:
        p.move(dt)

    # Runs over all pairs without duplicates
    for i in range(len(particles)):
        for j in range(i+1, len(particles)):
            if (distance(particles[i],particles[j]) <= 2*particles[i].radius):
                colision(particles[i],particles[j])

    for p in particles:
        p.edgeColision()

    for p in particles:
        x_register.append(p.posX)

    # Save data for CSV
    for idx, p in enumerate(particles):
        spd = np.sqrt(p.velX**2 + p.velY**2)
        records.append((t, idx+1, p.posX, p.posY, p.velX, p.velY, spd))

    frame_num += 1
    save_frame(particles, t, frame_num)

# Export CSV
csv_path = os.path.join(code_dir, 'results_python.csv')
with open(csv_path, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['t', 'particle', 'x', 'y', 'vx', 'vy', 'speed'])
    writer.writerows(records)
print(f"CSV saved: results_python.csv  ({len(records)} rows)")

# GIF
paths = sorted(glob.glob(os.path.join(code_dir, 'frames', 'frame_*.png')))
frames_gif = [Image.open(p).convert('RGB') for p in paths]
frames_gif[0].save(os.path.join(code_dir, 'simulation.gif'), save_all=True,
                   append_images=frames_gif[1:], duration=dt*1000, loop=0)
print(f"Gif saved: simulation.gif")
