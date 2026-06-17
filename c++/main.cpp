#include <iostream>
#include <cmath>

#include "particle.hpp"

double distance(Particle particle1, Particle particle2){
  double dis = 0;
  for (int i = 0; i<3; i++){
    dis += (particle1.pos[i]-particle2.pos[i])*(particle1.pos[i]-particle2.pos[i]);
  }
  return std::sqrt(dis);
}

void colision(Particle particle1, Particle particle2){
  double a = 0;
  double b = 0;
  for (int i = 0; i<3; i++){
    a += (particle1.vel[i] - particle2.vel[i])*(particle1.pos[i]-particle2.pos[i]);
    b += (particle1.pos[i]-particle2.pos[i])*(particle1.pos[i]-particle2.pos[i]);
  }

  // Particles are already moving away from each other,
  // no need to modify velocities
  if (a>0) return; 

  for (int i = 0; i<3; i++){
    particle1.vel[i] -= (particle1.pos[i]-particle2.pos[i])*a/b;
    particle2.vel[i] -= (particle1.pos[i]-particle2.pos[i])*a/b;
  }

}


int main(){
  double t = 0;
  double tf = 10;
  double dt = 0.01;

  std::array<Particle, 8> particles = {
    Particle({0.25,0.25,0.25}),
    Particle({0.25,0.25,0.75}),
    Particle({0.25,0.75,0.25}),
    Particle({0.25,0.75,0.75}),
    Particle({0.75,0.25,0.25}),
    Particle({0.75,0.25,0.75}),
    Particle({0.75,0.75,0.25}),
    Particle({0.75,0.75,0.75}),
  };

  while (t <= tf){
    std::cout << t << '\n';
    // TODO: Draw Particles


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

  return 0;
}
