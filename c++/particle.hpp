#ifndef PARTICLE_HPP
#define PARTICLE_HPP

#include <array>

class Particle {
  public:
    double radius;

    // Arrays since size is fixed
    std::array<double,3> pos;
    std::array<double,3> vel;

    Particle(); // Random position and velocity
    Particle(double r); // Random position and velocity
    Particle(std::array<double,3> pos); // Random Velocity
    Particle(std::array<double,3> pos, std::array<double,3> vel);

    void move(double dt);
    void edgeColision();
};

#endif
