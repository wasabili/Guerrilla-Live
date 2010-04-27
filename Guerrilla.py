#!/usr/bin/env python
#-*- coding:utf-8 -*-

import pygame
from pygame.locals import *
import sys

from lib.constants  import *
from lib.utils      import load_image, load_sound
from lib.objects    import *
from lib.gamedata   import GameData


class Guerrilla(object):

    def __init__(self):

        # make a window
        self.fullscreen = False
        self._screen = pygame.display.set_mode(SCR_RECT.size, SRCALPHA|DOUBLEBUF|HWSURFACE)
        pygame.display.set_caption(GAME_TITLE)

        # load contents
        self.load_images()
        self.load_sounds()

        # Initialize Game object
        self.init_game()

        self.font = pygame.font.SysFont(None, 40) #FIXME

        # start mainloop
        clock = pygame.time.Clock()
        while True:
            clock.tick(60)
            self.update()
            dirty = self.draw(self._screen)
            self.debug(self._screen, str(clock.get_fps()))  #FIXME
            pygame.display.update(dirty)
            self.key_handler()
            self.triggerstatechange()


    def init_game(self, first=True):
        """Initialize Game object"""

        # Init data
        self._pending_game_state = None
        self.gamedata = GameData()

        # Drawing Objects
        if first:
            self.game_state = SELECT #FIXME FIXME
            self.creditdraw = CreditDraw()                      # Credit Objects #FIXME destroy when it is not needed
            self.startdraw = StartDraw()                        # Start Objects
            self.selectdraw = SelectDraw()                      # Select Objects
        else:
            self.game_state = SELECT
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
                self.entergameover()

        elif self.game_state == GAMEOVER:
            self.gameoverdraw.update()

        elif self.game_state == HELP:
            #self.selectdraw.update()  #FIXME
            self.helpdraw.update()
            if self.helpdraw.hasclosed():
                self.pendingchangestate(SELECT)


    def draw(self, screen):
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


    def key_handler(self):
        """Handle user event"""

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == KEYDOWN and event.key == K_ESCAPE:   # Hit Escape
                pygame.quit()
                sys.exit()

            elif event.type == KEYDOWN and event.key == K_F2:       # Fullscreen
                self.togglefullscreen()

            elif event.type == KEYDOWN and event.key in (K_SPACE, K_RETURN):    # Hit Space

                if self.game_state == START:
                    self.pendingchangestate(SELECT)

                elif self.game_state == SELECT:
                    self.playnewgame()

                elif self.game_state == GAMEOVER:
                    self.init_game(first=False)                            # start new game

                elif self.game_state == HELP:
                    if not self.helpdraw.whileclosing():
                        self.helpdraw.close()


    def playnewgame(self):
        """Something is selected"""

        index = self.selectdraw.get_index()
        if index == 0:
            print 'ARCADE MODE is selected'  #FIXME
        elif index == 1:
            self.gamedata.initlevel(1)
            self.playdraw = PlayDraw(self.gamedata)
            self.pendingchangestate(PLAY)
        elif index == 2:
            self.gamedata.initlevel(2)
            self.playdraw = PlayDraw(self.gamedata)
            self.pendingchangestate(PLAY)
        elif index == 3:
            self.gamedata.initlevel(3)
            self.playdraw = PlayDraw(self.gamedata)
            self.pendingchangestate(PLAY)
        elif index == 4:
            self.gamedata.initlevel(4)
            self.playdraw = PlayDraw(self.gamedata)
            self.pendingchangestate(PLAY)
        elif index == 5:
            self.gamedata.initlevel(5)
            self.playdraw = PlayDraw(self.gamedata)
            self.pendingchangestate(PLAY)
        elif index == 6:
            self.helpdraw = HelpDraw()
            self.pendingchangestate(HELP)


    def entergameover(self):
        """prepare to enter gameover screen"""

        self.gamedata.lastscreen = self._screen.copy()
        self.gameoverdraw = GameoverDraw(self.gamedata)
        self.pendingchangestate(GAMEOVER)


    def pendingchangestate(self, state):
        self._pending_game_state = state

    def triggerstatechange(self):
        if self._pending_game_state is None:
            return
        else:
            self.game_state = self._pending_game_state
            self._pending_game_state = None


    def togglefullscreen(self):
        """Switch Fullscreen or not"""

        if self.fullscreen:
            self._screen = pygame.display.set_mode(SCR_RECT.size, SRCALPHA|DOUBLEBUF|HWSURFACE)
        else:
            self._screen = pygame.display.set_mode(SCR_RECT.size, SRCALPHA|DOUBLEBUF|HWSURFACE|FULLSCREEN)

        self.fullscreen = not self.fullscreen


    def load_images(self):
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


    def debug(self, screen, txt):
        screen.blit(self.font.render('debug: '+txt, False, (255,255,255)), (20,30))



def main():
    Guerrilla()

#import cProfile as profile TODO remove these
#profile.run('main()')
main()
