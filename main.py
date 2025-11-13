import pygame
from world import World
from renderer import Renderer
from eventHandler import EventHandler
from ui import Ui
import utils

def main():
    pygame.init()
    print("Press [M] to open the menu!")
    
    physics_accumulator = 0.0
    physics_timestep = 1.0 / utils.PHYSICS_RATE

    heat_accumulator = 0.0
    heat_timestep = 10.0 / utils.TARGET_FPS  # 10 frames no framerate alvo

    WORLD = World(utils.WORLD_WIDTH, utils.WORLD_HEIGTH, utils.CHUNK_SIZE)
    RENDERER = Renderer(WORLD, utils.CELL_SIZE)
    UI = Ui(RENDERER, WORLD)
    EVENT_HANDLER = EventHandler(RENDERER, WORLD, UI)

    clock = pygame.time.Clock()
    running = True

    while running:
        dt = clock.tick(utils.TARGET_FPS) / 1000.0
        dt = 0.1 if dt > 0.1 else dt

        eventsResult = EVENT_HANDLER.handle()
        if eventsResult is False:
            running = False
     
        mouseResults = EVENT_HANDLER.handleContinuosMouse()

        # implementação horrososa de dt, mas a preguiça fala mais alto
        if WORLD.Running:
            physics_accumulator += dt
            while physics_accumulator >= physics_timestep:
                WORLD.update()
                physics_accumulator -= physics_timestep

            heat_accumulator += dt
            while heat_accumulator >= heat_timestep:
                WORLD.updateHeat()
                heat_accumulator -= heat_timestep

        fps = clock.get_fps()
        RENDERER.render(f"{fps:.1f}")
        UI.render()
        pygame.display.flip()
        
        pygame.display.set_caption(f"SimuPOO")

    pygame.quit()
    
if __name__ == "__main__":
    main()
