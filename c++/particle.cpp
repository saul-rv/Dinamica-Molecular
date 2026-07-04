#include <random>
#include <array>
#include <cmath>

#include "particle.hpp"

Particle::Particle(){
  // Generates a non-deterministic number between 0.1 and 0.9
  // for the initial velocity and position
  std::random_device rd;
  std::mt19937 gen(rd());
  std::uniform_real_distribution<> dis(0.1, 0.9);

  pos = {dis(gen), dis(gen), dis(gen)};
  vel = {dis(gen), dis(gen), dis(gen)};
}

Particle::Particle(std::array<double,3> position){
  pos = position;

  // Generates a non-deterministic number between 0.2 and 1
  // as the initial velocity
  std::random_device rd;
  std::mt19937 gen(rd());
  std::uniform_real_distribution<> dis(0.2, 1.0);

  vel = {dis(gen), dis(gen), dis(gen)};
}

Particle::Particle(std::array<double,3> position, std::array<double,3> velocity){
  pos = position;
  vel = velocity;
}

void Particle::move(double dt){
  for (int i=0; i<3; i++){
    pos[i] += dt*vel[i];
  }
}

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

void colision(Particle &p1, Particle &p2){
  double a = 0.0;
  double b = 0.0;
  for (int i = 0; i<3; i++){
    a += (p1.vel[i] - p2.vel[i])*(p1.pos[i]-p2.pos[i]); // dx * dv
    b += (p1.pos[i] - p2.pos[i])*(p1.pos[i]-p2.pos[i]); // (dx)^2
  }

  // Particles are already moving away from each other,
  // no need to modify velocities
  if (a>0.0) return; 

  for (int i = 0; i<3; i++){
    p1.vel[i] -= (p1.pos[i]-p2.pos[i])*a/b;
    p2.vel[i] += (p1.pos[i]-p2.pos[i])*a/b;
  }
}

// Sqrt is slow, so we compare squared distances
double distanceSq(Particle &p1, Particle &p2){
  double dis = 0.0;
  for (int i = 0; i<3; i++){
    dis += (p1.pos[i]-p2.pos[i])*(p1.pos[i]-p2.pos[i]);
  }
  return dis;
}
