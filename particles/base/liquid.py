from particles.base import Particle
from utils import Vector2
import random

class Liquid(Particle):
    def __init__(self, name: str, color: tuple[int, int, int, int], density: float, heat_transfer_rate: float):
        super().__init__(name, color, density, heat_transfer_rate)
        self.VISCOSITY = 0
        self.LOOK_FOR_RANGE = 5

        self._viscosity_frames = 0
        self.Preferred_fluid_direction = random.choice((-1, 1))

    def update(self, WORLD, position):
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
        self._viscosity_frames += 1
        if self._viscosity_frames < self.VISCOSITY: 
            self.movedThisFrame = True
            return
        self._viscosity_frames = 0

        downDirection = Vector2(position.X, position.Y + 1)
        if WORLD.getParticle(downDirection) is None:
            self.movedThisFrame = True
            WORLD.killAndMove(position, downDirection)
            WORLD.wakeUpNeighbors(position, downDirection)
            return

        directionVector = Vector2(position.X + self.Preferred_fluid_direction, position.Y)

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
