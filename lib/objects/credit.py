#!/usr/bin/env python
#-*- coding:utf-8 -*-

import pygame
from pygame.locals import *

from lib.constants  import *
from base           import *

#########################################################################################
#                     CREDIT ANIMATION                                                  #
#########################################################################################


class CreditDraw():

    def __init__(self):
        # Sprite Group
        self.credit_all = BaseGroup()

        # Register groups to sprites
        AuthorCredit.containers = self.credit_all

        # Objects
        self.author = AuthorCredit()
    
    def update(self):
        self.credit_all.update()

    def draw(self):
        self.credit_all.draw()

    def hasfinished(self):
        return self.author.hasfinished()


class AuthorCredit(BaseSpriteFont):
    """Start Background"""

    FADEIN, WAIT, FADEOUT, EXTRA, END = range(5)
    state = FADEIN
    y = SCR_RECT.height/2
    text = 'Wasabi Presents'
    color = (1.0, 1.0, 1.0)
    fontsize = 10
    
    def __init__(self):
        BaseSpriteFont.__init__(self)

        self.y -= self.measure_string(self.text)[1]/2

        self.frame = 0
        self.opaque = 0
        self.speed = 3
        self.wait = 80
        self.extra = 40

    def update(self):
        if self.state == self.FADEIN:
            if self.opaque + self.speed < 255:
                self.opaque += self.speed
            else:
                self.opaque = 255
                self.state = self.WAIT
                self.frame = 0
        
        elif self.state == self.WAIT:
            if self.frame > self.wait:
                self.state = self.FADEOUT

        elif self.state == self.FADEOUT:
            if self.opaque - self.speed > 0:
                self.opaque -= self.speed
            else:
                self.opaque = 0
                self.state = self.EXTRA
                self.frame = 0

        elif self.state == self.EXTRA:
            if self.frame > self.extra:
                self.state = self.END
        
        self.frame += 1

    def hasfinished(self):
        return self.state == self.END



