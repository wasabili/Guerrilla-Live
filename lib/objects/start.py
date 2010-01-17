#!/usr/bin/env python
#-*- coding:utf-8 -*-

import pygame
from pygame.locals import *

from lib.constants  import *
from lib.utils      import set_transparency_to_surf
from base           import *

#########################################################################################
#                     START ANIMATION                                                   #
#########################################################################################


class StartDraw():

    def __init__(self):
        self.bg_start = BackgroundStart()
        self.title = TitleStart()
        self.pushspace = PushSpaceStart()

    def update(self):
        self.bg_start.update()
        self.title.update()
        self.pushspace.update()

    def draw(self, screen):
        screen.fill((0,0,0))
        screen.blit(self.bg_start.image, (self.bg_start.rect.x, self.bg_start.rect.y))
        screen.blit(self.title.image, (self.title.rect.x, self.title.rect.y))
        screen.blit(self.pushspace.image, (self.pushspace.rect.x, self.pushspace.rect.y))


class BackgroundStart():
    """Start Background"""

    opaque = 0
    speed = 3

    def __init__(self):
        self.original_image = self.image.copy()
        self.rect = self.image.get_rect()

    def update(self):  #FIXME

        if self.opaque < 255:
            if self.opaque + self.speed < 255:
                self.opaque += self.speed
            else:
                self.opaque = 255

            self.image = self.original_image.copy()
            self.image.set_alpha(self.opaque)

        else:
            self.image = self.original_image


class TitleStart():

    y = 250

    opaque = 0
    speed = 3

    def __init__(self):
        self.rect = self.image.get_rect()
        self.rect.x = (SCR_RECT.width - self.rect.width)/2
        self.rect.y = self.y

        self.original_image = self.image.copy()

    def update(self):  #FIXME
        if self.opaque < 255:
            if self.opaque + self.speed < 255:
                self.opaque += self.speed
            else:
                self.opaque = 255

            self.image = self.original_image.copy()
            set_transparency_to_surf(self.image, self.opaque)

        else:
            self.image = self.original_image


class PushSpaceStart(StringObjectBase):

    y = 500
    text = 'PUSH SPACE KEY'
    color = (255, 255, 255)
    fontsize = 40

    wait = 75

    def __init__(self):
        StringObjectBase.__init__(self)

        self.original_image = self.image.copy()
        self.opaque = 0
        self.speed = 3
        self.min_opaque = 55
        self.max_opaque = 200

        self.frame = 0
        self.blink = False


    def update(self):

        if self.frame < self.wait:

            self.image = self.original_image.copy()
            set_transparency_to_surf(self.image, 0)
            self.frame += 1

        else:
            if not self.blink:
                if self.opaque + self.speed > self.max_opaque:
                    self.blink = True

            else:
                if self.opaque+self.speed < self.min_opaque or self.opaque+self.speed > self.max_opaque:
                    self.speed *= -1

            self.opaque += self.speed
            self.image = self.original_image.copy()
            set_transparency_to_surf(self.image, self.opaque)



