#include <random>
#include <array>
#include <cmath>

#include "particle.hpp"

namespace {
  // Generates a non-deterministic number
  // for the initial velocity and position
  // Separated into a namespace to make it
  // shared among particles
  std::random_device rd;
  std::mt19937 gen(rd());
  std::uniform_real_distribution<> disPos(0.1, 0.9);
  std::uniform_real_distribution<> disVel(-1, 1);
}

Particle::Particle(){
  pos = {disPos(gen), disPos(gen), disPos(gen)};
  vel = {disVel(gen), disVel(gen), disVel(gen)};

  calculateGridPos();
}

Particle::Particle(std::array<double,3> position){
  pos = position;
  vel = {disVel(gen), disVel(gen), disVel(gen)};

  calculateGridPos();
}

Particle::Particle(std::array<double,3> position, std::array<double,3> velocity){
  pos = position;
  vel = velocity;
  calculateGridPos();
}

int cellIndex(double coord){
  int index = std::floor(coord/(2*radius));
  if (index < 0) index = 0;
  if (index >= lenGrid) index = lenGrid - 1;
  return index;
}

void Particle::calculateGridPos(){
  gridPos = lenGrid*lenGrid*cellIndex(pos[0]) + lenGrid*cellIndex(pos[1]) + cellIndex(pos[2]);
}

void Particle::move(double dt){
  for (int i=0; i<3; i++){
    pos[i] += dt*vel[i];
  }
  calculateGridPos();
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

  // Randomly positioned particles can get very close,
  // stops them from exploding
  if (b < 1e-8) b = 1e-8;

  double c = a/b;

  for (int i = 0; i<3; i++){
    p1.vel[i] -= (p1.pos[i]-p2.pos[i])*c;
    p2.vel[i] += (p1.pos[i]-p2.pos[i])*c;
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
