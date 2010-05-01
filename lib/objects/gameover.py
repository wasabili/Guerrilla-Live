#!/usr/bin/env python
#-*- coding:utf-8 -*-

import pygame
from pygame.locals import *

from lib.constants  import *
from base           import *
from gloss          import Texture

#########################################################################################
#                     GAMEOVER ANIMATION                                                #
#########################################################################################


class GameoverDraw():

    def __init__(self, gamedata):
        # Sprite Group
        self.gameover_all = BaseGroup()

        # Register groups to sprites
        BackgroundGameover.containers       = self.gameover_all
        ScoreGameover.containers            = self.gameover_all
        PushSpaceGameover.containers        = self.gameover_all

        # Objects
        if gamedata.win():
            self.bg_gameover = BackgroundGameover(True)
            self.score = ScoreGameover(gamedata.getscore())
            self.pushspace = PushSpaceGameover()
        else:
            self.bg_gameover = BackgroundGameover(False)
            self.pushspace = PushSpaceGameover()

    def update(self):
        self.gameover_all.update()

    def draw(self):
        self.gameover_all.draw()


class BackgroundGameover(BaseSprite):
    """Background fades in when a player loses"""

    opaque = 1.0
    speed = -0.04

    def __init__(self, win):
        if win:
            self.orig_texture= self.wintexture
        else:
            self.orig_texture = self.losetexture
        self.texture = self.orig_texture
        BaseSprite.__init__(self)

        self.rect.topleft = (0, 0)

        from OpenGL.GL import *
        OpenGL.ERROR_CHECKING = False
        from OpenGL.GL.EXT.framebuffer_object import *
        from OpenGL.GLU import *
        # キャプチャ
        glReadBuffer(GL_FRONT)
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        data = glReadPixels(0, 0, 1024, 768, GL_RGBA, GL_UNSIGNED_BYTE)
        # 画像を保存
        self.game_capture = Texture(pygame.image.fromstring(data, (1024,768), "RGBA", True))

    def update(self):
        self.opaque = max(self.opaque + self.speed, 0)

    def draw(self):
        self.texture = self.game_capture
        self.opaque = self.opaque
        BaseSprite.draw(self)
        self.texture = self.orig_texture
        self.opaque = 1 - self.opaque
        BaseSprite.draw(self)
        self.opaque = 1 - self.opaque


class ScoreGameover(BaseSpriteFont):

    y = 300
    text = 'SCORE: {0}'
    color = (0, 0, 0)
    fontsize = 30

    def __init__(self, score):
        self.text = self.text.format(score)
        BaseSpriteFont.__init__(self)
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
    color = (0.5, 0.5, 0.5)
    wait = 60

    def __init__(self):
        BasePushSpaceSprite.__init__(self)
        self.opaque = 0.0
        self.speed = 0.1


