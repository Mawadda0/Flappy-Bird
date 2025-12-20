import pygame
import socket
import json
import random
import pickle
import time

# -------------------- NETWORK --------------------
BROADCAST_PORT = 50000
GAME_PORT = 50001

server_addr = None
seed = None
game_started = False
start_time = 0

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("", BROADCAST_PORT))
sock.setblocking(False)

#search for host message that is broadcasted
def find_host():
    global server_addr
    try:
        data, addr = sock.recvfrom(1024)
        msg = json.loads(data.decode())
        if msg["type"] == "DISCOVER":
            server_addr = (addr[0], msg["port"])
            print("[CLIENT] Server found:", server_addr)
    except:
        pass

#waiting for the starting message from host
def wait_for_start():
    global seed, game_started, start_time
    try:
        data, _ = sock.recvfrom(1024)
        msg = json.loads(data.decode())

        if msg["type"] == "START":
            seed = msg["seed"]
            start_time = msg["start_time"]
            random.seed(seed)
            game_started = True
            print("[CLIENT] Game starting with seed:", seed)
    except:
        pass
def send(msg):
    if server_addr:
        sock.sendto(json.dumps(msg).encode(), server_addr)

def generate_client_pipes(client_socket, pipes_list, Pipe_Class, GAME_HEIGHT):
    # Receive the data (buffer size large enough for the list)
    data = client_socket.recv(4096 * 8)
    coordinates = pickle.loads(data)
    
    # Constants for spacing (Calculated from main.py: 1500ms timer * 60fps * 2 speed = 180px)
    start_x = 800
    spacing = 180 
    TOP = True
    BOTTOM = False
    
    for i, y in enumerate(coordinates):
        current_x = start_x + (i * spacing)
        open_space = GAME_HEIGHT / 3
        
        # Create Top Pipe using the received Y
        top_pipe = Pipe_Class(TOP)
        top_pipe.y = y
        top_pipe.x = current_x  # Position it correctly in the timeline
        pipes_list.append(top_pipe)
        
        # Create Bottom Pipe based on Top Pipe
        bottom_pipe = Pipe_Class(BOTTOM)
        bottom_pipe.y = top_pipe.y + top_pipe.height + open_space
        bottom_pipe.x = current_x
        pipes_list.append(bottom_pipe)
