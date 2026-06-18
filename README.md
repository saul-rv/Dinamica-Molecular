# Dinámica Molecular en Dos Dimensiones: Discos Sólidos

### Integrantes:

* Saúl Rodríguez Víquez - C5J102
* Mauro Cerdas Flores - C31960
* César Arce Gómez - C30621

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


