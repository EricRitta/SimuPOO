from particles.base import Particle
from utils import Vector2
import random

class MovableSolid(Particle):
    def __init__(self, name: str, color: tuple[int, int, int, int], density: float, heat_transfer_rate: float):
        super().__init__(name, color, density, heat_transfer_rate)

    def update(self, WORLD, position):
        liquidMove = self._inLiquid_movement(WORLD, position)
        if liquidMove: return
        self._movement(WORLD, position)
    
    def sleepAndActivateNeighbors(self, WORLD, position):
        if self.movedThisFrame:
            self._dead_frames = 0
            return

        self._dead_frames += 1
        if not self.wokenByNeighbors:
            WORLD.wakeUpNeighbors(position, None)
        if self._dead_frames >= 60:
            self.wokenByNeighbors = False
            self.isActive = False



    def _movement(self, WORLD, position):
        directions = [
            Vector2(position.X - 1, position.Y + 1),
            Vector2(position.X + 1, position.Y + 1),
        ]
        random.shuffle(directions)
        directions.insert(0, Vector2(position.X, position.Y + 1))

        for vector in directions:
            particle = WORLD.getParticle(vector)
            if particle is None:
                WORLD.killAndMove(position, vector)
                WORLD.wakeUpNeighbors(position, vector)
                self.movedThisFrame = True
                break

    def _inLiquid_movement(self, WORLD, position):
        directions = [(0, 1), (-1, 1), (1, 1)]
        random.shuffle(directions)
        
        for cx, cy in directions:
            vector = Vector2(position.X + cx, position.Y + cy)
            foundParticle = WORLD.getParticle(vector)
            if foundParticle and hasattr(foundParticle, "VISCOSITY"):
                if foundParticle.DENSITY < self.DENSITY:
                    self.movedThisFrame = True

                    # calcular resistencia
                    diff = abs(self.DENSITY - foundParticle.DENSITY)
                    max_diff = max(self.DENSITY, foundParticle.DENSITY)
                    diff_normalized = diff / max_diff
                    resistence = round(5 - (4 * diff_normalized))

                    self.sink_timer += 1
                    if self.sink_timer >= resistence:
                        self.sink_timer = 0
                        WORLD.swapParticles(position, vector)
                        WORLD.wakeUpNeighbors(position, vector)
                        return True
                    return True
        

