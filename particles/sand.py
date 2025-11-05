from particles.base import MovableSolid

class Sand(MovableSolid):
    def __init__(self):
        super().__init__(
            "Sand",                                 # Particle Name 
            (195, 180, 130, 15),                    # Particle Color tuple[RED, GREEN, BLUE, VARIATION]
            3,                                      # Particle Density
            1.0,                                    # Particle Heat Capacity (maior = mais resistencia ao hea)
            0.2,                                   # Particle Heat Conductivity (maior = mais perda de calor)
        )

