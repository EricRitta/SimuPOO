

import pygame
from Ar import Ar
from Sand import Sand
from Agua import Agua

# Exemplo: criar uma lista 10x10 cheia de instâncias de Ar


def isSolid(pixel):
	return pixel.estado == "solido"



# Configurações do jogo
TAM_PIXEL = 10
LINHAS = 50
COLUNAS = 50
LARGURA = COLUNAS * TAM_PIXEL
ALTURA = LINHAS * TAM_PIXEL

# Inicializa a matriz de pixels (tudo ar)
matriz = [[Ar(temperatura=20.0) for _ in range(COLUNAS)] for _ in range(LINHAS)]

def desenhar_tela(screen, matriz):
	for y in range(LINHAS):
		for x in range(COLUNAS):
			cor = matriz[y][x].cor
			pygame.draw.rect(screen, cor, (x*TAM_PIXEL, y*TAM_PIXEL, TAM_PIXEL, TAM_PIXEL))

def atualizar_areia(matriz):
	# Percorre de baixo para cima para simular queda
	for y in range(LINHAS-2, -1, -1):
		for x in range(COLUNAS):
			import random
			# Atualiza areia
			if isinstance(matriz[y][x], Sand):
				if isinstance(matriz[y+1][x], Ar):
					matriz[y+1][x], matriz[y][x] = matriz[y][x], matriz[y+1][x]
				elif x > 0 and isinstance(matriz[y+1][x-1], Ar):
					matriz[y+1][x-1], matriz[y][x] = matriz[y][x], matriz[y+1][x-1]
				elif x < COLUNAS-1 and isinstance(matriz[y+1][x+1], Ar):
					matriz[y+1][x+1], matriz[y][x] = matriz[y][x], matriz[y+1][x+1]

			# Atualiza água
			if isinstance(matriz[y][x], Agua):
				moved = False
				# Tenta cair para baixo
				if isinstance(matriz[y+1][x], Ar):
					matriz[y+1][x], matriz[y][x] = matriz[y][x], matriz[y+1][x]
					moved = True
				else:
					# Tenta escorrer para os lados (aleatório)
					dirs = []
					if x > 0 and isinstance(matriz[y][x-1], Ar):
						dirs.append(-1)
					if x < COLUNAS-1 and isinstance(matriz[y][x+1], Ar):
						dirs.append(1)
					if dirs:
						dx = random.choice(dirs)
						matriz[y][x+dx], matriz[y][x] = matriz[y][x], matriz[y][x+dx]
						moved = True
				# Tenta escorrer diagonalmente se não moveu
				if not moved:
					diag_dirs = []
					if x > 0 and isinstance(matriz[y+1][x-1], Ar):
						diag_dirs.append(-1)
					if x < COLUNAS-1 and isinstance(matriz[y+1][x+1], Ar):
						diag_dirs.append(1)
					if diag_dirs:
						dx = random.choice(diag_dirs)
						matriz[y+1][x+dx], matriz[y][x] = matriz[y][x], matriz[y+1][x+dx]

def main():
	pygame.init()
	screen = pygame.display.set_mode((LARGURA, ALTURA))
	pygame.display.set_caption('Jogo da Areia')
	clock = pygame.time.Clock()
	rodando = True
	mouse_esquerdo_pressionado = False
	mouse_direito_pressionado = False
	while rodando:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				rodando = False
			elif event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:
					mouse_esquerdo_pressionado = True
				elif event.button == 3:
					mouse_direito_pressionado = True
			elif event.type == pygame.MOUSEBUTTONUP:
				if event.button == 1:
					mouse_esquerdo_pressionado = False
				elif event.button == 3:
					mouse_direito_pressionado = False

		mx, my = pygame.mouse.get_pos()
		x = mx // TAM_PIXEL
		y = my // TAM_PIXEL
		if 0 <= x < COLUNAS and 0 <= y < LINHAS:
			if mouse_esquerdo_pressionado:
				matriz[y][x] = Sand(temperatura=20.0)
			if mouse_direito_pressionado:
				matriz[y][x] = Agua(temperatura=20.0)

		atualizar_areia(matriz)
		desenhar_tela(screen, matriz)
		pygame.display.flip()
		clock.tick(60)
	pygame.quit()

if __name__ == '__main__':
	main()

# Agora lista_ar é uma matriz 10x10 de objetos Ar
