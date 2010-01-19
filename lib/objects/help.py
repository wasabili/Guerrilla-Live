#!/usr/bin/env python
#-*- coding:utf-8 -*-

import pygame
from pygame.locals import *

from lib.constants  import *
from lib.utils      import set_transparency_to_surf
from base           import *
            
#########################################################################################
#                     HELP ANIMATION                                                    #
#########################################################################################


class HelpDraw():

    def __init__(self):

        self.get_bg = True

        self.bg_help = BackgroundHelp()
        self.cover_help = CoverHelp()
        self.contents_help = ContentsHelp(self.cover_help)
        self.pushspace_help = PushSpaceHelp(self.cover_help)

        self.closing = False
        self.closed = False
        self.opaque = 255
        self.speed = 30

    def update(self):

        self.bg_help.update()
        self.cover_help.update()
        self.contents_help.update()
        self.pushspace_help.update()

    def draw(self, screen):

        # Background
        screen.fill((255,255,255))
        screen.blit(self.bg_help.image, (0,0))

        # Foreground
        newsurf = screen.copy()
        newsurf.blit(self.cover_help.image, (self.cover_help.rect.x, self.cover_help.rect.y))
        newsurf.blit(self.contents_help.image, (self.contents_help.rect.x, self.contents_help.rect.y))
        newsurf.blit(self.pushspace_help.image, (self.pushspace_help.rect.x, self.pushspace_help.rect.y))
        
        if not self.closing:
            screen.blit(newsurf, (0,0))
        else:
            if self.opaque - self.speed > 0:
                self.opaque -= self.speed
            else:
                self.opaque = 0
                self.closed = True
            newsurf.set_alpha(self.opaque)
            screen.blit(newsurf, (0,0))

    def close(self):
        self.closing = True
        self.bg_help.back()

    def whileclosing(self):
        return self.closing

    def hasclosed(self):
        return self.closed


class BackgroundHelp():

    def __init__(self):
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
            

    def back(self):
        self.goforward = False
        self.frame = len(self.images)
        self.cycle = 1
        

class CoverHelp():

    ENTER, SHOW, EXIT = range(3)
    FIRST, SECOND, WAIT = range(3)

    def __init__(self):
        self.rect = None
        self.frame = 0
        self.state = self.ENTER
        self.step = self.FIRST
        self.speed = 30
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

        width = int(SCR_RECT.width-self.fpx*2)
        height = int(SCR_RECT.height-self.fpy*2)
        newsurf = pygame.Surface((width, height))
        newsurf = newsurf.convert_alpha()
        newsurf.fill((0,0,0,128))

        self.image = newsurf
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = int(self.fpx), int(self.fpy)

    def isshowstate(self):
        return self.state == self.SHOW


class ContentsHelp():
    
    def __init__(self, cover_help):
        self.rect = self.image.get_rect()
        self.cover_help = cover_help

        self.original_image = self.image.copy()

    def update(self):
        if self.cover_help.isshowstate():
            self.image = self.original_image
        else:
            self.image = pygame.Surface(SCR_RECT.size, SRCALPHA)
            self.image.fill((0,0,0,0))


class PushSpaceHelp(StringObjectBase):

    y = 690
    text = 'PUSH SPACE KEY'
    frame = 0
    color = (255, 255, 255)
    fontsize = 40

    def __init__(self, cover_help):
        StringObjectBase.__init__(self)
        self.original_image = self.image.copy()

        self.opaque = 0
        self.speed = 3
        self.min_opaque = 55
        self.max_opaque = 255
        self.frame = 0
        self.blink = False

        self.cover_help = cover_help

    def update(self):
        if not self.cover_help.isshowstate():

            self.image = pygame.Surface(self.original_image.get_size()).convert_alpha()
            self.image.fill((0,0,0,0))
            self.frame += 1

        else:
            if not self.blink:
                if self.opaque + self.speed > self.max_opaque:
                    self.speed *= -1
                    self.blink = True

            else:
                if self.opaque+self.speed < self.min_opaque or self.opaque+self.speed > self.max_opaque:
                    self.speed *= -1

            self.opaque += self.speed
            self.image = self.original_image.copy()
            set_transparency_to_surf(self.image, self.opaque)

