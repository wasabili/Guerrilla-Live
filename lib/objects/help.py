#!/usr/bin/env python
#-*- coding:utf-8 -*-

import pygame
from pygame.locals import *
import sys

from lib.constants  import *
from lib.utils      import set_transparency_to_surf
from base           import *
from start          import PushSpaceStart
            
#########################################################################################
#                     HELP ANIMATION                                                    #
#########################################################################################


class HelpDraw():

    def __init__(self):
        # Sprite Group
        self.help_all = pygame.sprite.LayeredDirty()

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

        self.base_surf = pygame.Surface(SCR_RECT.size, HWSURFACE)

        self.closing = False
        self.closed = False

    def update(self):
        self.help_all.update()
        self.closed = self.cover_help.hasclosed()

    def draw(self, screen):
        return self.help_all.draw(screen)

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


class BackgroundHelp(pygame.sprite.DirtySprite):

    def __init__(self):
        pygame.sprite.DirtySprite.__init__(self, self.containers)
        self.dirty = 2

        self.index = 0
        self.image = self.images[self.index]
        self.rect = SCR_RECT

        self.frame = 0
        self.cycle = 3

        self.goforward = True

    def update(self):

        if self.goforward:
            if self.frame%self.cycle == 0 and self.index < len(self.images)-1:
                self.index += 1
                self.image = self.images[self.index]

            self.frame += 1

        else:
            if self.frame%self.cycle == 0 and self.index > 0:
                self.index -= 1
                self.image = self.images[self.index]

            self.frame -= 1
            

    def close(self):
        self.goforward = False
        self.frame = len(self.images)
        self.cycle = 1
        

class CoverHelp(pygame.sprite.DirtySprite):

    ENTER, SHOW, EXIT = range(3)
    FIRST, SECOND, WAIT = range(3)

    def __init__(self):
        pygame.sprite.DirtySprite.__init__(self, self.containers)
        self.dirty = 2

        self.rect = None
        self.frame = 0
        self.state = self.ENTER
        self.step = self.FIRST
        self.speed = 30
        self.opaque = 128
        self.opaque_speed = 10
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


        width = int(SCR_RECT.width-self.fpx*2)
        height = int(SCR_RECT.height-self.fpy*2)
        newsurf = pygame.Surface((width, height), SRCALPHA|HWSURFACE)
        newsurf.fill((0,0,0,self.opaque))

        self.image = newsurf
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = int(self.fpx), int(self.fpy)

    def isshowstate(self):
        return self.state == self.SHOW

    def close(self):
        self.state = self.EXIT

    def hasclosed(self):
        return self.state == self.EXIT and self.opaque == 0


class ContentsHelp(pygame.sprite.DirtySprite):
    
    def __init__(self, cover_help):
        pygame.sprite.DirtySprite.__init__(self, self.containers)
        self.dirty = 2

        self.none_image = pygame.Surface((0,0))
        self.rect = self.image.get_rect()
        self.cover_help = cover_help

        self.original_image = self.image.copy()

    def update(self):
        if self.cover_help.isshowstate():
            self.image = self.original_image
        else:
            self.image = self.none_image
            self.rect = self.image.get_rect()


class PushSpaceHelp(PushSpaceStart):

    y = 690

    def __init__(self, cover_help):
        PushSpaceStart.__init__(self)

        self.wait = sys.maxint
        self.cover_help = cover_help

    def update(self):
        if self.cover_help.isshowstate():
            self.wait = -1
        PushSpaceStart.update(self)

