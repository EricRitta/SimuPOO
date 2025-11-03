from abc import ABC, abstractmethod
import utils
import random

class Particle(ABC):
    def __init__(self, name: str, color: tuple[int, int, int, int], density: float, heat_transfer_rate: float):
        # Constantes defaults
        self.NAME = name
        self.DENSITY = density
        self.HEAT_TRANSFER_RATE = heat_transfer_rate
        self._COLOR = (
            max(0, min(255, color[0] + random.randint(-color[3], color[3]))),
            max(0, min(255, color[1] + random.randint(-color[3], color[3]))),
            max(0, min(255, color[2] + random.randint(-color[3], color[3])))
        )
        
        # Temperatura
        self.Temperature = utils.AMBIENT_TEMPERATURE
        self.MAX_TEMPERATURE = 1500.0
        self.HEAT_START_TEMP = 200.0

        # Game things
        self.movedThisFrame = True
        self.Current_Frame = 0
        self.sink_timer = 0

        self.isActive = True
        self.wokenByNeighbors = False
        self._dead_frames = 0

    @property
    def Color(self):
        if self.Temperature <= self.HEAT_START_TEMP:
            return self._COLOR
        
        base = self._COLOR
        factor = min((self.Temperature - self.HEAT_START_TEMP) / (self.MAX_TEMPERATURE - self.HEAT_START_TEMP), 1.0)
        
        subfactor = factor / 0.5
        target = (255, 0, 0)
        if factor >= 0.5:
            subfactor = (factor - 0.5) / 0.5
            target = (255, 255, 0)
            base = (255, 0, 0)

        final_color = (
            int(base[0] + (target[0] - base[0]) * subfactor),
            int(base[1] + (target[1] - base[1]) * subfactor),
            int(base[2] + (target[2] - base[2]) * subfactor),
        )
        return final_color

    @abstractmethod
    def update(self, WORLD, position):
        """Up"""

    @abstractmethod
    def sleepAndActivateNeighbors(self, WORLD, position):
        """Metodo de ativação para quando acabar"""
