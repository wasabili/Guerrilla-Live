#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from lib.objects    import *

class GameData(object):
    """Manage data while playing"""

    WIN, LOSE = range(2)
    SHOT, SUBSHOT, MACHINEGUN, BOMB = range(4)

    killed = 0
    bosslimit = sys.maxint
    
    gage_limit = 300

    def __init__(self):
        pass

    def initlevel(self, level):

        self.weapon_mode = self.SHOT

        self.level = level
        self.result = self.LOSE
        self.lastscreen = None

        self.subweapon_counter = 0
        self.subweapon_limiter = 0
 

        if level == 1:
            self.killed = 0
            self.bosslimit = 250
            self.enemies = [
                (EColi, 0.075, 0.02)
            ]
            self.boss = BigEColi

        elif level == 2:
            self.killed = 0
            self.bosslimit = 350
            self.enemies = [
                (EColi, 0.15, 0.04)
            ]
            self.boss = BigEColi

        elif level == 3:
            self.killed = 0
            self.bosslimit = 400
            self.enemies = [
                (EColi, 0.10, 0.05),
                (EColi2, 0.02, 0.005)
            ]
            self.boss = BigEColi

        elif level == 4:
            self.killed = 0
            self.bosslimit = 500
            self.enemies = [
                (EColi, 0.15, 0.075)
            ]
            self.boss = BigEColi

        elif level == 5:
            self.killed = 0
            self.bosslimit = 800
            self.enemies = [
                (EColi, 0.075, 0.03),
                (EColi2, 0.05, 0.01)
            ]
            self.boss = BigEColi


    def win(self):
        return self.result == self.WIN

    def killed_enemies(self, amount):
        self.killed += amount
        if self.weapon_mode == self.SHOT:
            self.subweapon_counter = min(self.subweapon_counter+amount, self.gage_limit)

    def getscore(self):    #FIXME
        return self.killed*10

    def is_bosslimit_broken(self):  #FIXME
        return self.killed >= self.bosslimit



