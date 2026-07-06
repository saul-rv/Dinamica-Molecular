import random

class Particle:
    """Particle to be simulated

    The class stores postions and velocities in x and y
    outside of a list for better performance.

    Atttibutes:
        posX: A float indicating the x position of the particle
        posY: A float indicating the y position of the particle
        velX: A float indicating the x velocity of the particle
        velY: A float indicating the y velocity of the particle
        radius: A float indicating the fixed radius of the particle
    """

    radius = 0.1
    def __init__(self, pos, vel=None):
        """Initializes the instance with an initial position and velocity.

        vel is initialized as None so that each particle can be assigned
        a different random velocity by default.

        Args:
            pos: List with initial position
            vel: List with initial velocity
        """
        self.posX = pos[0]
        self.posY = pos[1]

        if vel is None:
            vel = [random.random() for _ in range(2)]

        self.velX = vel[0]
        self.velY = vel[1]

    def move(self, dt):
        self.posX += dt*self.velX
        self.posY += dt*self.velY

    def edgeColision(self):
        """Checks for colision with edges."""
        if self.posX <= self.radius:
            self.velX = abs(self.velX)
        elif self.posX >= 1-self.radius:
            self.velX = -abs(self.velX)

        if self.posY <= self.radius:
            self.velY = abs(self.velY)
        elif self.posY >= 1-self.radius:
            self.velY = -abs(self.velY)
