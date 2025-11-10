from utils import Vector2
import pygame
import utils

# Constantes -----------------------
SELECTED_COLOR = utils.SELECTED_COLOR
OUT_BORDER_COLOR = utils.OUT_BORDER_COLOR
IN_BORDER_COLOR = utils.IN_BORDER_COLOR

OUT_BORDER_DIVISOR = utils.OUT_BORDER_DIVISOR
IN_BORDER_DIVISOR = utils.IN_BORDER_DIVISOR
INSIDE_DIVISOR = utils.INSIDE_DIVISOR

FULLY_SELECTED_FRAMES = utils.FULLY_SELECTED_FRAMES
SELECTED_BONUS_RADIUS = utils.SELECTED_BONUS_RADIUS

DEFAULT_BUTTON_SPACE = utils.DEFAULT_BUTTON_SPACE
#------------------------------------

class CircleButton:
    def __init__(self, name: str, color: tuple[int, int, int]):
        self.NAME = name
        self.COLOR = color

        self.Position = Vector2(0, 0)
        self.Hovering = False
        self.SelectedFrames = 0
        self.Active = False
    
        self.current_radius = 0
        self.in_border_radius = 0
        self.inside_radius = 0

    def _updatePos(self, position: Vector2, ui_bar_heigth: (int, float), cell_size: (int, float)):
        self.Position = position
        selected_size = SELECTED_BONUS_RADIUS * cell_size

        t = self.SelectedFrames / FULLY_SELECTED_FRAMES
        eased_t = utils.BezierInAcc(t)
        size_ratio = selected_size * eased_t

        self.current_radius = ((ui_bar_heigth / 2) / OUT_BORDER_DIVISOR) + size_ratio
        self.in_border_radius = (self.current_radius / IN_BORDER_DIVISOR)
        self.inside_radius = (self.in_border_radius / INSIDE_DIVISOR)
    
    def _drawInfo(self, RENDERER, font):
        if self.SelectedFrames > 0:
            t = self.SelectedFrames / FULLY_SELECTED_FRAMES
            progress = utils.BezierInAcc(t)
            
            alpha = int(255 * progress)
            text_offset = (self.current_radius + (3 * RENDERER.cell_size)) * progress
            text_y = self.Position.Y + text_offset
            
            text_surface = font.render(self.NAME, True, (255, 255, 255))
            text_surface.set_alpha(alpha)
            
            text_rect = text_surface.get_rect(center=(self.Position.X, text_y))
            RENDERER.screen.blit(text_surface, text_rect)

    def draw(self, RENDERER, font, position: Vector2):
        ui_bar_heigth = RENDERER.ui_bar_heigth
        cell_size = RENDERER.cell_size
        self._updatePos(position, ui_bar_heigth, cell_size)
        self._drawInfo(RENDERER, font)

        out_color = OUT_BORDER_COLOR if not self.Active else SELECTED_COLOR
        pygame.draw.circle(
            RENDERER.screen,
            out_color,
            (position.X, position.Y),
            self.current_radius,
        )
        pygame.draw.circle(
            RENDERER.screen,
            IN_BORDER_COLOR,
            (position.X, position.Y),
            self.in_border_radius,
        )
        pygame.draw.circle(
            RENDERER.screen,
            self.COLOR,
            (position.X, position.Y),
            self.inside_radius,
        )

class Ui:
    def __init__(self, RENDERER, WORLD):
        self.WORLD = WORLD
        self.RENDERER = RENDERER

        self.ButtonsList = []
        self.MAX_SCROLLFRAMES = int(self.RENDERER.ui_bar_heigth * max(1, len(self.ButtonsList) - 6))
        self.SCROLL_JUMP = 10

        self.SelectedButton = None
        self.ScrollFrames = 0

        self.font = pygame.font.Font(None, int(6 * self.RENDERER.cell_size))
        for particle in utils.PARTICLES_INFO:
            self.ButtonsList.append(CircleButton(particle["Name"], particle["Color"]))

    @property
    def CurrentParticle(self):
        if self.SelectedButton is None: return None
        button = self.ButtonsList[self.SelectedButton]
        return None if not button else button.NAME

    @property
    def HoveringNow(self):
        for i, button in enumerate(self.ButtonsList):
            if button.Hovering is True:
                return i 

    def handleResize(self):
        percentage = self.ScrollFrames / self.MAX_SCROLLFRAMES
        self.MAX_SCROLLFRAMES = int(self.RENDERER.ui_bar_heigth * max(1, len(self.ButtonsList) - 6))
        self.ScrollFrames = self.MAX_SCROLLFRAMES * percentage
        self.font = pygame.font.Font(None, int(6 * self.RENDERER.cell_size))

    def render(self):
        mouse_pos = pygame.mouse.get_pos()
        circle_Y = self.RENDERER.ui_bar_heigth / 2
        radius = circle_Y
        default_spacing = (radius + (SELECTED_BONUS_RADIUS * self.RENDERER.cell_size)) * DEFAULT_BUTTON_SPACE
        dynamic_spacing = ((radius * 2) + (SELECTED_BONUS_RADIUS * self.RENDERER.cell_size)) * DEFAULT_BUTTON_SPACE

        for i, button in enumerate(self.ButtonsList):
            circle_X = default_spacing + (dynamic_spacing * i) - min(self.ScrollFrames, self.MAX_SCROLLFRAMES)
            if circle_X - radius > self.RENDERER.window_width / 2: continue
            if circle_X + radius < 0: continue

            mouseHover = self.__isMouseHovering(mouse_pos, (circle_X, circle_Y), radius)
            if mouseHover:
                button.Hovering = True
                button.SelectedFrames = min(FULLY_SELECTED_FRAMES, button.SelectedFrames + 1)
            else:
                button.Hovering = False
                button.SelectedFrames = max(0, button.SelectedFrames - 1)

            button.draw(self.RENDERER, self.font, Vector2(circle_X, circle_Y))

        # Barra segundaria, vai pela metade para esconder os circulos
        ui_bar_height = int(self.RENDERER.ui_bar_heigth)
        pygame.draw.rect(
            self.RENDERER.screen, 
            self.RENDERER.UI_BAR_COLOR, 
            (self.RENDERER.window_width / 2, 0, self.RENDERER.window_width / 2, ui_bar_height)
        )

        # Separados, só por estética mesmo
        separator_height = ui_bar_height
        separator_width = 2 * self.RENDERER.cell_size
        pygame.draw.rect(
            self.RENDERER.screen,
            self.RENDERER.BACKGROUND_COLOR,
            (self.RENDERER.window_width / 2, 0, separator_width, separator_height),
        )

    def __isMouseHovering(self, mousePos: tuple[int, int], buttonPos: tuple[int, int], radius: (int, float)) -> bool:
        dx = mousePos[0] - buttonPos[0]
        dy = mousePos[1] - buttonPos[1]
        distance_squared = dx * dx + dy * dy
        return distance_squared <= radius * radius
