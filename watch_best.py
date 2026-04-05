import neat
import os
import pygame
import pickle
from game import Game
from ai_controller import get_state_vector
from renderer import Renderer

def watch_best():
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    model_path = os.path.join(local_dir, 'best_snake.pkl')
    
    if not os.path.exists(model_path):
        print(f"No saved model found at {model_path}. Please complete training first via `python train.py`.")
        return
        
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path
    )
    
    # Load the winner
    with open(model_path, 'rb') as f:
        genome = pickle.load(f)
        
    net = neat.nn.FeedForwardNetwork.create(genome, config)
    
    renderer = Renderer()
    clock = pygame.time.Clock()
    
    print("Watching the best generation continuously. Close the window to stop.")
    
    run_loop = True
    iteration = 1
    
    while run_loop:
        # Loop forever
        game = Game(20, 20)
        
        # We loop until the game dies
        while game.alive:
            running, action = renderer.handle_events()
            if not running:
                run_loop = False
                break
                
            renderer.draw_state([game], [genome], iteration, 1, game.score, game.score, show_all=True, speed_mode="1X")
            
            state = get_state_vector(game)
            output = net.activate(state)
            
            action_vec = [0, 0, 0]
            action_vec[output.index(max(output))] = 1
            
            game.step(action_vec)
            
            clock.tick(15) # Comfortable viewing speed
            
        iteration += 1

    pygame.quit()

if __name__ == "__main__":
    watch_best()
