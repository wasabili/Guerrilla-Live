#!/usr/bin/env python
#-*- coding:utf-8 -*-

import pygame
from pygame.locals import *
import time

from lib.sprite     import *
from lib.constants  import *
from lib.utils      import set_transparency_to_surf
from base           import *


#########################################################################################
#                     SELECT ANIMATION                                                  #
#########################################################################################


class SelectDraw():

    def __init__(self):
        # Sprite Group
        self.select_all = BaseGroup()

        # Register groups to sprites
        DescriptionSelect.containers        = self.select_all
        SidebarSelect.containers            = self.select_all
        HighlightSelect.containers          = self.select_all
        BlinkerSelect.containers            = self.select_all
        ArcadeSelect.containers             = self.select_all
        LevelSelect.containers              = self.select_all
        HelpSelect.containers               = self.select_all
        EffectSelect.containers             = self.select_all

        # Layer
        BackgroundSelect._layer     = -100
        ArcadeSelect._layer         = 100
        LevelSelect._layer          = 100
        HelpSelect._layer           = 100
        HighlightSelect._layer      = 99
        BlinkerSelect._layer        = 100
        DescriptionSelect._layer    = 150
        SidebarSelect._layer        = 150
        EffectSelect._layer         = 200

        # Objects
        self.description = DescriptionSelect()
        self.sidebar = SidebarSelect()
        self.blinker = BlinkerSelect()
        self.highlight = HighlightSelect(self.blinker, self.description, self.sidebar)

        self.arcade = ArcadeSelect()
        self.level1 = LevelSelect(1)
        self.level2 = LevelSelect(2)
        self.level3 = LevelSelect(3)
        self.level4 = LevelSelect(4)
        self.level5 = LevelSelect(5)
        self.help = HelpSelect()

        self.ef_select = EffectSelect()


    def update(self):
        self.select_all.update()

    def draw(self):
        self.select_all.draw()

    def get_index(self):
        return self.highlight.get_index()

    def init(self):
        self.description.init()
        self.sidebar.init()
        self.blinker.init()
        self.highlight.init()
        self.ef_select = EffectSelect()


class BackgroundSelect(BaseSprite):
    """Select Background"""

    def __init__(self):
        BaseSprite.__init__(self)

    def update(self):
        pass


class ArcadeSelect(BaseSpriteFont):

    y = 270
    x = 350
    text = 'ARCADE MODE'
    color = (255, 255, 255)
    fontsize = 80

    def __init__(self):
        BaseSpriteFont.__init__(self)


class LevelSelect(BaseSpriteFont):

    y = 350
    x = 350
    text = 'LEVEL {0}'
    color = (255, 255, 255)
    fontsize = 80

    def __init__(self, num):
        self.text = self.text.format(num)
        self.y = self.y + 60*(num-1)
        BaseSpriteFont.__init__(self)


class HelpSelect(BaseSpriteFont):

    y = 670
    x = 350
    text = 'HELP'
    color = (255, 255, 255)
    fontsize = 80

    def __init__(self):
        BaseSpriteFont.__init__(self)


class HighlightSelect(BaseSprite):

    entrylist = [(350, 270), (350, 350), (350, 410), (350, 470), (350, 530), (350, 590), (350, 670)]
    diffx = -60
    diffy = -6

    wait = 0.12

    def __init__(self, blinker, description, sidebar):
        BaseSprite.__init__(self)

        self.rect.x = self.entrylist[0][0] + self.diffx
        self.rect.y = self.entrylist[0][1] + self.diffy

        self.blinker = blinker
        self.description = description
        self.sidebar = sidebar

        self.timer = 0
        self.oldindex = 0
        self.index = 0

    def update(self):

        self.key_handler()

        # Move Highlight
        if self.oldindex != self.index:
            self.rect.x = self.entrylist[self.index][0] + self.diffx
            self.rect.y = self.entrylist[self.index][1] + self.diffy
            self.oldindex = self.index
            self.dirty = 1
            
    def key_handler(self):

        if time.clock() - self.timer > self.wait:
            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[K_UP] and self.index >= 1:
                self.index -= 1
                self.blinker.change(self.index, True)
                self.description.change(self.index, True)
                self.sidebar.change(self.index, True)
                self.timer = time.clock()
            if pressed_keys[K_DOWN] and self.index <= len(self.entrylist)-2:
                self.index += 1
                self.blinker.change(self.index, False)
                self.description.change(self.index, False)
                self.sidebar.change(self.index, False)
                self.timer = time.clock() 

    def get_index(self):
        return self.index

    def init(self):
        self.rect.x = self.entrylist[0][0] + self.diffx
        self.rect.y = self.entrylist[0][1] + self.diffy
        self.timer = 0
        self.oldindex = 0
        self.index = 0


class BlinkerSelect(BaseSprite):

    animecycle = 4
    pos = (10, 5)

    def __init__(self):
        # Create images
        self.texture = pygame.Surface((30, 50), SRCALPHA|HWSURFACE)
        self.texture.fill((128,128,128,128))
        BaseSprite.__init__(self)

        self.rect.center = (315, 294)
        self.draw_image = True
        self.frame = 0

    def update(self):

        if self.frame/self.animecycle%2 == 0:
            self.draw_image = True
        else:
            self.draw_image = False
        self.frame += 1

    def draw(self):
        if self.draw_image:
            BaseSprite.draw(self)

    def change(self, index, up):

        corner = HighlightSelect.entrylist[index]
        self.rect.x = corner[0] + HighlightSelect.diffx + self.pos[0]
        self.rect.y = corner[1] + HighlightSelect.diffy + self.pos[1]

    def init(self):
        self.rect.center = (315, 294)
        self.frame = 0


class DescriptionSelect():

    def __init__(self):

        DescriptionPartSelect.containers    = self.containers
        DescriptionPartSelect._layer        = self._layer
        self.parts = []
        self.parts.append(DescriptionPartSelect(self.textures[0], 0))
        self.parts.append(DescriptionPartSelect(self.textures[1], DescriptionPartSelect.xlimit))
        self.parts.append(DescriptionPartSelect(self.textures[2], DescriptionPartSelect.xlimit))
        self.parts.append(DescriptionPartSelect(self.textures[3], DescriptionPartSelect.xlimit))
        self.parts.append(DescriptionPartSelect(self.textures[4], DescriptionPartSelect.xlimit))
        self.parts.append(DescriptionPartSelect(self.textures[5], DescriptionPartSelect.xlimit))
        self.parts.append(DescriptionPartSelect(self.textures[6], DescriptionPartSelect.xlimit))

    def change(self, index, up):
        if up:
            self.parts[index+1].change_speed(1) # add animation
            self.parts[index].change_speed(-1)  # add animation
        else:
            self.parts[index-1].change_speed(1) # add animation
            self.parts[index].change_speed(-1)  # add animation

    def init(self):
        self.parts[0].init(0)
        for i in range(1, 7):
            self.parts[i].init(DescriptionPartSelect.xlimit)


class DescriptionPartSelect(BaseSprite):

    anime = 15
    xstart = 290
    xlimit = 800
    speed = xlimit/anime

    def __init__(self, texture, x):
        self.texture = texture
        BaseSprite.__init__(self)

        self.rect.x = self.xstart
        self.rect.y = 35

        self.x = x
        self.vx = 0

    def change_speed(self, direction):
        self.vx = direction*self.speed

    def update(self):

        self.rect.x = self.xstart + self.x

        if self.vx != 0:
            self.dirty = 1

            n = self.x + self.vx
            if n < 0:
                self.x = 0
                self.vx = 0
            elif n > self.xlimit:
                self.x = self.xlimit
                self.vx = 0
            else:
                self.x = n

    def init(self, x):
        self.rect.x = self.xstart
        self.x = x
        self.vx = 0


class SidebarSelect(BaseSprite):
 
    speed = 5
    frames = int(255/speed)

    def __init__(self):
        BaseSprite.__init__(self)
 
        self.rect.topleft = (-50, 0)
 
        self.index = 0
        self.remains = 0
        self.up = False 

        self.sub_images = []
        for i, image in enumerate(self.images):
            for j in range(self.frames):
                tmp = image.copy()
                tmp.set_alpha(j*self.speed)
                self.sub_images += [tmp]

    def change(self, index, up):
        self.up = up
        self.index = index
        self.remains = self.frames
 
    def update(self):
 
        if self.remains > 0 and not self.up:              # Animation has not finished
            self.ditry = 1

            i = self.frames-self.remains
            j = self.index*self.frames+i
            image = self.sub_images[j]
            self.image.blit(image, (0,0))

            self.remains -= 1

        elif self.remains > 0 and self.up:
            self.ditry = 1

            i = self.frames-self.remains
            j = self.index*self.frames+i
            image = self.sub_images[j]
            self.image.blit(image, (0,0))

            self.remains -= 1

        elif self.remains == 0:
            self.dirty = 1

            self.remains -= 1
            self.image = self.images[self.index].copy()

    def init(self):
        self.image = self.images[0].copy().convert_alpha()
        self.index = 0
        self.remains = 0
        self.up = False


class EffectSelect(DirtySprite):
    """Select effects"""

    speed = -10

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

            if self.opaque + self.speed > 0:
                self.opaque += self.speed
            else:
                self.image = self.none_image
                self.rect = Rect(0,0,0,0)
                self.opaque = 0
                self.dirty = 0


