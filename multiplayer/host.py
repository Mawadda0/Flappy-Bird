import pygame
import random
import socket
import threading
import time
import pickle

#seed and ports configs
BROADCAST_PORT = 50000
GAME_PORT = 50001
BROADCAST_MSG = b"FLAPPY_HOST"
START_MSG = b"START"
clients = set()
seed = random.randint(0, 999999)
#the host init for broadcasting message
def broadcast_host():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    while True:
        s.sendto(BROADCAST_MSG, ("255.255.255.255", BROADCAST_PORT))
        time.sleep(1)
#waiting for the messages from the client
def udp_listener():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(("", GAME_PORT))
    while True:
        data, addr = s.recvfrom(1024)
        if data == b"FLAP":
            print("FLAP from", addr)
        elif data == b"JOIN":
            clients.add(addr)
            s.sendto(f"{START_MSG.decode()}:{seed}".encode(), addr)

def send_map_coordinates(client_socket):
    # Constants from main.py used for generation
    pipe_y = 0
    pipe_height = 512
    coordinates = []
    
    # Generate 100 pipes (enough for a long game)
    for _ in range(100):
        # The exact math from main.py:
        random_pipe_y = pipe_y - pipe_height/4 - random.random()*(pipe_height/2)
        coordinates.append(random_pipe_y)
    
    # Serialize the list and send it
    data = pickle.dumps(coordinates)
    client_socket.send(data)



#-------------------------------------#-------------------------------------#----------------------------
# 1. SETUP & CONFIG
#-------------------------------------#-------------------------------------#----------------------------
pygame.init()

screen_info = pygame.display.Info()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bird")

clock = pygame.time.Clock()
FPS = 60

#-------------------------------------#-------------------------------------#----------------------------
# bird handler
#-------------------------------------#-------------------------------------#----------------------------
BIRD_SIZE = 80
try:
    bird_image = pygame.image.load("./version_two/blue.png").convert_alpha()
    bird_image = pygame.transform.scale(bird_image, (BIRD_SIZE, BIRD_SIZE))
except:
    bird_image = pygame.Surface((BIRD_SIZE, BIRD_SIZE))
    bird_image.fill((255, 255, 0))

max_down_speed = 100
gravity = 0.4
jump_strength = -5

class Bird():
    def __init__(self):
        self.x = WIDTH / 3
        self.y = HEIGHT / 2
        self.speed_y = 0

bird = Bird()

def jump_bird(bird):
    bird.speed_y = jump_strength

def update_bird(bird):
    bird.speed_y += gravity
    if bird.speed_y > max_down_speed:
        bird.speed_y = max_down_speed
    
    bird.y += bird.speed_y

    if bird.y < 0:
        bird.y = 0            
        bird.speed_y = 0      

    angle = -bird.speed_y * 2
    rotated_bird = pygame.transform.rotate(bird_image, angle)
    bird_rect = rotated_bird.get_rect(center = (bird.x + BIRD_SIZE / 2, bird.y + BIRD_SIZE / 2))
    screen.blit(rotated_bird, bird_rect.topleft)

def get_bird_hitbox(bird):
    return pygame.Rect(bird.x + 25, bird.y + 25, BIRD_SIZE - 50, BIRD_SIZE - 50)

#-------------------------------------#-------------------------------------#----------------------------
