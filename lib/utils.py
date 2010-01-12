#!/usr/bin/env python
#-*- coding:utf-8 -*-

import pygame
from pygame.locals import *
import os
import Numeric

def load_image(filename, sprit=None, colorkey=None):
    """画像をロードして画像と矩形を返す"""
    filename = os.path.join("data", filename)
    try:
        image = pygame.image.load(filename)
    except pygame.error, message:
        print "Cannot load image:", filename
        raise SystemExit, message
    image = image.convert_alpha()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    if sprit is not None:
        return _split_image(image, sprit)
    return image

def _split_image(image, n):
    """横に長いイメージを同じ大きさのn枚のイメージに分割
    分割したイメージを格納したリストを返す"""
    image_list = []
    w = image.get_width()
    h = image.get_height()
    w1 = w / n
    for i in range(0, w, w1):
        surface = pygame.Surface((w1,h))
        surface.blit(image, (0,0), (i,0,w1,h))
        surface.set_colorkey(surface.get_at((0,0)), RLEACCEL)
        surface.convert()
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


def init_data():
    Data.score = 0
    Data.player_pos = (0, 0)

class Data(object):
    """Manage data while playing"""

    score = 0
    player_pos = (0, 0)


