import pygame

def check_collisions(bird_rect, pipes, floor_rect_y):
    """
    Checks collisions for bird against pipes, floor, and ceiling.
    """
    
    # 1. Loop through the list of pipes to check for hits
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return True

    # 2. Check if bird hit the floor
    if bird_rect.bottom >= floor_rect_y:
        return True
        
    # 3. Check if bird flew too high (ceiling)
    if bird_rect.top <= 0:
        return True

    # No collision detected
    return False