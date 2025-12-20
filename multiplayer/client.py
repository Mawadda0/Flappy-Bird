import pygame
import random
import socket
import threading

#ports init
BROADCAST_PORT = 50000
GAME_PORT = 50001

server_ip = None
seed = None

#search for host message that is broadcasted
def find_host():
    global server_ip, seed
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(("", BROADCAST_PORT))
    while True:
        data, addr = s.recvfrom(1024)
        if data == b"FLAPPY_HOST":
            server_ip = addr[0]
            join = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            join.sendto(b"JOIN", (server_ip, GAME_PORT))
            break

#waiting for the starting message from host
def wait_for_start():
    global seed
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(("", GAME_PORT))
    data, _ = s.recvfrom(1024)
    msg = data.decode()
    if msg.startswith("START"):
        seed = int(msg.split(":")[1])


def jump(sock):
    bird.speed_y = jump_strength
    sock.sendto(b"FLAP", (server_ip, GAME_PORT))

def update():
    bird.speed_y += gravity
    bird.speed_y = min(bird.speed_y, max_down_speed)
    bird.y += bird.speed_y
    screen.blit(bird_image, (bird.x, bird.y))

threading.Thread(target=find_host, daemon=True).start()
while server_ip is None:
    pass

wait_for_start()
random.seed(seed)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
running = True
while running:
    clock.tick(FPS)
    screen.fill((135, 206, 250))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            jump(sock)

    update()
    pygame.display.flip()

pygame.quit()
