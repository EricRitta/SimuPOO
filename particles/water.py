from particles.base import Liquid

class Water(Liquid):
    def __init__(self):
        super().__init__(
            "Water",                                 # Particle Name 
            (70, 140, 255, 10),                      # Particle Color tuple[RED, GREEN, BLUE, VARIATION]
            1,                                       # Particle Density
            0.1,                                     # Particle Heat Transfer Rate
        )
