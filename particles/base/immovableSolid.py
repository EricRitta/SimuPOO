from particles.base import Particle

class ImmovableSolid(Particle):
    def __init__(self, name: str, color: tuple[int, int, int, int], density: float, heat_transfer_rate: float):
        super().__init__(name, color, density, heat_transfer_rate)
        self.movedThisFrame = False
        self.isActive = False

    def update(self, WORLD, position):
        self.movedThisFrame = True
        self.isActive = False
    
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
