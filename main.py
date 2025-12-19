import pygame
import math
from sys import exit
import random

#-------------------------------------#-------------------------------------#----------------------------
# bird handler
#-------------------------------------#-------------------------------------#----------------------------
pygame.init()

screen_info = pygame.display.Info()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
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
gravity = 0.4
flap_strength = -5


#-------------------------------------#-------------------------------------#----------------------------
# pipes handler
#-------------------------------------#-------------------------------------#----------------------------

TOP = True
BOTTOM = False

class Pipe(pygame.Rect):
    def __init__(self,pos):
        pygame.Rect.__init__(self, pipe_x, pipe_y, pipe_width, pipe_height)
        self.pos=pos
        self.passed=False

GAME_WIDTH = WIDTH
GAME_HEIGHT= HEIGHT

pipe_x=GAME_WIDTH
pipe_y=0
pipe_width=64
pipe_height=512

top_pipe_image=pygame.image.load("./pipes/toppipe.png")
top_pipe_image=pygame.transform.scale(top_pipe_image,(pipe_width,pipe_height))
bottom_pipe_image=pygame.image.load("./pipes/bottompipe.png")
bottom_pipe_image=pygame.transform.scale(bottom_pipe_image,(pipe_width,pipe_height))

pipes=[]
speed_x=-2

pipes_timer=pygame.USEREVENT +0
pygame.time.set_timer(pipes_timer,1500)

def draw_pipes():
    for pipe in pipes:
        if pipe.pos == TOP:
            screen.blit(top_pipe_image, pipe)
        elif pipe.pos == BOTTOM:
            screen.blit(bottom_pipe_image, pipe)

def move_pipes():
    for pipe in pipes:
        pipe.x +=speed_x

    while  len(pipes) > 0 and pipes[0].x+pipe_width <0:
        pipes.pop(0)

def create_pipes():
    random_pipe_y=pipe_y - pipe_height/4 - random.random()*(pipe_height/2)  
    open_space=GAME_HEIGHT/3
    top_pipe=Pipe(TOP)
    top_pipe.y=random_pipe_y
    pipes.append(top_pipe)
    bottom_pipe=Pipe(BOTTOM)
    bottom_pipe.y=top_pipe.y+top_pipe.height+open_space
    pipes.append(bottom_pipe)



#-------------------------------------#-------------------------------------#----------------------------
# collision handler
#-------------------------------------#-------------------------------------#----------------------------
def check_collisions(bird_rect, pipes, floor_rect_y):
    # 1. Loop through the list of pipes to check for hits
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return True

    # 2. Check if bird hit the floor
    if bird_rect.bottom >= floor_rect_y:
        return True

    # No collision detected
    return False



#-------------------------------------#-------------------------------------#----------------------------
# main loop
#-------------------------------------#-------------------------------------#----------------------------

running = True
while running:
    clock.tick(FPS)
    screen.fill((135, 206, 250))


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type==pipes_timer:
            create_pipes()

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

    bird_rect = pygame.Rect(bird_x + 25, bird_y + 25, BIRD_SIZE - 50, BIRD_SIZE - 50)


    if check_collisions(bird_rect, pipes, HEIGHT):
        print("LOSER")
        running = False


    move_pipes()
    draw_pipes()
    pygame.display.update()

pygame.quit()
