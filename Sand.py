from Pixel import Pixel
import random

class Sand(Pixel):
	def __init__(self, temperatura: float, cor: tuple[int,int,int]=(255, 255, 0), delta_temperatura: float = 0.1):
		super().__init__(temperatura, cor, delta_temperatura)

	@property
	def cor(self) -> tuple[int, int, int]:
		return tuple(
			max(0, min(255, self._cor[i] + random.randint(-10, 10))) for i in range(3)
		)

	def atualizar(self):
		# Exemplo simples: aumenta a temperatura
		self.temperatura += self.delta_temperatura
    