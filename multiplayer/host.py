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