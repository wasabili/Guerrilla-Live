#!/usr/bin/env python
#-*- coding:utf-8 -*-

import pygame
from pygame.locals  import *
import gloss
import os.path

from lib.constants import *
from gloss          import Color

class BaseSprite(gloss.Sprite, pygame.sprite.Sprite):

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

    y = 0           # abstract
    x = 0           # abstract
    fontsize = 0    # abstract
    text = ''       # abstract
    color = (0,0,0) # abstract
    rotation = 0.0
    scale = 1.0
    opaque = 1.0

    def __init__(self, filename="DejaVuSans.ttf", size = 18, bold = False, underline = False, startcharacter = 32, endcharacter = 126):
        pygame.sprite.Sprite.__init__(self, self.containers)
        gloss.SpriteFont.__init__(self, filename=os.path.join('data', filename), size = self.fontsize, bold = False, underline = False, startcharacter = 32, endcharacter = 126)

    def draw(self, text = "Hello, Gloss!", position = (0, 0), rotation = 0.0, scale = 1.0, color = Color.WHITE, letterspacing = 0, linespacing = 0):
        gloss.SpriteFont.draw(self, text=self.text, position = (self.x, self.y), rotation = self.rotation, scale = self.scale, color = Color(self.color[0], self.color[1], self.color[2], self.opaque))




