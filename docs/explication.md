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

# Solución del Problema


