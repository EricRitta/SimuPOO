from particles.base import ImmovableSolid

class HeatAdd(ImmovableSolid):
    ORDER = 999
    NAME = "HeatAdd"
    IMAGE_NAME = "Aumentar Temperatura"
    IMAGE_COLOR = (255, 0, 0)
    DESCRIPTION = [
        "Usado para aumentar a",
        "Temperatura",
    ]
    CONCRETE = True

    def __init__(self):
        super().__init__(
            (0, 0, 0, 0),                      # Particle Color tuple[RED, GREEN, BLUE, VARIATION]
            6,                                       # Particle Density
            2.0,                                     # Particle Heat Capacity
            0.15,                                    # Particle Heat Conductivity
        )
