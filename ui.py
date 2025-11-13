from utils import Vector2
import pygame
import utils

# Curva bezier
def BezierInAcc(t: float) -> float:
    if t <= 0:
        return 0
    if t >= 1:
        return 1

    # peguei essa curva da ia fi, fico legal até
    return 1 - (1 - t)**2 * (2.7 * (1 - t) - 1.7)

class Button:
    def __init__(self, name: str, particle: str, color: tuple[int, int, int]):
        # Basic
        self.NAME = name
        self.PARTICLE = particle
        self.COLOR = color
        self.MAX_RADIUS = 0
        self.Position = Vector2(0, 0)
        self.Radius = 0

        # Variables
        self.SelectedFrames = 0
        self.Hovering = False
        self.Active = False

        # Constants
        self.MAX_SELECTED_FRAMES = 30

        self.MARGIN_COLOR = (200, 200, 200)
        self.SEPARATOR_COLOR = (20, 20, 20)
        self.SELECTED_COLOR = (200, 255, 100)
        self.SEPARATOR_DIVISOR = 1.1
        self.INSIDE_DIVISOR = 1.05

    def draw(self, RENDERER, font):
        # Texto do nome da particula
        if font is not None:
            self._drawInfo(RENDERER, font)

        # margin
        margin_color = self.MARGIN_COLOR if not self.Active else self.SELECTED_COLOR
        pygame.draw.circle(
            RENDERER.screen,
            margin_color,
            (self.Position.X, self.Position.Y),
            self.Radius,
        )

        # separador preto, bordinha pequena dentro da margin
        separetor_radius = self.Radius / self.SEPARATOR_DIVISOR
        pygame.draw.circle(
            RENDERER.screen,
            self.SEPARATOR_COLOR,
            (self.Position.X, self.Position.Y),
            separetor_radius,
        )

        # cor do botão em si
        pygame.draw.circle(
            RENDERER.screen,
            self.COLOR,
            (self.Position.X, self.Position.Y),
            separetor_radius / self.INSIDE_DIVISOR,
        )

    def _updateRadiusAndPosition(self, position: Vector2, max_radius):
        # Mudar a posição e o radius maximo para calcular o radius normal
        self.Position = position
        self.MAX_RADIUS = max_radius
        normal_radius = self.MAX_RADIUS * 0.8

        # bezierzinha pai, não tem como
        t = self.SelectedFrames / self.MAX_SELECTED_FRAMES
        eased_t = BezierInAcc(t)

        # Mudar o tamanho do raio de acordo com o tempo que ficou hovering
        radius_diff = self.MAX_RADIUS - normal_radius
        self.Radius = normal_radius + radius_diff * eased_t

    def _drawInfo(self, RENDERER, font):
        # se não tiver selected frames, nem renderiza
        if self.SelectedFrames > 0:
            # bezier para fazer animação suave
            t = self.SelectedFrames / self.MAX_SELECTED_FRAMES
            progress = BezierInAcc(t)
            
            # transparencia e posição baseado na bezier
            alpha = int(255 * progress)
            text_offset = (self.MAX_RADIUS + (3 * RENDERER.cell_size)) * progress
            text_y = self.Position.Y + text_offset
            
            # surface
            text_surface = font.render(self.NAME, True, (255, 255, 255))
            text_surface.set_alpha(alpha)
            
            # renderização do textin
            text_rect = text_surface.get_rect(center=(self.Position.X, text_y))
            RENDERER.screen.blit(text_surface, text_rect)


class Ui:
    def __init__(self, RENDERER, WORLD):
        # Basico
        self.WORLD = WORLD
        self.RENDERER = RENDERER
        self.MENU_DIVISOR = 5

        # Constants
        self.SCROLL_FORCE = 30

        # Valores da UI Superior
        self.ParticlesButtons = []
        bar_height = self.RENDERER.ui_bar_heigth
        possible_buttons = self.RENDERER.window_width / bar_height
        self.TOPUI_Max_ScrollFrames = int(bar_height * max(0, len(self.ParticlesButtons) - possible_buttons))
        self.TOPUI_ScrollFrames = 0
        self.TOPUI_SelectedButton = None

        # Valores do Menu
        self.isMenuOpen = False
        self.MENU_TEXT = (248, 249, 250)
        self.MENU_MARGIN = (33, 37, 41)
        self.MENU_BACKGROUND = (52, 58, 64)

        self.MENU_MAX_ANIMATION_FRAMES = 30
        self.MENU_AnimationFrames = 0

        self.MenuFont = pygame.font.Font(None, int(6 * self.RENDERER.cell_size))

        # code
        self.font = pygame.font.Font(None, int(6 * self.RENDERER.cell_size))
        for particle in utils.PARTICLES_INFO:
            self.ParticlesButtons.append(Button(particle["Name"], particle["Particle"], particle["Color"]))

    @property
    def menuWidth(self):
        return self.RENDERER.window_width / self.MENU_DIVISOR

    # mudar depois para ser global, ou seja, qualquer botão da UI
    @property
    def HoveringOnButton(self):
        for i, button in enumerate(self.ParticlesButtons):
            if button.Hovering is True:
                return i 

    @property
    def CurrentParticle(self):
        if self.TOPUI_SelectedButton is None: return None
        button = self.ParticlesButtons[self.TOPUI_SelectedButton]
        return None if not button else button.PARTICLE

    def handleResize(self):
        # TOPUI
        scroll_percentage = self.TOPUI_ScrollFrames / self.TOPUI_Max_ScrollFrames if self.TOPUI_Max_ScrollFrames > 0 else 0

        bar_height = self.RENDERER.ui_bar_heigth
        possible_buttons = self.RENDERER.window_width / bar_height
        self.TOPUI_Max_ScrollFrames = int(bar_height * max(0, len(self.ParticlesButtons) - possible_buttons))

        self.TOPUI_ScrollFrames = self.TOPUI_Max_ScrollFrames * scroll_percentage
        self.font = pygame.font.Font(None, int(6 * self.RENDERER.cell_size))

        # Menu
        self.MenuFont = pygame.font.Font(None, int(6 * self.RENDERER.cell_size))

    def render(self):
        self._renderTopUI()
        self._renderMenu()

# TOPUI -------------------------------------------------------------------------------------------------
    def _renderTopUI(self):
        mousePos = self.__getMouse()
        circle_MaxRadius = (self.RENDERER.ui_bar_heigth * 0.95) / 2
        circle_Y = self.RENDERER.offset_Y - self.RENDERER.ui_bar_heigth / 2

        for i, button in enumerate(self.ParticlesButtons):
            circle_X = (circle_MaxRadius * 1.2) + (circle_MaxRadius * 2) * i - min(self.TOPUI_ScrollFrames, self.TOPUI_Max_ScrollFrames)
            if circle_X - circle_MaxRadius > self.RENDERER.window_width: continue
            if circle_X + circle_MaxRadius < 0: continue

            button._updateRadiusAndPosition(Vector2(circle_X, circle_Y), circle_MaxRadius)
            mouseHovering = self.__isMouseInCircularBounds(mousePos, Vector2(circle_X, circle_Y), button.Radius)
            if mouseHovering:
                button.Hovering = True
                button.SelectedFrames = min(button.MAX_SELECTED_FRAMES, button.SelectedFrames + 1)
            else:
                button.Hovering = False
                button.SelectedFrames = max(0, button.SelectedFrames - 1)

            button.draw(self.RENDERER, self.font)

    def selectTOPUIButton(self, index):
        if self.TOPUI_SelectedButton == index: return
        # desativar tudo
        for button in self.ParticlesButtons:
            button.Active = False

        button = self.ParticlesButtons[index]
        if not button: return
        button.Active = True
        self.TOPUI_SelectedButton = index

### MENU ---------------------------------------------------------------------------------------------------
    def _renderMenu(self):
        if self.isMenuOpen:
            self.MENU_AnimationFrames = min(self.MENU_MAX_ANIMATION_FRAMES, self.MENU_AnimationFrames + 1)
        else:
            self.MENU_AnimationFrames = max(0, self.MENU_AnimationFrames - 1)
        self.__drawMenu()

    def __drawMenu(self):
        if self.MENU_AnimationFrames <= 0: return
        t = self.MENU_AnimationFrames / self.MENU_MAX_ANIMATION_FRAMES
        eased_t = BezierInAcc(t)

        # Tamanho
        menu_width = self.menuWidth * eased_t
        menu_height = self.RENDERER.window_height

        # MARGIN
        pygame.draw.rect(
            self.RENDERER.screen,
            self.MENU_MARGIN,
            (0, 0, menu_width, menu_height)
        )

        # BACKGROUND
        background_width = menu_width * 0.95
        background_height = menu_height * 0.98
        pygame.draw.rect(
            self.RENDERER.screen,
            self.MENU_BACKGROUND,
            ((menu_width - background_width) / 2, (menu_height - background_height) / 2, background_width, background_height)
        )

# PRIVADA: NÃO ACESSAR, REPITO, NÃO GOZAR
    def __getMouse(self) -> Vector2:
        mouse_X, mouse_Y = pygame.mouse.get_pos()
        return Vector2(mouse_X, mouse_Y)

    def __isMouseInCircularBounds(self, mousePos: Vector2, buttonPos: Vector2, radius) -> bool:
        if self.isMenuOpen: return False
        dx = mousePos.X - buttonPos.X
        dy = mousePos.Y - buttonPos.Y
        distance_squared = dx * dx + dy * dy
        return distance_squared <= radius**2
