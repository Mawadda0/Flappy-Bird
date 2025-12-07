import pygame
import math

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bird")

clock = pygame.time.Clock()
FPS = 60

BIRD_SIZE = 80
bird_image = pygame.image.load("bird2.png").convert_alpha()
bird_image = pygame.transform.scale(bird_image, (BIRD_SIZE, BIRD_SIZE))

bird_x = 150
bird_y = HEIGHT / 2
bird_speed_y = 0

gravity = 0.5
flap_strength = -10
max_down_speed = 12

running = True
while running:
    clock.tick(FPS)
    screen.fill((135, 206, 250))


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        bird_speed_y = flap_strength


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
