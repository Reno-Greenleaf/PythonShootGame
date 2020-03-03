# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 11:05:00 2013

@author: Leo
"""

import pygame
from sys import exit
from pygame.locals import *
from gameRole import *
import random
from pool import Pool


pool = Pool()
# Initialize the game
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('飞机大战'.decode('utf-8'))

# Loading game music
bullet_sound = pygame.mixer.Sound('resources/sound/bullet.wav')
enemy1_down_sound = pygame.mixer.Sound('resources/sound/enemy1_down.wav')
game_over_sound = pygame.mixer.Sound('resources/sound/game_over.wav')
bullet_sound.set_volume(0.3)
enemy1_down_sound.set_volume(0.3)
game_over_sound.set_volume(0.3)
pygame.mixer.music.load('resources/sound/game_music.wav')
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.25)

# Loading background image.
background = pygame.image.load('resources/image/background.png').convert()
game_over = pygame.image.load('resources/image/gameover.png')

# Add players aircraft.
player = pool.create_player((200, 600))

enemies1 = pygame.sprite.Group()

# Store the destroyed aircraft for rendering the wrecking sprite animation.
enemies_down = pygame.sprite.Group()

enemy_frequency = 0
score = 0
clock = pygame.time.Clock()

running = True

while running:
    # Maximum framerate of the game is 60.
    clock.tick(60)

    # Generating enemy aircraft.
    if enemy_frequency == 50:
        enemy1_pos = [random.randint(0, SCREEN_WIDTH - 57), -43]
        enemy1 = pool.create_enemy(enemy1_pos)
        enemies1.add(enemy1)
        enemy_frequency = 0

    enemy_frequency += 1
    enemies1.update()

    for enemy in enemies1:
        # Determine if the player is hit.
        if pygame.sprite.collide_circle(enemy, player):
            enemies_down.add(enemy)
            enemies1.remove(enemy)
            player.collided()
            game_over_sound.play()
            break

    # Add the enemy object that was hit to the destroyed enemy group to render the destroy animation.
    enemies1_down = pygame.sprite.groupcollide(enemies1, player.bullets, 1, 1)

    for enemy_down in enemies1_down:
        enemies_down.add(enemy_down)

    # Drawing background.
    screen.blit(background, (0, 0))

    # Drawing player plane.
    player.update()
    screen.blit(player.image, player.rect)

    if player.down_index > 47:
        running = False

    # Draw a wreck animation.
    for enemy_down in enemies_down:
        if enemy_down.down_index == 0:
            enemy1_down_sound.play()

        if enemy_down.down_index > 7:
            enemies_down.remove(enemy_down)
            score += 1000
            continue

        screen.blit(enemy_down.down_imgs[enemy_down.down_index // 2], enemy_down.rect)
        enemy_down.down_index += 1

    # Drawing bullets and enemy planes.
    player.bullets.draw(screen)
    enemies1.draw(screen)

    # Draw a score.
    score_font = pygame.font.Font(None, 36)
    score_text = score_font.render(str(score), True, (128, 128, 128))
    text_rect = score_text.get_rect()
    text_rect.topleft = [10, 10]
    screen.blit(score_text, text_rect)

    # Update screen.
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
            
    # Listening for keyboard events.
    key = pygame.key.get_pressed()
    player.key_pressed(key)


font = pygame.font.Font(None, 48)
text = font.render('Score: '+ str(score), True, (255, 0, 0))
text_rect = text.get_rect()
text_rect.centerx = screen.get_rect().centerx
text_rect.centery = screen.get_rect().centery + 24
screen.blit(game_over, (0, 0))
screen.blit(text, text_rect)

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    pygame.display.update()
