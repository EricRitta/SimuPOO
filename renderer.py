import pygame
from utils import Vector2

class Renderer:
    def __init__(self, world, cell_size: int = 2):
        # Constantes
        self.WORLD = world
        self.UI_BAR_CELLS = 6
        self.MENU_WIDTH = 200

        self.LETTERBOX_COLOR = (50, 50, 50)
        self.BACKGROUND_COLOR = (20, 20, 20)
        self.UI_BAR_COLOR = (200, 200, 200)
        
        # Cores do menu
        self.MENU_BG_COLOR = (60, 60, 70)
        self.MENU_BORDER_COLOR = (100, 100, 110)
        self.MENU_HIGHLIGHT_COLOR = (80, 80, 150)
        self.MENU_TEXT_COLOR = (240, 240, 240)
        self.MENU_INSTRUCTION_COLOR = (180, 180, 200)

        # Tela
        self.cell_size = cell_size
        self.DEFAULT_WIDTH = self.WORLD.WIDTH * cell_size + self.MENU_WIDTH
        self.DEFAULT_HEIGTH = self.WORLD.HEIGTH * cell_size + (self.UI_BAR_CELLS * cell_size)
        
        self.window_width = self.DEFAULT_WIDTH
        self.window_height = self.DEFAULT_HEIGTH
        self.screen = pygame.display.set_mode(
            (self.window_width, self.window_height), 
            pygame.RESIZABLE | pygame.HWSURFACE | pygame.DOUBLEBUF
        )
        
        # Calcular a escala baseado no mundo
        self._calculate_scale()

    @property
    def ui_bar_heigth(self):
        return self.UI_BAR_CELLS * self.cell_size

    def handle_resize(self, new_width: int, new_height: int):
        if new_width != self.window_width or new_height != self.window_height:
            self.window_width = new_width
            self.window_height = new_height
            self._calculate_scale()

    def is_menu_click(self, screen_x: int, screen_y: int) -> bool:
        return screen_x < self.MENU_WIDTH

    def world_to_screen(self, world_pos: Vector2) -> tuple[float, float]:
        screen_x = self.offset_X + (world_pos.X * self.cell_size) + (self.MENU_WIDTH if hasattr(self, 'menu_visible') and self.menu_visible else 0)
        screen_y = self.offset_Y + (world_pos.Y * self.cell_size)
        return screen_x, screen_y
    
    def screen_to_world(self, screen_x: int, screen_y: int) -> Vector2:
        # Ajusta a coordenada X para considerar o menu
        adjusted_x = screen_x - (self.MENU_WIDTH if hasattr(self, 'menu_visible') and self.menu_visible else 0)
        world_x = int((adjusted_x - self.offset_X) / self.cell_size)
        world_y = int((screen_y - self.offset_Y) / self.cell_size)

        if 0 <= world_x < self.WORLD.WIDTH and 0 <= world_y < self.WORLD.HEIGTH:
            return Vector2(world_x, world_y)
        return None

    def render(self, show_menu=False, current_particle=None, all_particles=None):
        self.menu_visible = show_menu
        
        self.screen.fill(self.LETTERBOX_COLOR)

        # Desenhar menu se visível
        if show_menu:
            self._draw_menu(current_particle, all_particles)

        # Barra superior para a UI 
        ui_bar_height = int(self.ui_bar_heigth)
        bar_x = self.MENU_WIDTH if show_menu else 0
        bar_width = self.window_width - (self.MENU_WIDTH if show_menu else 0)
        pygame.draw.rect(self.screen, self.UI_BAR_COLOR, (bar_x, 0, bar_width, ui_bar_height))

        # World grid
        world_width = int(self.WORLD.WIDTH * self.cell_size)
        world_height = int(self.WORLD.HEIGTH * self.cell_size)
        grid_x = self.offset_X + (self.MENU_WIDTH if show_menu else 0)
        pygame.draw.rect(
            self.screen, 
            self.BACKGROUND_COLOR, 
            (int(grid_x), int(self.offset_Y), world_width, world_height)
        )

        # Renderização direta das partículas - sem cache intermediário
        for chunk_Y in range(self.WORLD.Chunks_Quantity_Y - 1, -1, -1):
            for chunk_X in range(self.WORLD.Chunks_Quantity_X):
                chunk = self.WORLD.Chunks[chunk_Y][chunk_X]
                if chunk.isActive:
                    self._render_chunk(chunk, show_menu)

        pygame.display.flip()

    def _draw_menu(self, current_particle, all_particles):
        # Fundo do menu
        pygame.draw.rect(self.screen, self.MENU_BG_COLOR, (0, 0, self.MENU_WIDTH, self.window_height))
        pygame.draw.rect(self.screen, self.MENU_BORDER_COLOR, (self.MENU_WIDTH, 0, 2, self.window_height))
        
        # Título do menu
        font_title = pygame.font.SysFont('Arial', 16, bold=True)
        title = font_title.render("PARTÍCULAS:", True, self.MENU_TEXT_COLOR)
        self.screen.blit(title, (10, 10))
        
        # Lista de partículas
        font_item = pygame.font.SysFont('Arial', 14)
        for i, particle in enumerate(all_particles):
            y_pos = 45 + i * 35
            
            # Destacar a partícula selecionada
            if particle == current_particle:
                pygame.draw.rect(self.screen, self.MENU_HIGHLIGHT_COLOR, 
                               (5, y_pos - 3, self.MENU_WIDTH - 10, 30))
            
            # Nome da partícula
            text = font_item.render(particle, True, self.MENU_TEXT_COLOR)
            self.screen.blit(text, (15, y_pos))
        
        # Instruções
        font_small = pygame.font.SysFont('Arial', 11)
        instructions = [
            "INSTRUÇÕES:",
            "Clique: Colocar partícula",
            "Botão Direito: Remover",
            "Espaço: Pausar/Continuar",
            "F11: Tela Cheia",
            "M: Mostrar/Ocultar Menu",
            "Tab: Próxima partícula"
        ]
        
        for i, instruction in enumerate(instructions):
            color = self.MENU_TEXT_COLOR if i == 0 else self.MENU_INSTRUCTION_COLOR
            text = font_small.render(instruction, True, color)
            self.screen.blit(text, (10, self.window_height - 130 + i * 18))

    def _calculate_scale(self):
        # Calcula a altura da barra UI baseada no cell_size atual
        ui_bar_height = self.UI_BAR_CELLS * self.cell_size
        
        # Escala da barra superior da UI
        available_height = self.window_height - ui_bar_height

        # Escala total da janela (considerando menu)
        available_width = self.window_width - (self.MENU_WIDTH if hasattr(self, 'menu_visible') and self.menu_visible else 0)

        scale_X = available_width / self.WORLD.WIDTH
        scale_Y = available_height / self.WORLD.HEIGTH

        # Atualiza o cell_size baseado na menor escala
        self.cell_size = min(scale_X, scale_Y)

        # Recalcula offsets com o novo cell_size
        self.offset_X = (available_width - (self.WORLD.WIDTH * self.cell_size)) / 2
        ui_bar_height = self.UI_BAR_CELLS * self.cell_size
        self.offset_Y = ui_bar_height + (available_height - (self.WORLD.HEIGTH * self.cell_size)) / 2

    def _render_chunk(self, chunk, show_menu):
        # Inicio da conversal para coordenada mundial
        base_x = chunk.Position.X * self.WORLD.CHUNK_SIZE
        base_y = chunk.Position.Y * self.WORLD.CHUNK_SIZE
        
        # Offset do menu
        menu_offset = self.MENU_WIDTH if show_menu else 0
        
        # Itera pelas células do chunk
        for grid_y in range(self.WORLD.CHUNK_SIZE):
            world_y = base_y + grid_y
            screen_y = self.offset_Y + (world_y * self.cell_size)
            screen_y_INT = int(screen_y)
            next_y = int(screen_y + self.cell_size)
            height = max(1, next_y - screen_y_INT)

            for grid_x in range(self.WORLD.CHUNK_SIZE):
                particle = chunk.GRID[grid_y][grid_x]
                if not isinstance(particle, (int, float)):

                    world_x = base_x + grid_x
                    screen_x = self.offset_X + (world_x * self.cell_size) + menu_offset
                    screen_x_INT = int(screen_x)
                    next_x = int(screen_x + self.cell_size)
                    width = max(1, next_x - screen_x_INT)

                    # Desenha a partícula
                    pygame.draw.rect(
                        self.screen,
                        particle.Color,
                        (screen_x_INT, screen_y_INT, width, height)
                    )