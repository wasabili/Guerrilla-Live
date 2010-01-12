#!/usr/bin/env python
#-*- coding:utf-8 -*-

import pygame
from pygame.locals import *
import math

from constants import *
from utils     import Data, set_transparency_to_surf


class StringBaseSprite(pygame.sprite.Sprite):

    y = 0           # abstract
    fontfamily = None   # abstract
    fontsize = 0    # abstract
    text = ''       # abstract
    color = (0,0,0) # abstract

    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)

        self.font = pygame.font.SysFont(self.fontfamily, self.fontsize)
        self.image = self.font.render(self.text, True, self.color)

        self.rect = self.image.get_rect()
        self.rect.x = (SCR_RECT.width-self.image.get_width())/2
        self.rect.y = self.y



#########################################################################################
#                     PLAYING ANIMATION                                                 #
#########################################################################################


class BackgroundPlaying(pygame.sprite.Sprite):
    """Background follows player's move"""

    mag = 0.3

    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)

        magged_size = (int(SCR_RECT.width*(1+self.mag)), int(SCR_RECT.height*(1+self.mag)))
        #self.image = pygame.transform.chop(self.image, Rect(0, SCR_RECT.bottom, SCR_RECT.width, SCR_RECT.height-self.image.get_height()))
        print 'test'
        self.image = pygame.transform.scale(self.image, (magged_size[0], int(magged_size[1]*(1024.0/770))))

        self.x = -magged_size[0]*(self.mag/(1+self.mag))/2.0
        self.y = -magged_size[1]*(self.mag/(1+self.mag))/2.0

        self.rect = self.image.get_rect()
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def update(self):
        pos = Data.player_pos
        start = SCR_RECT.center

        self.rect.x = self.x + (start[0] - pos[0])*self.mag
        self.rect.y = self.y + (start[1] - pos[1])*self.mag


class Player(pygame.sprite.Sprite):
    """Own ship"""

    accel = 0.05
    reload_time = 5
    lives = 3

    hearts = []
    invincible = -1
    blink_interval = 10
    frame = 0L

    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.rect = self.image.get_rect()
        self.rect = Rect(0, 0, self.rect.width*1/4, self.rect.height*1/4)  #FIXME TEST
        self.rect.center = CENTER

        self.hearts = [HeartMark((30+60*x, SCR_RECT.height-30)) for x in range(self.lives)]

        self.fpx = float(self.rect.x)
        self.fpy = float(self.rect.y)
        self.fpvx = 0
        self.fpvy = 0

        self.reload_timer = 0

    def killed_once(self):
        """A player is killed once"""

        if self.is_invincible():  # Already being invincible
            return True

        self.lives -= 1
        if self.lives < 0:        # remains no life
            return False
        else:
            self.hearts.pop().kill()                 # remove one heart
            self.original_image = self.image.copy()  # for blinking
            self.invincible = 300                    # invincible time
            return True

    def is_invincible(self):
        return self.invincible >= 0

    def update(self):

        if self.invincible > 0:
            self.invincible -= 1
            self.frame += 1
            self.image = self.original_image.copy()
            if (self.frame/self.blink_interval)%2 == 0:
                set_transparency_to_surf(self.image, 64)
            else:
                set_transparency_to_surf(self.image, 255)
        elif self.invincible == 0:
            self.invincible -= 1
            self.image = self.original_image

        # Accel player
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_LEFT] or pressed_keys[K_a]:
            self.fpvx -= self.accel
        if pressed_keys[K_RIGHT] or pressed_keys[K_d]:
            self.fpvx += self.accel
        if pressed_keys[K_UP] or pressed_keys[K_w]:
            self.fpvy -= self.accel
        if pressed_keys[K_DOWN] or pressed_keys[K_s]:
            self.fpvy += self.accel

        # Restrict player position inside SCR_RECT
        if SCR_RECT.right <= self.rect.right and self.fpvx > 0:
            self.fpvx = 0
        if SCR_RECT.left >= self.rect.left and self.fpvx < 0:
            self.fpvx = 0
        if SCR_RECT.top >= self.rect.top and self.fpvy < 0:
            self.fpvy = 0
        if SCR_RECT.bottom <= self.rect.bottom and self.fpvy > 0:
            self.fpvy = 0

        self.fpx += self.fpvx
        self.fpy += self.fpvy
        self.rect.x = int(self.fpx)
        self.rect.y = int(self.fpy)
        self.rect.clamp_ip(SCR_RECT)        

        Data.player_pos = self.rect.center

        # Shoot a shot
        mouse_pressed = pygame.mouse.get_pressed()
        if mouse_pressed[0]:
            if self.reload_timer > 0:  # Unable to shoot while reloading
                self.reload_timer -= 1
            else:
                # Shoot
                Player.shot_sound.play()
                x, y = pygame.mouse.get_pos()
                Shot(self.rect.center, (x,y))
                self.reload_timer = self.reload_time


class Shot(pygame.sprite.Sprite):
    """プレイヤーが発射するビーム"""

    speed = 9  # 移動速度

    def __init__(self, start, target):
        pygame.sprite.Sprite.__init__(self, self.containers)

        self.rect = self.image.get_rect()
        self.rect.center = start

        # Calculate radian to the target
        self.direction = math.atan2(target[1]-start[1], target[0]-start[0])
        # Calculate position and speed
        self.fpx = float(self.rect.x)
        self.fpy = float(self.rect.y)
        self.fpvx = math.cos(self.direction) * self.speed
        self.fpvy = math.sin(self.direction) * self.speed

    def update(self):
        # Move
        self.fpx += self.fpvx
        self.fpy += self.fpvy
        self.rect.x = int(self.fpx)
        self.rect.y = int(self.fpy)

        # 画面外に出たらオブジェクトを破棄
        if not SCR_RECT.contains(self.rect):
            self.kill()


class EColi(pygame.sprite.Sprite):
    """E.Coli"""

    speed = 1.2  # 移動速度
    animecycle = 18  # アニメーション速度
    frame = 0

    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self, self.containers)

        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.center = pos

        self.target = Data.player_pos
        self.start = pos

        # 終点の角度を計算
        self.direction = math.atan2(float(self.target[1]-self.start[1]), float(self.target[0]-self.start[0]))

        # 速度を計算
        self.fpx = float(self.rect.x)
        self.fpy = float(self.rect.y)
        self.fpvx = math.cos(self.direction) * self.speed
        self.fpvy = math.sin(self.direction) * self.speed

    def init(self, pos):
        frame = 0
        # set pos
        self.rect.center = pos
        self.rect.clamp_ip(SCR_RECT)
        self.fpx = float(self.rect.x)
        self.fpy = float(self.rect.y)
        self.add(self.containers)

    def update(self):

        # キャラクターアニメーション
        self.frame += 1
        self.image = self.images[self.frame/self.animecycle%2]

        # 終点の角度を計算
        self.target = Data.player_pos
        self.start = self.rect.center
        self.direction = math.atan2(float(self.target[1]-self.start[1]), float(self.target[0]-self.start[0]))

        # rotate
        self.image = pygame.transform.rotate(self.image, -180*self.direction/math.pi)

        # Move
        self.fpvx = math.cos(self.direction) * self.speed
        self.fpvy = math.sin(self.direction) * self.speed
        self.fpx += self.fpvx
        self.fpy += self.fpvy
        self.rect.x = int(self.fpx)
        self.rect.y = int(self.fpy)


class HeartMark(pygame.sprite.Sprite):
    """Life remains"""

    animecycle = 1
    frame = 0

    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self, self.containers)

        self.image = self.images[0]

        self.rect = self.image.get_rect()
        self.rect.center = pos

        self.max_frame = len(self.images) * self.animecycle  # a frame to disappear

    def update(self):
        # Character Animation
        self.image = self.images[self.frame/self.animecycle]
        self.frame += 1
        if self.frame == self.max_frame:
            self.frame = 0


class Explosion(pygame.sprite.Sprite):
    """Explosion effect"""

    animecycle = 2  # アニメーション速度
    frame = 0L

    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self, self.containers)

        self.image = self.images[0]

        self.rect = self.image.get_rect()
        self.rect.center = pos

        self.max_frame = len(self.images) * self.animecycle  # a frame to disappear

    def update(self):
        # Character Animation
        self.image = self.images[self.frame/self.animecycle]
        self.frame += 1
        if self.frame == self.max_frame:
            self.kill()  # disappear


#########################################################################################
#                     OPENING ANIMATION                                                 #
#########################################################################################


class EColiOpening(EColi):
    """Opening Animation"""

    speed = 1.5

    def __init__(self, pos):
        EColi.__init__(self, pos)
        self.fpvx = self.speed
        self.fpvy = 0

    def update(self):
        # Character Animation
        self.frame += 1
        self.image = self.images[self.frame/self.animecycle%2]

        # Move
        self.fpx += self.fpvx
        self.fpy += self.fpvy
        self.rect.x = int(self.fpx)
        self.rect.y = int(self.fpy)

        # loop, loop, loop
        if SCR_RECT.right < self.rect.left:
            self.fpx = -200



class TitleOpening(StringBaseSprite):

    y = 100
    text = 'Guerrilla Live(!)'
    color = (255, 0, 0)
    fontsize = 80

    def __init__(self):
        StringBaseSprite.__init__(self)

class PushSpaceOpening(StringBaseSprite):

    y = 300
    text = 'PUSH SPACE KEY'
    color = (255, 255, 255)
    fontsize = 40

    def __init__(self):
        StringBaseSprite.__init__(self)

        self.original_image = self.image.copy()
        self.opaque = 100
        self.speed = 3
        self.min_opaque = 55
        self.max_opaque = 200


    def update(self):
        if self.opaque+self.speed < self.min_opaque or self.opaque+self.speed > self.max_opaque:
            self.speed *= -1
        self.opaque += self.speed

        self.image = self.original_image.copy()
        set_transparency_to_surf(self.image, self.opaque)


class CreditOpening(StringBaseSprite):

    y = 680
    text = 'Powered by Wasabi'
    color = (255, 255, 255)
    fontsize = 20

    def __init__(self):
        StringBaseSprite.__init__(self)


#########################################################################################
#                     GAMEOVER ANIMATION                                                #
#########################################################################################


class BackgroundGameover(pygame.sprite.Sprite):
    """Background fades in when a player loses"""

    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)

        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

        self.original_image = self.image.copy()
        self.opaque = 10
        self.speed = 2
        self.opaque_lg = 255
        self.speed_lg = -30


    def update(self):
        if self.opaque < 255:
            if self.opaque + self.speed < 255:
                self.opaque += self.speed
            else:
                self.opaque = 255

        if self.opaque_lg > 0:
            if self.opaque_lg + self.speed_lg > 0:
                self.opaque_lg += self.speed_lg
            else:
                self.opaque_lg = 0


        self.image = self.original_image.copy()
        self.image.set_alpha(self.opaque)
        self.lastgame = self.lastgame_image.copy()
        self.lastgame.set_alpha(self.opaque_lg)

        newsurf = pygame.Surface((SCR_RECT.width, SCR_RECT.height))
        newsurf.convert_alpha()
        newsurf.blit(self.image, (0,0))
        newsurf.blit(self.lastgame, (0,0))

        self.image = newsurf


class TitleGameover(StringBaseSprite):

    y = 100
    text = 'GAME OVER'
    color = (128, 128, 128)
    fontsize = 80
    
    def __init__(self):
        StringBaseSprite.__init__(self)

        self.original_image = self.image.copy()
        self.opaque = 10
        self.speed = 2

    def update(self):
        if self.opaque < 255:
            if self.opaque + self.speed < 255:
                self.opaque += self.speed
            else:
                self.opaque = 255

        self.image = self.original_image.copy()
        set_transparency_to_surf(self.image, self.opaque)


class ScoreGameover(StringBaseSprite):

    y = 300
    text = 'Score: {0}'
    color = (128, 128, 128)
    fontsize = 60

    def __init__(self):
        StringBaseSprite.__init__(self)
        self.opaque = 10
        self.speed = 2


    def update(self):
        self.original_image = self.font.render(self.text.format(Data.score), True, self.color)
        self.rect.x = (SCR_RECT.width-self.image.get_width())/2

        if self.opaque < 255:
            if self.opaque + self.speed < 255:
                self.opaque += self.speed
            else:
                self.opaque = 255

        self.image = self.original_image.copy()
        set_transparency_to_surf(self.image, self.opaque)


class PushSpaceGameover(PushSpaceOpening):

    y = 600
    frame = 0
    color = (128, 128, 128)

    def __init__(self):
        PushSpaceOpening.__init__(self)
        self.image = pygame.Surface((0, 0))
        self.opaque = 100
        self.speed = 7
        self.min_opaque = 55

    def update(self):
        if self.frame > 60:
            PushSpaceOpening.update(self)
        else:
            self.frame += 1

            
