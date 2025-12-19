import math
import sys
import subprocess
import os
from tkinter import *
from PIL import Image, ImageTk
import pygame 
import ctypes

# This finds the folder where this script is saved
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

#Get each file path
def get_path(filename):
    return os.path.join(BASE_DIR, filename)

root = Tk()
root.title("Flappy Bird Intro")
root.attributes('-fullscreen', True)
root.bind("<Escape>", lambda event: root.destroy())

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# --- MUSIC SETUP ---
pygame.mixer.init()
# Use dynamic paths for audio
pygame.mixer.music.load(get_path("backgroundmp.mp3")) 
pygame.mixer.music.play(-1) 
click_sound = pygame.mixer.Sound(get_path("Point.mp3")) 
click_sound.set_volume(1)

canvas = Canvas(root, highlightthickness=0, bg="skyblue")
canvas.pack(fill="both", expand=True)

# --- 1. CUSTOM FONT LOADER ---
FONT_PATH = get_path("FSEX300.ttf") 
FONT_NAME = "Fixedsys Excelsior 301"

def load_custom_font(path):
    if os.path.exists(path):
        ctypes.windll.gdi32.AddFontResourceExW(path, 0x10, 0)
    else:
        print(f"Font not found at: {path}")

load_custom_font(FONT_PATH)

# --- BACKGROUND ---
bg_img = Image.open(get_path("background.png")).resize((screen_width, screen_height), Image.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_img)
canvas.create_image(0, 0, image=bg_photo, anchor="nw")

# --- TITLE IMAGES ---
flappy_img = Image.open(get_path("flappyword.png")).resize((350, 100), Image.NEAREST)
flappy_photo = ImageTk.PhotoImage(flappy_img)
id_flappy = canvas.create_image((screen_width//1.9) - 10, screen_height//2.2 - 50, image=flappy_photo, anchor="e", state='hidden')

bird_word_img = Image.open(get_path("birdword.png")).resize((250, 100), Image.NEAREST)
bird_word_photo = ImageTk.PhotoImage(bird_word_img)
id_bird_word = canvas.create_image((screen_width//1.9) + 10, screen_height//2.2 - 50, image=bird_word_photo, anchor="w", state='hidden')

#--- Buttons ---
btn_width = 220
btn_height = 60
btn_y = screen_height // 2.3 + 100
gap = 40

btn_start_x = (screen_width // 2) - (btn_width // 2) - (gap // 2)
btn_multi_x = (screen_width // 2) + (btn_width // 2) + (gap // 2)

def create_rounded_rect(canvas, x, y, w, h, corner_radius, **kwargs):
    x1, y1 = x - w//2, y - h//2
    x2, y2 = x + w//2, y + h//2
    points = (
        x1+corner_radius, y1, x1+corner_radius, y1, x2-corner_radius, y1, x2-corner_radius, y1, x2, y1,
        x2, y1+corner_radius, x2, y1+corner_radius, x2, y2-corner_radius, x2, y2-corner_radius, x2, y2,
        x2-corner_radius, y2, x2-corner_radius, y2, x1+corner_radius, y2, x1+corner_radius, y2, x1, y2,
        x1, y2-corner_radius, x1, y2-corner_radius, x1, y1+corner_radius, x1, y1+corner_radius, x1, y1
    )
    return canvas.create_polygon(points, smooth=True, **kwargs)

btn_bg = create_rounded_rect(canvas, btn_start_x, btn_y, btn_width, btn_height, corner_radius=20,
                             fill="#fcbe2e", outline="#e08021", width=5, state='hidden', tags="start_btn")
btn_text = canvas.create_text(btn_start_x, btn_y, text="START GAME", fill="white",
                              font=(FONT_NAME, 18), state='hidden', tags="start_btn")

btn_multi_bg = create_rounded_rect(canvas, btn_multi_x, btn_y, btn_width, btn_height, corner_radius=20,
                             fill="#fcbe2e", outline="#e08021", width=5, state='hidden', tags="multi")
btn_multi_text = canvas.create_text(btn_multi_x, btn_y, text="MULTIPLAYER", fill="white",
                              font=(FONT_NAME, 18), state='hidden', tags="multi")

# --- HOVER LOGIC ---
hover_states = {"start_btn": False, "multi": False}
game_running = True

def check_hover(event):
    if not game_running: return
    buttons = [("start_btn", btn_start_x, btn_y), ("multi", btn_multi_x, btn_y)]
    any_hovered = False
    for tag, bx, by in buttons:
        if canvas.itemcget(tag, "state") != 'normal': continue
        l, r = bx - btn_width // 2, bx + btn_width // 2
        t, b = by - btn_height // 2, by + btn_height // 2
        if l <= event.x <= r and t <= event.y <= b:
            canvas.config(cursor="hand2")
            any_hovered = True
            if not hover_states[tag]:
                hover_states[tag] = True
                canvas.move(tag, 0, -5)
        else:
            if hover_states[tag]:
                hover_states[tag] = False
                canvas.move(tag, 0, 5)
    if not any_hovered: canvas.config(cursor="")

canvas.bind('<Motion>', check_hover)

# --- NAVIGATION LOGIC ---
def launch_game(script_name):
    global game_running
    if click_sound: click_sound.play()
    game_running = False
    root.update()
    pygame.time.delay(300) 
    root.destroy()
    
    script_path = get_path(script_name)
    subprocess.Popen([sys.executable, script_path])

canvas.tag_bind("start_btn", "<Button-1>", lambda e: launch_game("start.py"))  #We will add the actual file here
canvas.tag_bind("multi", "<Button-1>", lambda e: launch_game("multiplayer.py"))#We will add the actual file here

# --- PIPE & BIRD ---
pipe_img = Image.open(get_path("pipe.png")).resize((650, 850), Image.LANCZOS)
pipe_photo = ImageTk.PhotoImage(pipe_img)
pipe_x = screen_width - 180
pipe_target_y, pipe_current_y = -200, -600
pipe_id = canvas.create_image(pipe_x, pipe_current_y, image=pipe_photo, anchor="n")

bird_raw_img = Image.open(get_path("bird22.png")).resize((200, 200), Image.LANCZOS)
bird_photo = ImageTk.PhotoImage(bird_raw_img)
x, base_y = 0, screen_height // 4
bird_id = canvas.create_image(x, base_y, image=bird_photo)

sway_position = 0
is_retreating = False
bird_stopped = False
pipe_descending = False

# --- THE ANIMATION LOOP ---
def move():
    global x, sway_position, is_retreating, bird_stopped, pipe_current_y, pipe_descending
    if not game_running: return

    sway_position += 0.08
    current_y = base_y + math.sin(sway_position) * 50

    if x > (pipe_x - 500): pipe_descending = True
    if pipe_descending and pipe_current_y < pipe_target_y:
        pipe_current_y += 15
        canvas.coords(pipe_id, pipe_x, pipe_current_y)

    if bird_stopped:
        canvas.itemconfig(id_flappy, state='normal')
        canvas.itemconfig(id_bird_word, state='normal')
        canvas.itemconfig("start_btn", state='normal')
        canvas.itemconfig("multi", state='normal') 
        canvas.lift("start_btn")
        canvas.lift("multi") 
        canvas.lift(bird_id)
    elif is_retreating:
        x -= 10
        if x <= screen_width // 3.5:
            x = screen_width // 3.5
            is_retreating = False
            bird_stopped = True
    else:
        x += 6
        if x > (pipe_x - 110): is_retreating = True

    canvas.coords(bird_id, x, current_y)
    root.after(20, move)

move()
root.mainloop()