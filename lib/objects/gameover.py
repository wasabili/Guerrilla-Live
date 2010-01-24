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
        # Sprite Group
        self.gameover_all = pygame.sprite.LayeredDirty()

        # Register groups to sprites
        BackgroundGameover.containers       = self.gameover_all
        TitleGameover.containers            = self.gameover_all
        ScoreGameover.containers            = self.gameover_all
        PushSpaceGameover.containers        = self.gameover_all

        # Objects
        self.bg_gameover = BackgroundGameover(gamedata.result == gamedata.WIN, gamedata.lastscreen)
        self.title = TitleGameover()
        self.score = ScoreGameover(gamedata.get_score())
        self.pushspace = PushSpaceGameover()

        self.gamedata = gamedata

    def update(self):
        self.gameover_all.update()

    def draw(self, screen):
        return self.gameover_all.draw(screen)  #FIXME bg


class BackgroundGameover(pygame.sprite.DirtySprite):
    """Background fades in when a player loses"""

    def __init__(self, win, lastscreen):
        pygame.sprite.DirtySprite.__init__(self, self.containers)
        self.dirty = 2

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

        self.lastgame_image = lastscreen


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


class TitleGameover(StringSpriteBase):

    y = 100
    text = 'GAME OVER'
    color = (128, 128, 128)
    fontsize = 80
    
    def __init__(self):
        StringSpriteBase.__init__(self)

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


class ScoreGameover(StringSpriteBase):

    y = 300
    text = 'Score: {0}'
    color = (128, 128, 128)
    fontsize = 60

    def __init__(self, score):
        StringSpriteBase.__init__(self)
        self.opaque = 10
        self.speed = 2

        self.score = score

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


