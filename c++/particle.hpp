#ifndef PARTICLE_HPP
#define PARTICLE_HPP

#include <array>

class Particle {
  private:
    // Where do I place it?
    Particle();
  public:
    double radius;

    // Arrays since size is fixed
    std::array<double,3> pos;
    std::array<double,3> vel;

    Particle(std::array<double,3> pos);
    Particle(std::array<double,3> pos, std::array<double,3> vel);

    void move(double dt);
    void edgeColision();
};

#endif
