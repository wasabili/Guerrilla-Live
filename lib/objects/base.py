#!/usr/bin/env python
#-*- coding:utf-8 -*-

import pygame
from pygame.locals  import *
import gloss

from lib.constants import *

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
        gloss.Sprite.draw(self, position = self.rect.topleft, rotation = self.rotation, origin = (0, 0), scale = self.scale, color = color)

class BaseGroup(pygame.sprite.LayeredUpdates):

    def __init__(self, *sprites, **kargs):
        pygame.sprite.LayeredUpdates.__init__(self, sprites, kargs)

    def draw(self, screen=None):
        for spr in self.sprites():
            spr.draw()



class BaseSpriteFont(gloss.SpriteFont):

    y = 0           # abstract
    x = None        # abstract
    fontfamily = None   # abstract
    fontsize = 0    # abstract
    text = ''       # abstract
    color = (0,0,0) # abstract

    def __init__(self):

        self.font = pygame.font.SysFont(self.fontfamily, self.fontsize)
        self.image = self.font.render(self.text, True, self.color)

        self.rect = self.image.get_rect()
        if self.x is None:
            self.rect.x = (SCR_RECT.width-self.image.get_width())/2
        else:
            self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        pass


