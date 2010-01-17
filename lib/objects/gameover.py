#!/usr/bin/env python
#-*- coding:utf-8 -*-

import pygame
from pygame.locals import *

from lib.constants  import *
from lib.utils      import set_transparency_to_surf
from base           import *
from start          import PushSpaceStart

#########################################################################################
#                     GAMEOVER ANIMATION                                                #
#########################################################################################


class GameoverDraw():

    def __init__(self, gamedata):  # FIXME win or lose
        self.gamedata = gamedata

        BackgroundGameover.lastgame_image = self.gamedata.get_lastscreen()
        ScoreGameover.score = self.gamedata.get_score()

        self.bg_gameover = BackgroundGameover(self.gamedata.result == self.gamedata.WIN)
        self.title = TitleGameover()
        self.score = ScoreGameover()
        self.pushspace = PushSpaceGameover()

    def update(self):
        self.bg_gameover.update()
        self.title.update()
        self.score.update()
        self.pushspace.update()

    def draw(self, screen):
        # Background
        screen.fill((255,255,255))
        screen.blit(self.bg_gameover.image, (0,0))

        # Foreground
        screen.blit(self.title.image, (self.title.rect.x, self.title.rect.y))
        screen.blit(self.score.image, (self.score.rect.x, self.score.rect.y))
        screen.blit(self.pushspace.image, (self.pushspace.rect.x, self.pushspace.rect.y))


class BackgroundGameover():
    """Background fades in when a player loses"""

    def __init__(self, win):
        if win:
            self.image = self.winimage
        else:
            self.image = self.loseimage

        self.original_image = self.image.copy()
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

        self.opaque = 10
        self.speed = 3
        self.opaque_lg = 255
        self.speed_lg = -30


    def update(self):
        if self.opaque < 255:
            if self.opaque + self.speed < 255:
                self.opaque += self.speed
            else:
                self.opaque = 255

        if self.opaque_lg > 0:
            if self.opaque_lg + self.speed_lg > 0:
                self.opaque_lg += self.speed_lg
            else:
                self.opaque_lg = 0


        self.image = self.original_image.copy()
        self.image.set_alpha(self.opaque)
        self.lastgame = self.lastgame_image.copy()
        self.lastgame.set_alpha(self.opaque_lg)

        newsurf = pygame.Surface((SCR_RECT.width, SCR_RECT.height))
        newsurf.convert_alpha()
        newsurf.blit(self.image, (0,0))
        newsurf.blit(self.lastgame, (0,0))

        self.image = newsurf


class TitleGameover(StringObjectBase):

    y = 100
    text = 'GAME OVER'
    color = (128, 128, 128)
    fontsize = 80
    
    def __init__(self):
        StringObjectBase.__init__(self)

        self.original_image = self.image.copy()
        self.opaque = 10
        self.speed = 2

    def update(self):
        if self.opaque < 255:
            if self.opaque + self.speed < 255:
                self.opaque += self.speed
            else:
                self.opaque = 255

        self.image = self.original_image.copy()
        set_transparency_to_surf(self.image, self.opaque)


class ScoreGameover(StringObjectBase):

    y = 300
    text = 'Score: {0}'
    color = (128, 128, 128)
    fontsize = 60

    def __init__(self):
        StringObjectBase.__init__(self)
        self.opaque = 10
        self.speed = 2

    def update(self):
        self.original_image = self.font.render(self.text.format(self.score), True, self.color)
        self.rect.x = (SCR_RECT.width-self.image.get_width())/2

        if self.opaque < 255:
            if self.opaque + self.speed < 255:
                self.opaque += self.speed
            else:
                self.opaque = 255

        self.image = self.original_image.copy()
        set_transparency_to_surf(self.image, self.opaque)


class PushSpaceGameover(PushSpaceStart):

    y = 600
    frame = 0
    color = (128, 128, 128)

    def __init__(self):
        PushSpaceStart.__init__(self)
        self.image = pygame.Surface((0, 0))
        self.opaque = 100
        self.speed = 7
        self.min_opaque = 55


