#include <iostream>
#include <vector>
#include <cmath>
#include <GLFW/glfw3.h>

#include "particle.hpp"

// Draw Sphere for particle
void drawSphere(float cx, float cy, float cz, float r) {
  const int stacks = 12;
  const int slices = 24;

  for (int i = 0; i < stacks; i++) {
    float lat0 = M_PI * (-0.5f + (float)i / stacks);
    float lat1 = M_PI * (-0.5f + (float)(i + 1) / stacks);

    float z0 = std::sin(lat0);
    float zr0 = std::cos(lat0);

    float z1 = std::sin(lat1);
    float zr1 = std::cos(lat1);

    glBegin(GL_QUAD_STRIP);

    for (int j = 0; j <= slices; j++) {
      float lng = 2.0f * M_PI * (float)j / slices;

      float x = std::cos(lng);
      float y = std::sin(lng);

      glNormal3f(x * zr0, y * zr0, z0);
      glVertex3f(cx + r * x * zr0, cy + r * y * zr0, cz + r * z0);

      glNormal3f(x * zr1, y * zr1, z1);
      glVertex3f(cx + r * x * zr1, cy + r * y * zr1, cz + r * z1);
    }

    glEnd();
  }
}

// Draw particle with glfw
void drawParticles(const std::vector<Particle>& particles){
  glPointSize(18.0f); // Size 
  glColor3f(0.1f, 0.8f, 1.0f); // Color
  
  for (const Particle& p : particles){
    drawSphere(p.pos[0], p.pos[1], p.pos[2], radius);
  }
}

// Tells How to show 3d space in a 2d screen
void setupCamera(double t){
  glMatrixMode(GL_PROJECTION);
  glLoadIdentity();

  glOrtho(-0.5, 1.5, -0.5, 1.5, -5.0, 5.0);

  glMatrixMode(GL_MODELVIEW);
  glLoadIdentity();

  glTranslatef(0.5f, 0.5f, -1.5f);    // Moves Scene
  glRotatef(25.0f, 1.0f, 0.0f, 0.0f); // Rotates 25 degrees in X
  glRotatef(t * 5.0f + 45.0f, 0.0f, 1.0f, 0.0f); // Rotates 45 degrees in Y
  glTranslatef(-0.5f, -0.5f, -0.5f);  // Moves Scene
}

void drawBox() {
  glColor3f(0.0f, 0.0f, 0.0f);
  glLineWidth(2.0f);

  glBegin(GL_LINES);

  // Bottom face z = 0
  glVertex3f(0, 0, 0); glVertex3f(1, 0, 0);
  glVertex3f(1, 0, 0); glVertex3f(1, 1, 0);
  glVertex3f(1, 1, 0); glVertex3f(0, 1, 0);
  glVertex3f(0, 1, 0); glVertex3f(0, 0, 0);

  // Top face z = 1
  glVertex3f(0, 0, 1); glVertex3f(1, 0, 1);
  glVertex3f(1, 0, 1); glVertex3f(1, 1, 1);
  glVertex3f(1, 1, 1); glVertex3f(0, 1, 1);
  glVertex3f(0, 1, 1); glVertex3f(0, 0, 1);

  // Vertical lines
  glVertex3f(0, 0, 0); glVertex3f(0, 0, 1);
  glVertex3f(1, 0, 0); glVertex3f(1, 0, 1);
  glVertex3f(1, 1, 0); glVertex3f(1, 1, 1);
  glVertex3f(0, 1, 0); glVertex3f(0, 1, 1);

  glEnd();
}

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

  int n = 5000;
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
