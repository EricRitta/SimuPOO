from particles.base import ImmovableSolid

class Mud(ImmovableSolid):
    def __init__(self):
        super().__init__(
            "Mud",                                  # Particle Name 
            (110, 100, 70, 15),                     # Particle Color tuple[RED, GREEN, BLUE, VARIATION]
            3,                                      # Particle Density
            1.2,                                    # Particle Heat Capacity
            0.15,                                   # Particle Heat Conductivity
        )
        self.TEMP_TO_DRY = 100.0

    def tempChanged(self, WORLD, position):
        if self.Temperature > self.TEMP_TO_DRY:
            coldParticle = WORLD.createParticleInstance('Dirt')
            coldParticle.Temperature = self.Temperature
            coldParticle.Current_Frame = self.Current_Frame
            WORLD.setParticle(None, position)
            WORLD.setInstancedParticle(coldParticle, position)
