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

#waiting for the starting message from host
def wait_for_start():