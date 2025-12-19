import pygame

pygame.mixer.init()


flap_sound = pygame.mixer.Sound("sounds/flap.wav")
hit_sound = pygame.mixer.Sound("hit.mp3")
score_sound = pygame.mixer.Sound("score.mp3")
game_over_sound = pygame.mixer.Sound("gameover.mp3")


flap_sound.set_volume(0.5)
hit_sound.set_volume(0.5)
score_sound.set_volume(0.5)
game_over_sound.set_volume(0.5)

def play_flap():
    flap_sound.play()

def play_hit():
    hit_sound.play()

def play_score():
    score_sound.play()

def play_game_over():
    game_over_sound.play()