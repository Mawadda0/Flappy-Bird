import pygame
from sys import exit
import random

GAME_WIDTH = 360
GAME_HEIGHT= 640

#pipe class
pipe_x=GAME_WIDTH
pipe_y=0
pipe_width=64
pipe_height=512

class Pipe(pygame.Rect):
    def __init__(self,img):
        pygame.Rect.__init__(self,pipe_x,pipe_y,pipe_width,pipe_height)
        self.img=img
        self.passed=False # انا سايبها عشان ال هيربط كلو ببعض انجويييي


top_pipe_image=pygame.image.load("toppipe.png")
top_pipe_image=pygame.transform.scale(top_pipe_image,(pipe_width,pipe_height))
bottom_pipe_image=pygame.image.load("bottompipe.png")
bottom_pipe_image=pygame.transform.scale(bottom_pipe_image,(pipe_width,pipe_height))

#logic pipesssssss

pipes=[]
speed_x=-2

def draw():
    for pipe in pipes:
        window.blit(pipe.img,pipe)

def move():
    for pipe in pipes:
        pipe.x +=speed_x

    while  len(pipes)  >0 and pipes[0].x+pipe_width <0:
        pipes.pop(0)

def create_pipes():
    random_pipe_y=pipe_y - pipe_height/4 - random.random()*(pipe_height/2)  
    open_space=GAME_HEIGHT/4
    top_pipe=Pipe(top_pipe_image)
    top_pipe.y=random_pipe_y
    pipes.append(top_pipe)
    bottom_pipe=Pipe(bottom_pipe_image)
    bottom_pipe.y=top_pipe.y+top_pipe.height+open_space
    pipes.append(bottom_pipe)

    #print(len(pipes))
    



pygame.init()
window =pygame.display.set_mode((GAME_WIDTH,GAME_HEIGHT))
pygame.display.set_caption("Flappy Bird")
clock=pygame.time.Clock()
pipes_timer=pygame.USEREVENT +0
pygame.time.set_timer(pipes_timer,1500)

while True: #game loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type==pipes_timer:
            create_pipes()
    move()
    draw()
    pygame.display.update()
    clock.tick(60) 