from particles.base import ImmovableSolid

class Mud(ImmovableSolid):
    NAME = "Mud"
    IMAGE_NAME = "Lama"
    IMAGE_COLOR = (110, 100, 70)
    CONCRETE = True

    def __init__(self):
        super().__init__(
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
            WORLD.setParticle(None, position, True)
            WORLD.setInstancedParticle(coldParticle, position)
