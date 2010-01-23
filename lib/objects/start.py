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
        self.start_all = pygame.sprite.LayeredDirty()

        # Register groups to sprites
        PushSpaceStart.containers   = self.start_all
        EffectStart.containers      = self.start_all

        # Objects
        self.pushspace  = PushSpaceStart()
        self.effect     = EffectStart()

    def update(self):
        self.start_all.update()

    def draw(self, screen):
        return self.start_all.draw(screen, BackgroundStart2.image)


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


class BackgroundStart2(pygame.sprite.DirtySprite):
    """Start Background"""

    def __init__(self):
        pygame.sprite.DirtySprite.__init__(self, self.containers)
        self.rect = self.image.get_rect()

    def update(self):
        pass


class EffectStart(pygame.sprite.DirtySprite):
    """Select effects"""

    speed = -1

    def __init__(self):
        pygame.sprite.DirtySprite.__init__(self, self.containers)

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
            self.image = self.original_image.copy()
            set_transparency_to_surf(self.image, self.opaque)



