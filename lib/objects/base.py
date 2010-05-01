#!/usr/bin/env python
#-*- coding:utf-8 -*-

import pygame
from pygame.locals  import *
import gloss
import os.path

from lib.constants import *
from gloss          import Color

class BaseSprite(gloss.Sprite, pygame.sprite.Sprite):

    #TODO
    # visible = True
    # dummy_texture
    # BaseAnimatedSprite

    opaque = 1.0
    rotation = 0.0
    scale = 1.0

    def __init__(self, texture=None, position=None):
        pygame.sprite.Sprite.__init__(self, self.containers)
        gloss.Sprite.__init__(self, self.texture)

        self.rect = pygame.rect.Rect(0, 0, self.texture.width, self.texture.height)

    def draw(self):
        color = gloss.Color(1, 1, 1, self.opaque)
        origin = None if self.rotation != 0.0 else (0, 0)
        gloss.Sprite.draw(self, position = self.rect.topleft, rotation = self.rotation, origin = origin, scale = self.scale, color = color)

class BaseGroup(pygame.sprite.LayeredUpdates):

    def __init__(self, *sprites, **kargs):
        pygame.sprite.LayeredUpdates.__init__(self, sprites, kargs)

    def draw(self, screen=None):
        for spr in self.sprites():
            spr.draw()



class BaseSpriteFont(gloss.SpriteFont, pygame.sprite.Sprite):

    y = None           # abstract
    x = None           # abstract
    fontsize = 0    # abstract
    text = ''       # abstract
    color = (0,0,0) # abstract
    rotation = 0.0
    scale = 1.0
    opaque = 1.0

    def __init__(self, filename="DejaVuSans.ttf", size = 18, bold = False, underline = False, startcharacter = 32, endcharacter = 126):
        pygame.sprite.Sprite.__init__(self, self.containers)
        gloss.SpriteFont.__init__(self, filename=os.path.join('data', filename), size = self.fontsize, bold = False, underline = False, startcharacter = 32, endcharacter = 126)

        if self.x is None:
            self.x = (SCR_RECT.width - self.measure_string(self.text)[0])/2
        if self.y is None:
            self.y = (SCR_RECT.height - self.measure_string(self.text)[1])/2

    def draw(self, text = "Hello, Gloss!", position = (0, 0), rotation = 0.0, scale = 1.0, color = Color.WHITE, letterspacing = 0, linespacing = 0):
        gloss.SpriteFont.draw(self, text=self.text, position = (self.x, self.y), rotation = self.rotation, scale = self.scale, color = Color(self.color[0], self.color[1], self.color[2], self.opaque))



class BasePushSpaceSprite(BaseSpriteFont):

    y = 500
    text = 'PUSH SPACE KEY'
    color = (1.0, 1.0, 1.0)
    fontsize = 20

    wait = 200

    def __init__(self):
        BaseSpriteFont.__init__(self)

        self.opaque = 0
        self.speed = 0.01
        self.min_opaque = 0.21
        self.max_opaque = 0.8

        self.frame = 0
        self.blink = False


    def update(self):

        if self.frame < self.wait:
            self.frame += 1

        else:
            if not self.blink and self.opaque + self.speed > self.max_opaque:  # Escape 'Not Blink' state!
                    self.blink = True

            elif self.blink and (self.opaque+self.speed < self.min_opaque or self.opaque+self.speed > self.max_opaque):  # Reverse speed 
                    self.speed *= -1

            self.opaque += self.speed



