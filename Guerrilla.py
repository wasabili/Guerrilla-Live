#!/usr/bin/env python
#-*- coding:utf-8 -*-

import pygame
from pygame.locals import *
import sys
import random
import time

from lib.constants  import *
from lib.utils      import load_image, load_sound, set_transparency_to_surf, init_data
from lib.sprites    import *


class Guerrilla(object):

    def __init__(self):
        # Initialize
        pygame.mixer.pre_init(22050, -16, 2, 2048)
        pygame.mixer.init(22050, -16, True, 2048)
        pygame.init()

        # make a window
        screen = pygame.display.set_mode(SCR_RECT.size, pygame.SRCALPHA, 32)
        pygame.display.set_caption(GAME_TITLE)

        # load contents
        self.load_images()
        self.load_sounds()

        # Initialize Game object
        self.init_game()

        # start mainloop
        clock = pygame.time.Clock()
        while True:
            clock.tick(60)
            self.update()
            self.draw(screen)
            pygame.display.update()
            self.key_handler()


    def init_game(self):
        """Initialize Game object"""

        # state of a game
        self.game_state = START

        # Create sprite groups
        self.overall = pygame.sprite.RenderUpdates()
        self.start_all = pygame.sprite.Group()          # Opening Screen
        self.pre_gameover_all = pygame.sprite.Group()   # GameOver Backgrounds
        self.gameover_all = pygame.sprite.Group()       # GameOver screen
        self.play_all = pygame.sprite.Group()           # Play screen
        self.ecolis = pygame.sprite.Group()             # E.Coli Group
        self.shots = pygame.sprite.Group()              # Beam Group

        # Assign default sprite groups
        EColiOpening.containers = self.overall, self.start_all
        TitleOpening.containers = self.overall, self.start_all
        CreditOpening.containers = self.overall, self.start_all
        PushSpaceOpening.containers = self.overall, self.start_all

        TitleGameover.containers = self.overall, self.gameover_all
        ScoreGameover.containers = self.overall, self.gameover_all
        PushSpaceGameover.containers = self.overall, self.gameover_all
        BackgroundGameover.containers = self.overall, self.pre_gameover_all #FIXME

        Player.containers = self.overall, self.play_all
        EColi.containers = self.overall, self.play_all, self.ecolis
        Shot.containers = self.overall, self.play_all, self.shots
        Explosion.containers = self.overall, self.play_all
        HeartMark.containers = self.overall, self.play_all

        # Playing Animation
        self.player = Player()  # own ship
        self.bg_playing = BackgroundPlaying()  #FIXME

        # Opening Animation
        self.start_animations = [] #FIXME
        self.start_animations += [EColiOpening((30, 500))]
        self.start_animations += [EColiOpening((100, 500))]
        self.start_animations += [EColiOpening((170, 500))]

        TitleOpening() #FIXME
        PushSpaceOpening() #FIXME
        CreditOpening() #FIXME

        # GameOver Animation
        TitleGameover() #FIXME
        ScoreGameover() #FIXME
        PushSpaceGameover() #FIXME
        BackgroundGameover() # FIXME

        # Recycle box
        self.recycled_ecolis = []

        # Init data
        init_data()


    def update(self):
        """Update state of a game"""

        if self.game_state == START:
            self.start_all.update()
        elif self.game_state == PLAY:
            self.play_all.update()
            self.gen_daichokin_randomly()
            self.collision_detection()  # detect collision between E.Coli and shots
        elif self.game_state == GAMEOVER:
            self.pre_gameover_all.update()
            self.gameover_all.update()


    def draw(self, screen):
        """Draw game"""

        if self.game_state == START:                # start
            screen.blit(self.backgrounds[0], (0, 0))   # Background
            self.start_all.draw(screen)

        elif self.game_state == PLAY:       # playing
            screen.fill((0,0,0))
            self.bg_playing.draw(screen)               # Background FIXME
            self.play_all.draw(screen)

        elif self.game_state == GAMEOVER:   # game over
            screen.fill((0,0,0))
            self.pre_gameover_all.draw(screen)         # Background
            self.gameover_all.draw(screen)

        elif self.game_state == GAMEEND:    # moratorium after gameover
            BackgroundGameover.lastgame_image = screen.copy()
            self.game_state = GAMEOVER


    def gen_daichokin_randomly(self):
        """Create E.Colis randomly"""

        freq = 0.15
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

            self.gen_ecoli((x, y))


    def gen_ecoli(self, pos):
        """Recycle killed E.Colis or create newly"""

        if len(self.recycled_ecolis) == 0:
            return EColi(pos)
        else:
            ecoli = self.recycled_ecolis.pop()
            ecoli.init(pos)
            return ecoli

    def recycle_ecoli(self, ecoli):
        """Recycle killed E.Colis"""

        self.recycled_ecolis.append(ecoli)

    def key_handler(self):
        """Handle user event"""

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and event.key == K_e: # FIXME debug
                self.game_state = GAMEEND
            elif event.type == KEYDOWN and event.key == K_SPACE:
                if self.game_state == START:
                    self.game_state = PLAY
                elif self.game_state == GAMEOVER:
                    self.init_game()  # start new game
                    self.game_state = START


    def collision_detection(self):
        """Detect collision"""

        # Between E.Colis and shots
        ecoli_collided = pygame.sprite.groupcollide(self.ecolis, self.shots, True, True)
        for ecoli in ecoli_collided.keys():
            self.recycle_ecoli(ecoli)
            EColi.kill_sound.play()
            Data.score += 10
            Explosion(ecoli.rect.center)  # Draw explosion

        # Between player and E.Colis
        player_collided = pygame.sprite.spritecollide(self.player, self.ecolis, True)
        if player_collided:  # If there is an E.Coli that touched player 
            if not self.player.is_invincible():
                Player.bomb_sound.play()
            if not self.player.killed_once(): # die once
                self.game_state = GAMEEND  # Game Over


    def load_images(self):
        """Load images"""

        # Register images into sprites
        Player.image = load_image("player.png")
        Shot.image = load_image("shot.png")
        EColi.images = load_image("ecolis.png", 3)
        Explosion.images = load_image("explosion.png", 16)
        HeartMark.images = load_image("heart-animation.png", 96)

        # Load background
        self.backgrounds = load_image("backgrounds.jpg", 3)
        BackgroundPlaying.image = self.backgrounds[1]
        BackgroundGameover.image = self.backgrounds[2]


    def load_sounds(self):
        """Load sounds"""

        # Register sounds into sprites
        EColi.kill_sound = load_sound("kill.ogg")
        Player.shot_sound = load_sound("shot.ogg")
        Player.bomb_sound = load_sound("bomb.wav")


if __name__ == "__main__":
    Guerrilla()
