from particles.base import ImmovableSolid

class Metal(ImmovableSolid):
    def __init__(self):
        super().__init__(
            "Metal",                                 # Particle Name 
            (100, 100, 100, 5),                      # Particle Color tuple[RED, GREEN, BLUE, VARIATION]
            6,                                       # Particle Density
            0.1,                                     # Particle Heat Transfer Rate
        )
