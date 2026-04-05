from game import Game

def verify_game_logic():
    print("Testing Game Initialization...")
    g = Game(10, 10)
    assert len(g.snake) == 1
    assert g.alive == True
    assert g.score == 0
    assert 0 <= g.apple[0] < 10 and 0 <= g.apple[1] < 10
    
    print("Testing Movement (Straight)...")
    head_start = g.snake[0]
    g.step([1, 0, 0]) # straight
    head_next = g.snake[0]
    # heading starts as (1, 0) so x should increase by 1
    assert head_next[0] == head_start[0] + 1
    assert head_next[1] == head_start[1]
    
    print("Testing Wall Collision...")
    # Move until wall (grid is 10x10, so max 9 steps from middle)
    for _ in range(15):
        if not g.alive:
            break
        g.step([1, 0, 0])
    assert g.alive == False
    
    print("All tests passed! Phase 1 Logic Verification Successful.")

if __name__ == "__main__":
    verify_game_logic()
