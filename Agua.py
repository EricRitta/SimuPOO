from Pixel import Pixel
import random

class Agua(Pixel):
	def __init__(self, temperatura: float, delta_temperatura: float = 0.1):
		super().__init__(temperatura, delta_temperatura)
		self._cor = (0, 0, 255)
		self._estado="liquido"

	@property
	def cor(self) -> tuple[int, int, int]:
		return self._cor

	@property
	def estado(self) -> str:
		return self._estado

	def atualizar(self):
		# Exemplo simples: aumenta a temperatura
		self.temperatura += self.delta_temperatura
    