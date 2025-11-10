import pygame
from world import World
from renderer import Renderer
from eventHandler import EventHandler
from ui import Ui
import utils

def main():
    pygame.init()
    
    physics_accumulator = 0.0
    physics_timestep = 1.0 / utils.PHYSICS_RATE

    heat_accumulator = 0.0
    heat_timestep = 10.0 / utils.TARGET_FPS  # 10 frames no framerate alvo

    WORLD = World(utils.WORLD_WIDTH, utils.WORLD_HEIGTH, utils.CHUNK_SIZE)
    RENDERER = Renderer(WORLD, utils.CELL_SIZE)
    UI = Ui(RENDERER, WORLD)
    HANDLER = EventHandler(RENDERER, WORLD, UI)

    clock = pygame.time.Clock()
    running = True

    all_particles = ["Dirt", "Water", "Metal", "Mud", "Fire", "Steam", "BlueFire"]
    particle_selector = 0
    current_particle = "Dirt"

    while running:
        dt = clock.tick(utils.TARGET_FPS) / 1000.0
        dt = 0.1 if dt > 0.1 else dt

        eventsResult = HANDLER.handleEvents()
        if eventsResult is False:
            running = False
     
        mouseResults = HANDLER.handleContinuosMouse()

        if WORLD.Running:
            physics_accumulator += dt
            while physics_accumulator >= physics_timestep:
                WORLD.update()
                physics_accumulator -= physics_timestep

            heat_accumulator += dt
            while heat_accumulator >= heat_timestep:
                WORLD.updateHeat()
                heat_accumulator -= heat_timestep

        RENDERER.render()
        UI.render()
        pygame.display.flip()
        
        fps = clock.get_fps()
        paused_text = "[PAUSED]" if not WORLD.Running else ""
        pygame.display.set_caption(f"{paused_text} SimuPOO - FPS: {fps:.1f} - Selected: {current_particle}")

    pygame.quit()
    
if __name__ == "__main__":
    main()
