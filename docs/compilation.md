# Compilación y ejecución del Programa

Para compilar y ejecutar este proyecto se deben realizar las acciones mostradas acontinuación para cada una de las versiones.

## Versión de Python

### Ejecución
```
    python3 main.py
    python3 boltzmann.py
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

```
    g++ -c particle.cpp -o particle.o 
    g++ main.cpp particle.o -o particle.x -lglfw -lGL
    ./particle.x
```