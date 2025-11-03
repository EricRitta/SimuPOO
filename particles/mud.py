import random
from utils import Vector2
from particles.base import MovableSolid

class Mud(MovableSolid):
    def __init__(self):
        super().__init__(
            "Mud",                                  # Particle Name 
            (110, 100, 70, 15),                     # Particle Color tuple[RED, GREEN, BLUE, VARIATION]
            3,                                      # Particle Density
            0.1,                                    # Particle Heat Transfer Rate
        )
