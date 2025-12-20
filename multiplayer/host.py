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
  pass
#waiting for the messages from the client
def udp_listener():
      pass

 

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