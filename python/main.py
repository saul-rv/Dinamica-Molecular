from particle import Particle
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os
import csv

code_dir = os.path.dirname(os.path.abspath(__file__))

def distance(particle1, particle2):
    '''Returns the distance between 2 particles

    Args:
        particle1: First particle
        particle1: Second particle
    '''
    return np.sqrt((particle1.posX-particle2.posX)**2
                  +(particle1.posY-particle2.posY)**2)


def collision(particle1, particle2):
    '''Modifies the velocity of 2 colliding particles

    The calculation is based on the equation found in:
    <https://en.wikipedia.org/wiki/Elastic_collision#Two-dimensional_collision_with_two_moving_objects>.
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

t = 0
tf = 20
dt = 0.02
particles = [Particle([0.25,0.25]), Particle([0.75,0.75]),
             Particle([0.25,0.75]), Particle([0.75,0.25])]

 
# Register data for CSV
records = [(0.0, idx+1, p.posX, p.posY, p.velX, p.velY,
            np.sqrt(p.velX**2 + p.velY**2))
           for idx, p in enumerate(particles)]

# Snapshot list for animation
snapshots = [(t, [(p.posX, p.posY, p.velX, p.velY) for p in particles])]

print(f"{t:.2f}:")
print(f"p1 = {particles[0].posX},{particles[0].posY}")
print(f"p2 = {particles[1].posX},{particles[1].posY}")

while (t <= tf):
while t <= tf:
    t += dt
    for p in particles:
        p.move(dt)

    # Runs over all pairs without duplicates
    for i in range(len(particles)):
        for j in range(i+1, len(particles)):
            if distance(particles[i],particles[j]) <= particles[i].radius + particles[j].radius: 
                collision(particles[i],particles[j])

    for p in particles:
        p.edgeColision()

    for idx, p in enumerate(particles):
            spd = np.sqrt(p.velX**2 + p.velY**2)
            records.append((t, idx+1, p.posX, p.posY, p.velX, p.velY, spd))

    snapshots.append((t, [(p.posX, p.posY, p.velX, p.velY) for p in particles]))

    print(f"{t:.2f}:")
    print(f"p1 = {particles[0].posX},{particles[0].posY}")
    print(f"p2 = {particles[1].posX},{particles[1].posY}")

# Export CSV
csv_path = os.path.join(code_dir, 'results_python.csv')
with open(csv_path, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['t', 'particle', 'x', 'y', 'vx', 'vy', 'speed'])
    writer.writerows(records)
print(f"CSV saved: results_python.csv  ({len(records)} rows)")

# Animation
fig, ax = plt.subplots(figsize=(6, 6))
colors = ['green', 'orange', 'red', 'blue', 'purple', 'cyan']
 
def draw_frame(frame):
    t_frame, states = snapshots[frame]
    ax.cla()
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect('equal')
    ax.set_title(f't = {t_frame:.2f}', fontsize=14)
    ax.set_facecolor('#f5f5f5')
    for i, (posX, posY, velX, velY) in enumerate(states):
        ax.add_patch(plt.Circle((posX, posY), particles[i].radius,
                                color=colors[i % len(colors)], alpha=0.85))
        vel = np.sqrt(velX**2 + velY**2)
        if vel > 1e-9:
            scale = particles[i].radius / vel
            ax.annotate('',
                        xy=(posX + scale*velX, posY + scale*velY),
                        xytext=(posX, posY),
                        arrowprops=dict(arrowstyle='->', color='black', lw=2))
 
ani = animation.FuncAnimation(fig, draw_frame, frames=len(snapshots),
                               interval=dt * 1000)
ani.save(os.path.join(code_dir, 'simulation.gif'), writer='pillow')
print("GIF saved: simulation.gif")
