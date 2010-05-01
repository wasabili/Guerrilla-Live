#!/usr/bin/env python
#-*- coding:utf-8 -*-

import pygame
from pygame.locals import *
import sys

from lib.constants  import *
from base           import BaseSprite, BaseGroup, BasePushSpaceSprite
from gloss          import Gloss, Texture, Color

#########################################################################################
#                     HELP ANIMATION                                                    #
#########################################################################################


class HelpDraw():

    def __init__(self):
        # Sprite Group
        self.help_all = BaseGroup()

        # Register groups to sprites
        BackgroundHelp.containers   = self.help_all
        CoverHelp.containers        = self.help_all
        ContentsHelp.containers     = self.help_all
        PushSpaceHelp.containers    = self.help_all

        # Objects
        self.bg_help = BackgroundHelp()
        self.cover_help = CoverHelp()
        self.contents_help = ContentsHelp(self.cover_help)
        self.pushspace_help = PushSpaceHelp(self.cover_help)

        self.closing = False
        self.closed = False

    def update(self):
        self.help_all.update()
        self.closed = self.cover_help.hasclosed()

    def draw(self):
        self.help_all.draw()

    def close(self):
        self.closing = True
        self.bg_help.close()
        self.cover_help.close()
        self.contents_help.kill()
        self.pushspace_help.kill()

    def whileclosing(self):
        return self.closing

    def hasclosed(self):
        return self.closed


class BackgroundHelp(BaseSprite):

    def __init__(self):
        self.index = 0
        self.texture = self.textures[self.index]
        BaseSprite.__init__(self)

        self.frame = 0
        self.cycle = 3

        self.goforward = True

    def update(self):

        if self.goforward:
            if self.frame%self.cycle == 0 and self.index < len(self.textures)-1:
                self.index += 1
                self.texture = self.textures[self.index]

            self.frame += 1

        else:
            if self.frame%self.cycle == 0 and self.index > 0:
                self.index -= 1
                self.texture = self.textures[self.index]

            self.frame -= 1

    def close(self):
        self.goforward = False
        self.frame = len(self.textures)
        self.cycle = 1


class CoverHelp(BaseSprite):

    ENTER, SHOW, EXIT = range(3)
    FIRST, SECOND, WAIT = range(3) # of ENTER state

    def __init__(self):
        self.texture = Texture(pygame.Surface(SCR_RECT.size, SRCALPHA|HWSURFACE))
        BaseSprite.__init__(self)

        self.frame = 0
        self.state = self.ENTER
        self.step = self.FIRST
        self.speed = 30
        self.opaque = 0.5
        self.opaque_speed = 0.04
        self.wait = 10
        self.fpx = SCR_RECT.width/2.0-3
        self.fpy = SCR_RECT.height/2.0-3

    def update(self):

        if self.state == self.ENTER:
            if self.step == self.FIRST:
                if self.fpx - self.speed > 0:
                    self.fpx -= self.speed
                else:
                    self.fpx = 0
                    self.step = self.WAIT
                    self.frame = 0

            elif self.step == self.WAIT:
                if self.frame > self.wait:
                    self.step = self.SECOND

            elif self.step == self.SECOND:
                if self.fpy - self.speed > 0:
                    self.fpy -= self.speed
                else:
                    self.fpy = 0
                    self.state = self.SHOW
                    self.frame = 0

            self.frame += 1
        elif self.state == self.SHOW:
            self.fpx = 0
            self.fpy = 0 
        elif self.state == self.EXIT:
            self.fpx = 0
            self.fpy = 0
            self.opaque = max(self.opaque - self.opaque_speed, 0)

    def draw(self):
        if self.frame:
            position = (int(self.fpx), int(self.fpy))
            width = int(SCR_RECT.width-self.fpx*2)
            height = int(SCR_RECT.height-self.fpy*2)
            color = Color(0, 0, 0, self.opaque)
            Gloss.draw_box(position = position, width = width, height = height, rotation = 0.0, origin = (0, 0), scale = 1, color = color)

    def isshowstate(self):
        return self.state == self.SHOW

    def close(self):
        self.state = self.EXIT

    def hasclosed(self):
        return self.state == self.EXIT and self.opaque == 0


class ContentsHelp(BaseSprite):
    
    pos = (74, 74)

    def __init__(self, cover_help):
        BaseSprite.__init__(self, self.containers)

        self.rect.topleft = self.pos
        self.visible = False
        self.cover_help = cover_help

    def update(self):
        if self.cover_help.isshowstate():
            self.visible = True
        else:
            self.visible = False

    def draw(self):
        if self.visible:
            BaseSprite.draw(self)


class PushSpaceHelp(BasePushSpaceSprite):

    y = 690

    def __init__(self, cover_help):
        BasePushSpaceSprite.__init__(self)

        self.wait = sys.maxint
        self.cover_help = cover_help

    def update(self):
        if self.cover_help.isshowstate():
            self.wait = -1
        BasePushSpaceSprite.update(self)

