import pygame

pygame.init()

score = 0

try:
    score_font = pygame.font.Font(None, 60)
except pygame.error as e:
    print(f"Font loading error: {e}")
    score_font = pygame.font.Font(None, 60)

def check(bird , pipes,score):
    for pipe in pipes:
        if bird.rect.left > pipe.x and not pipe.scored:
            score += 1
            pipe.scored = True
            print(score)
    return score        
def display(screen, score, width):        
    score_surface = score_font.render(str(int(score)), True, (255, 255, 255))
    score_rect = score_surface.get_rect(center=(width // 2, 50))
    screen.blit(score_surface, score_rect)
def reset():
    return 0

