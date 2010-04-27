#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sys

import pygame
from pygame.locals  import *
from gloss.gloss    import *

from lib.constants  import *
from lib.utils      import load_image, load_sound
from lib.objects    import *
from lib.gamedata   import GameData


class Guerrilla(GlossGame):

    def load_content(self):

        """Load images"""
        # Register images into sprites
        Player.images                   = load_image("player.png", 480)
        Shot.shot_image                 = load_image("shot.png")
        EColi.images                    = load_image("ecoli.png", 3)
        EColi2.images                   = load_image("ecoli2.png", 2)
        BigEColi.images                 = load_image("big-ecoli.png", 2)  #FIXME FIXME
        Explosion.images                = load_image("explosion.png", 16)
        HeartMark.images                = load_image("heart-animation.png", 96)
        WeaponPanel.images              = [load_image("weaponpanel"+str(x)+".png") for x in range(1, 4)]
        WeaponSelector.image            = load_image("weapon-selector-arrow.png")
        DisplayWeapon.images            = [load_image("current-weapon"+str(x)+".png") for x in range(1, 5)]

        # Gage
        Gage.image_red                  = load_image("gage-red.png")
        Gage.image_blue                 = load_image("gage-blue.png")
        GageSeparator.image             = load_image("gage-separator.png")


        # Select
        DescriptionSelect.images        = load_image("description.png", 7)  #FIXME
        HighlightSelect.image           = load_image("highlight.png")
        SidebarSelect.images            = [load_image("sidebar"+str(x)+".png").convert() for x in range(1, 8)]

        # Help
        BackgroundHelp.images           = [load_image("help-background"+str(x)+".png").convert() for x in range(10)]
        ContentsHelp.image              = load_image('help-contents.png')

        # Load background
        BackgroundStart.image           = load_image("start.jpg")
        BackgroundSelect.image          = load_image("select.jpg")
        BackgroundPlay.images           = load_image("play.jpg", 5, True)

        # GameOver
        BackgroundGameover.loseimage    = load_image("gameover-lose.jpg")
        BackgroundGameover.winimage     = load_image("gameover-win.jpg")

        # Initialize Game object
        self.game_state = CREDIT
        self.gamedata = GameData()
        self.creditdraw = CreditDraw()
        self.startdraw = StartDraw()
        self.selectdraw = SelectDraw()

        self.on_key_down = self.handle_key_presses


    def init_game(self, first=True):
        """Initialize Game object"""

        # Init data
        self._pending_game_state = None
        self.gamedata = GameData()

        self.selectdraw.init()


    def update(self):
        """Update state of a game"""

        if self.game_state == CREDIT:
            self.creditdraw.update()
            if self.creditdraw.hasfinished():
                self.pendingchangestate(START)

        elif self.game_state == START:
            self.startdraw.update()

        elif self.game_state == SELECT:
            self.selectdraw.update()

        elif self.game_state == PLAY:
            self.playdraw.update()
            if self.playdraw.hasfinished():
                self.gamedata.lastscreen = self._screen.copy()
                self.gameoverdraw = GameoverDraw(self.gamedata)
                self.pendingchangestate(GAMEOVER)

        elif self.game_state == GAMEOVER:
            self.gameoverdraw.update()

        elif self.game_state == HELP:
            #self.selectdraw.update()  #FIXME
            self.helpdraw.update()
            if self.helpdraw.hasclosed():
                self.pendingchangestate(SELECT)


    def draw(self):
        """Draw game"""

        if self.game_state == CREDIT:
            drawer = self.creditdraw

        elif self.game_state == START:          # start
            drawer = self.startdraw

        elif self.game_state == SELECT:         # select
            drawer = self.selectdraw

        elif self.game_state == PLAY:           # play
            drawer = self.playdraw

        elif self.game_state == GAMEOVER:       # game over
            drawer = self.gameoverdraw

        elif self.game_state == HELP:
            drawer = self.helpdraw

        return drawer.draw(screen)


    def handle_key_presses(self, event):
        """Handle user event"""

        if event.type == QUIT or event.key == K_ESCAPE:
            sys.exit()

        elif event.key in (K_SPACE, K_RETURN):

            if self.game_state == START:
                self.pendingchangestate(SELECT)

            elif self.game_state == SELECT:
                index = self.selectdraw.get_index()
                if index == 0:
                    print 'ARCADE MODE is selected'  #FIXME
                elif index in range(1, 6):
                    self.gamedata.initlevel(index)
                    self.playdraw = PlayDraw(self.gamedata)
                    self.pendingchangestate(PLAY)
                elif index == 6:
                    self.helpdraw = HelpDraw()
                    self.pendingchangestate(HELP)

            elif self.game_state == GAMEOVER:
                self.init_game()
                self.pendingchangestate(SELECT)

            elif self.game_state == HELP:
                if not self.helpdraw.whileclosing():
                    self.helpdraw.close()



game = Guerrilla("Guerrilla Live(!)")
Gloss.screen_resolution = SCR_RECT.size
Gloss.full_screen = False
game.run()

