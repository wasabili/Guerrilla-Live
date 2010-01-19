#!/usr/bin/env python
#-*- coding:utf-8 -*-

import pygame
from pygame.locals import *
import sys

from lib.constants  import *
from lib.utils      import load_image, load_sound
from lib.objects    import *


class Guerrilla(object):

    def __init__(self):
        # Initialize
        #pygame.mixer.pre_init(22050, -16, 2, 128)
        pygame.mixer.init(22050, -16, True, 0)
        pygame.init()

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
            if dirty is None:
                pygame.display.flip()
            else:
                pygame.display.update(dirty)
            self.key_handler()
            self.triggerstatechange()


    def init_game(self):
        """Initialize Game object"""

        # Init data
        self._pending_game_state = None
        self.gamedata = GameData()
        self.game_state = START #FIXME FIXME

        # Drawing Objects
        self.creditdraw = CreditDraw()                      # Credit Objects #FIXME destroy when it is not needed
        self.startdraw = StartDraw()                        # Start Objects
        self.selectdraw = SelectDraw()                      # Select Objects


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
                    self.init_game()                            # start new game
                    self.pendingchangestate(START)

                elif self.game_state == HELP:
                    if not self.helpdraw.whileclosing():
                        self.helpdraw.close()


    def playnewgame(self):
        """Something is selected"""

        index = self.selectdraw.get_index()
        if index == 0:
            pass
        elif index == 1:
            self.gamedata.initlevel(1)
            self.playdraw = PlayDraw(self.gamedata)
            self.pendingchangestate(PLAY)
        elif index == 2:
            self.gamedata.initlevel(2)
            self.playdraw = PlayDraw(self.gamedata)
            self.pendingchangestate(PLAY)
        elif index == 3:
            pass
        elif index == 4:
            pass
        elif index == 5:
            pass
        elif index == 6:
            self.helpdraw = HelpDraw()
            self.pendingchangestate(HELP)


    def entergameover(self):
        """prepare to enter gameover screen"""

        self.gamedata.set_lastscreen(self._screen.copy())
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
        Player.images                   = load_image("player3.png", 480)
        Shot.shot_image                 = load_image("shot.png")
        EColi.images                    = load_image("ecoli.png", 3)
        EColi2.image                    = load_image("ecoli2.png")
        BigEColi.image                  = load_image("big-ecoli.png")  #FIXME FIXME
        Explosion.images                = load_image("explosion.png", 16)
        HeartMark.images                = load_image("heart-animation.png", 96)
        Gage.image                      = load_image("gage.png")

        TitleStart.image                = load_image("logo.png")
        DescriptionSelect.images        = load_image("description.png", 7)  #FIXME
        HighlightSelect.image           = load_image("highlight.png")
        SidebarSelect.images            = load_image("sidebar.jpg", 7)  #FIXME
        SidebarSelect2.images           = load_image("sidebar.jpg", 7)

        BackgroundHelp.images           = load_image('help.png', 10)
        ContentsHelp.image              = load_image('help-contents.png')

        # Load background
        BackgroundStart.image           = load_image("start.jpg")
        BackgroundSelect.image          = load_image("select.jpg")
        BackgroundDescription.image     = load_image("description-bg.png")
        BackgroundPlay.images           = load_image("play.jpg", 2)
        BackgroundGameover.loseimage    = load_image("lose.jpg")
        BackgroundGameover.winimage     = load_image("win.jpg")


    def load_sounds(self):
        """Load sounds"""

#        # BGM FIXME
#        pyglet.options['audio'] = ('alsa', 'openal', 'silent')
#        self.mediaplayer = pyglet.media.Player()
#        bgm = pyglet.media.load('data/resident_evil.wav', streaming=False)
#        self.mediaplayer.queue(bgm)
#        self.mediaplayer.play()
#        self.mediaplayer.eos_action = pyglet.media.Player.EOS_LOOP
#        pyglet.app.run()

#        pygame.mixer.music.load('data/resident_evil.wav')
#        pygame.mixer.music.play(-1)

        # Register sounds into sprites
        EColi.kill_sound = load_sound("kill.oga")
        Player.shot_sound = load_sound("shot.oga")
        Player.bomb_sound = load_sound("bomb.oga")


    def debug(self, screen, txt):
        screen.blit(self.font.render('debug: '+txt, False, (255,255,255)), (20,20))



class GameData(object):
    """Manage data while playing"""

    WIN, LOSE = range(2)
    SHOT, SUBSHOT = range(2)

    killed = 0
    bosslimit = sys.maxint
    
    subshot_timelimit = 300

    def __init__(self):
        pass

    def initlevel(self, level):

        self.weapon_mode = self.SHOT

        self.level = level
        self.result = self.LOSE
        self.lastscreen = None
        self.subshot_timer = 0
        self.subshot_counter = 0

        if level == 1:
            self.killed = 0
            self.bosslimit = 450
            self.enemies = [
                (EColi, 0.10, 0.05)
            ]
            self.boss = BigEColi

        if level == 2:
            self.killed = 0
            self.bosslimit = 800
            self.enemies = [
                (EColi, 0.10, 0.03),
                (EColi2, 0.05, 0.01)
            ]
            self.boss = BigEColi #FIXME

    def killed_enemies(self, amount):
        self.killed += amount
        if self.weapon_mode == self.SUBSHOT:
            self.subshot_counter = 0
        else:
            self.subshot_counter += amount

    def get_score(self):    #FIXME
        return self.killed*10

    def is_bosslimit_broken(self):  #FIXME
        return self.killed >= self.bosslimit

    def set_lastscreen(self, surface):
        self.lastscreen = surface

    def get_lastscreen(self):
        return self.lastscreen



def main():
    Guerrilla()

import cProfile as profile
profile.run('main()')

