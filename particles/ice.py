from particles.base import ImmovableSolid

class Ice(ImmovableSolid):
    NAME = "Ice"
    IMAGE_NAME = "Gelo"
    IMAGE_COLOR = (185, 210, 235)
    DESCRIPTION = [
        "GELO",
        'Gelo é a forma sólida da água,',
        'formado quando a temperatura',
        'cai abaixo de 0°C. Suas moléculas',
        'ficam organizadas em estrutura',
        'cristalina hexagonal rígida.',
        "",
        "",
        "COMPORTAMENTO",
        '',
        "Permanece estático (sólido).",
        "",
        "Não é afetado por gravidade.",
        "",
        "Derrete virando água (>0°C),",
        "ou em contato com fogo.",
        "",
        "Esfria partículas adjacentes",
        "",
    ]
    CONCRETE = True

    def __init__(self):
        super().__init__(
            (70, 140, 255, 10),                     # Particle Color tuple[RED, GREEN, BLUE, VARIATION]
            3,                                      # Particle Density
            1.2,                                    # Particle Heat Capacity
            0.15,                                   # Particle Heat Conductivity
        )
        self.COLD_COLOR_START = 0.0
        self.MIN_TEMP_COLOR = -100.0
        self.Temperature = -50.0

    def tempChanged(self, WORLD, position):
        if self.Temperature > self.COLD_COLOR_START:
            liquidParticle = WORLD.createParticleInstance('Water')
            liquidParticle.Temperature = self.Temperature
            liquidParticle.Current_Frame = self.Current_Frame
            WORLD.setParticle(None, position, True)
            WORLD.setInstancedParticle(liquidParticle, position)
