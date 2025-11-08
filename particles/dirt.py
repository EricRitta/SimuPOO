import random
from particles.base import MovableSolid

class Dirt(MovableSolid):
    def __init__(self):
        super().__init__(
            "Dirt",                                 # Particle Name 
            (180, 145, 90, 10),                    # Particle Color tuple[RED, GREEN, BLUE, VARIATION]
            3,                                      # Particle Density
            1.0,                                    # Particle Heat Capacity (maior = mais resistencia ao hea)
            0.2,                                   # Particle Heat Conductivity (maior = mais perda de calor)
        )
        if random.randint(1, 10) == 1:
            self._COLOR = (
                max(0, min(255, 150 + random.randint(-10, 10))),
                max(0, min(255, 150 + random.randint(-10, 10))),
                max(0, min(255, 150 + random.randint(-10, 10)))
            )
