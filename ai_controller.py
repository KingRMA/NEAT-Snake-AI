import numpy as np

def get_state_vector(game):
    # State Vector: 12 Inputs
    # 1. Danger Straight
    # 2. Danger Right
    # 3. Danger Left
    # 4. Food Above
    # 5. Food Below
    # 6. Food Left
    # 7. Food Right
    # 8. Moving Up
    # 9. Moving Down
    # 10. Moving Left
    # 11. Moving Right
    # 12. Snake Length
    
    head_x, head_y = game.snake[0]
    dx, dy = game.heading
    
    # Calculate points around head
    point_straight = (head_x + dx, head_y + dy)
    # Turn right: (dx, dy) -> (-dy, dx)
    point_right = (head_x - dy, head_y + dx)
    # Turn left: (dx, dy) -> (dy, -dx)
    point_left = (head_x + dy, head_y - dx)
    
    def is_collision(pt):
        # Wrap point to simulate the game logic
        pt_wrapped = (pt[0] % game.width, pt[1] % game.height)
        if pt_wrapped in game.snake:
            return True
        return False
        
    danger_straight = 1 if is_collision(point_straight) else 0
    danger_right = 1 if is_collision(point_right) else 0
    danger_left = 1 if is_collision(point_left) else 0
    
    food_above = 1 if game.apple[1] < head_y else 0
    food_below = 1 if game.apple[1] > head_y else 0
    food_left = 1 if game.apple[0] < head_x else 0
    food_right = 1 if game.apple[0] > head_x else 0
    
    moving_up = 1 if game.heading == (0, -1) else 0
    moving_down = 1 if game.heading == (0, 1) else 0
    moving_left = 1 if game.heading == (-1, 0) else 0
    moving_right = 1 if game.heading == (1, 0) else 0
    
    snake_len = len(game.snake)
    
    return [
        danger_straight, danger_right, danger_left,
        food_above, food_below, food_left, food_right,
        moving_up, moving_down, moving_left, moving_right,
        snake_len
    ]
