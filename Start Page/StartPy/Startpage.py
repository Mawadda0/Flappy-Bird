import math
import sys
import subprocess
import os
from tkinter import *
from PIL import Image, ImageTk
import pygame  # IMPORT PYGAME HERE

root = Tk()
root.title("Flappy Bird Intro")

# 1. Full Screen Setup
root.attributes('-fullscreen', True)
root.bind("<Escape>", lambda event: root.destroy())

# --- SCREEN SETUP ---
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# --- MUSIC SETUP ---
pygame.mixer.init()
pygame.mixer.music.load("backgroundmp.mp3") 
pygame.mixer.music.play(-1) 

click_sound = pygame.mixer.Sound("Point.mp3") 
click_sound.set_volume(0.5)


canvas = Canvas(root, highlightthickness=0, bg="skyblue")
canvas.pack(fill="both", expand=True)

# --- BACKGROUND ---
bg_img = Image.open("background.png").resize((screen_width, screen_height), Image.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_img)
canvas.create_image(0, 0, image=bg_photo, anchor="nw")


# --- TITLE IMAGES ---
flappy_img = Image.open("flappyword.png").resize((350, 100), Image.NEAREST)
flappy_photo = ImageTk.PhotoImage(flappy_img)
id_flappy = canvas.create_image((screen_width//1.9) - 10, screen_height//2.2 - 50, image=flappy_photo, anchor="e", state='hidden')
bird_word_img = Image.open("birdword.png").resize((250, 100), Image.NEAREST)
bird_word_photo = ImageTk.PhotoImage(bird_word_img)
id_bird_word = canvas.create_image((screen_width//1.9) + 10, screen_height//2.2 - 50, image=bird_word_photo, anchor="w", state='hidden')

# --- BUTTON ---
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

btn_x = screen_width // 2
btn_y = screen_height // 2.3 + 100
btn_width = 200
btn_height = 60

btn_bg = create_rounded_rect(canvas, btn_x, btn_y, btn_width, btn_height, corner_radius=20,
                             fill="#fcbe2e", outline="#e08021", width=5,
                             state='hidden', tags="start_btn")

btn_text = canvas.create_text(btn_x, btn_y, text="Start Game", fill="white",
                              font=("Arial", 20, "bold"),
                              state='hidden', tags="start_btn")

# --- FIXED HOVER LOGIC ---
is_hovered = False

def check_hover(event):
    global is_hovered
    
    # Check if game is running and button is visible
    if not game_running:
        canvas.config(cursor="") # Reset cursor if game ending
        return
    if canvas.itemcget("start_btn", "state") != 'normal':
        return

    # Calculate the static "Hit Box"
    left_x = btn_x - btn_width // 2
    right_x = btn_x + btn_width // 2
    top_y = btn_y - btn_height // 2
    bottom_y = btn_y + btn_height // 2

    # Check if mouse is inside the box
    if left_x <= event.x <= right_x and top_y <= event.y <= bottom_y:
        # === 1. CHANGE CURSOR TO HAND ===
        canvas.config(cursor="hand2") 
        
        # If inside and not already hovered, move UP
        if not is_hovered:
            is_hovered = True
            try:
                canvas.move("start_btn", 0, -5)
            except:
                pass
    else:
        # === 2. RESET CURSOR TO ARROW ===
        canvas.config(cursor="") 
        
        # If outside and currently hovered, move DOWN
        if is_hovered:
            is_hovered = False
            try:
                canvas.move("start_btn", 0, 5)
            except:
                pass

canvas.bind('<Motion>', check_hover)

# --- PIPE IMAGE ---
pipe_img = Image.open("pipe.png").resize((650, 850), Image.LANCZOS)
pipe_photo = ImageTk.PhotoImage(pipe_img)
pipe_x = screen_width - 180
pipe_target_y = -200
pipe_current_y = -600
pipe_id = canvas.create_image(pipe_x, pipe_current_y, image=pipe_photo, anchor="n")

# --- BIRD ---
img = Image.open("bird22.png").resize((200, 200), Image.LANCZOS)
bird = ImageTk.PhotoImage(img)
x = 0
base_y = screen_height // 4
bird_id = canvas.create_image(x, base_y, image=bird)

# VARIABLES
sway_position = 0
is_retreating = False
bird_stopped = False
pipe_descending = False
game_running = True

move_after_id = None

# --- OPEN NEXT PAGE ---
def open_next_page(event):
    global game_running, move_after_id

    # 1. Play the sound
    if click_sound:
        click_sound.play()
        
        # 2. IMPORTANT: Pause slightly to let the sound actually come out
        # before the window destroys itself. (300 milliseconds)
        root.update() # Keep screen drawn
        pygame.time.delay(300) 

    game_running = False

    # Unbind the motion checker so it stops firing
    canvas.unbind('<Motion>')
    canvas.tag_unbind("start_btn", "<Button-1>")

    if move_after_id is not None:
        try:
            root.after_cancel(move_after_id)
        except:
            pass

    root.destroy()

    # Path to game
    bird2_path = r"D:\Coding\Flappy Bird\bird2.py"
    
    subprocess.Popen([sys.executable, bird2_path])

canvas.tag_bind("start_btn", "<Button-1>", open_next_page)

# --- ANIMATION LOOP ---
def move():
    global x, sway_position, is_retreating, bird_stopped
    global pipe_current_y, pipe_descending, game_running, move_after_id

    if not game_running:
        return

    sway_position += 0.08
    current_y = base_y + math.sin(sway_position) * 50

    # Pipe logic
    if x > (pipe_x - 500):
        pipe_descending = True
    if pipe_descending and pipe_current_y < pipe_target_y:
        pipe_current_y += 15
        canvas.coords(pipe_id, pipe_x, pipe_current_y)

    # Bird movement logic
    if bird_stopped:
        canvas.itemconfig(id_flappy, state='normal')
        canvas.itemconfig(id_bird_word, state='normal')
        canvas.itemconfig("start_btn", state='normal')
        
        # Ensure items are on top
        canvas.lift(id_flappy)
        canvas.lift(id_bird_word)
        canvas.lift("start_btn")
        canvas.lift(bird_id)

    elif is_retreating:
        x -= 10
        if x <= screen_width // 3.5:
            x = screen_width // 3.5
            is_retreating = False
            bird_stopped = True

    else:
        x += 6
        if x > (pipe_x - 110):
            is_retreating = True

    canvas.coords(bird_id, x, current_y)
    canvas.lift(bird_id)

    move_after_id = root.after(20, move)

# Start logic
root.update()
move()
root.mainloop()