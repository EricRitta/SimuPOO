

import pygame
import random

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

def atualizar_fisica(matriz):
	
	# Percorre de baixo para cima para simular física
	for y in range(LINHAS-2, -1, -1):
		for x in range(COLUNAS):
			pixel_atual = matriz[y][x]
			
			# Comportamento para SÓLIDOS
			if pixel_atual.estado == "solido":
				# Sólidos caem se houver algo menos denso embaixo (gás ou líquido)
				if y < LINHAS-1 and matriz[y+1][x].densidade < pixel_atual.densidade:
					matriz[y+1][x], matriz[y][x] = matriz[y][x], matriz[y+1][x]
				# Se não pode cair direto, tenta rolar para as diagonais
				elif y < LINHAS-1:
					dirs = []
					if x > 0 and matriz[y+1][x-1].densidade < pixel_atual.densidade:
						dirs.append(-1)
					if x < COLUNAS-1 and matriz[y+1][x+1].densidade < pixel_atual.densidade:
						dirs.append(1)
					if dirs:
						dx = random.choice(dirs)
						matriz[y+1][x+dx], matriz[y][x] = matriz[y][x], matriz[y+1][x+dx]
			
			# Comportamento para LÍQUIDOS
			elif pixel_atual.estado == "liquido":
				moved = False
				
				# Líquidos caem se houver algo menos denso embaixo
				if y < LINHAS-1 and matriz[y+1][x].densidade < pixel_atual.densidade:
					matriz[y+1][x], matriz[y][x] = matriz[y][x], matriz[y+1][x]
					moved = True
				
				# Se não pode cair, tenta fluir horizontalmente (sempre tenta se espalhar)
				if not moved:
					dirs = []
					if x > 0 and matriz[y][x-1].densidade < pixel_atual.densidade:
						dirs.append(-1)
					if x < COLUNAS-1 and matriz[y][x+1].densidade < pixel_atual.densidade:
						dirs.append(1)
					if dirs:
						dx = random.choice(dirs)
						matriz[y][x+dx], matriz[y][x] = matriz[y][x], matriz[y][x+dx]
						moved = True
				
				# Se ainda não moveu, tenta fluir diagonalmente para baixo
				if not moved and y < LINHAS-1:
					diag_dirs = []
					if x > 0 and matriz[y+1][x-1].densidade < pixel_atual.densidade:
						diag_dirs.append(-1)
					if x < COLUNAS-1 and matriz[y+1][x+1].densidade < pixel_atual.densidade:
						diag_dirs.append(1)
					if diag_dirs:
						dx = random.choice(diag_dirs)
						matriz[y+1][x+dx], matriz[y][x] = matriz[y][x], matriz[y+1][x+dx]
						moved = True
				

			
			# Comportamento para GASOSOS
			elif pixel_atual.estado == "gasoso":
				# Gases fazem movimento aleatório de convecção (movimento sutil)
				if random.random() < 0.05:  # 5% de chance de movimento
					dirs = []
					# Movimento aleatório, mas com tendência a subir
					if x > 0:
						dirs.append((-1, 0))  # esquerda
					if x < COLUNAS-1:
						dirs.append((1, 0))   # direita
					if y > 0:
						dirs.extend([(0, -1), (0, -1)])  # cima (dupla chance)
					if y < LINHAS-1:
						dirs.append((0, 1))   # baixo
					
					if dirs:
						dx, dy = random.choice(dirs)
						ny, nx = y + dy, x + dx
						# Troca apenas com outros gases
						if matriz[ny][nx].estado == "gasoso":
							matriz[ny][nx], matriz[y][x] = matriz[y][x], matriz[ny][nx]

def main():
	pygame.init()
	screen = pygame.display.set_mode((LARGURA, ALTURA))
	pygame.display.set_caption('Simulação Física - Esquerdo: Sólido | Direito: Líquido | R: Reset')
	clock = pygame.time.Clock()
	rodando = True
	mouse_esquerdo_pressionado = False
	mouse_direito_pressionado = False
	tempo_ultimo_bloco_esq = 0
	tempo_ultimo_bloco_dir = 0
	DELAY_BLOCO_MS = 30 
	
	while rodando:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				rodando = False
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_r:
					# Reset da matriz - volta tudo para ar
					for y in range(LINHAS):
						for x in range(COLUNAS):
							matriz[y][x] = Ar(temperatura=20.0)
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
			agora = pygame.time.get_ticks()
			if mouse_esquerdo_pressionado:
				if agora - tempo_ultimo_bloco_esq > DELAY_BLOCO_MS:
					matriz[y][x] = Sand(temperatura=20.0)
					tempo_ultimo_bloco_esq = agora
			if mouse_direito_pressionado:
				if agora - tempo_ultimo_bloco_dir > DELAY_BLOCO_MS:
					matriz[y][x] = Agua(temperatura=20.0)
					tempo_ultimo_bloco_dir = agora

		atualizar_fisica(matriz)
		desenhar_tela(screen, matriz)
		pygame.display.flip()
		clock.tick(60)
	pygame.quit()

if __name__ == '__main__':
	main()

# Agora lista_ar é uma matriz 10x10 de objetos Ar
