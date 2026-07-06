# Compilación y ejecución del Programa

Para compilar y ejecutar este proyecto se deben realizar las acciones mostradas acontinuación para cada una de las versiones.

## Versión de Python

### Ejecución
```
    python3 main.py
    python3 boltzmann.py
```
El script boltzmann.py también se puede utilizar de manera independiente para analizar otro archivo .csv:
```
    python3 boltzmann.py example.csv
```
## Versión de C++

### Instalacion de dependencias OpenGL

En Arch / CachyOS:

```
    sudo pacman -S glfw mesa
```

En Debian / Ubuntu / Linux Mint:

```
    sudo apt update
    sudo apt install libglfw3-dev libgl1-mesa-dev
```

### Compilacion

Versión gráfica (c++/graphics)
```
    g++ -c particle.cpp -c graphics.cpp -O3
    g++ main.cpp *.o -o particle.x -lglfw -lGL -O3
    ./particle.x
```
Versión datos, produce un csv con las velocidades y posiciones (c++/data)
```
    g++ -c particle.cpp -O3
    g++ main.cpp *.o -o particle.x -lglfw -lGL -O3
    ./particle.x
```