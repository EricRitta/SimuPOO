from utils import Vector2
import pygame
import utils

class EventHandler:
    def __init__(self, RENDERER, WORLD, UI):
        self.UI = UI
        self.WORLD = WORLD
        self.RENDERER = RENDERER

        # Brush
        self.LastDrawCenterPoint = None

# MÉTODO PRINCIPAL ----------------------------------------------
    def handle(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            elif event.type == pygame.VIDEORESIZE:
                self.RENDERER.handle_resize(event.w, event.h)
                self.UI.handleResize()

            elif event.type == pygame.KEYDOWN:
                result = self.__handleKeydown(event.key)
                if result is False:
                    return False

            elif event.type == pygame.MOUSEWHEEL:
                self.__handleMouseWheel(event)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.__handleMousePress()

# TECLADO -------------------------------------------------------------------
    def __handleKeydown(self, key):
        # pausar
        if key == pygame.K_ESCAPE:
            self.WORLD.Running = not self.WORLD.Running

        # ir para o proximo frame
        if key == pygame.K_SPACE:
            if not self.WORLD.Running:
                self.WORLD.update()

        # fullscreen
        if key == pygame.K_F11:
            self.RENDERER.Fullscreen = not self.RENDERER.Fullscreen

            if self.RENDERER.Fullscreen:
                self.RENDERER.screen = pygame.display.set_mode(
                    (0, 0), 
                    pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF
                )
                display_info = pygame.display.Info()
                self.RENDERER.handle_resize(display_info.current_w, display_info.current_h)

            else:
                self.RENDERER.screen = pygame.display.set_mode(
                    (self.RENDERER.DEFAULT_WIDTH, self.RENDERER.DEFAULT_HEIGTH),
                    pygame.RESIZABLE | pygame.HWSURFACE | pygame.DOUBLEBUF
                )
                self.RENDERER.handle_resize(self.RENDERER.DEFAULT_WIDTH, self.RENDERER.DEFAULT_HEIGTH)

            self.UI.handleResize()


# MOUSE ---------------------------------------------------------------------------------
    # BRUSH __________________________________________________________________
    def handleContinuosMouse(self):
        M1, SCROLL, M2 = pygame.mouse.get_pressed()
        if M1 or M2:
            mousePos = self.__getMouse()
            worldCenterPoint = self.RENDERER.screen_to_world(mousePos.X, mousePos.Y)
            if worldCenterPoint:

                particleName = None if M2 else self.UI.CurrentParticle
                if self.LastDrawCenterPoint is None: self.LastDrawCenterPoint = worldCenterPoint
                self.WORLD.iterateAndApplyMethodBetweenTwoPoints(
                    self.LastDrawCenterPoint,
                    worldCenterPoint,
                    lambda w, pos: self.__drawPoints(particleName, pos)
                )
                self.LastDrawCenterPoint = worldCenterPoint

        else:
            self.LastDrawCenterPoint = None

    def __drawPoints(self, particleName: str, point: Vector2):
        for dy in range(-utils.BRUSH_RADIUS, utils.BRUSH_RADIUS + 1):
            for dx in range(-utils.BRUSH_RADIUS, utils.BRUSH_RADIUS + 1):
                if dx*dx + dy*dy <= utils.BRUSH_RADIUS**2:

                    existingParticle = self.WORLD.getParticle(Vector2(point.X + dx, point.Y + dy))
                    if existingParticle is False: return
                    if existingParticle is None or existingParticle.NAME != particleName:
                        self.WORLD.setParticle(particleName, Vector2(point.X + dx, point.Y + dy), True)
    # ____________________________________________________________________________

    def __handleMousePress(self):
        pressed = pygame.mouse.get_pressed()
        if pressed[0]:
            hoverButtonIndex = self.UI.HoveringOnButton
            if hoverButtonIndex is not None:
                self.UI.selectTOPUIButton(hoverButtonIndex)

    def __handleMouseWheel(self, event):
        mouse_X, mouse_Y = pygame.mouse.get_pos()
        if self.__isMouseInTOPUIBounds(Vector2(mouse_X, mouse_Y)):
            self.UI.TOPUI_ScrollFrames = min(self.UI.TOPUI_Max_ScrollFrames, self.UI.TOPUI_ScrollFrames + (event.y * self.UI.SCROLL_FORCE))
            self.UI.TOPUI_ScrollFrames = max(0, self.UI.TOPUI_ScrollFrames)
        else:
            utils.BRUSH_RADIUS = max(0, utils.BRUSH_RADIUS + event.y)

    def __isMouseInTOPUIBounds(self, mousePos: Vector2):
        maxPos = Vector2(self.RENDERER.window_width, self.RENDERER.ui_bar_heigth)
        xBound = maxPos.X - mousePos.X
        yBound = maxPos.Y - mousePos.Y

        if xBound > maxPos.X or xBound < 0: return False
        if yBound > maxPos.Y or yBound < 0: return False
        return True

    def __getMouse(self) -> Vector2:
        mouse_X, mouse_Y = pygame.mouse.get_pos()
        return Vector2(mouse_X, mouse_Y)
