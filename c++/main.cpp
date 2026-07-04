#include <iostream>
#include <vector>
#include <cmath>
#include <GLFW/glfw3.h>

#include "particle.hpp"

double distance(Particle& particle1, Particle& particle2){
  double dis = 0.0;
  for (int i = 0; i<3; i++){
    dis += (particle1.pos[i]-particle2.pos[i])*(particle1.pos[i]-particle2.pos[i]);
  }
  return std::sqrt(dis);
}

void colision(Particle& particle1, Particle& particle2){
  double a = 0.0;
  double b = 0.0;
  for (int i = 0; i<3; i++){
    a += (particle1.vel[i] - particle2.vel[i])*(particle1.pos[i]-particle2.pos[i]); // dx * dv
    b += (particle1.pos[i]-particle2.pos[i])*(particle1.pos[i]-particle2.pos[i]); // (dx)^2
  }

  // Particles are already moving away from each other,
  // no need to modify velocities
  if (a>0.0) return; 

  for (int i = 0; i<3; i++){
    particle1.vel[i] -= (particle1.pos[i]-particle2.pos[i])*a/b;
    particle2.vel[i] += (particle1.pos[i]-particle2.pos[i])*a/b;
  }

}

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
    drawSphere(p.pos[0], p.pos[1], p.pos[2], p.radius);
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
  if (!window) {
    std::cerr << "Error: no se pudo crear la ventana de GLFW." << std::endl;
    glfwTerminate();
    return -1;
  }
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

  int n = 500;
  std::vector<Particle> particles;
  particles.reserve(n);
  for (int i=0; i<n; i++){
      particles.emplace_back(0.01);
  }

  while (!glfwWindowShouldClose(window) && t <= tf){
    // std::cout << t << '\n';
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT); // Errase last frame
    setupCamera(t);					// Sets Scene
    drawBox();						// Draw Box
    drawParticles(particles); 				// Draw Particle
    glfwSwapBuffers(window); 				// Sync Window
    glfwPollEvents();	      				// =

    // TODO: Add spatial hashing
    for (int i=0; i<particles.size(); i++){
      for (int j=i+1; j<particles.size(); j++){
        if (distance(particles[i],particles[j]) <= 2*particles[i].radius){
          colision(particles[i],particles[j]);
        }
      }
    }

    for (int i=0; i<particles.size(); i++){
      particles[i].edgeColision();
    }

    for (int i=0; i<particles.size(); i++){
      particles[i].move(dt);
    }

    t += dt;
  }
  
  glfwTerminate(); // Cleans Glfw Library
  return 0;
}
