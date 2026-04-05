import random

class Game:
    def __init__(self, width=20, height=20, seed=None):
        self.width = width
        self.height = height
        self.seed = seed
        self.reset()
        
    def reset(self):
        self.snake = [(self.width // 2, self.height // 2)]
        self.heading = (1, 0) # (dx, dy)
        self.score = 0
        self.alive = True
        self.frame_count = 0
        self.frames_since_last_apple = 0
        self._spawn_apple()
        
    def _spawn_apple(self):
        if self.seed is not None:
            # Seed the RNG based on the generation seed + the snake's current score
            # This ensures all snakes in the generation chase the exact same sequence of apples!
            random.seed(self.seed + self.score)
            
        while True:
            self.apple = (random.randint(0, self.width - 1), random.randint(0, self.height - 1))
            if self.apple not in self.snake:
                break
        
        if self.seed is not None:
            # Reset the global seed so we don't mess up other random processes like NEAT mutations
            random.seed()

    def step(self, action):
        """
        action: list or tuple of 3 values [straight, right, left]
        if None, continues in current heading
        """
        if not self.alive:
            return False
            
        self.frame_count += 1
        self.frames_since_last_apple += 1
        
        # Determine new heading
        dx, dy = self.heading
        if action is not None:
            # Action format is [straight, right, left] (argmax)
            idx = action.index(max(action))
            if idx == 1: # Turn right relative to current heading
                # up (0, -1) -> right (1, 0) -> down (0, 1) -> left (-1, 0)
                # math for 90 deg right turn: (x, y) -> (-y, x)
                dx, dy = -dy, dx
            elif idx == 2: # Turn left relative to current heading
                # math for 90 deg left turn: (x, y) -> (y, -x)
                dx, dy = dy, -dx
        
        self.heading = (dx, dy)
        
        # Calculate new head position with WRAP-AROUND mechanics
        head_x, head_y = self.snake[0]
        new_head = ((head_x + dx) % self.width, (head_y + dy) % self.height)
            
        # Check collisions (tail)
        if new_head in self.snake:
            self.alive = False
            return False
            
        # Move snake
        self.snake.insert(0, new_head)
        
        # Check apple
        if new_head == self.apple:
            self.score += 1
            self.frames_since_last_apple = 0
            self._spawn_apple()
        else:
            self.snake.pop()
            
        # Time limit completely removed as requested
        # (Though we might still need a safety kill in the trainer if fitness crashes)
            
        return True
