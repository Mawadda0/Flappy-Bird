import pygame
import random
import socket
import threading
import pickle

#ports init
BROADCAST_PORT = 50000
GAME_PORT = 50001

server_ip = None
seed = None

#search for host message that is broadcasted
def find_host():
    pass

#waiting for the starting message from host
def wait_for_start():
    pass

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
