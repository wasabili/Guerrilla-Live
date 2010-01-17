#!/usr/bin/env python
#-*- coding:utf-8 -*-

import pygame
from pygame.locals import *

from lib.constants import *

class StringObjectBase():

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


