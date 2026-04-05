import pygame
from game import Game
from renderer import Renderer

def main():
    game = Game(20, 20)
    renderer = Renderer(cell_size=20, grid_width=20, grid_height=20)
    clock = pygame.time.Clock()
    
    running = True
    action = None
    
    while running:
        # 1. Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                # Based on the action space: [straight, right, left] (relative to heading)
                # To make this playable by human, we translate WASD mapping to relative turns.
                # Actually, translating absolute to relative is tricky on the fly. 
                # Let's map arrows to absolute, but step expects relative. We'll hack absolute inputs for human mode.
                pass
                
        # For a simple manual play verify, let's just use absolute keys directly, modifying the game heading
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and game.heading != (0, 1):
            game.heading = (0, -1)
        elif keys[pygame.K_DOWN] and game.heading != (0, -1):
            game.heading = (0, 1)
        elif keys[pygame.K_LEFT] and game.heading != (1, 0):
            game.heading = (-1, 0)
        elif keys[pygame.K_RIGHT] and game.heading != (-1, 0):
            game.heading = (1, 0)
            
        # 2. Step Game (passing None means keep current heading)
        if game.alive:
            game.step(None)
            
        # 3. Render
        renderer.draw_state(game)
        
        # 4. Tick
        clock.tick(10) # 10 frames per second
        
    pygame.quit()

if __name__ == "__main__":
    main()
