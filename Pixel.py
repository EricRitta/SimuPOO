from abc import ABC, abstractmethod

class Pixel(ABC):
    def __init__(self, temperatura: float, delta_temperatura: float, capacidade_termica: float = 1.0):
        self._temperatura = temperatura
        self._delta_temperatura = delta_temperatura
        self._capacidade_termica = capacidade_termica
    @property
    def capacidade_termica(self) -> float:
        return self._capacidade_termica

    @capacidade_termica.setter
    def capacidade_termica(self, value: float):
        self._capacidade_termica = value

    @property
    def temperatura(self) -> float:
        return self._temperatura

    @temperatura.setter
    def temperatura(self, value: float):
        self._temperatura = value

    @property
    def cor(self) -> tuple[int,int,int]:
        return self._cor
    
    @property
    def densidade(self) -> float:
        return self._densidade

    @property
    def estado(self) -> str:
        return self._estado

    @property
    def delta_temperatura(self) -> float:
        return self._delta_temperatura

    @delta_temperatura.setter
    def delta_temperatura(self, value: float):
        self._delta_temperatura = value

    @abstractmethod
    def atualizar(self):
        pass

