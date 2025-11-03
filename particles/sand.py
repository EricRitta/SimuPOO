import random
from utils import Vector2
from particles.base import MovableSolid

class Sand(MovableSolid):
    def __init__(self):
        super().__init__(
            "Sand",                                 # Particle Name 
            (195, 180, 130, 15),                    # Particle Color tuple[RED, GREEN, BLUE, VARIATION]
            3,                                      # Particle Density
            1.0,                                    # Particle Heat Capacity (maior = mais resistencia ao hea)
            0.05,                                   # Particle Heat Conductivity (maior = mais perda de calor)
        )
        self.Temperature = 800
    
    def _inLiquid_movement(self, WORLD, position):
        directions = [(0, 1), (-1, 1), (1, 1)]
        random.shuffle(directions)
        
        for cx, cy in directions:
            vector = Vector2(position.X + cx, position.Y + cy)
            foundParticle = WORLD.getParticle(vector)
            if foundParticle and hasattr(foundParticle, "VISCOSITY"):
                WORLD.killAndReplace(position, "Mud")
                return True

