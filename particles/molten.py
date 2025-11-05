from particles.base import Liquid

class Molten(Liquid):
    def __init__(self):
        super().__init__(
            "Molten",                                 # Particle Name 
            (255, 255, 255, 0),                      # Particle Color tuple[RED, GREEN, BLUE, VARIATION]
            10,                                       # Particle Density
            1.0,                                     # Particle Heat Capacity
            0.2,                                     # Particle Heat Conductivity
        )
        self.VISCOSITY = 3
        self.Temperature = 2000
        
        self.COLD_PARTICLE = None
        self.TEMPERATURE_TO_COLD = 800.0

    def tempChanged(self, WORLD, position):
        if not self.COLD_PARTICLE: return
        if self.Temperature <= self.TEMPERATURE_TO_COLD:
            coldParticle = WORLD.createParticleInstance(self.COLD_PARTICLE)
            coldParticle.Temperature = self.Temperature
            coldParticle.Current_Frame = self.Current_Frame
            WORLD.setParticle(None, position)
            WORLD.setInstancedParticle(coldParticle, position)
            self.movedThisFrame = True
