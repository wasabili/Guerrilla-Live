#!/usr/bin/env python
#-*- coding:utf-8 -*-

import pygame
from pygame.locals import *
import os
import sys
import Numeric

def load_image(filename, sprit=None, autotrans=False, colorkey=None):
    """画像をロードして画像と矩形を返す"""
    filename = os.path.join("data", filename)
    try:
        image = pygame.image.load(filename)
    except pygame.error, message:
        print "Cannot load image:", filename
        raise SystemExit, message
    if autotrans:
        if colorkey is None:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    image.convert_alpha()
    if sprit is not None:
        return _split_image(image, sprit, autotrans)
    return image

def _split_image(image, n, autotrans=False):
    """横に長いイメージを同じ大きさのn枚のイメージに分割
    分割したイメージを格納したリストを返す"""
    image_list = []
    w = image.get_width()
    h = image.get_height()
    w1 = w / n
    for i in range(0, w, w1):
        surface = pygame.Surface((w1,h))
        surface.blit(image, (0,0), (i,0,w1,h))
        if autotrans:
            surface.set_colorkey(surface.get_at((0,0)), RLEACCEL)
        surface.convert_alpha()
        image_list.append(surface)
    return image_list

def load_sound(filename):
    """サウンドをロード"""
    filename = os.path.join("data", filename)
    return pygame.mixer.Sound(filename)


def set_transparency_to_surf(image, transparency):
    """make the image background truely transparence"""

    pixels_alpha = pygame.surfarray.pixels_alpha(image)
    pixels_alpha[...] = (pixels_alpha * (transparency / 255.0)).astype(Numeric.UInt8)
    del pixels_alpha


class GameData(object):
    """Manage data while playing"""

    killed = 0
    bosslimit = sys.maxint
    score = 0

    def __init__(self, level): # FIXME imp level
        self.killed = 0
        self.bosslimit = 300


