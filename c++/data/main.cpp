#include <iostream>
#include <fstream>
#include <vector>
#include <cmath>

#include "particle.hpp"

int main(){
  double t =  0.0;
  double tf = 2.1;
  double dt = 0.01;

  int n = 25000;
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

  std::ofstream csv;
  csv.open("results_c++.csv");
  csv << "t,particle,x,speed\n";

  m = 0;
  while (t <= tf){
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

    if (m%10 == 0){
      for (int i=0; i<particles.size(); i++){
        double speed = 0;
        for (int j=0;j<3;j++){
          speed += particles[i].vel[j]*particles[i].vel[j];
        }
        csv << t << ',' << i+1 << ',' << particles[i].pos[0] 
            << ',' << std::sqrt(speed) << '\n';
      }
    }

    m++;
    t += dt;
  }

  csv.close();
  return 0;
}
