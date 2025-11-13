from particles.base import Particle
from utils import Vector2
import random

class Liquid(Particle):
    def __init__(self, name: str, color: tuple[int, int, int, int], density: float, heat_capacity: float, heat_conductivity: float):
        super().__init__(name, color, density, heat_capacity, heat_conductivity)
        self.MAX_DEAD_FRAMES = 20
        self.LOOK_UP = 5
        self.VISCOSITY = 1

        self._viscosity_frames = 0
        self.Preferred_fluid_direction = random.choice((-1, 1))

    def update(self, WORLD, position):
        if self._inFluid_movement(WORLD, position): return
        self._movement(WORLD, position)

    def sleepAndActivateNeighbors(self, WORLD, position):
        if self.movedThisFrame or WORLD.getParticle(position + Vector2(0, -1)) is None: 
            self._dead_frames = 0
            return

        self._dead_frames += 1
        if not self.wokenByNeighbors:
            WORLD.wakeUpNeighbors(position)
        if self._dead_frames >= self.MAX_DEAD_FRAMES:
            self.wokenByNeighbors = False
            self.isActive = False



    def _movement(self, WORLD, position):
        downDirection = Vector2(position.X, position.Y + 1)
        if WORLD.getParticle(downDirection) is None:
            self.movedThisFrame = True
            WORLD.killAndMove(position, downDirection)
            return
        
        self._viscosity_frames += 1
        if self._viscosity_frames < self.VISCOSITY:
            return
        self._viscosity_frames = 0
        
        lastPreferred = None
        lastOpposite = None
        
        for i in range(1, self.LOOK_UP + 1):
            preferredX = position.X + (i * self.Preferred_fluid_direction)
            
            diagonalDown = Vector2(preferredX, position.Y + 1)
            if WORLD.getParticle(diagonalDown) is None:
                lastPreferred = (preferredX, position.Y + 1)
                break  
            
            lateral = Vector2(preferredX, position.Y)
            if WORLD.getParticle(lateral) is None:
                lastPreferred = (preferredX, position.Y)
            else:
                break  
        
        if lastPreferred is None:
            for i in range(1, self.LOOK_UP + 1):
                oppositeX = position.X - (i * self.Preferred_fluid_direction)
                
                diagonalDown = Vector2(oppositeX, position.Y + 1)
                if WORLD.getParticle(diagonalDown) is None:
                    lastOpposite = (oppositeX, position.Y + 1)
                    break
                
                lateral = Vector2(oppositeX, position.Y)
                if WORLD.getParticle(lateral) is None:
                    lastOpposite = (oppositeX, position.Y)
                else:
                    break
            
            if lastOpposite is not None:
                self.Preferred_fluid_direction *= -1
                dirX, dirY = lastOpposite
                self.movedThisFrame = True
                WORLD.killAndMove(position, Vector2(dirX, dirY))
        else:
            dirX, dirY = lastPreferred
            self.movedThisFrame = True
            WORLD.killAndMove(position, Vector2(dirX, dirY))

    def _inFluid_movement(self, WORLD, position):
        directions = [(0, 1), (-1, 1), (1, 1)]
        random.shuffle(directions)
        
        for cx, cy in directions:
            vector = Vector2(position.X + cx, position.Y + cy)
            foundParticle = WORLD.getParticle(vector)
            if not foundParticle: return
            if foundParticle.NAME == self.NAME: return
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
