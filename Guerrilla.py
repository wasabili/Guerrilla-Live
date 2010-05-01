#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
import sys

import pygame
from pygame.locals  import *

from lib.constants  import *
from lib.objects    import *
from lib.gamedata   import GameData

from gloss          import GlossGame, Gloss, Texture

#gloss.enable_multisampling = True #TODO
os.environ['SDL_VIDEO_CENTERED'] = '1'
os.environ['SDL_AUDIODRIVER'] = 'esd'

class Guerrilla(GlossGame):

    def load_content(self):

        def load_image(filename, split=None):
            if split is None:
                return Texture(os.path.join("data", filename))
            else:
                image_list = []
                image = pygame.image.load(os.path.join("data", filename))
                w = image.get_width()
                h = image.get_height()
                for i in range(0, w, w/split):
                    surface = pygame.Surface((w/split,h), image.get_flags())
                    surface.blit(image, (0,0), (i,0,w/split,h))
                    image_list.append(Texture(surface))
                return image_list

        """Load images"""
        # Register images into sprites
        Player.textures                     = load_image("player.png", 480)
        Shot.texture                        = load_image("shot.png")
        EColi.textures                      = load_image("ecoli.png", 3)
        EColi2.textures                     = load_image("ecoli2.png", 2)
        BigEColi.textures                   = load_image("big-ecoli.png", 2)  #FIXME FIXME
        Explosion.textures                  = load_image("explosion.png", 16)
        HeartMark.textures                  = load_image("heart-animation.png", 96)
        WeaponPanel.textures                = [load_image("weaponpanel"+str(x)+".png") for x in range(1, 4)]
        WeaponSelector.texture              = load_image("weapon-selector-arrow.png")
        DisplayWeapon.textures              = [load_image("current-weapon"+str(x)+".png") for x in range(1, 5)]
        Gage.texture_red                    = load_image("gage-red.png")
        Gage.texture_blue                   = load_image("gage-blue.png")
        GageSeparator.texture               = load_image("gage-separator.png")


        # Select
        DescriptionSelect.textures          = load_image("description.png", 7)  #FIXME
        HighlightSelect.texture             = load_image("highlight.png")
        SidebarSelect.textures              = [load_image("sidebar"+str(x)+".png") for x in range(1, 8)]

        # Help
        BackgroundHelp.textures           = [load_image("help-background"+str(x)+".png") for x in range(10)]
        ContentsHelp.texture              = load_image('help-contents.png')

        # Load background
        BackgroundSelect.texture          = load_image("select.jpg")
        BackgroundPlay.textures           = load_image("play.jpg", 5)

        # GameOver
        BackgroundGameover.losetexture    = load_image("gameover-lose.jpg")
        BackgroundGameover.wintexture     = load_image("gameover-win.jpg")

        # init game
        self.selectdraw = SelectDraw()
        self.init_game()

        self.on_key_down = self.handle_key_presses


    def init_game(self):
        """Initialize Game object"""

        # Init data
        self.gamedata = GameData()
        self.selectdraw.init()
        self.game_state = SELECT


    def update(self):
        """Update state of a game"""

        print Gloss.elapsed_seconds #TODO

        if self.game_state == SELECT:
            self.selectdraw.update()

        elif self.game_state == PLAY:
            self.playdraw.update()
            if self.playdraw.hasfinished():
                self.gamedata.lastscreen = self._screen.copy()
                self.gameoverdraw = GameoverDraw(self.gamedata)
                self.game_state = GAMEOVER

        elif self.game_state == GAMEOVER:
            self.gameoverdraw.update()

        elif self.game_state == HELP:
            #self.selectdraw.update()  #TODO
            self.helpdraw.update()
            if self.helpdraw.hasclosed():
                self.game_state = SELECT


    def draw(self):
        """Draw game"""

        gloss.Gloss.clear(gloss.Color.BLACK)

        if self.game_state == SELECT:         # select
            drawer = self.selectdraw

        elif self.game_state == PLAY:           # play
            drawer = self.playdraw

        elif self.game_state == GAMEOVER:       # game over
            drawer = self.gameoverdraw

        elif self.game_state == HELP:
            drawer = self.helpdraw

        drawer.draw()


    def handle_key_presses(self, event):
        """Handle user event"""

        if event.type == QUIT or event.key == K_ESCAPE:
            sys.exit()

        elif event.key in (K_SPACE, K_RETURN):

            if self.game_state == SELECT:
                index = self.selectdraw.get_index()
                if index == 0:
                    print 'ARCADE MODE is selected'  #TODO
                elif index in range(1, 6):
                    self.gamedata.initlevel(index)
                    self.playdraw = PlayDraw(self.gamedata)
                    self.game_state = PLAY
                elif index == 6:
                    self.helpdraw = HelpDraw()
                    self.game_state = HELP

            elif self.game_state == GAMEOVER:
                self.init_game()

            elif self.game_state == HELP:
                if not self.helpdraw.whileclosing():
                    self.helpdraw.close()



game = Guerrilla("Guerrilla Live(!)")
Gloss.screen_resolution = 1024, 768
Gloss.full_screen = False
game.run()

