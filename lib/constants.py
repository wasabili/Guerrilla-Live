#!/usr/bin/env python
#-*- coding:utf-8 -*-

from pygame.locals import *

DATA_DIR = 'data'
START, PLAY, GAMEOVER, SELECT, HELP, CREDIT = range(6)  # states of a game
WIDTH = 1024
HEIGHT = 768
SCR_RECT = Rect(0, 0, WIDTH, HEIGHT)
CENTER = (WIDTH/2, HEIGHT/2)
