'''Verifica la conservación de energía cinética en la simulación.
En un sistema de colisiones elásticas, la energía cinética total del
sistema debe mantenerse constante en el tiempo. Este script corre la
simulación y grafica la energía total en cada paso para verificar que
la física esté correctamente implementada.
'''

from particle import Particle
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

code_dir = os.path.dirname(os.path.abspath(__file__))


def distance(particle1, particle2):
    return np.sqrt((particle1.posX - particle2.posX)**2
                  + (particle1.posY - particle2.posY)**2)


def colision(particle1, particle2):
    a = (particle1.velX - particle2.velX) * (particle1.posX - particle2.posX) \
        + (particle1.velY - particle2.velY) * (particle1.posY - particle2.posY)
    if a > 0:
        return
    b = (particle1.posX - particle2.posX)**2 + (particle1.posY - particle2.posY)**2

    particle1.velX -= (particle1.posX - particle2.posX) * a / b
    particle1.velY -= (particle1.posY - particle2.posY) * a / b
    particle2.velX -= (particle2.posX - particle1.posX) * a / b
    particle2.velY -= (particle2.posY - particle1.posY) * a / b


def total_kinetic_energy(particles, mass=1.0):
    """Suma la energia cinetica (1/2 * m * v^2) de todas las particulas."""
    return sum(0.5 * mass * (p.velX**2 + p.velY**2) for p in particles)


def run_energy_check(tf=20, dt=0.02):
    particles = [Particle([0.25, 0.25]), Particle([0.75, 0.75]),
                 Particle([0.25, 0.75]), Particle([0.75, 0.25])]

    t = 0
    times = [t]
    energies = [total_kinetic_energy(particles)]

    while t <= tf:
        t += dt
        for p in particles:
            p.move(dt)

        for i in range(len(particles)):
            for j in range(i + 1, len(particles)):
                if distance(particles[i], particles[j]) <= 2 * particles[i].radius:
                    colision(particles[i], particles[j])

        for p in particles:
            p.edgeColision()

        times.append(t)
        energies.append(total_kinetic_energy(particles))

    return times, energies


if __name__ == "__main__":
    times, energies = run_energy_check()

    e0 = energies[0]
    max_dev = max(abs(e - e0) for e in energies)
    print(f"Energia inicial: {e0:.6f}")
    print(f"Maxima desviacion respecto a la energia inicial: {max_dev:.6e}")

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(times, energies, color='steelblue')
    ax.set_xlabel('Tiempo', fontsize=12)
    ax.set_ylabel('Energia cinetica total', fontsize=12)
    ax.set_title('Conservacion de energia en la simulacion', fontsize=13)
    ax.set_ylim(bottom=0)
    plt.tight_layout()
    plt.savefig(os.path.join(code_dir, 'energy_conservation.png'), dpi=120)
    plt.close()
    print("Grafico guardado: energy_conservation.png")
