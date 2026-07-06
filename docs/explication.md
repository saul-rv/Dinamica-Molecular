# Enunciado del Problema

Utilizando las ecuaciones de cinemática, elabore un programa en dos dimensiones con 4 discos sólidos de radio $r$ que se mueven sin fricción ni momento angular dentro de una caja de longitud unitaria. A estos discos se les puede asociar una energía cinetica inicial aleatoria, resultando así en una distribución de velocidades aleatoria para el sistema.

Milestones:

- Implementar la solución en Python.
- Inicializar el sistema a partir de posiciones conocidas y una distribucion de velocidades aleatoria.
- Elaborar subrutinas que evalúan si los discos chocan con la pared o chocan entre ellos (choques a pares) y a la vez calculen las nuevas velocidades (magnitud y dirección) y posiciones del sistema. Considere que no se pierde energía en estos choques.
- Determinar cuál es el evento más próximo a suceder (ya sea colisión con pared o colisión a pares) y en qué momento se da.
- Mover todos los discos la distancia correspondiente a este tiempo y evaluar de nuevo cuándo es el siguiente choque dentro del sistema de nuevo.
- Visualizar por medio de matplotlib la posición de cada uno de los discos dentro de la caja y guardar el correspondiente archivo para realizar una película al final del calculo.
- Aumentar el número de discos presentes, así como también poder variar el radio $r$ de los discos.
- Elaborar un histograma de las posiciones de los centros de los discos a lo largo del eje $x$.

# Fundamentos

**Toda la mate y fisica para resolver, analisis y ecuaciones**

# Solución del Problema

En primer lugar, se establece las clase **Particle** la cual contiene el estado de cada disco y sus métodos físicos

Teniendo el objeto de estudio definido, el **Main** se encarga de llevar a cabo la simulación completa. 

## Condiciones Iniciales

Para el caso de estudio se establece el número de particulas en $N = 4$ y se designan sus posiciones dentro de la caja:

|Particula|Posición|
|:---:|:---:|
|1|[0.25, 0.25]|
|2|[0.75, 0.75]|
|3|[0.25, 0.75]|
|4|[0.75, 0.25]|

El siguiente paso es determinar las velocidades iniciales para cada particula, cada una de estas debe de ser independiente y generada aleatoriamente, esto se implemento mediante la función:

|Lenguaje|FunciónS|
|:---:|:---:|
|Python|**random.random()**|
|C++|**a**|

## Rutinas

Al tener las condiciones iniciales del sistema establecidas, lo siguiente es determinar las rutinas para **Detectar** y **Resolver** las colisiones que sucedan dentro de la caja, ya sea contra las paredes o entre las particulas.

### Colisión entre paredes

#### Python - edgeColision():

La clase Particle verifica, para cada componente espacial, si el disco ha alcanzado o sobrepasado el límite de la caja considerando su radio. Al detectarse una colisión, la componente de velocidad perpendicular a la pared se invierte tomando su valor absoluto, lo cual garantiza que el disco siempre se aleje de la pared independientemente de si llegó exactamente al límite o lo cruzó ligeramente por efecto del paso de tiempo discreto.

```
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
```

#### C++ - 

### Colisión entre discos

#### Python - colision():

Calcula las nuevas velocidades de dos discos que se solapan. El algoritmo primero verifica que los discos se estén acercando, si el producto punto entre la diferencia de velocidades y la diferencia de posiciones es positivo, las partículas ya se están separando y no se modifica ninguna velocidad. De lo contrario, se aplica la fórmula de colisión elástica bidimensional

```
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
```

#### C++ - 

## Visualización

## Distribución de Velocidades

En dos dimensiones, la distribución de la rapidez escalar $v = |v| = \sqrt(vx²+vy²)$ resulta ser la distribución de Rayleigh, que es el caso bidimensional de la distribución de Maxwell-Boltzmann:

$$
f(v) = a · v · \exp(\frac{-a · v^2}{2}), \qquad con \quad a = \frac{2}{<v^2>}
$$

```
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
```