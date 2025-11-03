

import pygame
import random

from Ar import Ar
from Sand import Sand
from Agua import Agua

# Exemplo: criar uma lista 10x10 cheia de instâncias de Ar


def isSolid(pixel):
	return pixel.estado == "solido"



# Configurações do jogo
TAM_PIXEL = 30
LINHAS = 50
COLUNAS = 50
LARGURA = COLUNAS * TAM_PIXEL
ALTURA = LINHAS * TAM_PIXEL

# Inicializa a matriz de pixels (tudo ar)
matriz = [[Ar(temperatura=20.0) for _ in range(COLUNAS)] for _ in range(LINHAS)]

def desenhar_tela(screen, matriz, bloco_selecionado, temperatura_pixel):
	# Barra de seleção de blocos
	barra_altura = 30
	# Desenha o retângulo de fundo do cabeçalho
	pygame.draw.rect(screen, (230, 230, 230), (0, 0, LARGURA, barra_altura))

	opcoes = [
		("Areia", (194, 178, 128)),
		("Água", (0, 0, 255)),
		("Ar", (200, 200, 200)),
	]
	for i, (nome, cor) in enumerate(opcoes):
		rect = pygame.Rect(i*60, 0, 60, barra_altura)
		pygame.draw.rect(screen, cor, rect)
		if bloco_selecionado == nome:
			pygame.draw.rect(screen, (255,0,0), rect, 3)
		font = pygame.font.SysFont(None, 20)
		txt = font.render(nome, True, (0,0,0))
		screen.blit(txt, (i*60+5, 5))

	# Indicador de temperatura
	font = pygame.font.SysFont(None, 24)
	temp_text = font.render(f"Temp: {int(temperatura_pixel)}°C", True, (255,0,0))
	screen.blit(temp_text, (400, 5))

	# Campo de jogo
	for y in range(LINHAS):
		for x in range(COLUNAS):
			cor = matriz[y][x].cor
			pygame.draw.rect(screen, cor, (x*TAM_PIXEL, y*TAM_PIXEL+barra_altura, TAM_PIXEL, TAM_PIXEL))

def atualizar_fisica(matriz):
	
	# Troca de temperatura entre vizinhos
	for y in range(LINHAS):
		for x in range(COLUNAS):
			pixel = matriz[y][x]
			vizinhos = []
			for dy in [-1, 0, 1]:
				for dx in [-1, 0, 1]:
					if dx == 0 and dy == 0:
						continue
					ny, nx = y + dy, x + dx
					if 0 <= ny < LINHAS and 0 <= nx < COLUNAS:
						vizinhos.append(matriz[ny][nx])
			for vizinho in vizinhos:
				# Troca proporcional ao delta_temperatura e capacidade térmica
				temp_diff = pixel.temperatura - vizinho.temperatura
				# Fator de troca leva em conta a capacidade térmica média
				cap_media = (pixel.capacidade_termica + vizinho.capacidade_termica) / 2
				troca = temp_diff * 0.25 * min(pixel.delta_temperatura, vizinho.delta_temperatura) / cap_media
				pixel.temperatura -= troca
				vizinho.temperatura += troca

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
				# Movimento suave para gases
				if random.random() < 0.2:
					moved = False
					# Gás mais denso desce
					if y < LINHAS-1 and matriz[y+1][x].estado == "gasoso" and matriz[y+1][x].densidade > pixel_atual.densidade:
						matriz[y+1][x], matriz[y][x] = matriz[y][x], matriz[y+1][x]
						moved = True
					# Gás menos denso sobe
					elif y > 0 and matriz[y-1][x].estado == "gasoso" and matriz[y-1][x].densidade < pixel_atual.densidade:
						matriz[y-1][x], matriz[y][x] = matriz[y][x], matriz[y-1][x]
						moved = True
					# Diagonais para baixo (mais denso)
					elif y < LINHAS-1:
						diag_dirs = []
						if x > 0 and matriz[y+1][x-1].estado == "gasoso" and matriz[y+1][x-1].densidade > pixel_atual.densidade:
							diag_dirs.append(-1)
						if x < COLUNAS-1 and matriz[y+1][x+1].estado == "gasoso" and matriz[y+1][x+1].densidade > pixel_atual.densidade:
							diag_dirs.append(1)
						if diag_dirs:
							dx = random.choice(diag_dirs)
							matriz[y+1][x+dx], matriz[y][x] = matriz[y][x], matriz[y+1][x+dx]
							moved = True
					# Diagonais para cima (menos denso)
					elif y > 0:
						diag_dirs = []
						if x > 0 and matriz[y-1][x-1].estado == "gasoso" and matriz[y-1][x-1].densidade < pixel_atual.densidade:
							diag_dirs.append(-1)
						if x < COLUNAS-1 and matriz[y-1][x+1].estado == "gasoso" and matriz[y-1][x+1].densidade < pixel_atual.densidade:
							diag_dirs.append(1)
						if diag_dirs:
							dx = random.choice(diag_dirs)
							matriz[y-1][x+dx], matriz[y][x] = matriz[y][x], matriz[y-1][x+dx]
							moved = True
					# Movimento lateral aleatório se não moveu
					if not moved:
						dirs = []
						if x > 0 and matriz[y][x-1].estado == "gasoso":
							dirs.append(-1)
						if x < COLUNAS-1 and matriz[y][x+1].estado == "gasoso":
							dirs.append(1)
						if dirs:
							dx = random.choice(dirs)
							matriz[y][x+dx], matriz[y][x] = matriz[y][x], matriz[y][x+dx]

def main():
    pygame.init()
    barra_altura = 30
    screen = pygame.display.set_mode((LARGURA, ALTURA+barra_altura))
    pygame.display.set_caption('Simulação Física - Selecione o bloco na barra | R: Reset')
    clock = pygame.time.Clock()
    rodando = True
    mouse_pressionado = False
    tempo_ultimo_bloco = 0
    DELAY_BLOCO_MS = 30
    bloco_selecionado = "Areia"
    opcoes = ["Areia", "Água", "Ar"]

    global temperatura_pixel
    temperatura_pixel = 20.0
    temperatura_min = -500.0
    temperatura_max = 2000.0
    temperatura_step = 5.0

    while rodando:
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_r]:
            for y in range(LINHAS):
                for x in range(COLUNAS):
                    matriz[y][x] = Ar(temperatura=20.0)
        if pressed[pygame.K_z]:
            temperatura_pixel = min(temperatura_pixel + temperatura_step, temperatura_max)
        if pressed[pygame.K_x]:
            temperatura_pixel = max(temperatura_pixel - temperatura_step, temperatura_min)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodando = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mx, my = pygame.mouse.get_pos()
                    # Clique na barra de seleção
                    if my < barra_altura:
                        idx = mx // 60
                        if 0 <= idx < len(opcoes):
                            bloco_selecionado = opcoes[idx]
                    else:
                        mouse_pressionado = True
                elif event.button == 4:  # Scroll up
                    temperatura_pixel = min(temperatura_pixel + temperatura_step, temperatura_max)
                elif event.button == 5:  # Scroll down
                    temperatura_pixel = max(temperatura_pixel - temperatura_step, temperatura_min)

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    mouse_pressionado = False

        mx, my = pygame.mouse.get_pos()
        x = mx // TAM_PIXEL
        y = (my - barra_altura) // TAM_PIXEL
        if mouse_pressionado and my >= barra_altura:
            if 0 <= x < COLUNAS and 0 <= y < LINHAS:
                agora = pygame.time.get_ticks()
                if agora - tempo_ultimo_bloco > DELAY_BLOCO_MS:
                    if bloco_selecionado == "Areia":
                        matriz[y][x] = Sand(temperatura=temperatura_pixel)
                    elif bloco_selecionado == "Água":
                        matriz[y][x] = Agua(temperatura=temperatura_pixel)
                    elif bloco_selecionado == "Ar":
                        matriz[y][x] = Ar(temperatura=temperatura_pixel)
                    tempo_ultimo_bloco = agora

        atualizar_fisica(matriz)
        desenhar_tela(screen, matriz, bloco_selecionado, temperatura_pixel)
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()

if __name__ == '__main__':
	main()

# Agora lista_ar é uma matriz 10x10 de objetos Ar
