import pygame
import random
import socket
import threading
import time

#seed and ports configs
BROADCAST_PORT = 50000
GAME_PORT = 50001
BROADCAST_MSG = b"FLAPPY_HOST"
START_MSG = b"START"
clients = set()
seed = random.randint(0, 999999)
#the host init for broadcasting message
def broadcast_host():

#waiting for the messages from the client
def udp_listener():
   