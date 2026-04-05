import pygame

class Renderer:
    def __init__(self, cell_size=20, grid_width=20, grid_height=20):
        self.cell_size = cell_size
        self.grid_width = grid_width
        self.grid_height = grid_height
        
        # Add 180px on the right for HUD
        self.hud_width = 180
        self.game_width = self.grid_width * self.cell_size
        self.window_width = self.game_width + self.hud_width
        self.window_height = self.grid_height * self.cell_size 
        
        pygame.init()
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption("NEAT AI Snake")
        
        pygame.font.init()
        self.font = pygame.font.SysFont("consolas", 14)
        self.font_large = pygame.font.SysFont("consolas", 18, bold=True)
        
        # Colors
        self.COLOR_BG = (20, 20, 20)
        self.COLOR_HUD_BG = (40, 40, 40)
        self.COLOR_SNAKE = (0, 150, 0, 100)
        self.COLOR_SNAKE_HEAD = (100, 255, 100, 150)
        self.COLOR_SNAKE_BEST = (0, 255, 255, 255) # Cyan for best
        self.COLOR_APPLE = (255, 50, 50)
        self.COLOR_TEXT = (220, 220, 220)

    def draw_state(self, games, ge, gen, alive, highest_fitness, best_all_time, show_all=True, speed_mode="FF"):
        self.screen.fill(self.COLOR_BG)
        
        game_surface = pygame.Surface((self.game_width, self.window_height), pygame.SRCALPHA)
        game_surface.fill(self.COLOR_BG)
        
        # Determine best snake index for "Best Only" view or highlighting
        best_idx = 0
        best_fit = -9999
        for i, g in enumerate(ge):
            if g.fitness > best_fit:
                best_fit = g.fitness
                best_idx = i
                
        # Draw apple - since all snakes share the same sequence, we ONLY draw the best snake's apple
        # This guarantees only one apple is on the screen at a time.
        for i, game in enumerate(games):
            if not game.alive: continue
            if i == best_idx:
                ax, ay = game.apple
                pygame.draw.rect(game_surface, self.COLOR_APPLE, 
                                 pygame.Rect(ax * self.cell_size, ay * self.cell_size, self.cell_size, self.cell_size))
                break # Only draw once
            
        # Draw snakes
        for i, game in enumerate(games):
            if not game.alive: continue
            if not show_all and i != best_idx: continue
            
            is_best = (i == best_idx)
            
            for seg_i, (sx, sy) in enumerate(game.snake):
                if is_best:
                    c = self.COLOR_SNAKE_BEST if seg_i == 0 else (0, 200, 200, 255)
                else:
                    c = self.COLOR_SNAKE_HEAD if seg_i == 0 else self.COLOR_SNAKE
                    
                pygame.draw.rect(game_surface, c, 
                                 pygame.Rect(sx * self.cell_size, sy * self.cell_size, self.cell_size, self.cell_size))
                                 
        self.screen.blit(game_surface, (0, 0))
        
        # Draw HUD Area
        pygame.draw.rect(self.screen, self.COLOR_HUD_BG, pygame.Rect(self.game_width, 0, self.hud_width, self.window_height))
        
        # Render Text
        pad_x = self.game_width + 10
        y_offset = 15
        spacing = 20
        
        def draw_text(text, y, is_large=False):
            f = self.font_large if is_large else self.font
            surf = f.render(text, True, self.COLOR_TEXT)
            self.screen.blit(surf, (pad_x, y))
            return y + spacing
            
        y_offset = draw_text("STATISTICS", y_offset, True)
        y_offset += 5
        y_offset = draw_text(f"Generation: {gen}", y_offset)
        y_offset = draw_text(f"Alive:      {alive}", y_offset)
        y_offset = draw_text(f"Highest Fit:{highest_fitness:.1f}", y_offset)
        y_offset = draw_text(f"Best AllTime:{best_all_time:.1f}", y_offset)
        
        y_offset += 20
        y_offset = draw_text("CONTROLS", y_offset, True)
        y_offset += 5
        
        v_mode_str = "ALL" if show_all else "BEST"
        y_offset = draw_text(f"[1] View: {v_mode_str}", y_offset)
        
        s_1x = "<" if speed_mode == "1X" else " "
        s_ff = "<" if speed_mode == "FF" else " "
        s_lt = "<" if speed_mode == "LIGHTNING" else " "
        
        y_offset = draw_text(f"[2] 1X Speed  {s_1x}", y_offset)
        y_offset = draw_text(f"[3] Fast Fwd  {s_ff}", y_offset)
        y_offset = draw_text(f"[4] Lightning {s_lt}", y_offset)
        
        pygame.display.flip()

    def handle_events(self):
        """ Returns (is_running, action_string) """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False, None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return True, "TOGGLE_VIEW"
                elif event.key == pygame.K_2:
                    return True, "SPEED_1X"
                elif event.key == pygame.K_3:
                    return True, "SPEED_FF"
                elif event.key == pygame.K_4:
                    return True, "SPEED_LIGHTNING"
        return True, None
