from particles.base import Liquid

class Molten(Liquid):
    NAME = "Molten"

    def __init__(self):
        super().__init__(
            (255, 255, 255, 0),                      # Particle Color tuple[RED, GREEN, BLUE, VARIATION]
            10,                                      # Particle Density
            1.0,                                     # Particle Heat Capacity
            0.2,                                     # Particle Heat Conductivity
        )
        self.LOOK_UP = 1
        self.VISCOSITY = 3

        self.ALIVE_TIME = 0
        self.MAX_ALIVE_TIME = 12

        self.Temperature = 1300
        self.COLD_PARTICLE_TEMP = 1300
        self.COLD_PARTICLE = None
        self.FREEZING_POINT = 800.0

    def tempChanged(self, WORLD, position):
        if not self.COLD_PARTICLE: return
        if self.ALIVE_TIME < self.MAX_ALIVE_TIME:
            self.ALIVE_TIME += 1
            self.Temperature = self.COLD_PARTICLE_TEMP

        if self.Temperature <= self.FREEZING_POINT:
            coldParticle = WORLD.createParticleInstance(self.COLD_PARTICLE)
            coldParticle.Temperature = self.Temperature
            coldParticle.Current_Frame = self.Current_Frame
            WORLD.setParticle(None, position, True)
            WORLD.setInstancedParticle(coldParticle, position)
