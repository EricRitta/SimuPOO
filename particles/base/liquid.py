from particles.base import Particle
from utils import Vector2
import random

class Liquid(Particle):
    def __init__(self, name: str, color: tuple[int, int, int, int], density: float, heat_capacity: float, heat_conductivity: float):
        super().__init__(name, color, density, heat_capacity, heat_conductivity)
        self.VISCOSITY = 0

        self._viscosity_frames = 0
        self.Preferred_fluid_direction = random.choice((-1, 1))

    def update(self, WORLD, position):
        inFluid = self._inFluid_movement(WORLD, position)
        if inFluid: return
        self._movement(WORLD, position)

    def sleepAndActivateNeighbors(self, WORLD, position):
        if self.movedThisFrame or WORLD.getParticle(position + Vector2(0, -1)) is None: 
            self._dead_frames = 0
            return

        self._dead_frames += 1
        if not self.wokenByNeighbors:
            WORLD.wakeUpNeighbors(position, None)
        if self._dead_frames >= 60:
            self.wokenByNeighbors = False
            self.isActive = False



    def _movement(self, WORLD, position):
        downDirection = Vector2(position.X, position.Y + 1)
        if WORLD.getParticle(downDirection) is None:
            self.movedThisFrame = True
            WORLD.killAndMove(position, downDirection)
            WORLD.wakeUpNeighbors(position, downDirection)
            return

        directionVector = Vector2(position.X + self.Preferred_fluid_direction, position.Y)

        self._viscosity_frames += 1
        if self._viscosity_frames < self.VISCOSITY: 
            return
        self._viscosity_frames = 0
        
        # Lado
        if WORLD.getParticle(directionVector) is None:
            self.movedThisFrame = True
            WORLD.killAndMove(position, directionVector)
            WORLD.wakeUpNeighbors(position, directionVector)
            return

        # Lado oposto
        directionVector.X = position.X - self.Preferred_fluid_direction
        if WORLD.getParticle(directionVector) is None:
            self.movedThisFrame = True
            WORLD.killAndMove(position, directionVector)
            WORLD.wakeUpNeighbors(position, directionVector)
            self.Preferred_fluid_direction = -self.Preferred_fluid_direction
            return

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
                        WORLD.wakeUpNeighbors(position, vector)
                        return True
                    return True
