import neat
import os
import pygame
import math
import sys
import pickle
from game import Game
from ai_controller import get_state_vector
from renderer import Renderer

# Globals to track statistics across generations
GEN = 0
BEST_FITNESS_ALL_TIME = -100000.0
HISTORY_WINS = []
BEST_GENOME_ALL_TIME = None

# User Toggles
SHOW_ALL = True
SPEED_MODE = "FF" # "1X", "FF", "LIGHTNING"
RENDERER = None

def eval_genomes(genomes, config):
    global GEN, BEST_FITNESS_ALL_TIME, SHOW_ALL, SPEED_MODE, RENDERER, HISTORY_WINS, BEST_GENOME_ALL_TIME
    GEN += 1
    
    nets = []
    games = []
    ge = []
    
    if RENDERER is None:
        RENDERER = Renderer()
        
    clock = pygame.time.Clock()
    
    max_fitness = []
    frames_no_improve = []
    was_within_5 = []
    within_5_timer = []
    
    for genome_id, genome in genomes:
        genome.fitness = 0.0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        games.append(Game(20, 20, seed=GEN))
        ge.append(genome)
        max_fitness.append(0.0)
        frames_no_improve.append(0)
        was_within_5.append(False)
        within_5_timer.append(0)

    initial_games_count = len(games)
    wins_this_gen = 0
    min_win_time = float('inf')

    run = True
    while run and len(games) > 0:
        # Event Handling
        running, action = RENDERER.handle_events()
        if not running:
            # Safely capture the absolute best genome before forcefully crashing the Pygame instance!
            import copy
            for g in ge:
                if g.fitness > BEST_FITNESS_ALL_TIME:
                    BEST_FITNESS_ALL_TIME = g.fitness
                    BEST_GENOME_ALL_TIME = copy.deepcopy(g)
            if BEST_GENOME_ALL_TIME is not None:
                with open('best_snake.pkl', 'wb') as f:
                    pickle.dump(BEST_GENOME_ALL_TIME, f)
            pygame.quit()
            sys.exit(0)
            
        if action == "TOGGLE_VIEW":
            SHOW_ALL = not SHOW_ALL
        elif action == "SPEED_1X":
            SPEED_MODE = "1X"
        elif action == "SPEED_FF":
            SPEED_MODE = "FF"
        elif action == "SPEED_LIGHTNING":
            SPEED_MODE = "LIGHTNING"
            
        best_fitness_gen = max([g.fitness for g in ge]) if ge else 0.0
        
        # Rendering
        if SPEED_MODE != "LIGHTNING":
            RENDERER.draw_state(games, ge, GEN, len(games), best_fitness_gen, max(BEST_FITNESS_ALL_TIME, best_fitness_gen), SHOW_ALL, SPEED_MODE)
        elif len(games) == 50 or len(games) == 0: 
            # In lightning mode, perhaps just pump events to keep OS happy occasionally
            pygame.event.pump()
            
        # Step all games
        for i, game in enumerate(games):
            if not game.alive:
                continue
                
            state = get_state_vector(game)
            output = nets[i].activate(state)
            
            action_vec = [0, 0, 0]
            action_vec[output.index(max(output))] = 1
            
            # Correct Wrap-Around (Toroidal) Distance Function
            def t_dist(hx, hy, ax, ay, w, h):
                dx = min(abs(hx - ax), w - abs(hx - ax))
                dy = min(abs(hy - ay), h - abs(hy - ay))
                return math.hypot(dx, dy)

            def t_manhattan(hx, hy, ax, ay, w, h):
                dx = min(abs(hx - ax), w - abs(hx - ax))
                dy = min(abs(hy - ay), h - abs(hy - ay))
                return dx + dy
                
            m_dist = t_manhattan(game.snake[0][0], game.snake[0][1], game.apple[0], game.apple[1], game.width, game.height)
            if m_dist <= 5 and not was_within_5[i]:
                was_within_5[i] = True
                within_5_timer[i] = 5

            dist_before = t_dist(game.snake[0][0], game.snake[0][1], game.apple[0], game.apple[1], game.width, game.height)
            
            score_before = game.score
            game.step(action_vec)
            score_after = game.score
            
            if game.alive:
                dist_after = t_dist(game.snake[0][0], game.snake[0][1], game.apple[0], game.apple[1], game.width, game.height)
                # Apply distance reinforcement based on toroidal distance (shortest path including wraps)
                if dist_after < dist_before:
                    ge[i].fitness += 0.1 # Reward for heading towards apple
                elif dist_after > dist_before:
                    ge[i].fitness -= 1.0 # Penalty for going further from apple
            
            if score_after > score_before:
                ge[i].fitness += 30.0
                was_within_5[i] = False # Successfully got it, reset timer
            else:
                if was_within_5[i]:
                    within_5_timer[i] -= 1
                    if within_5_timer[i] <= 0:
                        ge[i].fitness -= 5.0
                        within_5_timer[i] = 5 # Restart the doom countdown repeatedly until eaten!
                
            if not game.alive:
                ge[i].fitness -= 10.0
            elif game.score >= (game.width * game.height) - 1:
                # WIN CONDITION! Filled the screen.
                game.alive = False
                wins_this_gen += 1
                min_win_time = min(min_win_time, game.frame_count)
                ge[i].fitness += 100.0
            elif ge[i].fitness < -50:
                # DESPAIR DEATH: Kills infinitely looping runaways to prevent locking the entire process
                game.alive = False
                
            # Stagnation Rule: Penalty if 5 frames pass WITHOUT INCREASING FITNESS
            if game.alive:
                if ge[i].fitness > max_fitness[i]:
                    max_fitness[i] = ge[i].fitness
                    frames_no_improve[i] = 0
                else:
                    frames_no_improve[i] += 1
                    if frames_no_improve[i] > 0 and frames_no_improve[i] % 5 == 0:
                        ge[i].fitness -= 0.1
                
        # Remove dead games
        i = 0
        import copy
        while i < len(games):
            if not games[i].alive:
                # Dynamically deepcopy the highest recorded fitness organically so it is immune to elitism resets
                if ge[i].fitness > BEST_FITNESS_ALL_TIME:
                    BEST_FITNESS_ALL_TIME = ge[i].fitness
                    BEST_GENOME_ALL_TIME = copy.deepcopy(ge[i])
                    with open('best_snake.pkl', 'wb') as f:
                        pickle.dump(BEST_GENOME_ALL_TIME, f)
                        
                games.pop(i)
                nets.pop(i)
                ge.pop(i)
                max_fitness.pop(i)
                frames_no_improve.pop(i)
                was_within_5.pop(i)
                within_5_timer.pop(i)
            else:
                i += 1
                
        # Speed Limiter
        if SPEED_MODE == "1X":
            clock.tick(15)
        elif SPEED_MODE == "FF":
            clock.tick() # Uncapped but yielding
        # LIGHTNING doesn't block at all
        
    BEST_FITNESS_ALL_TIME = max(BEST_FITNESS_ALL_TIME, best_fitness_gen)
    
    # Track history of successful generations
    if wins_this_gen > 0:
        HISTORY_WINS.append(min_win_time)
    else:
        HISTORY_WINS = [] # Reset streak if a generation failed to win entirely
        
    print(f"Gen {GEN}: Wins = {wins_this_gen}, Current Win Streak = {len(HISTORY_WINS)}")

    # Check the strict 50-generation stopping condition
    if len(HISTORY_WINS) >= 50:
        last_50 = HISTORY_WINS[-50:]
        # If the minimum time (fastest win) in the last 50 hasn't improved since the oldest entry of those 50
        if min(last_50) >= last_50[0]:
            print(f"\n*** TRUE WIN CONDITION MET ***")
            print(f"The last 50 generations consecutively achieved a win, and the time to win is no longer improving (plateaued at ~{min(last_50)} frames)!")
            
            # Ensure the definitive all-time best is saved
            if BEST_GENOME_ALL_TIME is not None:
                with open('best_snake.pkl', 'wb') as f:
                    pickle.dump(BEST_GENOME_ALL_TIME, f)
                
            pygame.quit()
            sys.exit(0)
    
def run_neat():
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path
    )
    
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    
    print("Starting Main Event Loop with Pygame HUD.")
    print("Controls: 1=View Mode, 2=1X Speed, 3=FF Speed, 4=Lightning Speed")
    try:
        # Pass None so that training runs infinitely until the True Win criteria is dynamically met
        winner = p.run(eval_genomes, None)
    except SystemExit:
        # User manually closed pygame window, clean exit caught
        pass
    
    if BEST_GENOME_ALL_TIME is not None:
        print("\nTraining completed or interrupted. All-time highest fitness:", BEST_GENOME_ALL_TIME.fitness)
        print("The best genome was securely auto-saved to best_snake.pkl.")

if __name__ == "__main__":
    run_neat()
