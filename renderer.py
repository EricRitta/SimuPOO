import pygame
from utils import Vector2

class Renderer:
    def __init__(self, world, cell_size: int = 2):
        # Constantes
        self.WORLD = world
        self.UI_BAR_CELLS = 6

        self.LETTERBOX_COLOR = (50, 50, 50)
        self.BACKGROUND_COLOR = (20, 20, 20)
        self.UI_BAR_COLOR = (200, 200, 200)

        # Tela
        self.cell_size = cell_size
        self.DEFAULT_WIDTH = self.WORLD.WIDTH * cell_size
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

    def world_to_screen(self, world_pos: Vector2) -> tuple[float, float]:
        screen_x = self.offset_X + (world_pos.X * self.cell_size)
        screen_y = self.offset_Y + (world_pos.Y * self.cell_size)
        return screen_x, screen_y
    
    def screen_to_world(self, screen_x: int, screen_y: int) -> Vector2:
        world_x = int((screen_x - self.offset_X) / self.cell_size)
        world_y = int((screen_y - self.offset_Y) / self.cell_size)

        if 0 <= world_x < self.WORLD.WIDTH and 0 <= world_y < self.WORLD.HEIGTH:
            return Vector2(world_x, world_y)
        return None

    def render(self):
        # Enche a tela de cinza
        self.screen.fill(self.LETTERBOX_COLOR)

        # Barra superior para a UI 
        ui_bar_height = int(self.ui_bar_heigth)
        pygame.draw.rect(self.screen, self.UI_BAR_COLOR, (0, 0, self.window_width, ui_bar_height))

        # World grid
        world_width = int(self.WORLD.WIDTH * self.cell_size)
        world_height = int(self.WORLD.HEIGTH * self.cell_size)
        pygame.draw.rect(self.screen, self.BACKGROUND_COLOR, (int(self.offset_X), int(self.offset_Y), world_width, world_height))

        # Renderização direta das partículas - sem cache intermediário
        for chunk_Y in range(self.WORLD.Chunks_Quantity_Y - 1, -1, -1):
            for chunk_X in range(self.WORLD.Chunks_Quantity_X):
                chunk = self.WORLD.Chunks[chunk_Y][chunk_X]
                if chunk.isActive:
                    self._render_chunk(chunk)

        pygame.display.flip()

    def _calculate_scale(self):
        # Calcula a altura da barra UI baseada no cell_size atual
        ui_bar_height = self.UI_BAR_CELLS * self.cell_size
        
        # Escala da barra superior da UI
        available_height = self.window_height - ui_bar_height

        # Escala total da janela
        scale_X = self.window_width / self.WORLD.WIDTH
        scale_Y = available_height / self.WORLD.HEIGTH

        # Atualiza o cell_size baseado na menor escala
        self.cell_size = min(scale_X, scale_Y)

        # Recalcula offsets com o novo cell_size
        self.offset_X = (self.window_width - (self.WORLD.WIDTH * self.cell_size)) / 2
        ui_bar_height = self.UI_BAR_CELLS * self.cell_size
        self.offset_Y = ui_bar_height + (available_height - (self.WORLD.HEIGTH * self.cell_size)) / 2

    def _render_chunk(self, chunk):
        # Início da conversão para coordenada mundial
        base_x = chunk.Position.X * self.WORLD.CHUNK_SIZE
        base_y = chunk.Position.Y * self.WORLD.CHUNK_SIZE
        
        # Pre-calcular valores constantes
        cell_size = self.cell_size
        offset_X = self.offset_X
        offset_Y = self.offset_Y
        chunk_size = self.WORLD.CHUNK_SIZE
        screen = self.screen
        
        # Escolhe método de renderização baseado no tamanho da célula
        use_fill = cell_size <= 2
        
        # Itera pelas células do chunk
        for grid_y in range(chunk_size):
            # Otimização: calcula valores de Y uma vez por linha
            world_y = base_y + grid_y
            screen_y = offset_Y + (world_y * cell_size)
            next_y = int(screen_y + cell_size)
            screen_y_int = int(screen_y)
            height = max(1, next_y - screen_y_int)
            
            for grid_x in range(chunk_size):
                particle = chunk.GRID[grid_y][grid_x]
                
                if particle is not None:
                    # Posição mundial da partícula
                    world_x = base_x + grid_x
                    
                    # Converte para coordenadas da tela
                    screen_x = offset_X + (world_x * cell_size)
                    next_x = int(screen_x + cell_size)
                    screen_x_int = int(screen_x)
                    width = max(1, next_x - screen_x_int)

                    # Renderiza diretamente
                    if use_fill:
                        screen.fill(particle.Color, (screen_x_int, screen_y_int, width, height))
                    else:
                        pygame.draw.rect(screen, particle.Color, (screen_x_int, screen_y_int, width, height))
