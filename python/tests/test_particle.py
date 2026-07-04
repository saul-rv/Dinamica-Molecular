"""Pruebas unitarias para la clase Particle."""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from particle import Particle


def test_move_updates_position_correctly():
    p = Particle([0.5, 0.5], vel=[1.0, 2.0])
    p.move(dt=0.1)
    assert abs(p.posX - 0.6) < 1e-9
    assert abs(p.posY - 0.7) < 1e-9


def test_move_with_zero_velocity_stays_still():
    p = Particle([0.3, 0.3], vel=[0.0, 0.0])
    p.move(dt=1.0)
    assert p.posX == 0.3
    assert p.posY == 0.3


def test_edge_collision_bounces_off_left_wall():
    p = Particle([0.05, 0.5], vel=[-1.0, 0.0])
    p.edgeColision()
    assert p.velX > 0  # debe rebotar hacia la derecha


def test_edge_collision_bounces_off_right_wall():
    p = Particle([0.95, 0.5], vel=[1.0, 0.0])
    p.edgeColision()
    assert p.velX < 0  # debe rebotar hacia la izquierda


def test_edge_collision_bounces_off_bottom_wall():
    p = Particle([0.5, 0.05], vel=[0.0, -1.0])
    p.edgeColision()
    assert p.velY > 0


def test_edge_collision_bounces_off_top_wall():
    p = Particle([0.5, 0.95], vel=[0.0, 1.0])
    p.edgeColision()
    assert p.velY < 0


def test_edge_collision_no_change_when_away_from_walls():
    p = Particle([0.5, 0.5], vel=[1.0, -1.0])
    p.edgeColision()
    assert p.velX == 1.0
    assert p.velY == -1.0


def test_speed_is_conserved_after_edge_collision():
    """El rebote no debe cambiar la magnitud de la velocidad, solo su signo."""
    p = Particle([0.05, 0.5], vel=[-2.0, 0.0])
    speed_before = (p.velX**2 + p.velY**2) ** 0.5
    p.edgeColision()
    speed_after = (p.velX**2 + p.velY**2) ** 0.5
    assert abs(speed_before - speed_after) < 1e-9
