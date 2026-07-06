# Dinámica Molecular en Dos Dimensiones: Discos Sólidos

### Integrantes:

* Saúl Rodríguez Víquez - C5J102
* Mauro Cerdas Flores - C31960
* César Arce Gómez - C30621
* Dayana Murillo Guzmán - C5H759

---

## Compilation

Hay que correr los siguientes comandos para compilar el proyecto

### Intalacion de dependencias OpenGL

En Arch / CachyOS:

```bash
sudo pacman -S glfw mesa
```

En Debian / Ubuntu / Linux Mint:

```bash
sudo apt update
sudo apt install libglfw3-dev libgl1-mesa-dev
```
## Compilacion

```bash
g++ -c particle.cpp -o particle.o 
g++ main.cpp particle.o -o particle.x -lglfw -lGL
./particle.x
```
### Compilación alternativa con CMake

También se puede compilar usando CMake, que gestiona las dependencias de forma más simple:

```bash
cd c++
mkdir build && cd build
cmake ..
make
./main
```

---

## Simulación en Python (2D)

Se instalan las dependencias:

```bash
pip install -r python/requirements.txt
```

Se ejecuta la simulación:

```bash
python python/main.py
```

Esto genera `python/frames/` con las imágenes de cada paso, `python/simulation.gif` con la animación completa, y `python/histogram_pos_x.png` con el histograma de posiciones.
