from particles.base import Liquid

class Water(Liquid):
    ORDER = 2
    NAME = "Water"
    IMAGE_NAME = "Água"
    IMAGE_COLOR = (70, 140, 255)
    CONCRETE = True

    def __init__(self):
        super().__init__(
            (70, 140, 255, 10),                      # Particle Color tuple[RED, GREEN, BLUE, VARIATION]
            1,                                       # Particle Density
            4.0,                                     # Particle Heat Capacity
            0.2,                                     # Particle Heat Conductivity
        )
        self.BOILING_POINT = 100.0

    def tempChanged(self, WORLD, position):
        if self.Temperature > self.BOILING_POINT:
            WORLD.killAndReplace(position, "Steam")
