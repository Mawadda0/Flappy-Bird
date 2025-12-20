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

def get_path(filename):
    return os.path.join(BASE_DIR, filename)

root = Tk()
root.title("Flappy Bird Multiplayer Mode")
root.attributes('-fullscreen', True)
root.bind("<Escape>", lambda event: root.destroy())

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# --- MUSIC SETUP ---
pygame.mixer.init()
try:
    pygame.mixer.music.load(get_path("backgroundmp.mp3")) 
    pygame.mixer.music.play(-1) 
    click_sound = pygame.mixer.Sound(get_path("Point.mp3")) 
    click_sound.set_volume(1)
except:
    click_sound = None

canvas = Canvas(root, highlightthickness=0, bg="skyblue")
canvas.pack(fill="both", expand=True)

# --- FONT ---
FONT_PATH = get_path("FSEX300.ttf") 
FONT_NAME = "Fixedsys Excelsior 301"

def load_custom_font(path):
    if os.path.exists(path):
        ctypes.windll.gdi32.AddFontResourceExW(path, 0x10, 0)

load_custom_font(FONT_PATH)

# --- BACKGROUND ---
bg_img = Image.open(get_path("background.png")).resize((screen_width, screen_height), Image.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_img)
canvas.create_image(0, 0, image=bg_photo, anchor="nw")

# --- PIPES (STATIC) ---
pipe_img_raw = Image.open(get_path("pipe.png")).resize((650, 850), Image.LANCZOS)
pipe_top_photo = ImageTk.PhotoImage(pipe_img_raw)
# Bottom pipe is the same image rotated 180 degrees
pipe_bottom_photo = ImageTk.PhotoImage(pipe_img_raw.rotate(180))

# Top-Right Pipe
canvas.create_image(screen_width - 150, -250, image=pipe_top_photo, anchor="n")
# Bottom-Left Pipe
canvas.create_image(150, screen_height + 200, image=pipe_bottom_photo, anchor="s")

#--- BUTTONS SETUP ---
btn_width = 250
btn_height = 70
gap = 10
btn_x = screen_width // 2
btn_find_y = (screen_height // 2.2) - (btn_height // 2) - (gap // 2)
btn_host_y = (screen_height // 2.1) + (btn_height // 2) + (gap // 2)

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

# Find Game Button (State set to 'normal' from start)
create_rounded_rect(canvas, btn_x, btn_find_y, btn_width, btn_height, corner_radius=20,
                    fill="#fcbe2e", outline="#e08021", width=5, state='normal', tags="find_game_btn")
canvas.create_text(btn_x, btn_find_y, text="Find Game", fill="white",
                   font=(FONT_NAME, 20), state='normal', tags="find_game_btn")

# Host Game Button (State set to 'normal' from start)
create_rounded_rect(canvas, btn_x, btn_host_y, btn_width, btn_height, corner_radius=20,
                    fill="#fcbe2e", outline="#e08021", width=5, state='normal', tags="host_game_btn")
canvas.create_text(btn_x, btn_host_y, text="Host Game", fill="white",
                   font=(FONT_NAME, 20), state='normal', tags="host_game_btn")

# --- HOVER LOGIC ---
hover_states = {"find_game_btn": False, "host_game_btn": False}
game_running = True

def check_hover(event):
    if not game_running: return
    buttons = [("find_game_btn", btn_x, btn_find_y), ("host_game_btn", btn_x, btn_host_y)]
    any_hovered = False
    
    for tag, bx, by in buttons:
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

# --- NAVIGATION ---
def launch_game(script_name):
    global game_running
    if click_sound: click_sound.play()
    game_running = False
    root.update()
    pygame.time.delay(300) 
    root.destroy()
    
    script_path = get_path(script_name)
    subprocess.Popen([sys.executable, script_path])

canvas.tag_bind("find_game_btn", "<Button-1>", lambda e: launch_game("find.py"))
canvas.tag_bind("host_game_btn", "<Button-1>", lambda e: launch_game("host.py"))

# --- BIRD ---
bird_raw_img = Image.open(get_path("bird22.png")).resize((180, 180), Image.LANCZOS)
bird_photo = ImageTk.PhotoImage(bird_raw_img)
bird_id = canvas.create_image(screen_width//2, screen_height//2, image=bird_photo)

# Animation
anim_t = 0
def animate():
    global anim_t
    if not game_running: return

    anim_t += 0.03
    
    # Bird movement
    offset_x = math.sin(anim_t * 0.7) * (screen_width * 0.25)
    offset_y = math.cos(anim_t * 0.5) * (screen_height * 0.15)
    
    # Update bird position
    new_x = (screen_width // 2) + offset_x
    new_y = (screen_height // 3) + offset_y
    
    canvas.coords(bird_id, new_x, new_y)
    
    # Keep buttons and bird on top of pipes
    canvas.lift(bird_id)
    canvas.lift("find_game_btn")
    canvas.lift("host_game_btn")
    
    root.after(20, animate)

animate()
root.mainloop()