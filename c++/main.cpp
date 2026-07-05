#include <iostream>
#include <vector>
#include <cmath>
#include <GLFW/glfw3.h>

#include "particle.hpp"
#include "graphics.hpp"

int main(){
  // Create all Graphics
  glfwInit();
  GLFWwindow* window = glfwCreateWindow(800, 600, "Sistema de Particulas", nullptr, nullptr);
  glfwMakeContextCurrent(window);
  glEnable(GL_DEPTH_TEST);
  glClearColor(0.92f, 0.92f, 0.92f, 1.0f);
  
  glEnable(GL_LIGHTING);
  glEnable(GL_LIGHT0);
  glEnable(GL_COLOR_MATERIAL);
 
  float lightPos[] = {2.0f, 2.0f, 3.0f, 1.0f};
  glLightfv(GL_LIGHT0, GL_POSITION, lightPos);

  double t = 0.0;
  double tf = 10.0;
  double dt = 0.01;

  int n = 25000;
  std::vector<Particle> particles;
  particles.reserve(n);
  for (int i=0; i<n; i++){
      particles.emplace_back();
  }

  std::array<int, 27> dxArray;
  int m = 0;
  for (int i=-1; i<=1; i++){
    for (int j=-1; j<=1; j++){
      for (int k=-1; k<=1; k++){
        dxArray[m] = i + j*lenGrid + k*lenGrid*lenGrid;
        m++;
      }
    }
  }

  std::vector<int> cellCount(lenGrid*lenGrid*lenGrid+1);
  std::vector<int> particleMap(n);

  while (!glfwWindowShouldClose(window) && t <= tf){
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT); // Errase last frame
    setupCamera(t);					// Sets Scene
    drawBox();						// Draw Box
    drawParticles(particles); 				// Draw Particle
    glfwSwapBuffers(window); 				// Sync Window
    glfwPollEvents();	      				// =

    std::fill(cellCount.begin(), cellCount.end(), 0);

    // Count particles in each cell
    for (Particle &p : particles){
      cellCount[p.gridPos] += 1;
    }

    // Compute the partial sum
    for (int i=1; i<cellCount.size(); i++){
      cellCount[i] += cellCount[i-1];
    }

    // Fill particle map
    for (int i=0; i<particles.size(); i++){
      cellCount[particles[i].gridPos] -= 1;
      particleMap[cellCount[particles[i].gridPos]] = i;
    }

    for (int i=0; i<particles.size(); i++){
      for (int dx : dxArray){
        int cell = particles[i].gridPos + dx;
        if (cell < 0 || cell >= lenGrid*lenGrid*lenGrid) continue;

        int nParticlesCell = cellCount[cell + 1] - cellCount[cell];
        if (nParticlesCell == 0) continue;

        for (int j=0; j<nParticlesCell; j++){
          int k = particleMap[cellCount[cell] + j];
          if (i<k && distanceSq(particles[i], particles[k]) <= 4*radius*radius){
            colision(particles[i], particles[k]);
          }
        }
      }
    }

    for (Particle &p : particles){
      p.edgeColision();
      p.move(dt);
    }

    t += dt;
  }
  
  glfwTerminate(); // Cleans Glfw Library
  return 0;
}
