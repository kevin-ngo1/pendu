import pygame
from pygame.locals import *
import random
import os

pygame.init()
pygame.mixer.init()

#Fenetre
screen_height = 600
screen_width = 1100
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('JJK Pendu')
background = pygame.image.load("image/pendu_background.jpg ")
background = pygame.transform.scale(background, (screen_width, screen_height))

#Music

#Son
pygame.mixer.music.load("song/Hakus.mp3")
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1) 


#Fonctions

#Choisir un mot dans le fichier
def choose_word():
    with open("mots.txt", "r") as file:
        mots = file.readlines()
        mot_choisi = random.choice(mots).strip()
        return mot_choisi
    
def word_random_hide(mot_choisi):
    hide=""
    hide += "_" * len(mot_choisi)
    return hide

def check_errors(errors, max_errors):
    if errors >= max_errors:
        return True
    return False


#Variables

violet="#c671de"
gojo_ini=pygame.image.load("image/gojo.png")
gojo= pygame.transform.scale(gojo_ini, (400,350))
toji_ini=pygame.image.load("image/toji.png")
toji= pygame.transform.scale(toji_ini, (400,380))
toji_dead_ini=pygame.image.load("image/toji_dead.png")
toji_dead= pygame.transform.scale(toji_dead_ini, (400,350))
ball_ini=pygame.image.load("image/ball.png")
ball= pygame.transform.scale(ball_ini, (200,200))
ball_x = 80
ball_y = 300
toji_x =800
word_guess = choose_word()
mot_cache = word_random_hide(word_guess)
font_jjk_path = os.path.join("font", "JujutsuKaisen.ttf")
font_jjk = pygame.font.Font(font_jjk_path, 50)
font_jjk_errors = pygame.font.Font(font_jjk_path, 25)
font_jjk_victory = pygame.font.Font(font_jjk_path, 80)
text = font_jjk.render(mot_cache, True, (255, 255, 255))
errors=0
incorrect_letters = []

#RUN les évènements et jeu
run = True
game_restart=False
while run:

    screen.blit(background, (0, 0))
    screen.blit(gojo, (-100,280))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN and pygame.K_a <= event.key <= pygame.K_z:
            lettre = chr(event.key).lower()
            if lettre in word_guess:
                mot_cache_list = list("".join(mot_cache))
                for i, char in enumerate(word_guess):
                    if char == lettre:
                        mot_cache_list[i] = lettre
                mot_cache = "".join(mot_cache_list)
            else:
                errors+=1
                ball_x += 110
                incorrect_letters.append(lettre)

    if check_errors(errors, 7):
        loss_text = font_jjk.render('Vous avez perdu !', True, (violet))
        restart = font_jjk.render('Appuyer sur espace', True, (violet))
        screen.blit(loss_text,(screen_width//2-320, screen_height//2-150))
        screen.blit(restart,(screen_width//2-340, screen_height//2-70))
        screen.blit(toji_dead, (800,300))
        ball_x = -200
        toji=-200
        game_restart = True

    if "_" not in mot_cache:
        finish = font_jjk_victory.render('Bravo !', True, (violet))
        restart = font_jjk.render('Appuyer sur espace', True, (violet))
        screen.blit(finish,(screen_width//2-200, screen_height//2-150))
        screen.blit(restart,(screen_width//2-340, screen_height//2-50))
        game_restart = True
      
    text = font_jjk.render(" ".join(mot_cache), True, (255, 255, 255))
    screen.blit(text, (30,50))
    incorrect_text = font_jjk_errors.render(f'Erreurs: {" ".join(incorrect_letters)}', True, (255, 255, 255))
    screen.blit(incorrect_text, (screen_width - 500, 20))

    if ball_x != -200:  # Affiche la balle si elle n'est pas en dehors de l'écran
        screen.blit(ball, (ball_x, ball_y))
        screen.blit(toji, (toji_x,250))
        

    pygame.display.update()

    while game_restart:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                game_restart = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                word_guess = choose_word()
                mot_cache = word_random_hide(word_guess)
                text = font_jjk.render(mot_cache, True, (255, 255, 255))
                errors = 0
                incorrect_letters = []
                ball_x= 80
                toji = pygame.transform.scale(toji_ini, (400, 380))
                game_restart = False
                run = True

pygame.quit()