from abc import ABC, abstractmethod

class Pixel(ABC):
    def __init__(self, temperatura: float, cor: tuple[int,int,int], delta_temperatura: float):
        self._temperatura = temperatura
        self._cor = cor
        self._delta_temperatura = delta_temperatura

    @property
    def temperatura(self) -> float:
        return self._temperatura

    @temperatura.setter
    def temperatura(self, value: float):
        self._temperatura = value

    @property
    def cor(self) -> tuple[int,int,int]:
        return self._cor

    @cor.setter
    def cor(self, value: tuple[int,int,int]):
        self._cor = value

    @property
    def delta_temperatura(self) -> float:
        return self._delta_temperatura

    @delta_temperatura.setter
    def delta_temperatura(self, value: float):
        self._delta_temperatura = value

    @abstractmethod
    def atualizar(self):
        pass

