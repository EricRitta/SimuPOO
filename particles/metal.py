from particles.base import ImmovableSolid

class Metal(ImmovableSolid):
    ORDER = 3
    NAME = "Metal"
    IMAGE_COLOR = (100, 100, 100)
    CONCRETE = True

    def __init__(self):
        super().__init__(
            (100, 100, 100, 5),                      # Particle Color tuple[RED, GREEN, BLUE, VARIATION]
            6,                                       # Particle Density
            2.0,                                     # Particle Heat Capacity
            0.15,                                     # Particle Heat Conductivity
        )
