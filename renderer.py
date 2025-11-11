import pygame
import utils
from utils import Vector2

class Renderer:
    def __init__(self, world, cell_size: int = 2):
        # Constantes
        self.WORLD = world
        self.UI_BAR_CELLS = 14

        self.LETTERBOX_COLOR = (30, 30, 30)
        self.BACKGROUND_COLOR = (20, 20, 20)
        self.UI_BAR_COLOR = (30, 30, 30)

        # Tela
        self.cell_size = cell_size
        self.DEFAULT_WIDTH = self.WORLD.WIDTH * cell_size
        self.DEFAULT_HEIGTH = self.WORLD.HEIGTH * cell_size #+ (self.UI_BAR_CELLS * cell_size)
        
        self.window_width = self.DEFAULT_WIDTH
        self.window_height = self.DEFAULT_HEIGTH
        self.screen = pygame.display.set_mode(
            (self.window_width, self.window_height), 
            pygame.RESIZABLE | pygame.HWSURFACE | pygame.DOUBLEBUF
        )
        
        self.Fullscreen = False
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
        pygame.draw.rect(
            self.screen, 
            self.BACKGROUND_COLOR, 
            (int(self.offset_X), int(self.offset_Y), world_width, world_height)
        )

        # Renderização direta das partículas - sem cache intermediário
        for chunk_Y in range(self.WORLD.Chunks_Quantity_Y - 1, -1, -1):
            for chunk_X in range(self.WORLD.Chunks_Quantity_X):
                chunk = self.WORLD.Chunks[chunk_Y][chunk_X]
                if chunk.isActive:
                    self._render_chunk(chunk)

        self._render_brush_preview()

    def _render_brush_preview(self):
            if utils.BRUSH_RADIUS <= 0:
                return
            
            mouse_x, mouse_y = pygame.mouse.get_pos()
            worldPos = self.screen_to_world(mouse_x, mouse_y)
            if not worldPos: return

            radius_in_pixels = int(utils.BRUSH_RADIUS * self.cell_size)
            diameter = radius_in_pixels * 2 + 4
            preview_surface = pygame.Surface((diameter, diameter), pygame.SRCALPHA)
            
            pygame.draw.circle(
                preview_surface,
                (255, 255, 255, 50),
                (diameter // 2, diameter // 2),
                radius_in_pixels
            )
            
            self.screen.blit(preview_surface, (mouse_x - diameter // 2, mouse_y - diameter // 2))

    def _calculate_scale(self):
        scale_X = self.window_width / self.WORLD.WIDTH
        scale_Y = self.window_height / (self.WORLD.HEIGTH + self.UI_BAR_CELLS)

        self.cell_size = min(scale_X, scale_Y)

        ui_bar_height = self.UI_BAR_CELLS * self.cell_size
        world_pixel_height = self.WORLD.HEIGTH * self.cell_size

        self.offset_X = (self.window_width - (self.WORLD.WIDTH * self.cell_size)) / 2
        self.offset_Y = ui_bar_height
    
    def _render_chunk(self, chunk):
        # Inicio da conversal para coordenada mundial
        base_x = chunk.Position.X * self.WORLD.CHUNK_SIZE
        base_y = chunk.Position.Y * self.WORLD.CHUNK_SIZE
        
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
                    screen_x = self.offset_X + (world_x * self.cell_size)
                    screen_x_INT = int(screen_x)
                    next_x = int(screen_x + self.cell_size)
                    width = max(1, next_x - screen_x_INT)

                    # Desenha a partícula
                    pygame.draw.rect(
                        self.screen,
                        particle.Color,
                        (screen_x_INT, screen_y_INT, width, height)
                    )
