from abc import ABC, abstractmethod
import utils
import random

class Particle(ABC):
    ORDER = 999
    NAME = "Particle"
    #IMAGE_NAME = "Partícula"
    DESCRIPTION = [
        "Não há descrição disponível",
        "para a partícula selecionada."
    ]
    IMAGE_COLOR = (255, 255, 255)
    CONCRETE = False
    
    def __init__(self, color: tuple[int, int, int, int], density: float, heat_capacity: float, heat_conductivity: float):
        # Constantes defaults
        self.DENSITY = density
        self.HEAT_CAPACITY = heat_capacity
        self.HEAT_CONDUCTIVITY = heat_conductivity
        self._COLOR = (
            max(0, min(255, color[0] + random.randint(-color[3], color[3]))),
            max(0, min(255, color[1] + random.randint(-color[3], color[3]))),
            max(0, min(255, color[2] + random.randint(-color[3], color[3])))
        )
        
        # Temperatura
        self.Temperature = utils.AMBIENT_TEMPERATURE
        self.MAX_TEMPERATURE = utils.MAX_CELL_TEMPERATURE
        self.MIN_TEMPERATURE = utils.MIN_CELL_TEMPERATURE

        self.MAX_TEMP_COLOR = 2000.0
        self.MIN_TEMP_COLOR = self.MIN_TEMPERATURE
        self.HEAT_COLOR_START = 200.0
        self.COLD_COLOR_START = -50

        # Game things
        self.MAX_DEAD_FRAMES = 5
        self.movedThisFrame = True
        self.Current_Frame = 0
        self.sink_timer = 0

        self.isActive = True
        self.wokenByNeighbors = False
        self._dead_frames = 0

    @property
    def Color(self):
        temp = self.Temperature
        if self.COLD_COLOR_START < temp <= self.HEAT_COLOR_START:
            return self._COLOR
        
        base = self._COLOR

        # Geladinha uiii
        if temp <= self.COLD_COLOR_START:
            actual_temp = max(temp, self.MIN_TEMP_COLOR)
            factor = min((self.COLD_COLOR_START - actual_temp) / (self.COLD_COLOR_START - self.MIN_TEMP_COLOR), 1.0)

            return (
                int(base[0] + (255 - base[0]) * factor),
                int(base[1] + (255 - base[1]) * factor),
                int(base[2] + (255 - base[2]) * factor),
            )

        # Quentinha ai ai
        actualTemp = min(temp, self.MAX_TEMP_COLOR)
        factor = min((actualTemp - self.HEAT_COLOR_START) / (self.MAX_TEMP_COLOR - self.HEAT_COLOR_START), 1.0)
        
        subfactor = factor * 2
        target = (255, 0, 0)
        if factor >= 0.5:
            subfactor = (factor - 0.5) / 0.5
            target = (255, 255, 0)
            base = (255, 0, 0)

        return (
            int(base[0] + (target[0] - base[0]) * subfactor),
            int(base[1] + (target[1] - base[1]) * subfactor),
            int(base[2] + (target[2] - base[2]) * subfactor),
        )

    @abstractmethod
    def update(self, WORLD, position):
        """Up"""

    @abstractmethod
    def sleepAndActivateNeighbors(self, WORLD, position):
        """Metodo de ativação para quando acabar"""

    def tempChanged(self, WORLD, position):
        pass
