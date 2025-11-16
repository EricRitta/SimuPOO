from particles.base import Particle

class ImmovableSolid(Particle):
    ORDER = 100

    def __init__(self, color: tuple[int, int, int, int], density: float, heat_capacity: float, heat_conductivity: float):
        super().__init__(color, density, heat_capacity, heat_conductivity)
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
            WORLD.wakeUpNeighbors(position)
        if self._dead_frames >= self.MAX_DEAD_FRAMES:
            self.wokenByNeighbors = False
            self.isActive = False
