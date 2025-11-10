import pygame
from world import World
from renderer import Renderer
import utils

def main():
    pygame.init()
    
    physics_accumulator = 0.0
    physics_timestep = 1.0 / utils.PHYSICS_RATE

    heat_accumulator = 0.0
    heat_timestep = 10.0 / utils.TARGET_FPS  # 10 frames no framerate alvo

    WORLD = World(utils.WORLD_WIDTH, utils.WORLD_HEIGTH, utils.CHUNK_SIZE)
    RENDERER = Renderer(WORLD, utils.CELL_SIZE)

    clock = pygame.time.Clock()
    running = True
    paused = False
    fullscreen = False

    all_particles = ["Dirt", "Water", "Metal", "Mud", "Fire", "Steam", "BlueFire"]
    particle_selector = 0
    current_particle = "Dirt"

    # Variáveis do menu
    show_menu = True

    while running:
        dt = clock.tick(utils.TARGET_FPS) / 1000.0
        dt = 0.1 if dt > 0.1 else dt

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.VIDEORESIZE:
                RENDERER.handle_resize(event.w, event.h)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    particle_selector += 1
                    if particle_selector > (len(all_particles) - 1): particle_selector = 0
                    current_particle = all_particles[particle_selector]

                if event.key == pygame.K_SPACE:
                    paused = not paused

                if event.key == pygame.K_F11:
                    fullscreen = not fullscreen
                    if fullscreen:
                        RENDERER.screen = pygame.display.set_mode(
                            (0, 0), 
                            pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF
                        )
                        display_info = pygame.display.Info()
                        RENDERER.handle_resize(display_info.current_w, display_info.current_h)
                    else:
                        RENDERER.screen = pygame.display.set_mode(
                            (RENDERER.DEFAULT_WIDTH, RENDERER.DEFAULT_HEIGTH),
                            pygame.RESIZABLE | pygame.HWSURFACE | pygame.DOUBLEBUF
                        )
                        RENDERER.handle_resize(RENDERER.DEFAULT_WIDTH, RENDERER.DEFAULT_HEIGTH)
                
                # Tecla M para mostrar/ocultar menu
                if event.key == pygame.K_m:
                    show_menu = not show_menu

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Botão esquerdo do mouse
                    mouse_X, mouse_Y = pygame.mouse.get_pos()
                    
                    # Verificar se clicou no menu
                    if show_menu and RENDERER.is_menu_click(mouse_X, mouse_Y):
                        menu_item_height = 30
                        menu_start_y = 40
                        
                        for i, particle in enumerate(all_particles):
                            item_y = menu_start_y + i * menu_item_height
                            if item_y <= mouse_Y <= item_y + menu_item_height:
                                current_particle = particle
                                particle_selector = i
                                break

        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_buttons[0] or mouse_buttons[2]:
            mouse_X, mouse_Y = pygame.mouse.get_pos()

            # Só processar clique no mundo se não estiver clicando no menu
            if not (show_menu and RENDERER.is_menu_click(mouse_X, mouse_Y)):
                worldPos = RENDERER.screen_to_world(mouse_X, mouse_Y)
                if worldPos:
                    particle_type = None if mouse_buttons[2] else current_particle

                    brush_size = 1
                    for dy in range(-brush_size, brush_size + 1):
                        for dx in range(-brush_size, brush_size + 1):
                            realWorldPos = worldPos + utils.Vector2(dx, dy)

                            if 0 <= realWorldPos.X < WORLD.WIDTH and 0 <= realWorldPos.Y < WORLD.HEIGTH:
                                WORLD.setParticle(particle_type, realWorldPos)
        
        if not paused:
            physics_accumulator += dt
            while physics_accumulator >= physics_timestep:
                WORLD.update()
                physics_accumulator -= physics_timestep

            heat_accumulator += dt
            while heat_accumulator >= heat_timestep:
                WORLD.updateHeat()
                heat_accumulator -= heat_timestep

        # Renderização com menu
        RENDERER.render(show_menu=show_menu, current_particle=current_particle, all_particles=all_particles)
        
        fps = clock.get_fps()
        paused_text = "[PAUSED]" if paused else ""
        menu_text = "" if show_menu else " | [M] Menu"
        pygame.display.set_caption(f"{paused_text} SimuPOO - FPS: {fps:.1f} - Selected: {current_particle}{menu_text}")

    pygame.quit()
    
if __name__ == "__main__":
    main()