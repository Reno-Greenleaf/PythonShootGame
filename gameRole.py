# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 16:36:03 2013

@author: Leo
"""

import pygame
from pygame.sprite import Sprite, Group
from pygame import locals as l, Rect

SCREEN_WIDTH = 480
SCREEN_HEIGHT = 800

TYPE_SMALL = 1
TYPE_MIDDLE = 2
TYPE_BIG = 3


class Bullet(Sprite):
    def __init__(self, bullet_img, init_pos):
        Sprite.__init__(self)
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.midbottom = init_pos
        self.speed = 10

    def update(self):
        self.rect.top -= self.speed

        if self.rect.bottom < 0:
            self.kill()


class Player(Sprite):
    def __init__(self, plane_img, images, init_pos):
        Sprite.__init__(self)
        self.bullet_img = plane_img.subsurface(Rect(1004, 987, 9, 21))
        self.images = images                            # Used to store a list of player object sprite images.
        self.rect = self.images[0].get_rect()            # Initialize the rectangle where the image is located.
        self.rect.topleft = init_pos                    # Initialize the coordinates of the upper left corner of the rectangle.
        self.speed = 8                                  # Initialize the player speed, here is a certain value.
        self.bullets = Group()                          # A collection of bullets fired by the player's aircraft.
        self.img_index = 0                              # Player sprite image index.
        self.is_hit = False                             # Whether the player is hit.
        self.image = self.images[self.img_index]
        self.shoot_frequency = 0
        self.down_index = 16

    def update(self):
        self.image = self.images[self.img_index]
        self.bullets.update()

        if self.is_hit:
            self.img_index = self.down_index // 8
            self.down_index += 1
            return

        self.shoot_frequency += 1

        if self.shoot_frequency == 15:
            bullet = Bullet(self.bullet_img, self.rect.midtop)
            self.bullets.add(bullet)
            self.shoot_frequency = 0

        self.img_index = self.shoot_frequency // 8

    def collided(self):
        self.is_hit = True

    def key_pressed(self, key):
        if self.is_hit:
            return

        if key[l.K_w] or key[l.K_UP]:
            self._move_up()

        if key[l.K_s] or key[l.K_DOWN]:
            self._move_down()

        if key[l.K_a] or key[l.K_LEFT]:
            self._move_left()

        if key[l.K_d] or key[l.K_RIGHT]:
            self._move_right()

    def _move_up(self):
        """ React to up key press. """
        if self.rect.top <= 0:
            self.rect.top = 0
        else:
            self.rect.top -= self.speed

    def _move_down(self):
        """ React to down key press. """
        if self.rect.top >= SCREEN_HEIGHT - self.rect.height:
            self.rect.top = SCREEN_HEIGHT - self.rect.height
        else:
            self.rect.top += self.speed

    def _move_left(self):
        """ React to left up key press. """
        if self.rect.left <= 0:
            self.rect.left = 0
        else:
            self.rect.left -= self.speed

    def _move_right(self):
        """ React to right key press. """
        if self.rect.left >= SCREEN_WIDTH - self.rect.width:
            self.rect.left = SCREEN_WIDTH - self.rect.width
        else:
            self.rect.left += self.speed


class Enemy(Sprite):
    def __init__(self, enemy_img, enemy_down_imgs, init_pos):
       Sprite.__init__(self)
       self.image = enemy_img
       self.rect = self.image.get_rect()
       self.rect.topleft = init_pos
       self.down_imgs = enemy_down_imgs
       self.speed = 2
       self.down_index = 0

    def update(self):
        self.rect.top += self.speed

        if self.rect.top > SCREEN_HEIGHT:
            self.kill()