# Enunciado del Problema

Utilizando las ecuaciones de cinemática, elabore un programa en dos dimensiones con 4 discos sólidos de radio $r$ que se mueven sin fricción ni momento angular dentro de una caja de longitud unitaria. A estos discos se les puede asociar una energía cinetica inicial aleatoria, resultando así en una distribución de velocidades aleatoria para el sistema.

Milestones:

- Implementar la solución en Python.
- Inicializar el sistema a partir de posiciones conocidas y una distribucion de velocidades aleatoria.
- Elaborar subrutinas que evalúan si los discos chocan con la pared o chocan entre ellos (choques a pares) y a la vez calculen las nuevas velocidades (magnitud y dirección) y posiciones del sistema. Considere que no se pierde energía en estos choques.
- Visualizar por medio de matplotlib la posición de cada uno de los discos dentro de la caja y guardar el correspondiente archivo para realizar una película al final del calculo.
- Aumentar el número de discos presentes, así como también poder variar el radio $r$ de los discos.
- Elaborar un histograma de las posiciones de los centros de los discos a lo largo del eje $x$.

# Fundamentos

Para la simulación, se supone que las partículas se pueden modelar utilizando las ecuaciones de cinemática.
Mientras estas no colisionan, se supone que se mueven a velocidad constante:
$$
x(t) = x_0 + v_xt
$$
Y análogamente en las demás dimensiones. Las partículas se mueven en intervalos de tiempo $dt$ y para revisar
colisiones constantemente. Con las paredes, las colisiones se suponen elásticas, por lo que
únicamente la dirección de las velocidades es modificada (invertida en la dirección perpendicular a la colisión).
Para las colisiones entre partículas, la conservación de la energía y del momentum llevan al resultado:
$$
\textbf{v}'_1 = \textbf{v}_1 - \frac{2m_2}{m_1+m_2} \frac{(\textbf{v}_1-\textbf{v}_2)\cdot(\textbf{x}_1-\textbf{x}_2)}{|\textbf{x}_1-\textbf{x}_2|^2} (\textbf{x}_1 - \textbf{x}_2 )
$$
$$
\textbf{v}'_2 = \textbf{v}_2 - \frac{2m_1}{m_1+m_2} \frac{(\textbf{v}_2-\textbf{v}_1)\cdot(\textbf{x}_2-\textbf{x}_1)}{|\textbf{x}_2-\textbf{x}_1|^2} (\textbf{x}_1 - \textbf{x}_2 )
$$

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

#### Python:

La clase Particle verifica, para cada componente espacial, si el disco ha alcanzado o sobrepasado el límite de la caja considerando su radio. Al detectarse una colisión, la componente de velocidad perpendicular a la pared se invierte tomando su valor absoluto, lo cual garantiza que el disco siempre se aleje de la pared independientemente de si llegó exactamente al límite o lo cruzó ligeramente por efecto del paso de tiempo discreto.

```python
def edgeColision(self):
        if self.posX <= self.radius:
            self.velX = abs(self.velX)
        elif self.posX >= 1-self.radius:
            self.velX = -abs(self.velX)

        if self.posY <= self.radius:
            self.velY = abs(self.velY)
        elif self.posY >= 1-self.radius:
            self.velY = -abs(self.velY)
```

#### C++:
```c++
void Particle::edgeColision(){
  for (int i=0; i<3; i++){
    if (pos[i] <= radius){
      vel[i] = std::abs(vel[i]);
    }
    else if (pos[i] >= 1-radius){
      vel[i] = -std::abs(vel[i]);
    }
  }
}
```

### Colisión entre discos

#### Python:

Calcula las nuevas velocidades de dos discos que se solapan. El algoritmo primero verifica que los discos se estén acercando, si el producto punto entre la diferencia de velocidades y la diferencia de posiciones es positivo, las partículas ya se están separando y no se modifica ninguna velocidad. De lo contrario, se aplica la fórmula de colisión elástica bidimensional
```python
def colision(particle1, particle2):
    a = (particle1.velX-particle2.velX)*(particle1.posX-particle2.posX) \
        + (particle1.velY-particle2.velY)*(particle1.posY-particle2.posY)
    if a>0: return
    b = (particle1.posX-particle2.posX)**2 + (particle1.posY-particle2.posY)**2

    particle1.velX -= (particle1.posX-particle2.posX)*a/b
    particle1.velY -= (particle1.posY-particle2.posY)*a/b
    particle2.velX -= (particle2.posX-particle1.posX)*a/b
    particle2.velY -= (particle2.posY-particle1.posY)*a/b
```

#### C++:
```c++
void Particle::edgeColision(){
  for (int i=0; i<3; i++){
    if (pos[i] <= radius){
      vel[i] = std::abs(vel[i]);
    }
    else if (pos[i] >= 1-radius){
      vel[i] = -std::abs(vel[i]);
    }
  }
}
```

## Visualización

## Distribución de Velocidades

En dos dimensiones, la distribución de la rapidez escalar $v = |v| = \sqrt(vx²+vy²)$ resulta ser la distribución de Rayleigh, que es el caso bidimensional de la distribución de Maxwell-Boltzmann:

$$
f(v) = a · v · \exp(\frac{-a · v^2}{2}), \qquad con \quad a = \frac{2}{<v^2>}
$$

```python
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