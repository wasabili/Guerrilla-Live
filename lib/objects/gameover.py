#!/usr/bin/env python
#-*- coding:utf-8 -*-

import pygame
from pygame.locals import *

from lib.constants  import *
from base           import *

#########################################################################################
#                     GAMEOVER ANIMATION                                                #
#########################################################################################


class GameoverDraw():

    def __init__(self, gamedata):  # FIXME win or lose
        # Sprite Group
        self.gameover_all = BaseGroup()

        # Register groups to sprites
        BackgroundGameover.containers       = self.gameover_all
        ScoreGameover.containers            = self.gameover_all
        PushSpaceGameover.containers        = self.gameover_all

        # Objects
        self.bg_gameover = BackgroundGameover(gamedata.result==gamedata.WIN, gamedata.lastscreen)
        self.pushspace = PushSpaceGameover()
        if gamedata.result == gamedata.WIN:
            self.score = ScoreGameover(gamedata.get_score())

        self.gamedata = gamedata

    def update(self):
        self.gameover_all.update()

    def draw(self):
        self.gameover_all.draw()


class BackgroundGameover(BaseSprite):
    """Background fades in when a player loses"""

    opaque = 255
    speed = -10

    def __init__(self, win, lastscreen):
        BaseSprite.__init__(self)

        if win:
            self.image = self.winimage
        else:
            self.image = self.loseimage

        self.original_image = self.image.copy()
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

        self.lastgame_image = lastscreen

    def update(self):
        if self.opaque > 0:

            self.im1 = self.original_image.copy()
            self.im2 = self.lastgame_image.copy()

            self.im1.set_alpha(255-self.opaque)
            self.im2.set_alpha(self.opaque)

            self.image = pygame.Surface(SCR_RECT.size)
            self.image.convert_alpha()
            self.image.blit(self.im1, (0,0))
            self.image.blit(self.im2, (0,0))

            self.opaque += self.speed
        else:
            self.image = self.original_image


class ScoreGameover(BaseSprite):

    y = 300
    text = 'SCORE: {0}'
    color = (0, 0, 0)
    fontsize = 30

    def __init__(self, score):
        text = text.format(score)
        BaseSprite.__init__(self)
        self.opaque = 0.04
        self.speed = 0.008

    def update(self):

        if self.opaque < 1.0:
            if self.opaque + self.speed < 1.0:
                self.opaque += self.speed
            else:
                self.opaque = 1.0


class PushSpaceGameover(BasePushSpaceSprite):

    y = 600
    color = (128, 128, 128)
    wait = 60

    def __init__(self):
        BasePushSpaceSprite.__init__(self)
        self.opaque = 0
        self.speed = 3


