from Pixel import Pixel
import random

class Ar(Pixel):
	def __init__(self, temperatura: float, delta_temperatura: float = 0.1):
		super().__init__(temperatura, delta_temperatura)
		self._cor = (150, 255, 255)  # cor padrão fixa

	@property
	def cor(self) -> tuple[int, int, int]:
		return self._cor

	def atualizar(self):
		# Exemplo simples: aumenta a temperatura
		self.temperatura += self.delta_temperatura
    