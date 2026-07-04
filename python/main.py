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


#Combined frames
def save_combined_frame(particles, t, speed_history, frame_num, output_dir=None):
    '''Saves a side-by-side frame: simulation panel (left) and speed histogram (right).

    The histogram grows as data accumulates throughout the simulation.
    A theoretical Maxwell-Boltzmann 2D (Rayleigh distribution) curve is
    overlaid once enough data points are available (> 10 samples).

    The 2D Maxwell-Boltzmann speed PDF is:
        f(v) = a · v · exp(−a · v² / 2)   with  a = 2 / <v²>

    Args:
        particles:     List of Particle objects
        t:             Current simulation time
        speed_history: All recorded speeds accumulated so far
        frame_num:     Frame index for filename ordering
        output_dir:    Folder where PNG files are saved
    '''
    if output_dir is None:
        output_dir = os.path.join(code_dir, 'frames')
    colors = ['green', 'orange', 'red', 'blue', 'purple', 'cyan']

    fig, (ax_sim, ax_hist) = plt.subplots(1, 2, figsize=(11, 5))

    #Sim
    ax_sim.set_xlim(0, 1)
    ax_sim.set_ylim(0, 1)
    ax_sim.set_aspect('equal')
    ax_sim.set_title(f't = {t:.2f}', fontsize=13)
    ax_sim.set_facecolor('#f5f5f5')
    for index, p in enumerate(particles):
        circle = plt.Circle((p.posX, p.posY), p.radius,
                             color=colors[index % len(colors)], alpha=0.85)
        ax_sim.add_patch(circle)
        vel = np.sqrt(p.velX**2 + p.velY**2)
        if vel > 1e-9:
            scale = p.radius / vel
            ax_sim.annotate('',
                            xy=(p.posX + scale*p.velX, p.posY + scale*p.velY),
                            xytext=(p.posX, p.posY),
                            arrowprops=dict(arrowstyle='->', color='black', lw=2))

    #Histo
    speeds = np.array(speed_history)
    ax_hist.set_xlabel('Rapidez |v|', fontsize=11)
    ax_hist.set_ylabel('Densidad de probabilidad', fontsize=11)
    ax_hist.set_title('Distribución de rapideces (acumulada)', fontsize=12)

    if len(speeds) > 1:
        ax_hist.hist(speeds, bins=20, color='tomato', edgecolor='white',
                     density=True, alpha=0.80, label='Datos simulados')
        #Maxwell-Boltzmann
        # f(v) = a·v·exp(−a·v²/2), a = 2/<v²>
        if len(speeds) > 10:
            v2_mean = np.mean(speeds**2)
            if v2_mean > 0:
                a_param = 2.0 / v2_mean
                v_range = np.linspace(0, speeds.max() * 1.15 + 0.01, 200)
                rayleigh = a_param * v_range * np.exp(-a_param * v_range**2 / 2)
                ax_hist.plot(v_range, rayleigh, 'b--', lw=2.2,
                             label='Maxwell-Boltzmann (2D)')

        ax_hist.legend(loc='upper right', fontsize=9)

    os.makedirs(output_dir, exist_ok=True)
    plt.tight_layout()
    plt.savefig(f'{output_dir}/frame_{frame_num:05d}.png', dpi=80)
    plt.close()

#Clear frames
frames_dir = os.path.join(code_dir, 'frames')
if os.path.exists(frames_dir):
    shutil.rmtree(frames_dir)

t = 0
tf = 20
dt = 0.02
particles = [Particle([0.25,0.25]), Particle([0.75,0.75]),
             Particle([0.25,0.75]), Particle([0.75,0.25])]
x_register = [p.posX for p in particles]

#History for CSV
speed_history = [np.sqrt(p.velX**2 + p.velY**2) for p in particles]
records = [(0.0, idx+1, p.posX, p.posY, p.velX, p.velY, spd)
           for idx, (p, spd) in enumerate(zip(particles, speed_history))]

frame_num = 0
save_combined_frame(particles, t, speed_history, frame_num)
 
print(f"{t:.2f}:")
print(f"p1 = {particles[0].posX},{particles[0].posY}")
print(f"p2 = {particles[1].posX},{particles[1].posY}")
 
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

    #Register
    for idx, p in enumerate(particles):
        spd = np.sqrt(p.velX**2 + p.velY**2)
        speed_history.append(spd)
        records.append((t, idx+1, p.posX, p.posY, p.velX, p.velY, spd))

    frame_num += 1
    save_combined_frame(particles, t, speed_history, frame_num)
 
    print(f"{t:.2f}:")
    print(f"p1 = {particles[0].posX},{particles[0].posY}")
    print(f"p2 = {particles[1].posX},{particles[1].posY}")
 
#Histogram
fig, ax = plt.subplots(figsize=(8, 5))
ax.hist(x_register, bins=20, color='steelblue', edgecolor='white', density=True)
ax.set_xlabel('Posición x', fontsize=12)
ax.set_ylabel('Densidad de probabilidad', fontsize=12)
ax.set_title('Histograma de posiciones en x de los centros de los discos', fontsize=13)
ax.set_xlim(0, 1)
plt.tight_layout()
plt.savefig(os.path.join(code_dir, 'histogram_pos_x.png'), dpi=120)
plt.close()
print("Histograma guardado: histogram_pos_x.png")

#Create CSV
csv_path = os.path.join(code_dir, 'results_python.csv')
with open(csv_path, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['t', 'particle', 'x', 'y', 'vx', 'vy', 'speed'])
    writer.writerows(records)
print(f"CSV guardado: results_python.csv  ({len(records)} filas)")
 
#GIF
paths = sorted(glob.glob(os.path.join(code_dir, 'frames', 'frame_*.png')))
frames_gif = [Image.open(p).convert('RGB') for p in paths]
frames_gif[0].save(os.path.join(code_dir, 'simulation.gif'), save_all=True,
                   append_images=frames_gif[1:], duration=dt*1000, loop=0)
print(f"Gif guardado: simulation.gif")
