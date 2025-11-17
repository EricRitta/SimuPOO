from particles.base import ImmovableSolid

class ColdAdd(ImmovableSolid):
    ORDER = 999
    NAME = "ColdAdd"
    IMAGE_NAME = "Diminuir Temperatura"
    IMAGE_COLOR = (0, 0, 255)
    DESCRIPTION = [
        "Usado para diminuir a",
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
