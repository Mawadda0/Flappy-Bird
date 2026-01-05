import os
import subprocess
import sys
import pygame
import math
from sys import exit
import random

#-------------------------------------#-------------------------------------#----------------------------
# 1. SETUP & CONFIG
#-------------------------------------#-------------------------------------#----------------------------
pygame.init()

screen_info = pygame.display.Info()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bird")

clock = pygame.time.Clock()
FPS = 60

#-------------------------------------#-------------------------------------#----------------------------
# bird handler
#-------------------------------------#-------------------------------------#----------------------------
BIRD_SIZE = 80
try:
    bird_image = pygame.image.load("./version_two/bird2.png").convert_alpha()
    bird_image = pygame.transform.scale(bird_image, (BIRD_SIZE, BIRD_SIZE))
except:
    bird_image = pygame.Surface((BIRD_SIZE, BIRD_SIZE))
    bird_image.fill((255, 255, 0))

max_down_speed = 100
gravity = 0.4
jump_strength = -8  # Increased slightly for better feel with single-press jumping

class Bird():
    def __init__(self):
        self.x = WIDTH / 3
        self.y = HEIGHT / 2
        self.speed_y = 0

bird = Bird()

def jump_bird(bird):
    bird.speed_y = jump_strength

def update_bird(bird):
    bird.speed_y += gravity
    if bird.speed_y > max_down_speed:
        bird.speed_y = max_down_speed
    
    bird.y += bird.speed_y

    if bird.y < 0:
        bird.y = 0            
        bird.speed_y = 0      

    angle = -bird.speed_y * 2
    rotated_bird = pygame.transform.rotate(bird_image, angle)
    bird_rect = rotated_bird.get_rect(center = (bird.x + BIRD_SIZE / 2, bird.y + BIRD_SIZE / 2))
    screen.blit(rotated_bird, bird_rect.topleft)

def get_bird_hitbox(bird):
    return pygame.Rect(bird.x + 25, bird.y + 25, BIRD_SIZE - 50, BIRD_SIZE - 50)

#-------------------------------------#-------------------------------------#----------------------------
# pipes handler
#-------------------------------------#-------------------------------------#----------------------------

TOP = True
BOTTOM = False

def reset_game():
    bird.y = HEIGHT / 2
    bird.speed_y = 0
    pipes.clear()
    return 0  # score

class Pipe(pygame.Rect):
    def __init__(self,pos):
        pygame.Rect.__init__(self, pipe_x, pipe_y, pipe_width, pipe_height)
        self.pos=pos
        self.passed=False

GAME_WIDTH = WIDTH
GAME_HEIGHT= HEIGHT

pipe_x=GAME_WIDTH
pipe_y=0
pipe_width=64
pipe_height=512

try:
    top_pipe_image=pygame.image.load("./pipes/toppipe.png")
    top_pipe_image=pygame.transform.scale(top_pipe_image,(pipe_width,pipe_height))
    bottom_pipe_image=pygame.image.load("./pipes/bottompipe.png")
    bottom_pipe_image=pygame.transform.scale(bottom_pipe_image,(pipe_width,pipe_height))
except:
    top_pipe_image=pygame.Surface((pipe_width,pipe_height))
    bottom_pipe_image=pygame.Surface((pipe_width,pipe_height))

pipes=[]
speed_x=-2

pipes_timer=pygame.USEREVENT +0
pygame.time.set_timer(pipes_timer,1500)

def draw_pipes():
    for pipe in pipes:
        if pipe.pos == TOP:
            screen.blit(top_pipe_image, pipe)
        elif pipe.pos == BOTTOM:
            screen.blit(bottom_pipe_image, pipe)

def move_pipes():
    for pipe in pipes:
        pipe.x +=speed_x

    while  len(pipes) > 0 and pipes[0].x+pipe_width <0:
        pipes.pop(0)

def create_pipes():
    random_pipe_y=pipe_y - pipe_height/4 - random.random()*(pipe_height/2)  
    open_space=GAME_HEIGHT/3
    top_pipe=Pipe(TOP)
    top_pipe.y=random_pipe_y
    pipes.append(top_pipe)
    bottom_pipe=Pipe(BOTTOM)
    bottom_pipe.y=top_pipe.y+top_pipe.height+open_space
    pipes.append(bottom_pipe)

#-------------------------------------#-------------------------------------#----------------------------
# collision handler
#-------------------------------------#-------------------------------------#----------------------------
def check_collisions(bird_rect, pipes, floor_rect_y):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return True
            
    if bird_rect.bottom >= floor_rect_y:
        return True
        
    return False

#-------------------------------------#-------------------------------------#----------------------------
# score handler
#-------------------------------------#-------------------------------------#----------------------------

score = 0

try:
    score_font = pygame.font.Font("pixel.ttf", 50)
except FileNotFoundError:
    print("pixel.ttf not found, using default font.")
    score_font = pygame.font.Font(None, 60)

def check_score(bird_rect, pipes, score):
    for pipe in pipes:
        if bird_rect.left > pipe.x and not pipe.passed:
            score += 0.5
            pipe.passed = True
    return score

def draw_score(screen, score, width):        
    score_surface = score_font.render(str(int(score)), True, (255, 255, 255))
    score_rect = score_surface.get_rect(center=(width // 2, 50))
    screen.blit(score_surface, score_rect)

def reset_score():
    return 0


#-------------------------------------#-------------------------------------#----------------------------
# PAUSE MENU CLASS
#-------------------------------------#-------------------------------------#----------------------------
class PauseMenu:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        try:
            self.font = pygame.font.Font("pixel.ttf", 50)
        except Exception as e:
            self.font = pygame.font.SysFont('Arial', 50, bold=True)
            
        self.WHITE = (255, 255, 255)
        self.ORANGE = (252, 190, 46)
        
        btn_width = 300 
        btn_height = 70 
        gap = 100        
        
        cx, cy = screen_width // 2, screen_height // 2
        
        self.btn_continue = pygame.Rect(0, 0, btn_width, btn_height)
        self.btn_continue.center = (cx, cy - gap)

        self.btn_restart = pygame.Rect(0, 0, btn_width, btn_height)
        self.btn_restart.center = (cx, cy)       

        self.btn_menu = pygame.Rect(0, 0, btn_width, btn_height)
        self.btn_menu.center = (cx, cy + gap)    

    def draw(self, screen):
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.set_alpha(150)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        title_surf = self.font.render("PAUSED", True, self.WHITE)
        title_rect = title_surf.get_rect(center=(self.screen_width//2, self.screen_height//2 - 200))
        screen.blit(title_surf, title_rect)

        self._draw_button(screen, self.btn_continue, "Continue")
        self._draw_button(screen, self.btn_restart, "Restart")
        self._draw_button(screen, self.btn_menu, "Main Menu")

    def _draw_button(self, screen, rect, text):
        pygame.draw.rect(screen, self.ORANGE, rect, border_radius=15)
        pygame.draw.rect(screen, self.WHITE, rect, 4, border_radius=15)
        
        txt_surf = self.font.render(text, True, self.WHITE)
        txt_rect = txt_surf.get_rect(center=rect.center)
        screen.blit(txt_surf, txt_rect)

    def handle_click(self, pos):
        if self.btn_continue.collidepoint(pos):
            return "continue"
        if self.btn_restart.collidepoint(pos):
            return "restart"
        if self.btn_menu.collidepoint(pos):
            return "menu"
        return None

pause_menu = PauseMenu(WIDTH, HEIGHT)

#-------------------------------------#-------------------------------------#----------------------------
# GAME OVER CLASS
#-------------------------------------#-------------------------------------#----------------------------
class GameOver:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.GOLD = (255, 215, 0)

        try:
            self.large_font = pygame.font.Font("./pixel.TTF", 60)
            self.small_font = pygame.font.Font("./pixel.TTF", 30)
        except FileNotFoundError:
            self.large_font = pygame.font.SysFont('Arial', 60, bold=True)
            self.small_font = pygame.font.SysFont('Arial', 40)

    def draw(self, screen, final_score):
        game_over_text = self.large_font.render("GAME OVER", True, self.RED)
        game_over_rect = game_over_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 60))
        
        score_text = self.large_font.render(f"Score: {int(final_score)}", True, self.GOLD)
        score_rect = score_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2))

        restart_text = self.small_font.render("Press SPACE or UP or W to Restart", True, self.WHITE)
        restart_rect = restart_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 60))

        screen.blit(game_over_text, game_over_rect)
        screen.blit(score_text, score_rect)
        screen.blit(restart_text, restart_rect)

    def draw_start_screen(self, screen):
        title_text = self.large_font.render("GET READY", True, self.GOLD)
        title_rect = title_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 50))
        
        start_text = self.small_font.render("Press SPACE or UP or W to Start", True, self.WHITE)
        start_rect = start_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 50))
        
        screen.blit(title_text, title_rect)
        screen.blit(start_text, start_rect)

    def check_for_restart(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_UP or event.key == pygame.K_w:
                return True
        return False

game_over_screen = GameOver(WIDTH, HEIGHT)

#-------------------------------------#-------------------------------------#----------------------------
# BACKGROUND LOGIC
#-------------------------------------#-------------------------------------#----------------------------
try:
    bg_surface = pygame.image.load("background.jpeg").convert()
    bg_surface = pygame.transform.scale(bg_surface, (WIDTH, HEIGHT))
    has_background = True
except FileNotFoundError:
    print("background.jpeg not found. Using solid color.")
    has_background = False

bg_x1 = 0
bg_x2 = WIDTH
bg_speed = 1 

#-------------------------------------#-------------------------------------#----------------------------
# sound handler (UPDATED)
#-------------------------------------#-------------------------------------#----------------------------
pygame.mixer.init()

# --- Load Existing Sounds ---
try:
    flap_sound = pygame.mixer.Sound("./sound/flap.mp3")
    hit_sound = pygame.mixer.Sound("./sound/hit.mp3")
    score_sound = pygame.mixer.Sound("./sound/score.mp3")
    game_over_sound = pygame.mixer.Sound("./sound/gameover.mp3")
    
    flap_sound.set_volume(1)
    hit_sound.set_volume(0.5)
    score_sound.set_volume(0.5)
    game_over_sound.set_volume(0.5)
except:
    print("Warning: One or more basic sounds not found.")

# --- NEW: Load Pause Sound ---
try:
    
    pause_sound = pygame.mixer.Sound("./sound/Jump.wav") 
    pause_sound.set_volume(0.5)
except:
    print("Warning: ./sound/pause.mp3 not found. Creating silent placeholder.")
    pause_sound = pygame.mixer.Sound(buffer=bytearray([0]*100)) # Silent dummy sound

def sound_flap_play():
    flap_sound.play()

def sound_hit_play():
    hit_sound.play()

def sound_score_play():
    score_sound.play()

def sound_game_over_play():
    game_over_sound.play()

def sound_pause_play():
    pause_sound.play()


#-------------------------------------#-------------------------------------#----------------------------
# MAIN LOOP (UPDATED)
#-------------------------------------#-------------------------------------#----------------------------

running = True
game_active = False   
waiting_for_start = True 
game_paused = False

while running:
    clock.tick(FPS)
    
    # 1. DRAW BACKGROUND 
    if has_background:
        if game_active and not waiting_for_start and not game_paused: 
            bg_x1 -= bg_speed
            bg_x2 -= bg_speed
        
        if bg_x1 <= -WIDTH: bg_x1 = WIDTH
        if bg_x2 <= -WIDTH: bg_x2 = WIDTH
            
        screen.blit(bg_surface, (bg_x1, 0))
        screen.blit(bg_surface, (bg_x2, 0))
    else:
        screen.fill((135, 206, 250)) 

    # 2. EVENT HANDLING
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # --- INPUT HANDLING (MOVED JUMP HERE FOR SOUND FIX) ---
        if event.type == pygame.KEYDOWN:
            
            # PAUSE CHECK (With Sound)
            if event.key == pygame.K_ESCAPE:
                if game_active and not waiting_for_start:
                    sound_pause_play() # Play pause sound
                    game_paused = not game_paused
            
            # START GAME CHECK
            if waiting_for_start:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP or event.key == pygame.K_w:
                    waiting_for_start = False
                    game_active = True
                    bird.speed_y = jump_strength
                    sound_flap_play()
            
            # JUMP CHECK (During active game)
            # We moved this here so sound plays once per press, not 60 times a second
            elif game_active and not game_paused:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP or event.key == pygame.K_w:
                    jump_bird(bird)
                    sound_flap_play() # Play jump sound
            
            # RESTART CHECK (Game Over)
            elif not game_active and not waiting_for_start:
                if game_over_screen.check_for_restart(event):
                    score = reset_game()
                    bg_x1, bg_x2 = 0, WIDTH
                    game_active = True
                    waiting_for_start = True # Go back to "Get Ready"

        # --- PAUSE MENU CLICK HANDLING ---
        if game_paused and event.type == pygame.MOUSEBUTTONDOWN:
            action = pause_menu.handle_click(event.pos)
            
            if action == "continue":
                game_paused = False
                
            elif action == "restart":
                score = reset_game()
                bg_x1, bg_x2 = 0, WIDTH
                game_paused = False
                game_active = True
                waiting_for_start = True
                
            elif action == "menu":
                running = False 
                
        # Pipe Timer
        if not game_paused and game_active and not waiting_for_start:
            if event.type == pipes_timer:
                create_pipes()
    
    # 3. GAME UPDATE & DRAW
    if not game_paused:
        
        if not waiting_for_start:
            draw_pipes()

        if waiting_for_start:
            screen.blit(bird_image, (bird.x, bird.y))
            game_over_screen.draw_start_screen(screen)
            
        elif game_active:
            # Note: We removed the keys = pygame.key.get_pressed() block for jumping.
            # It is now handled in the Event Loop above.

            update_bird(bird)
            move_pipes()
            
            bird_hitbox = get_bird_hitbox(bird)
            new_score = check_score(bird_hitbox, pipes, score)
            if (new_score > score):
                score = new_score
                sound_score_play()
                
            draw_score(screen, score, WIDTH)

            if check_collisions(bird_hitbox, pipes, HEIGHT):
                sound_hit_play()
                sound_game_over_play()
                game_active = False
                
        else: # Game Over State
            angle = -bird.speed_y * 2
            rotated_bird = pygame.transform.rotate(bird_image, angle)
            bird_rect = rotated_bird.get_rect(center = (bird.x + BIRD_SIZE / 2, bird.y + BIRD_SIZE / 2))
            screen.blit(rotated_bird, bird_rect.topleft)
            game_over_screen.draw(screen, score)

    # 4. DRAW PAUSE MENU (If paused)
    if game_paused:
        draw_pipes()
        screen.blit(bird_image, (bird.x, bird.y))
        draw_score(screen, score, WIDTH)
        pause_menu.draw(screen)

    pygame.display.update()

pygame.quit()