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
		return self._cor

	@property
	def estado(self) -> str:
		return self._estado

	def atualizar(self):
		# Exemplo simples: aumenta a temperatura
		self.temperatura += self.delta_temperatura
    