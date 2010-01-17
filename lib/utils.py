#!/usr/bin/env python
#-*- coding:utf-8 -*-

import pygame
from pygame.locals import *
import os
import sys
import numpy
import time
from collections import deque


def load_image(filename, sprit=None, colorkey=False):
    """画像をロードして画像と矩形を返す"""
    filename = os.path.join("data", filename)
    try:
        image = pygame.image.load(filename)
    except pygame.error, message:
        print "Cannot load image:", filename
        raise SystemExit, message
    if colorkey:
        colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    if sprit is not None:
        return _split_image(image, sprit, colorkey)
    return image

def _split_image(image, n, colorkey=False):
    """横に長いイメージを同じ大きさのn枚のイメージに分割
    分割したイメージを格納したリストを返す"""
    image_list = []
    w = image.get_width()
    h = image.get_height()
    w1 = w / n
    for i in range(0, w, w1):
        surface = pygame.Surface((w1,h), image.get_flags())
        surface.blit(image, (0,0), (i,0,w1,h))
        if colorkey:
            surface.set_colorkey(surface.get_at((0,0)), RLEACCEL)
        image_list.append(surface)
    return image_list

def load_sound(filename):
    """サウンドをロード"""
    filename = os.path.join("data", filename)
    return pygame.mixer.Sound(filename)



def set_transparency_to_surf(image, transparency):
    """make the image background truely transparence"""

    pixels_alpha = pygame.surfarray.pixels_alpha(image)
    pixels_alpha[...] = (pixels_alpha * (transparency / 255.0)).astype(numpy.uint8)
    del pixels_alpha

########################################################################################
#                   Recycle                                                            #
########################################################################################

recycled_ecolis = deque()
recycled_shots = deque()

def get_recycled_ecoli(pos):
    """Recycle killed E.Colis"""

    global recycled_ecolis

    if recycled_ecolis:
        ecoli = recycled_ecolis.pop()
        ecoli.init(pos)
        return ecoli
    else:
        return False


def recycle_ecoli(ecoli):
    """Recycle killed E.Colis"""

    global recycled_ecolis

    recycled_ecolis.append(ecoli)


def get_recycled_shot(start, target):
    """Recycle killed shot"""

    global recycled_shots

    if recycled_shots:
        shot = recycled_shots.pop()
        shot.init(start, target)
        return shot
    else:
        return False


def recycle_shot(shot):
    """Recycle killed Shots"""

    global recycled_shots

    recycled_shots.append(shot)



