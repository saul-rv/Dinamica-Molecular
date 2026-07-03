cmake_minimum_required(VERSION 3.10)
project(ParticleSimulation CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(glfw3 REQUIRED)
find_package(OpenGL REQUIRED)

add_executable(main
    main.cpp
    particle.cpp
)

target_link_libraries(main
    glfw
    OpenGL::GL
)
