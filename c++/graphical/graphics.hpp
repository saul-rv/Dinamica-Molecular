#ifndef GRAPHICS_HPP
#define GRAPHICS_HPP

#include "particle.hpp"
#include <vector>

void drawSphere(float cx, float cy, float cz, float r);
void drawParticles(const std::vector<Particle>& particles);
void setupCamera(double t);
void drawBox();

#endif
