from Pixel import Pixel
import random

class Sand(Pixel):
	def __init__(self, temperatura: float, delta_temperatura: float = 0.05):
		# Areia (sólido granular) troca calor mais devagar
		super().__init__(temperatura, delta_temperatura)
		self._cor = (max(0, min(255, 255+random.randint(-10, 10))), max(0, min(255, 255+random.randint(-10, 10))), max(0, min(255, 0+random.randint(-10, 10)))) 
		self._estado="solido"
		self._densidade = 1600

	@property
	def cor(self) -> tuple[int, int, int]:
		return tuple([max(0, min(255, self._cor[0]+self._temperatura)), max(0, min(255, self._cor[1]-self._temperatura)), max(0, min(255, self._cor[2]-self._temperatura))])

	@property
	def estado(self) -> str:
		return self._estado

	def atualizar(self):
		# Exemplo simples: aumenta a temperatura
		self.temperatura += self.delta_temperatura
    