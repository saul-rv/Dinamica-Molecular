#ifndef PARTICLE_HPP
#define PARTICLE_HPP

#include <cmath>
#include <array>

const double radius = 0.003;
const int lenGrid = std::ceil(0.5/radius);

class Particle {
  public:

    // Arrays since size is fixed
    std::array<double,3> pos;
    std::array<double,3> vel;

    int gridPos;

    Particle(); // Random position and velocity
    Particle(std::array<double,3> pos); // Random Velocity
    Particle(std::array<double,3> pos, std::array<double,3> vel);

    void calculateGridPos();
    void move(double dt);
    void edgeColision();
};

void colision(Particle &p1, Particle &p2);
double distanceSq(Particle &p1, Particle &p2);

#endif
