from particles.base import Particle
from utils import Vector2
import random

class Gas(Particle):
    def __init__(self, name: str, color: tuple[int, int, int, int], density: float, heat_capacity: float, heat_conductivity: float):
        super().__init__(name, color, density, heat_capacity, heat_conductivity)
        self.WEIGHT = 3
        self._weight_frames = 0

    def update(self, WORLD, position):
        inGas = self._inGas_movement(WORLD, position)
        if inGas: return
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
        self._weight_frames += 1
        if self._weight_frames < self.WEIGHT: 
            return
        self._weight_frames = 0

        upDir = (0, -1)
        allDir = [(1, 0), (-1, 0)]
        random.shuffle(allDir)
        allDir.insert(0, upDir)

        if random.randint(1, 10) == 1:
            random.shuffle(allDir)

        direction = Vector2(0, 0)
        for cx, cy in allDir:
            direction.X = position.X + cx
            direction.Y = position.Y + cy
            if WORLD.getParticle(direction) is None:
                self.movedThisFrame = True
                WORLD.killAndMove(position, direction)
                WORLD.wakeUpNeighbors(position, direction)
                break


    def _inGas_movement(self, WORLD, position):
        directions = [(0, -1), (-1, -1), (1, -1)]
        random.shuffle(directions)
        
        for cx, cy in directions:
            vector = Vector2(position.X + cx, position.Y + cy)
            foundParticle = WORLD.getParticle(vector)
            if not foundParticle: return
            if hasattr(foundParticle,  "WEIGHT") or hasattr(foundParticle, "VISCOSITY"):

                if self.Temperature > foundParticle.Temperature:
                    self.movedThisFrame = True
                    WORLD.swapParticles(position, vector)
                    WORLD.wakeUpNeighbors(position, vector)
                    return True

                else:
                    if foundParticle.DENSITY > self.DENSITY:
                        self.movedThisFrame = True
                        
                        if foundParticle.Temperature > self.Temperature:
                            return True
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
