import pygame
import math

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bird")

clock = pygame.time.Clock()
FPS = 60
scale = 0.65
bird_x = 150
bird_y = HEIGHT / 2

bird_speed_y = 0
flap_angle = 0
max_down_speed = 12
game_started = False
gravity = 0.3
flap_strength = -7


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
    if bird_y > HEIGHT - 40 * scale:
        bird_y = HEIGHT - 40 * scale
        bird_speed_y = 0

    flap_angle += 0.3
    wing_offset = math.sin(flap_angle) * 20 * scale


    bird_surf = pygame.Surface((120 * scale, 80 * scale), pygame.SRCALPHA)
    cx = 60 * scale
    cy = 40 * scale
    pygame.draw.circle(bird_surf, (255, 230, 0), (int(cx), int(cy)), int(38*scale))

    wing_points = [
        (cx - 20 * scale, cy),
        (cx - 70 * scale, cy - 20 * scale + wing_offset),
        (cx - 70 * scale, cy + 20 * scale + wing_offset)
    ]
    pygame.draw.polygon(bird_surf, (255, 200, 0), wing_points)
    beak_points = [
        (cx + 37 * scale, cy - 7.5 * scale),
        (cx + 37 * scale, cy + 7.5 * scale),
        (cx + 70 * scale, cy)
    ]
    pygame.draw.polygon(bird_surf, (255, 140, 0), beak_points)
    pygame.draw.circle(bird_surf, (0, 0, 0), (int(cx + 15 * scale), int(cy - 10 * scale)), int(6 * scale))
    pygame.draw.circle(bird_surf, (255, 255, 255), (int(cx + 13 * scale), int(cy - 12 * scale)), int(2 * scale))



    angle = -bird_speed_y * 2
    rotated_bird = pygame.transform.rotate(bird_surf, angle)
    bird_rect = rotated_bird.get_rect(center = (bird_x, bird_y))
    screen.blit(rotated_bird, bird_rect.topleft)

    pygame.display.update()

pygame.quit()
