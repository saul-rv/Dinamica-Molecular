"""Simulacion de dinamica molecular por eventos discretos.

A diferencia de main.py (que avanza en pasos de tiempo fijos), esta
version calcula el instante exacto del proximo evento -- choque con
pared o choque entre dos discos -- y avanza el sistema exactamente
esa cantidad de tiempo antes de resolver la colision. Esto evita
traslapes y aproximaciones del metodo de paso fijo.

Tambien permite variar la cantidad de discos y su radio.
"""

import math
import random
import os
import glob
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image

from particle import Particle

code_dir = os.path.dirname(os.path.abspath(__file__))


def initial_positions(n, radius):
    """Coloca n particulas sin traslape mediante muestreo por rechazo."""
    positions = []
    max_tries = 10000
    for _ in range(n):
        for _ in range(max_tries):
            x = random.uniform(radius, 1 - radius)
            y = random.uniform(radius, 1 - radius)
            if all(math.hypot(x - px, y - py) > 2 * radius for px, py in positions):
                positions.append((x, y))
                break
        else:
            raise RuntimeError(
                "No se pudo colocar todas las particulas sin traslape; "
                "reduzca N o el radio."
            )
    return positions


def time_to_wall(p):
    """Tiempo hasta que la particula p choque con una pared, y el eje."""
    tx = math.inf
    if p.velX < 0:
        tx = (p.radius - p.posX) / p.velX
    elif p.velX > 0:
        tx = (1 - p.radius - p.posX) / p.velX

    ty = math.inf
    if p.velY < 0:
        ty = (p.radius - p.posY) / p.velY
    elif p.velY > 0:
        ty = (1 - p.radius - p.posY) / p.velY

    return (tx, 'x') if tx <= ty else (ty, 'y')


def time_to_pair(p1, p2):
    """Tiempo hasta que dos particulas colisionen entre si (o inf)."""
    dx = p1.posX - p2.posX
    dy = p1.posY - p2.posY
    dvx = p1.velX - p2.velX
    dvy = p1.velY - p2.velY

    dvdr = dx * dvx + dy * dvy
    if dvdr >= 0:
        return math.inf  # se estan alejando

    dvdv = dvx**2 + dvy**2
    if dvdv == 0:
        return math.inf

    drdr = dx**2 + dy**2
    sigma = p1.radius + p2.radius
    d = dvdr**2 - dvdv * (drdr - sigma**2)
    if d < 0:
        return math.inf  # no van a chocar

    t = -(dvdr + math.sqrt(d)) / dvdv
    return t if t > 0 else math.inf


def resolve_pair_collision(p1, p2):
    """Aplica la formula de colision elastica (misma fisica que main.py)."""
    dx = p1.posX - p2.posX
    dy = p1.posY - p2.posY
    dvx = p1.velX - p2.velX
    dvy = p1.velY - p2.velY

    a = dvx * dx + dvy * dy
    b = dx**2 + dy**2

    p1.velX -= dx * a / b
    p1.velY -= dy * a / b
    p2.velX += dx * a / b
    p2.velY += dy * a / b


def save_frame(particles, t, frame_num, output_dir):
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

    os.makedirs(output_dir, exist_ok=True)
    plt.tight_layout()
    plt.savefig(f'{output_dir}/frame_{frame_num:05d}.png', dpi=80)
    plt.close()


def run(n_particles=4, radius=0.1, tf=20, frame_dt=0.05):
    positions = initial_positions(n_particles, radius)
    particles = [Particle(list(pos), radius=radius) for pos in positions]

    output_dir = os.path.join(code_dir, 'frames_event_driven')
    current_time = 0.0
    next_frame_time = 0.0
    frame_num = 0
    x_register = []

    save_frame(particles, current_time, frame_num, output_dir)
    frame_num += 1

    while current_time < tf:
        # Tiempo al proximo choque con pared, por particula
        wall_times = [time_to_wall(p) for p in particles]

        # Tiempo al proximo choque entre cada par
        pair_times = {}
        for i in range(len(particles)):
            for j in range(i + 1, len(particles)):
                pair_times[(i, j)] = time_to_pair(particles[i], particles[j])

        best_wall_t = min((t for t, _ in wall_times), default=math.inf)
        best_pair_t = min(pair_times.values(), default=math.inf)
        t_event = min(best_wall_t, best_pair_t, tf - current_time)

        # Guarda frames intermedios a intervalos regulares para la pelicula
        while next_frame_time <= current_time + t_event and next_frame_time <= tf:
            dt_frame = next_frame_time - current_time
            for p in particles:
                p.posX += dt_frame * p.velX
                p.posY += dt_frame * p.velY
            save_frame(particles, next_frame_time, frame_num, output_dir)
            for p in particles:
                x_register.append(p.posX)
            frame_num += 1
            current_time = next_frame_time
            t_event -= dt_frame
            next_frame_time += frame_dt

        # Avanza el resto hasta el evento y lo resuelve
        for p in particles:
            p.posX += t_event * p.velX
            p.posY += t_event * p.velY
        current_time += t_event

        if current_time >= tf:
            break

        if best_wall_t <= best_pair_t:
            idx = next(i for i, (t, _) in enumerate(wall_times) if t == best_wall_t)
            axis = wall_times[idx][1]
            if axis == 'x':
                particles[idx].velX *= -1
            else:
                particles[idx].velY *= -1
        else:
            (i, j) = next(k for k, t in pair_times.items() if t == best_pair_t)
            resolve_pair_collision(particles[i], particles[j])

    # Histograma de posiciones en x
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist(x_register, bins=20, color='steelblue', edgecolor='white', density=True)
    ax.set_xlabel('Posicion x', fontsize=12)
    ax.set_ylabel('Densidad de probabilidad', fontsize=12)
    ax.set_title('Histograma de posiciones en x (simulacion por eventos)', fontsize=13)
    ax.set_xlim(0, 1)
    plt.tight_layout()
    plt.savefig(os.path.join(code_dir, 'histogram_pos_x_event_driven.png'), dpi=120)
    plt.close()

    # Gif
    paths = sorted(glob.glob(os.path.join(output_dir, 'frame_*.png')))
    frames_gif = [Image.open(p).convert('RGB') for p in paths]
    frames_gif[0].save(os.path.join(code_dir, 'simulation_event_driven.gif'),
                        save_all=True, append_images=frames_gif[1:],
                        duration=frame_dt * 1000, loop=0)

    print("Listo: histogram_pos_x_event_driven.png y simulation_event_driven.gif generados.")


if __name__ == "__main__":
    # Parametros ajustables: numero de discos y radio
    run(n_particles=6, radius=0.08, tf=20)
