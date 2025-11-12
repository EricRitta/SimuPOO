from particles.base import Gas

class BlueFire(Gas):
    def __init__(self):
        super().__init__(
            "Fire",                                 # Particle Name 
            (255, 255, 255, 5),                    # Particle Color tuple[RED, GREEN, BLUE, VARIATION]
            -10,                                      # Particle Density
            0.5,                                    # Particle Heat Capacity (maior = mais resistencia ao hea)
            0.025,                                   # Particle Heat Conductivity (maior = mais perda de calor)
        )
        self.LAST_PARTICLE = None

        self.HEAT_START_TEMP = 1200
        self.MAX_TEMPERATURE = 3000
        self.Temperature = 3000

        self.WEIGHT = 0
        self.Life_Time = 90

    def update(self, WORLD, position):
        if self.killedByTime(WORLD, position): return
        super().update(WORLD, position)

    def killedByTime(self, WORLD, position):
        self.Life_Time -= 1
        if self.Life_Time <= 0:
            WORLD.setParticle(None, position)
            return True

    @property
    def Color(self):
        if self.Temperature <= self.HEAT_START_TEMP:
            return self._COLOR
        
        base = self._COLOR
        actualTemp = min(self.Temperature, self.MAX_TEMPERATURE)
        factor = min((actualTemp - self.HEAT_START_TEMP) / (self.MAX_TEMPERATURE - self.HEAT_START_TEMP), 1.0)
        
        subfactor = factor / 0.5
        target = (50, 50, 255)
        if factor >= 0.5:
            subfactor = (factor - 0.5) / 0.5
            target = (150, 150, 255)
            base = (50, 50, 255)

        final_color = (
            int(base[0] + (target[0] - base[0]) * subfactor),
            int(base[1] + (target[1] - base[1]) * subfactor),
            int(base[2] + (target[2] - base[2]) * subfactor),
        )
        return final_color
