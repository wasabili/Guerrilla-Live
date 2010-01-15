#!/usr/bin/env python
#-*- coding:utf-8 -*-

import pygame
from pygame.locals import *
import math
import time

from constants import *
from utils     import set_transparency_to_surf


player_pos = (0, 0)

class StringBaseSprite(pygame.sprite.Sprite):

    y = 0           # abstract
    x = None        # abstract
    fontfamily = None   # abstract
    fontsize = 0    # abstract
    text = ''       # abstract
    color = (0,0,0) # abstract

    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)

        self.font = pygame.font.SysFont(self.fontfamily, self.fontsize)
        self.image = self.font.render(self.text, True, self.color)

        self.rect = self.image.get_rect()
        if self.x is None:
            self.rect.x = (SCR_RECT.width-self.image.get_width())/2
        else:
            self.rect.x = self.x
        self.rect.y = self.y



#########################################################################################
#                     START ANIMATION                                                   #
#########################################################################################


class BackgroundStart():
    """Start Background"""

    enable_image_drawing = True

    opaque = 0
    speed = 3

    def draw(self, screen):  #FIXME

        if self.enable_image_drawing:
            if self.opaque < 255:
                if self.opaque + self.speed < 255:
                    self.opaque += self.speed
                else:
                    self.opaque = 255

                dummy = self.image.copy()
                dummy.set_alpha(self.opaque)

            else:
                dummy = self.image

            screen.fill((0, 0, 0))
            screen.blit(dummy, (0, 0))

        else:
            screen.fill((0,0,0))

class TitleOpening(pygame.sprite.Sprite):

    opaque = 0
    speed = 3

    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.rect = self.image.get_rect()
        self.rect.x = (SCR_RECT.width - self.rect.width)/2
        self.rect.y = self.y

        self.original_image = self.image.copy()

    def update(self):  #FIXME
        if self.opaque < 255:
            if self.opaque + self.speed < 255:
                self.opaque += self.speed
            else:
                self.opaque = 255

            self.image = self.original_image.copy()
            set_transparency_to_surf(self.image, self.opaque)

        else:
            self.image = self.original_image


class PushSpaceOpening(StringBaseSprite):

    y = 500
    text = 'PUSH SPACE KEY'
    color = (255, 255, 255)
    fontsize = 40

    frame = 0
    wait = 90

    def __init__(self):
        StringBaseSprite.__init__(self)

        self.original_image = self.image.copy()
        self.opaque = 100
        self.speed = 3
        self.min_opaque = 55
        self.max_opaque = 200


    def update(self):

        if self.frame >= self.wait:
            if self.opaque+self.speed < self.min_opaque or self.opaque+self.speed > self.max_opaque:
                self.speed *= -1
            self.opaque += self.speed

            self.image = self.original_image.copy()
            set_transparency_to_surf(self.image, self.opaque)

        else:
            self.frame += 1

            self.image = self.original_image.copy()
            set_transparency_to_surf(self.image, 0)

class CreditOpening(StringBaseSprite):

    y = 680
    text = 'Powered by Wasabi'
    color = (255, 255, 255)
    fontsize = 20

    def __init__(self):
        StringBaseSprite.__init__(self)


#########################################################################################
#                     SELECT ANIMATION                                                  #
#########################################################################################


class BackgroundSelect():
    """Select Background"""

    frame = 0

    opaque = 0
    speed = 50

    def draw(self, screen):
        if self.opaque < 255:
            if self.opaque + self.speed < 255:
                self.opaque += self.speed
            else:
                self.opaque = 255

            dummy = self.image.copy()
            dummy.set_alpha(self.opaque)

        else:
            dummy = self.image

        screen.fill((0, 0, 0))
        screen.blit(dummy, (0, 0))


class ArcadeSelect(StringBaseSprite):

    y = 270
    x = 350
    text = 'ARCADE MODE'
    color = (255, 255, 255)
    fontsize = 80

    def __init__(self):
        StringBaseSprite.__init__(self)


class LevelSelect(StringBaseSprite):

    y = 350
    x = 350
    text = 'LEVEL {0}'
    color = (255, 255, 255)
    fontsize = 80

    def __init__(self, num):
        self.text = self.text.format(num)
        self.y = self.y + 60*(num-1)
        StringBaseSprite.__init__(self)


class HelpSelect(StringBaseSprite):

    y = 670
    x = 350
    text = 'HELP'
    color = (255, 255, 255)
    fontsize = 80

    def __init__(self):
        StringBaseSprite.__init__(self)


class HighlightSelect(pygame.sprite.Sprite):

    entrylist = [(350, 270), (350, 350), (350, 410), (350, 470), (350, 530), (350, 590), (350, 670)]
    
    index = 0
    speed = 10
    frame = 0
    animecycle = 4
    wait = 0.08
    timer = 0
    

    def __init__(self, sidebar):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.font = pygame.font.SysFont(None, 80)
        self.font_height = self.font.render('TEXT', True, (64,64,64)).get_height()

        self.blinkimage = pygame.Surface((30, 50))
        self.blinkimage.fill((128,128,128))
        self.original_blinkimage = self.blinkimage.copy()
        self.original_image = self.image.copy()

        self.rect = self.image.get_rect()
        self.rect.x = self.entrylist[0][0]
        self.rect.y = self.entrylist[0][1] - (60-self.font_height)/2

        self.diffx = -60
        self.diffy = -6

        self.sidebar = sidebar

    def update(self):

        if time.time() - self.timer > self.wait:
            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[K_UP] and self.index >= 1:
                self.index -= 1
                self.sidebar.change(self.index)
                self.timer = time.time()
            if pressed_keys[K_DOWN] and self.index <= len(self.entrylist)-2:
                self.index += 1
                self.sidebar.change(self.index)
                self.timer = time.time()


        self.blinkimage = self.original_blinkimage.copy()
        if self.frame/self.animecycle%2 == 0:
            self.blinkimage.set_alpha(0)
        else:
            self.blinkimage.set_alpha(128)
        self.image = self.original_image.copy()
        self.image.blit(self.blinkimage, (10, 5))
        self.frame += 1

        if (self.rect.x-self.diffx, self.rect.y-self.diffy) != self.entrylist[self.index]: #FIXME
            self.rect.x = self.entrylist[self.index][0] + self.diffx
            self.rect.y = self.entrylist[self.index][1] + self.diffy
            
class SidebarSelect(pygame.sprite.Sprite):

    oldindex = 0
    newindex = 0
    frame = 0
    anime = 15
    animecycle = 4
    timer = 0
  
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)

        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.center = (120, SCR_RECT.height/2)

        self.fpy = float(self.rect.y)

        self.oldindex = 0
        self.newindex = 0

        self.starty = SCR_RECT.height
        self.speed = self.starty/self.anime

    def change(self, index):
        self.newindex = index
        self.frame = self.anime
        self.fpy = self.starty

    def update(self):

        if self.oldindex != self.newindex:
            newsurf = pygame.Surface((300, SCR_RECT.height))
            newsurf.fill((0,0,0))
            newsurf.blit(self.images[self.oldindex], (0,0))

            self.fpy = max(self.fpy - self.speed, 0)
            newsurf.blit(self.images[self.newindex], (0, self.fpy))

            self.image = newsurf

            if self.fpy == 0:
                self.oldindex = self.newindex
                
        else:
            self.image = self.images[self.oldindex]


#########################################################################################
#                     PLAYING ANIMATION                                                 #
#########################################################################################


class BackgroundPlaying():
    """Background follows player's move"""

    mag = 0.1

    def __init__(self):

        magged_size = (int(SCR_RECT.width*(1+self.mag)), int(SCR_RECT.height*(1+self.mag)))
        self.image = pygame.transform.scale(self.image, (magged_size[0], magged_size[1]))  #FIXME

        self.startx = -magged_size[0]*(self.mag/(1+self.mag))/2.0
        self.starty = -magged_size[1]*(self.mag/(1+self.mag))/2.0

    def draw(self, screen):
        pos = player_pos
        start = SCR_RECT.center

        x = self.startx + (start[0] - pos[0])*self.mag
        y = self.starty + (start[1] - pos[1])*self.mag

        screen.blit(self.image, (x, y))


class Player(pygame.sprite.Sprite):
    """Own ship"""

    enable_acceleration = True 
    speed = 2
    accel = 0.15
    dynamic_fc = 0.05
    max_speed = 4
    # When the object is static, its friction coefficient is supposed to be 0

    reload_time = 5
    frame = 0L

    lives = 3
    hearts = []
    invincible = -1
    blink_interval = 10

    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.rect = self.image.get_rect()
        self.rect = Rect(0, 0, self.rect.width*1/4, self.rect.height*1/4)  #FIXME TEST
        self.rect.center = CENTER

        self.hearts = [HeartMark((SCR_RECT.width - (60+60*x), SCR_RECT.height - 45)) for x in range(self.lives)]

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
            self.hearts.pop().destroy()                 # remove one heart
            self.original_image = self.image.copy()  # for blinking
            self.invincible = 300                    # invincible time
            return True

    def is_invincible(self):
        return self.invincible >= 0

    def update(self):
        global player_pos

        if self.invincible > 0:
            self.invincible -= 1
            self.frame += 1
            self.image = self.original_image.copy()
            if (self.frame/self.blink_interval)%2 == 0:
                #self.image.set_alpha(64) FIXME
                set_transparency_to_surf(self.image, 64)
            else:
                #self.image.set_alpha(255) FIXME
                set_transparency_to_surf(self.image, 255)
        elif self.invincible == 0:
            self.invincible -= 1
            self.image = self.original_image

        if self.enable_acceleration:
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

            # Calculate friction
            if self.fpvx > 0:
                self.fpvx -= self.dynamic_fc
            elif self.fpvx < 0:
                self.fpvx += self.dynamic_fc
            if self.fpvy > 0:
                self.fpvy -= self.dynamic_fc
            elif self.fpvy < 0:
                self.fpvy += self.dynamic_fc

            # Restrict player speed by max_speed
            if self.fpvx > self.max_speed:
                self.fpvx = self.max_speed
            elif self.fpvx < -self.max_speed:
                self.fpvx = -self.max_speed
            if self.fpvy > self.max_speed:
                self.fpvy = self.max_speed
            elif self.fpvy < -self.max_speed:
                self.fpvy = -self.max_speed

            # Restrict player position inside SCR_RECT
            if SCR_RECT.right <= self.rect.right and self.fpvx > 0:
                self.fpvx = 0
            if SCR_RECT.left >= self.rect.left and self.fpvx < 0:
                self.fpvx = 0
            if SCR_RECT.top >= self.rect.top and self.fpvy < 0:
                self.fpvy = 0
            if SCR_RECT.bottom <= self.rect.bottom and self.fpvy > 0:
                self.fpvy = 0

        else:
            # Move player
            self.fpvx, self.fpvy = 0, 0

            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[K_LEFT] or pressed_keys[K_a]:
                self.fpvx = -self.speed
            if pressed_keys[K_RIGHT] or pressed_keys[K_d]:
                self.fpvx = self.speed
            if pressed_keys[K_UP] or pressed_keys[K_w]:
                self.fpvy = -self.speed
            if pressed_keys[K_DOWN] or pressed_keys[K_s]:
                self.fpvy = self.speed

            # Restrict player position inside SCR_RECT
            self.rect.clamp_ip(SCR_RECT)  

        self.fpx += self.fpvx
        self.fpy += self.fpvy
        self.rect.x = int(self.fpx)
        self.rect.y = int(self.fpy)
        self.rect.clamp_ip(SCR_RECT)        

        player_pos = self.rect.center

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

        # Rotate image
        self.image = pygame.transform.rotate(self.image, -180*self.direction/math.pi)

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

        self.target = player_pos
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

        # キャラクターアニメーション FIXME
        self.frame += 1
        self.image = self.images[self.frame/self.animecycle%len(self.images)]

        # 終点の角度を計算
        self.target = player_pos
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


class BigEColi(pygame.sprite.Sprite):
    """Sample Boss: no attaching and no animation"""

    speed = 2  # 移動速度
    hp = 100
    animecycle = 2
    frame = 180
    animechap = 0
    roundr = 100
    point1 = (150, SCR_RECT.height/2)
    point2 = (point1[0]+roundr, point1[1])  # The center of the round
    av = 0  # Angular velocity

    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)

        self.rect = self.image.get_rect()
        self.rect.center = (-self.rect.width/2, -self.rect.height/2)

        # Calculate speed
        self.fpx = float(self.rect.center[0])
        self.fpy = float(self.rect.center[1])
        self.fpvx = 0
        self.fpvy = 0

        # 終点の角度を計算
        self.target = self.point1
        self.start = self.rect.center
        self.direction = math.atan2(float(self.target[1]-self.start[1]), float(self.target[0]-self.start[0]))

        # Move
        self.fpvx = math.cos(self.direction) * self.speed
        self.fpvy = math.sin(self.direction) * self.speed

        # Calculate Angular Velocity
        self.av = self.speed/(2*math.pi*self.roundr/360.0)

        print self.av

    def hit_once(self):

        # Player's shot hit me!
        self.hp -= 1
        return self.hp > 0

    def update(self):

        if self.animechap == 0:

            self.fpx = min(self.fpx + self.fpvx, self.point1[0])
            self.fpy = min(self.fpy + self.fpvy, self.point1[1])
            self.rect.center = (int(self.fpx), int(self.fpy))

            if self.rect.center == (int(self.point1[0]), int(self.point1[1])):
                self.animechap = 1

        elif self.animechap == 1:

            vx = math.cos(self.frame/180.0*math.pi) * self.roundr
            vy = math.sin(self.frame/180.0*math.pi) * self.roundr

            self.rect.center = (int(self.point2[0] + vx), int(self.point2[1] - vy))

            self.frame += self.av
            

class HeartMark(pygame.sprite.Sprite):
    """Life remains"""

    animecycle = 1
    frame = 0
    
    destroyed = False
    destroy_frame = 0
    destroy_limit = 60

    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self, self.containers)

        self.image = self.images[0]

        self.rect = self.image.get_rect()
        self.rect.center = pos

        self.max_frame = len(self.images) * self.animecycle  # a frame to rewind

    def update(self):
        # Character Animation
        self.image = self.images[self.frame/self.animecycle]
        self.frame += 1
        if self.frame == self.max_frame:
            self.frame = 0

        if self.destroyed:
            if self.destroy_frame >= self.destroy_limit:
                self.kill()

            dummy_image = self.image.copy()
            dummy_image.set_alpha(255*(1- self.destroy_frame/float(self.destroy_limit)))
            self.image = dummy_image

            self.destroy_frame += 1

    def destroy(self):
        self.destroyed = True

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
        self.speed = 3
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

    def __init__(self, gamedata):
        StringBaseSprite.__init__(self)
        self.opaque = 10
        self.speed = 2

        self.gamedata = gamedata

    def update(self):
        self.original_image = self.font.render(self.text.format(self.gamedata.score), True, self.color)
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

            
