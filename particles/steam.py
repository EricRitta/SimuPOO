from particles.base import Gas

class Steam(Gas):
    NAME = "Steam"
    IMAGE_NAME = "Vapor"
    IMAGE_COLOR = (175, 175, 175)
    DESCRIPTION = [
        "VAPOR",
        'Vapor é o estado gasoso da',
        'água, formado quando moléculas',
        'de H2O ganham energia suficiente',
        'para se dispersar no ar.',
        'É invisível a olho nu.',
        "",
        '',
        "COMPORTAMENTO",
        "",
        "Sobe naturalmente.",
        "",
        "Dispersa-se horizontalmente.",
        "",
        "Condensa virando água (<100°C).",
        "",
    ]
    CONCRETE = True

    def __init__(self):
        super().__init__(
            (175, 175, 175, 5),                     # Particle Color tuple[RED, GREEN, BLUE, VARIATION]
            -6,                                     # Particle Density
            2.0,                                    # Particle Heat Capacity (maior = mais resistencia ao hea)
            0.05,                                   # Particle Heat Conductivity (maior = mais perda de calor)
        )
        self.Temperature = 200.0

    def tempChanged(self, WORLD, position):
        if self.Temperature <= 100:
            water = WORLD.createParticleInstance("Water")
            water.Temperature = self.Temperature
            water.Current_Frame = self.Current_Frame
            WORLD.setParticle(None, position, True)
            WORLD.setInstancedParticle(water, position)
