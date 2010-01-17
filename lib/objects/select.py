#!/usr/bin/env python
#-*- coding:utf-8 -*-

import pygame
from pygame.locals import *
import time

from lib.constants  import *
from lib.utils      import set_transparency_to_surf
from base           import *


#########################################################################################
#                     SELECT ANIMATION                                                  #
#########################################################################################


class SelectDraw():

    def __init__(self):
        self.bg_select = BackgroundSelect()
        self.sidebar = SidebarSelect2()                     # FIXME
        self.highlight = HighlightSelect(self.sidebar)

        self.arcade = ArcadeSelect()
        self.level1 = LevelSelect(1)
        self.level2 = LevelSelect(2)
        self.level3 = LevelSelect(3)
        self.level4 = LevelSelect(4)
        self.level5 = LevelSelect(5)
        self.help = HelpSelect()

        self.ef_select = EffectSelect()

        self.objects = [
            self.bg_select,
            self.sidebar,
            self.highlight,
            self.arcade,
            self.level1,
            self.level2,
            self.level3,
            self.level4,
            self.level5,
            self.help,
            self.ef_select
        ]

    def update(self):
        for obj in self.objects:
            obj.update()

    def draw(self, screen):
        screen.fill((0,0,0))
        for obj in self.objects:
            screen.blit(obj.image, (obj.rect.x, obj.rect.y))

    def get_index(self):
        return self.highlight.get_index()


class BackgroundSelect():
    """Select Background"""

    def __init__(self):
        self.rect = self.image.get_rect()

    def update(self):
        pass


class ArcadeSelect(StringObjectBase):

    y = 270
    x = 350
    text = 'ARCADE MODE'
    color = (255, 255, 255)
    fontsize = 80

    def __init__(self):
        StringObjectBase.__init__(self)


class LevelSelect(StringObjectBase):

    y = 350
    x = 350
    text = 'LEVEL {0}'
    color = (255, 255, 255)
    fontsize = 80

    def __init__(self, num):
        self.text = self.text.format(num)
        self.y = self.y + 60*(num-1)
        StringObjectBase.__init__(self)


class HelpSelect(StringObjectBase):

    y = 670
    x = 350
    text = 'HELP'
    color = (255, 255, 255)
    fontsize = 80

    def __init__(self):
        StringObjectBase.__init__(self)


class HighlightSelect():

    entrylist = [(350, 270), (350, 350), (350, 410), (350, 470), (350, 530), (350, 590), (350, 670)]
    
    index = 0
    speed = 10
    frame = 0
    animecycle = 4
    wait = 0.12
    timer = 0
    

    def __init__(self, sidebar):
        self.font = pygame.font.SysFont(None, 80)
        self.font_height = self.font.render('TEXT', True, (64,64,64)).get_height()

        self.blinkimage = pygame.Surface((30, 50))
        self.blinkimage.fill((128,128,128))
        self.original_blinkimage = self.blinkimage.copy()
        self.original_image = self.image.copy()

        self.rect = self.image.get_rect()
        self.rect.x = self.entrylist[0][0]
        self.rect.y = self.entrylist[0][1] - (60-self.font_height)/2

        self.diffx = -60
        self.diffy = -6

        self.sidebar = sidebar

    def update(self):

        if time.time() - self.timer > self.wait:
            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[K_UP] and self.index >= 1:
                self.index -= 1
                self.sidebar.change(self.index, True)
                self.timer = time.time()
            if pressed_keys[K_DOWN] and self.index <= len(self.entrylist)-2:
                self.index += 1
                self.sidebar.change(self.index, False)
                self.timer = time.time()


        self.blinkimage = self.original_blinkimage.copy()
        if self.frame/self.animecycle%2 == 0:
            self.blinkimage.set_alpha(0)
        else:
            self.blinkimage.set_alpha(128)
        self.image = self.original_image.copy()
        self.image.blit(self.blinkimage, (10, 5))
        self.frame += 1

        if (self.rect.x-self.diffx, self.rect.y-self.diffy) != self.entrylist[self.index]: #FIXME
            self.rect.x = self.entrylist[self.index][0] + self.diffx
            self.rect.y = self.entrylist[self.index][1] + self.diffy
            
    def get_index(self):

        return self.index


class SidebarSelect():

    anime = 15
    timer = 0
  
    def __init__(self):

        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.center = (120, SCR_RECT.height/2)

        self.speed = SCR_RECT.height/self.anime

        self.order = []
        for i, image in enumerate(self.images):
            y = 0 if i == 0 else SCR_RECT.height
            self.order.append([image, y, 0])

    def change(self, index, up):
        if up:
            self.order[index+1][2] = self.speed  # add animation
        else:
            self.order[index][2] = -self.speed  # add animation

    def update(self):

        newsurf = pygame.Surface((300, SCR_RECT.height))
        newsurf.fill((0,0,0))

        for i, (image, fpy, fpvy) in enumerate(self.order):

            newsurf.blit(image, (0,int(fpy)))

            if fpvy < 0:
                fpy = max(fpy + fpvy, 0)
                self.order[i][1] = fpy
                if fpy == 0:
                    self.order[i][2] = 0
            elif fpvy > 0:
                fpy = min(fpy + fpvy, SCR_RECT.height)
                self.order[i][1] = fpy
                if fpy == SCR_RECT.height:
                    self.order[i][2] = 0

        self.image = newsurf


class SidebarSelect2(SidebarSelect):
 
    frame = 0

    def __init__(self):
 
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.center = (100, SCR_RECT.height/2)
 
        self.oldindex = 0
        self.newindex = 0
 
        self.starty = SCR_RECT.height
        self.speed = 15
        self.opaque = 0
 
    def change(self, index, up):
        self.oldindex = self.newindex
        self.newindex = index
        self.opaque = 0      
 
    def update(self):
 
        if self.oldindex != self.newindex:
            newsurf = pygame.Surface((300, SCR_RECT.height))
            newsurf.fill((0,0,0))
            newsurf.blit(self.images[self.oldindex], (0,0))
 
            if self.opaque < 255:
                if self.opaque + self.speed <255:
                    self.opaque += self.speed
                else:
                    self.opaque = 255

                dummy = self.images[self.newindex].copy()
                dummy.set_alpha(self.opaque)

                newsurf.blit(dummy, (0, 0))
            elif self.opaque == 255:
                self.oldindex = self.newindex

                newsurf.blit(self.images[self.newindex], (0, 0))
 
            newsurf.blit(self.mask, (0,0)) #FIXME 
            self.image = newsurf
 
        else:
            #self.image = self.images[self.oldindex] #FIXME FIXME
            self.image = self.images[self.oldindex].copy()
            self.image.blit(self.mask, (0,0))


class EffectSelect():
    """Select effects"""

    opaque = 255
    speed = -10

    def __init__(self):
        newsurf = pygame.Surface(SCR_RECT.size)
        newsurf.fill((0,0,0))
        self.original_image = newsurf
        self.image = self.original_image
        self.rect = self.image.get_rect()

    def update(self):
        if self.opaque > 0:
            if self.opaque + self.speed > 0:
                self.opaque += self.speed
            else:
                self.opaque = 0

            self.image = self.original_image.copy()
            self.image.set_alpha(self.opaque)


