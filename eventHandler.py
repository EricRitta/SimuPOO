from utils import Vector2
import pygame
import utils

class EventHandler:
    def __init__(self, RENDERER, WORLD, UI):
        self.UI = UI
        self.WORLD = WORLD
        self.RENDERER = RENDERER

    def handleEvents(self):
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

    def __handleKeydown(self, key):
        if key == pygame.K_ESCAPE:
            return False

        if key == pygame.K_SPACE:
            self.WORLD.Running = not self.WORLD.Running

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
    def handleContinuosMouse(self):
        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_buttons[0] or mouse_buttons[2]:
            mouse_X, mouse_Y = pygame.mouse.get_pos()

            worldPos = self.RENDERER.screen_to_world(mouse_X, mouse_Y)
            if worldPos:
                particle_type = None if mouse_buttons[2] else self.UI.CurrentParticle
                self.WORLD.setParticle(particle_type, worldPos)

    def __handleMousePress(self):
        pressed = pygame.mouse.get_pressed()
        if pressed[0]:
            hoverButtonIndex = self.UI.HoveringNow
            if hoverButtonIndex is not None:
                self.UI.SelectedButton = hoverButtonIndex
                self.UI.ButtonsList[hoverButtonIndex].Active = True

    def __handleMouseWheel(self, event):
        mouse_X, mouse_Y = pygame.mouse.get_pos()
        boundWidth = self.RENDERER.window_width
        boundHeight = self.RENDERER.ui_bar_heigth / 2
        if self.__isMouseInBounds(Vector2(mouse_X, mouse_Y), Vector2(boundWidth, boundHeight)):
            self.UI.ScrollFrames = min(self.UI.MAX_SCROLLFRAMES, self.UI.ScrollFrames + (event.y * self.UI.SCROLL_JUMP))
            self.UI.ScrollFrames = max(0, self.UI.ScrollFrames)

    def __isMouseInBounds(self, mousePos: Vector2, maxPos: Vector2):
        xBound = maxPos.X - mousePos.X
        yBound = maxPos.Y - mousePos.Y

        if xBound > maxPos.X or xBound < 0: return False
        if yBound > maxPos.Y or yBound < 0: return False
        return True
