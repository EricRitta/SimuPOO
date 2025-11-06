from particles.base import Gas

class Steam(Gas):
    def __init__(self):
        super().__init__(
            "Steam",                                 # Particle Name 
            (175, 175, 175, 5),                    # Particle Color tuple[RED, GREEN, BLUE, VARIATION]
            -6,                                      # Particle Density
            2.0,                                    # Particle Heat Capacity (maior = mais resistencia ao hea)
            0.05,                                   # Particle Heat Conductivity (maior = mais perda de calor)
        )
        self.Temperature = 200.0

    def tempChanged(self, WORLD, position):
        if self.Temperature <= 100:
            water = WORLD.createParticleInstance("Water")
            water.Temperature = self.Temperature
            water.Current_Frame = self.Current_Frame
            WORLD.setParticle(None, position)
            WORLD.setInstancedParticle(water, position)
