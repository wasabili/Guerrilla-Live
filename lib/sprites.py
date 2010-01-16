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
#                     CREDIT ANIMATION                                                  #
#########################################################################################


class AuthorCredit(StringBaseSprite):
    """Start Background"""

    FADEIN, WAIT, FADEOUT, EXTRA, END = range(5)
    state = FADEIN
    y = SCR_RECT.height/2
    text = 'Wasabi Presents'
    color = (255, 255, 255)
    fontsize = 20
    
    def __init__(self):
        StringBaseSprite.__init__(self)

        self.original_image = self.image.copy()
        self.frame = 0
        self.opaque = 0
        self.speed = 3
        self.wait = 80
        self.extra = 40

    def update(self):
        if self.state == self.FADEIN:
            if self.opaque + self.speed < 255:
                self.opaque += self.speed
            else:
                self.opaque = 255
                self.state = self.WAIT
                self.frame = 0
        
        elif self.state == self.WAIT:
            if self.frame > self.wait:
                self.state = self.FADEOUT

        elif self.state == self.FADEOUT:
            if self.opaque - self.speed > 0:
                self.opaque -= self.speed
            else:
                self.opaque = 0
                self.state = self.EXTRA
                self.frame = 0

        elif self.state == self.EXTRA:
            if self.frame > self.extra:
                self.state = self.END
        
        self.image = self.original_image.copy()
        set_transparency_to_surf(self.image, self.opaque)

        self.frame += 1

    def havefinished(self):
        return self.state == self.END

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

    y = 250

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

    wait = 75

    def __init__(self):
        StringBaseSprite.__init__(self)

        self.original_image = self.image.copy()
        self.opaque = 0
        self.speed = 3
        self.min_opaque = 55
        self.max_opaque = 200

        self.frame = 0
        self.blink = False


    def update(self):

        if self.frame < self.wait:

            self.image = self.original_image.copy()
            set_transparency_to_surf(self.image, 0)
            self.frame += 1

        else:
            if not self.blink:
                if self.opaque + self.speed > self.max_opaque:
                    self.blink = True

            else:
                if self.opaque+self.speed < self.min_opaque or self.opaque+self.speed > self.max_opaque:
                    self.speed *= -1

            self.opaque += self.speed
            self.image = self.original_image.copy()
            set_transparency_to_surf(self.image, self.opaque)



#########################################################################################
#                     SELECT ANIMATION                                                  #
#########################################################################################


class BackgroundSelect():
    """Select Background"""

    def draw(self, screen):

        screen.fill((0, 0, 0))
        screen.blit(self.image, (0, 0))


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
    wait = 0.12
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
                self.sidebar.change(self.index, True)
                self.timer = time.time()
            if pressed_keys[K_DOWN] and self.index <= len(self.entrylist)-2:
                self.index += 1
                self.sidebar.change(self.index, False)
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
            
    def get_index(self):

        return self.index


class SidebarSelect(pygame.sprite.Sprite):

    anime = 15
    timer = 0
  
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)

        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.center = (120, SCR_RECT.height/2)

        self.speed = SCR_RECT.height/self.anime

        self.order = []
        for i, image in enumerate(self.images):
            y = 0 if i == 0 else SCR_RECT.height
            self.order.append([image, y, 0])

    def change(self, index, up):
        if up:
            self.order[index+1][2] = self.speed  # add animation
        else:
            self.order[index][2] = -self.speed  # add animation

    def update(self):

        newsurf = pygame.Surface((300, SCR_RECT.height))
        newsurf.fill((0,0,0))

        for i, (image, fpy, fpvy) in enumerate(self.order):

            newsurf.blit(image, (0,int(fpy)))

            if fpvy < 0:
                fpy = max(fpy + fpvy, 0)
                self.order[i][1] = fpy
                if fpy == 0:
                    self.order[i][2] = 0
            elif fpvy > 0:
                fpy = min(fpy + fpvy, SCR_RECT.height)
                self.order[i][1] = fpy
                if fpy == SCR_RECT.height:
                    self.order[i][2] = 0

        self.image = newsurf


class SidebarSelect2(SidebarSelect):
 
    frame = 0

    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
 
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.center = (100, SCR_RECT.height/2)
 
        self.oldindex = 0
        self.newindex = 0
 
        self.starty = SCR_RECT.height
        self.speed = 15
        self.opaque = 0
 
    def change(self, index, up):
        self.oldindex = self.newindex
        self.newindex = index
        self.opaque = 0      
 
    def update(self):
 
        if self.oldindex != self.newindex:
            newsurf = pygame.Surface((300, SCR_RECT.height))
            newsurf.fill((0,0,0))
            newsurf.blit(self.images[self.oldindex], (0,0))
 
            if self.opaque < 255:
                if self.opaque + self.speed <255:
                    self.opaque += self.speed
                else:
                    self.opaque = 255

                dummy = self.images[self.newindex].copy()
                dummy.set_alpha(self.opaque)

                newsurf.blit(dummy, (0, 0))
            elif self.opaque == 255:
                self.oldindex = self.newindex

                newsurf.blit(self.images[self.newindex], (0, 0))
 
            newsurf.blit(self.mask, (0,0)) #FIXME 
            self.image = newsurf
 
        else:
            #self.image = self.images[self.oldindex] #FIXME FIXME
            self.image = self.images[self.oldindex].copy()
            self.image.blit(self.mask, (0,0))


class EffectSelect():
    """Select effects"""

    opaque = 255
    speed = -10

    def __init__(self):
        newsurf = pygame.Surface(SCR_RECT.size)
        newsurf.fill((0,0,0))
        self.image = newsurf

    def draw(self, screen):
        if self.opaque > 0:
            if self.opaque + self.speed > 0:
                self.opaque += self.speed
            else:
                self.opaque = 0

            dummy = self.image.copy()
            dummy.set_alpha(self.opaque)

            screen.blit(dummy, (0, 0))


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
    animecycle = 2

    lives = 3
    hearts = []
    invincible = -1
    blink_interval = 10

    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect = Rect(self.rect.width/8, self.rect.height/8, self.rect.width*3/4, self.rect.height*3/4)  #FIXME TEST
        self.rect.center = CENTER

        self.hearts = [HeartMark((SCR_RECT.width - (60+60*x), SCR_RECT.height - 45)) for x in range(self.lives)]

        self.fpx = float(self.rect.x)
        self.fpy = float(self.rect.y)
        self.fpvx = 0
        self.fpvy = 0

        self.frame = 0L
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
            self.invincible = 300                    # invincible time
            return True

    def is_invincible(self):
        return self.invincible >= 0

    def update(self):
        global player_pos

        # Character Animation
        self.image = self.images[self.frame/self.animecycle%len(self.images)]
        self.frame += 1

        if self.invincible > 0:
            self.invincible -= 1
            self.image = self.image.copy()
            if (self.frame/self.blink_interval)%2 == 0:
                self.image.set_alpha(64)
                #set_transparency_to_surf(self.image, 64) #FIXME
            else:
                self.image.set_alpha(255)
                #set_transparency_to_surf(self.image, 255) #FIXME
        elif self.invincible == 0:
            self.invincible -= 1

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
                #Player.shot_sound.play()  #FIXME
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

    def __init__(self):
        StringBaseSprite.__init__(self)
        self.opaque = 10
        self.speed = 2

    def update(self):
        self.original_image = self.font.render(self.text.format(self.score), True, self.color)
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

            
#########################################################################################
#                     HELP ANIMATION                                                    #
#########################################################################################


class HelpDraw():

    def __init__(self):

        self.get_bg = True

        self.bg_help = BackgroundHelp()
        self.cover_help = CoverHelp()
        self.contents_help = ContentsHelp(self.cover_help)
        self.pushspace_help = PushSpaceHelp(self.cover_help)

        self.closing = False
        self.closed = False
        self.opaque = 255
        self.speed = 30

    def update(self):

        self.bg_help.update()
        self.cover_help.update()
        self.contents_help.update()
        self.pushspace_help.update()

    def draw(self, screen):

        # Background
        screen.fill((255,255,255))
        screen.blit(self.bg_help.image, (0,0))

        # Foreground
        newsurf = screen.copy()
        newsurf.blit(self.cover_help.image, (self.cover_help.rect.x, self.cover_help.rect.y))
        newsurf.blit(self.contents_help.image, (self.contents_help.rect.x, self.contents_help.rect.y))
        newsurf.blit(self.pushspace_help.image, (self.pushspace_help.rect.x, self.pushspace_help.rect.y))
        
        if not self.closing:
            screen.blit(newsurf, (0,0))
        else:
            if self.opaque - self.speed > 0:
                self.opaque -= self.speed
            else:
                self.opaque = 0
                self.closed = True
            newsurf.set_alpha(self.opaque)
            screen.blit(newsurf, (0,0))

    def close(self):
        self.closing = True
        self.bg_help.back()

    def whileclosing(self):
        return self.closing

    def hasclosed(self):
        return self.closed

class BackgroundHelp():

    def __init__(self):
        self.index = 0
        self.image = self.images[self.index]
        self.rect = SCR_RECT

        self.frame = 0
        self.cycle = 3

        self.goforward = True

    def update(self):

        if self.goforward:
            if self.frame%self.cycle == 0 and self.index < len(self.images)-1:
                self.index += 1
                self.image = self.images[self.index]

            self.frame += 1

        else:
            if self.frame%self.cycle == 0 and self.index > 0:
                self.index -= 1
                self.image = self.images[self.index]

            self.frame -= 1
            

    def back(self):
        self.goforward = False
        self.frame = len(self.images)
        self.cycle = 1
        

class CoverHelp():

    ENTER, SHOW, EXIT = range(3)
    FIRST, SECOND, WAIT = range(3)

    def __init__(self):
        self.rect = None
        self.frame = 0
        self.state = self.ENTER
        self.step = self.FIRST
        self.speed = 30
        self.wait = 10
        self.fpx = SCR_RECT.width/2.0-3
        self.fpy = SCR_RECT.height/2.0-3

    def update(self):

        if self.state == self.ENTER:
            if self.step == self.FIRST:
                if self.fpx - self.speed > 0:
                    self.fpx -= self.speed
                else:
                    self.fpx = 0
                    self.step = self.WAIT
                    self.frame = 0

            elif self.step == self.WAIT:
                if self.frame > self.wait:
                    self.step = self.SECOND

            elif self.step == self.SECOND:
                if self.fpy - self.speed > 0:
                    self.fpy -= self.speed
                else:
                    self.fpy = 0
                    self.state = self.SHOW
                    self.frame = 0

            self.frame += 1
        elif self.state == self.SHOW:
            self.fpx = 0
            self.fpy = 0 

        width = int(SCR_RECT.width-self.fpx*2)
        height = int(SCR_RECT.height-self.fpy*2)
        newsurf = pygame.Surface((width, height))
        newsurf = newsurf.convert_alpha()
        newsurf.fill((0,0,0,128))

        self.image = newsurf
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = int(self.fpx), int(self.fpy)

    def isshowstate(self):
        return self.state == self.SHOW


class ContentsHelp():
    
    def __init__(self, cover_help):
        self.rect = self.image.get_rect()
        self.cover_help = cover_help

        self.original_image = self.image.copy()

    def update(self):
        if self.cover_help.isshowstate():
            self.image = self.original_image.copy()
        else:
            self.image = pygame.Surface(SCR_RECT.size).convert_alpha()
            self.image.fill((0,0,0,0))


class PushSpaceHelp(PushSpaceOpening):

    y = 690
    frame = 0
    color = (255, 255, 255)

    def __init__(self, cover_help):
        PushSpaceOpening.__init__(self)
        self.image = pygame.Surface((0, 0))
        self.opaque = 0
        self.speed = 3
        self.min_opaque = 55
        self.max_opaque = 255
        self.frame = 0

        self.cover_help = cover_help

    def update(self):
        if not self.cover_help.isshowstate():

            self.image = pygame.Surface(self.original_image.get_size()).convert_alpha()
            self.image.fill((0,0,0,0))
            self.frame += 1

        else:
            if not self.blink:
                if self.opaque + self.speed > self.max_opaque:
                    self.speed *= -1
                    self.blink = True

            else:
                if self.opaque+self.speed < self.min_opaque or self.opaque+self.speed > self.max_opaque:
                    self.speed *= -1

            self.opaque += self.speed
            self.image = self.original_image.copy()
            set_transparency_to_surf(self.image, self.opaque)
