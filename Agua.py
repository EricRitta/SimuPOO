from Pixel import Pixel
import random

class Agua(Pixel):
	def __init__(self, temperatura: float, delta_temperatura: float = 0.2, capacidade_termica: float = 3.0):
		# Água tem condutividade térmica intermediária e boa capacidade térmica
		super().__init__(temperatura, delta_temperatura, capacidade_termica)
		self._cor = (0, 0, 255)
		self._estado="liquido"
		self._densidade = 1000

	@property
	def cor(self) -> tuple[int, int, int]:
		return tuple([max(0, min(255, self._cor[0]+self._temperatura)), max(0, min(255, self._cor[1]-self._temperatura)), max(0, min(255, self._cor[2]-self._temperatura))])

	@property
	def estado(self) -> str:
		if self.temperatura < 0:
			return "solido"
		elif self.temperatura < 100:
			return "liquido"
		else:
			return "gasoso"

	def atualizar(self):
		# Exemplo simples: aumenta a temperatura
		self.temperatura += self.delta_temperatura
    