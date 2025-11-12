from particles.base import Particle
from utils import Vector2
import random

class MovableSolid(Particle):
    def __init__(self, name: str, color: tuple[int, int, int, int], density: float, heat_capacity: float, heat_conductivity: float):
        super().__init__(name, color, density, heat_capacity, heat_conductivity)

    def update(self, WORLD, position):
        if self._inFluid_movement(WORLD, position): return
        self._movement(WORLD, position)
    
    def sleepAndActivateNeighbors(self, WORLD, position):
        if self.movedThisFrame:
            self._dead_frames = 0
            return

        self._dead_frames += 1
        if not self.wokenByNeighbors:
            WORLD.wakeUpNeighbors(position)
        if self._dead_frames >= self.MAX_DEAD_FRAMES:
            self.wokenByNeighbors = False
            self.isActive = False



    def _movement(self, WORLD, position):
        allDir = [(-1, 1), (1, 1)]
        random.shuffle(allDir)
        allDir.insert(0, (0, 1))
        
        direction = Vector2(0, 0)
        for cx, cy in allDir:
            direction.X = position.X + cx
            direction.Y = position.Y + cy
            if WORLD.getParticle(direction) is None:
                self.movedThisFrame = True
                WORLD.killAndMove(position, direction)
                break

    def _inFluid_movement(self, WORLD, position):
        directions = [(0, 1), (-1, 1), (1, 1)]
        random.shuffle(directions)
        
        for cx, cy in directions:
            vector = Vector2(position.X + cx, position.Y + cy)
            foundParticle = WORLD.getParticle(vector)
            if not foundParticle: return
            if hasattr(foundParticle, "VISCOSITY") or hasattr(foundParticle,  "WEIGHT"):
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
                        return True
                    return True
        

