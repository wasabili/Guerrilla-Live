#!/usr/bin/env python
#-*- coding:utf-8 -*-

import pygame
from pygame.locals import *
import sys
import random
import time

from lib.constants  import *
from lib.utils      import load_image, load_sound, set_transparency_to_surf, GameData, recycle_ecoli, get_recycled_ecoli
from lib.sprites    import *


class Guerrilla(object):

    def __init__(self):
        # Initialize
        pygame.mixer.pre_init(22050, -16, 2, 256)
        pygame.mixer.init(22050, -16, True, 256)
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
            self.draw(self._screen)
            self.debug(self._screen, str(clock.get_fps()))  #FIXME
            pygame.display.update()
            self.key_handler()
            self.triggerstatechange()


    def init_game(self):
        """Initialize Game object"""

        # Init data
        self._pending_game_state = None
        self.gamedata = GameData()
        self.game_state = CREDIT

        # Create sprite groups
        self.overall = pygame.sprite.RenderUpdates()
        self.play_all = pygame.sprite.Group()           # Play screen
        self.ecolis = pygame.sprite.Group()             # E.Coli Group
        self.shots = pygame.sprite.Group()              # Beam Group
        self.bosses = pygame.sprite.Group()             # Bosses Group

        # Assign default sprite groups
        Player.containers = self.overall, self.play_all
        EColi.containers = self.overall, self.play_all, self.ecolis
        BigEColi.containers = self.overall, self.play_all, self.bosses
        Shot.containers = self.overall, self.play_all, self.shots
        Explosion.containers = self.overall, self.play_all
        HeartMark.containers = self.overall, self.play_all


        # Drawing Objects
        self.creditdraw = CreditDraw()                      # Credit Objects #FIXME destroy when it is not needed
        self.startdraw = StartDraw()                        # Start Objects
        self.selectdraw = SelectDraw()                      # Select Objects

        self.player = Player()  # own ship
        self.bg_playing = BackgroundPlaying()  #FIXME

        self.gameoverdraw = GameoverDraw(self.gamedata)     # GameOver Objects


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
            self.play_all.update()
            self.gen_ecoli_randomly(self.gamedata.freq)  #FIXME
            self.collision_detection()  # detect collision
            self.bosslimitbroke() and self.enterbossbattle() # FIXME

        elif self.game_state == PLAYBOSS:
            self.play_all.update()
            self.collision_detection()

        elif self.game_state == GAMEOVER:
            self.gameoverdraw.update()

        elif self.game_state == HELP:
            if self.helpdraw.hasclosed():
                self.pendingchangestate(SELECT)
            self.helpdraw.update()


    def draw(self, screen):
        """Draw game"""

        if self.game_state == CREDIT:
            self.creditdraw.draw(screen)

        elif self.game_state == START:          # start
            self.startdraw.draw(screen)

        elif self.game_state == SELECT:         # select
            self.selectdraw.draw(screen)

        elif self.game_state == PLAY:           # playing
            self.bg_playing.draw(screen)            # Background
            self.play_all.draw(screen)

        elif self.game_state == PLAYBOSS:
            self.bg_playing.draw(screen)
            self.play_all.draw(screen)

        elif self.game_state == GAMEOVER:   # game over
            self.gameoverdraw.draw(screen)

        elif self.game_state == HELP:
            self.helpdraw.draw(screen)

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

            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_RETURN):    # Hit Space

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


    def collision_detection(self):
        """Detect collision"""

        # Between E.Colis and shots
        ecoli_collided = pygame.sprite.groupcollide(self.ecolis, self.shots, True, True)
        for ecoli in ecoli_collided.keys():
            recycle_ecoli(ecoli)
            #EColi.kill_sound.play() #FIXME
            self.gamedata.killed += 1
            Explosion(ecoli.rect.center)  # Draw explosion

        # Between player and E.Colis
        player_collided = pygame.sprite.spritecollide(self.player, self.ecolis, True)
        if player_collided:  # If there is an E.Coli that touched player 
            if not self.player.is_invincible():
                #Player.bomb_sound.play()  #FIXME
                pass
            if not self.player.killed_once(): # die once
                self.entergameover(False)  # Game Over


        if self.game_state == PLAYBOSS:

            # Between Boss and shots
            shot_collided = pygame.sprite.spritecollide(self.boss, self.shots, True)
            for shot in shot_collided:
                #BigEColi.hit_sound.play() FIXME
                Explosion(shot.rect.center)  # Draw explosion
                if not self.boss.hit_once():
                    self.entergameover(True)
        
            # Between player and Boss
            player_collided = pygame.sprite.spritecollide(self.player, self.bosses, False)
            if player_collided:  # If there is an E.Coli that touched player 
                if not self.player.is_invincible():
                    #Player.bomb_sound.play() #FIXME
                    pass
                if not self.player.killed_once(): # die once
                    self.entergameover(False)  # Game Over


    def playnewgame(self):
        """Something is selected"""

        index = self.selectdraw.get_index()
        if index == 0:
            self.gamedata.initlevel(0, BigEColi)
            self.pendingchangestate(PLAY)
        if index == 6:
            self.helpdraw = HelpDraw()
            self.pendingchangestate(HELP)

    def entergameover(self, win=False):
        self.gamedata.resule = GameData.WIN if win else GameData.LOSE
        ScoreGameover.score = self.gamedata.get_score()
        BackgroundGameover.lastgame_image = self._screen.copy()
        self.pendingchangestate(GAMEOVER)

    def pendingchangestate(self, state):
        self._pending_game_state = state

    def triggerstatechange(self):
        if self._pending_game_state is None:
            return
        else:
            self.game_state = self._pending_game_state
            self._pending_game_state = None

    def gen_ecoli_randomly(self, freq):
        """Create E.Colis randomly"""

        if int(random.random()*(1/freq)) == 0:
            pos = random.random()*(WIDTH+HEIGHT)*2
            if pos < WIDTH:
                x = pos
                y = 0
            elif pos < WIDTH+HEIGHT:
                x = WIDTH
                y = pos - x
            elif pos < WIDTH*2+HEIGHT:
                x = pos - (WIDTH+HEIGHT)
                y = HEIGHT
            else:
                x = 0
                y = pos - (WIDTH*2+HEIGHT)

            get_recycled_ecoli((x, y)) or EColi((x,y))


    def bosslimitbroke(self):
        """Whether a player killed enough E.Colis to enter Boss Battle"""

        return self.gamedata.killed >= self.gamedata.bosslimit


    def enterbossbattle(self):
        """Enter boss battle"""

        self.boss = self.gamedata.boss()
        self.pendingchangestate(PLAYBOSS)


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
        Player.images = load_image("player.png", 100, autotrans=True)
        Shot.shot_image = load_image("shot.png")
        EColi.images = load_image("ecolis.png", 3, autotrans=True)
        BigEColi.image = load_image("big-ecoli.png")  #FIXME FIXME
        Explosion.images = load_image("explosion.png", 16, autotrans=True)
        HeartMark.images = load_image("heart-animation.png", 96, autotrans=True)

        TitleOpening.image = load_image("logo.png")
        HighlightSelect.image = load_image("highlight.png")
        SidebarSelect.images = load_image("sidebar.png", 7)
        SidebarSelect.mask = load_image("mask.png")  # FIXME FIXME

        BackgroundHelp.images = load_image('help.png', 10)
        ContentsHelp.image = load_image('help-contents.png')

        # Load background
        BackgroundStart.image = load_image("start.jpg")
        BackgroundSelect.image = load_image("select.jpg")
        BackgroundPlaying.image = load_image("play.jpg")
        BackgroundGameover.loseimage = load_image("lose.jpg")
        BackgroundGameover.winimage = load_image("win.png")


    def load_sounds(self):
        """Load sounds"""

        # Register sounds into sprites
        EColi.kill_sound = load_sound("kill.oga")
        Player.shot_sound = load_sound("shot.oga")
        Player.bomb_sound = load_sound("bomb.oga")


    def debug(self, screen, txt):
        screen.blit(self.font.render('debug: '+txt, False, (255,255,255)), (20,20))


if __name__ == "__main__":
    Guerrilla()
