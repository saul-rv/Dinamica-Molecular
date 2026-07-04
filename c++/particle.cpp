#include <random>
#include <array>
#include <cmath>

#include "particle.hpp"

Particle::Particle(){
  radius = 0.05;

  // Generates a non-deterministic number between 0.2 and 1
  // as the initial velocity
  std::random_device rd;
  std::mt19937 gen(rd());
  std::uniform_real_distribution<> dis(0.1, 0.9);

  pos = {dis(gen), dis(gen), dis(gen)};
  vel = {dis(gen), dis(gen), dis(gen)};
}

Particle::Particle(double R){
  radius = R;

  // Generates a non-deterministic number between 0.2 and 1
  // as the initial velocity
  std::random_device rd;
  std::mt19937 gen(rd());
  std::uniform_real_distribution<> dis(0.1, 0.9);

  pos = {dis(gen), dis(gen), dis(gen)};
  vel = {dis(gen), dis(gen), dis(gen)};
}

Particle::Particle(std::array<double,3> position){
  radius = 0.05;
  pos = position;

  // Generates a non-deterministic number between 0.2 and 1
  // as the initial velocity
  std::random_device rd;
  std::mt19937 gen(rd());
  std::uniform_real_distribution<> dis(0.2, 1.0);

  vel = {dis(gen), dis(gen), dis(gen)};
}

Particle::Particle(std::array<double,3> position, std::array<double,3> velocity){
  radius = 0.05;
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


