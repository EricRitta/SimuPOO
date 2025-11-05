import random
from utils import Vector2
from particles.base import MovableSolid

class Mud(MovableSolid):
    def __init__(self):
        super().__init__(
            "Mud",                                  # Particle Name 
            (110, 100, 70, 15),                     # Particle Color tuple[RED, GREEN, BLUE, VARIATION]
            3,                                      # Particle Density
            1.2,                                    # Particle Heat Capacity
            0.15,                                   # Particle Heat Conductivity
        )
