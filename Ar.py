from Pixel import Pixel
import random

class Ar(Pixel):
	def __init__(self, temperatura: float, delta_temperatura: float = 0.5, capacidade_termica: float = 1.0):
		# Ar tem alta difusão térmica (troca calor rápido), mas baixa capacidade térmica
		super().__init__(temperatura, delta_temperatura, capacidade_termica)
		self._cor = (150, 255, 255)  
		self._estado="gasoso"
		self._densidade = 0.0012

	@property
	def cor(self) -> tuple[int, int, int]:
		return tuple([max(0, min(255, self._cor[0]+self._temperatura)), max(0, min(255, self._cor[1]-self._temperatura)), max(0, min(255, self._cor[2]-self._temperatura))])

	@property
	def estado(self) -> str:
		if self.temperatura < -210:
			return "solido"
		elif self.temperatura < -190:
			return "liquido"
		else:
			return "gasoso"

	@property
	def densidade(self) -> float:
		return self._densidade+self._temperatura * 0.00001 

	def atualizar(self):
		# Exemplo simples: aumenta a temperatura
		self.temperatura += self.delta_temperatura
    