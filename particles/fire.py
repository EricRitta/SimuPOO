from particles.base import Gas

class Fire(Gas):
    ORDER = 4
    NAME = "Fire"
    IMAGE_NAME = "Fogo"
    IMAGE_COLOR = (255, 150, 50)
    CONCRETE = True

    def __init__(self):
        super().__init__(
            (100, 100, 100, 5),                    # Particle Color tuple[RED, GREEN, BLUE, VARIATION]
            -10,                                      # Particle Density
            0.5,                                    # Particle Heat Capacity (maior = mais resistencia ao hea)
            0.05,                                   # Particle Heat Conductivity (maior = mais perda de calor)
        )
        self.LAST_PARTICLE = None

        self.HEAT_START_TEMP = 0
        self.MAX_TEMPERATURE = 1200
        self.Temperature = 1200

        self.WEIGHT = 0
        self.Life_Time = 120

    def update(self, WORLD, position):
        dead = self.killedByTime(WORLD, position)
        if dead: return
        super().update(WORLD, position)

    def killedByTime(self, WORLD, position):
        self.Life_Time -= 1
        if self.Life_Time <= 0:
            WORLD.setParticle(None, position)
            return True
