from particles.base import ImmovableSolid

class Steel(ImmovableSolid):
    ORDER = 3
    NAME = "Steel"
    IMAGE_NAME = "Aço"
    IMAGE_COLOR = (100, 100, 100)
    CONCRETE = True

    def __init__(self):
        super().__init__(
            (100, 100, 100, 5),                      # Particle Color tuple[RED, GREEN, BLUE, VARIATION]
            6,                                       # Particle Density
            2.0,                                     # Particle Heat Capacity
            0.15,                                    # Particle Heat Conductivity
        )
        self.MELTING_POINT = 1300.0

    def tempChanged(self, WORLD, position):
        if self.Temperature > self.MELTING_POINT:
            molten = WORLD.createParticleInstance("Molten")
            molten.Current_Frame = self.Current_Frame
            molten.COLD_PARTICLE = "Steel"
            WORLD.setParticle(None, position, True)
            WORLD.setInstancedParticle(molten, position)
