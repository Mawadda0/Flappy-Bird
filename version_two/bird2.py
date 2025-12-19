import pygame
import math

pygame.init()

screen_info = pygame.display.Info()
WIDTH, HEIGHT = screen_info.current_w, screen_info.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Bird")

clock = pygame.time.Clock()
FPS = 60

BIRD_SIZE = 80
bird_image = pygame.image.load("./version_two/bird2.png").convert_alpha()
bird_image = pygame.transform.scale(bird_image, (BIRD_SIZE, BIRD_SIZE))

bird_x = WIDTH / 3
bird_y = HEIGHT / 2
bird_speed_y = 0
max_down_speed = 100
game_started = False
gravity = 0.6
flap_strength = -10

running = True
while running:
    clock.tick(FPS)
    screen.fill((135, 206, 250))


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        if not game_started:
            game_started = True
        bird_speed_y = flap_strength
    if game_started:
        bird_speed_y += gravity


    if bird_speed_y > max_down_speed:
        bird_speed_y = max_down_speed

    bird_y += bird_speed_y


    if bird_y < 0:
        bird_y = 0
        bird_speed_y = 0
    if bird_y > HEIGHT - BIRD_SIZE:
        bird_y = HEIGHT - BIRD_SIZE
        bird_speed_y = 0


    angle = -bird_speed_y * 2
    rotated_bird = pygame.transform.rotate(bird_image, angle)
    bird_rect = rotated_bird.get_rect(center = (bird_x + BIRD_SIZE / 2, bird_y + BIRD_SIZE / 2))
    
    screen.blit(rotated_bird, bird_rect.topleft)

    pygame.display.update()

pygame.quit()
