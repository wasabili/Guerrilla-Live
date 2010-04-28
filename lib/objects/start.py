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
        # Sprite Group
        self.start_all = BaseGroup()

        # Register groups to sprites
        PushSpaceStart.containers   = self.start_all
        EffectStart.containers      = self.start_all

        # Objects
        self.pushspace  = PushSpaceStart()
        self.effect     = EffectStart()

    def update(self):
        self.start_all.update()

    def draw(self):
        self.start_all.draw()


class BackgroundStart(DirtySprite):
    """Start Background"""

    def __init__(self):
        DirtySprite.__init__(self, self.containers)
        self.rect = self.image.get_rect()


class EffectStart(DirtySprite):
    """Select effects"""

    speed = -1

    def __init__(self):
        DirtySprite.__init__(self, self.containers)

        self.none_image = pygame.Surface((0,0), HWSURFACE)
        self.image = pygame.Surface(SCR_RECT.size, SRCALPHA|HWSURFACE)
        self.image.fill((0,0,0,255))
        self.rect = self.image.get_rect()

        self.opaque = 255

    def update(self):
        if self.opaque > 0:
            self.dirty = 1

            self.image.fill((0,0,0,self.opaque))

            self.opaque += self.speed

        else:
            self.kill()


class PushSpaceStart(StringSpriteBase):

    y = 500
    text = 'PUSH SPACE KEY'
    color = (255, 255, 255)
    fontsize = 40

    wait = 200

    def __init__(self):
        StringSpriteBase.__init__(self)

        self.original_image = self.image.copy()
        self.images = []
        for i in range(256):
            img = self.original_image.copy()
            set_transparency_to_surf(img, i)
            self.images.append(img)
        self.image = pygame.Surface((0,0))
        self.opaque = 0
        self.speed = 3
        self.min_opaque = 55
        self.max_opaque = 200

        self.frame = 0
        self.blink = False


    def update(self):
        self.dirty = 1

        if self.frame < self.wait:

            self.frame += 1

        else:
            if not self.blink and self.opaque + self.speed > self.max_opaque:  # Escape 'Not Blink' state!
                    self.blink = True

            elif self.blink and (self.opaque+self.speed < self.min_opaque or self.opaque+self.speed > self.max_opaque):  # Reverse speed 
                    self.speed *= -1

            self.opaque += self.speed
            #self.image = self.original_image.copy()
            #set_transparency_to_surf(self.image, self.opaque)
            self.image = self.images[self.opaque]



