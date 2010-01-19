#!/usr/bin/env python
#-*- coding:utf-8 -*-

import pygame
from pygame.locals import *
import math
import random
from collections    import deque

from lib.constants  import *
from lib.utils      import *
from base           import *


#########################################################################################
#                     PLAYING ANIMATION                                                 #
#########################################################################################


player_pos = (0, 0)


def recycle_or_gen_object(obj, *options):
    """If possible, salvage recycled object"""

    if obj.recyclebox:
        newobj = obj.recyclebox.pop()
        if options:
            newobj.init(*options)
        else:
            newobj.init()

    else:
        if options:
            obj(*options)
        else:
            obj()


class PlayDraw():

    shot_reload_time = 5

    def __init__(self, gamedata):
        # Create sprite groups
        self.play_all   = pygame.sprite.LayeredUpdates()           # Play screen
        self.enemies    = pygame.sprite.Group()                   # Enemy Group
        self.shots      = pygame.sprite.Group()                   # Beam Group
        self.bosses     = pygame.sprite.Group()                   # Bosses Group

        # Assign default sprite groups
        Player.containers           = self.play_all
        EColi.containers            = self.play_all, self.enemies
        EColi2.containers           = self.play_all, self.enemies
        BigEColi.containers         = self.play_all, self.enemies, self.bosses
        Shot.containers             = self.play_all, self.shots
        Explosion.containers        = self.play_all
        HeartMark.containers        = self.play_all
        Gage.containers             = self.play_all

        # Create recycle boxes
        EColi.recyclebox = deque()
        EColi2.recyclebox = deque()
        Shot.recyclebox = deque()

        # Set Layer
        Player._layer       = 100
        HeartMark._layer    = 200
        Explosion._layer    = 100
        Gage._layer         = 200
        GageMask._layer     = 300

        self.player = Player()
        self.bg_play = BackgroundPlay(gamedata.level)
        self.gage = Gage(gamedata)

        self.gamedata = gamedata
        self.boss = None
        self.gameover = False

        # Shot
        self.shot_reload_timer = 5

    def update(self):
        self.bg_play.update()
        self.play_all.update()

        self.collision_detection()  # detect collision

        # Shoot a shot
        mouse_pressed = pygame.mouse.get_pressed()
        if mouse_pressed[0]:
            # Normal Shot
            if self.gamedata.weapon_mode == self.gamedata.SHOT:
                if self.shot_reload_timer > 0:  # Unable to shoot while reloading
                    self.shot_reload_timer -= 1
                else:
                    # Shoot
                    #Player.shot_sound.play()  #FIXME
                    recycle_or_gen_object(Shot, player_pos, pygame.mouse.get_pos())
                    self.shot_reload_timer = self.shot_reload_time

            # Sub-Shot
            elif self.gamedata.weapon_mode == self.gamedata.SUBSHOT:
                self.gamedata.subshot_timer -= 1
                if self.shot_reload_timer > 0:  # Unable to shoot while reloading
                    self.shot_reload_timer -= 1
                else:
                    # Shoot
                    #Player.shot_sound.play()  #FIXME
                    TripleShot(player_pos, pygame.mouse.get_pos())
                    self.shot_reload_timer = self.shot_reload_time


        # Generate enemies
        if self.boss is None:
            # Create new enemies
            for enemy, freq, subfreq in self.gamedata.enemies:
                pos = self.gen_random_position(freq)
                if pos is not None:
                    recycle_or_gen_object(enemy, pos)

            # enter to boss battle?
            if self.gamedata.is_bosslimit_broken():
                self.boss = self.gamedata.boss()

        else:
            # Create new enemies
            for enemy, freq, subfreq in self.gamedata.enemies:
                pos = self.gen_random_position(subfreq)
                if pos is not None:
                    recycle_or_gen_object(enemy, pos)

            # player killed the boss?
            if not self.boss.alive():
                self.gamedata.result = self.gamedata.WIN
                self.gameover = True


    def draw(self, screen):
        screen.blit(self.bg_play.image, (self.bg_play.rect.x, self.bg_play.rect.y))     # Background
        self.play_all.draw(screen)                                                      # Objects


    def gen_random_position(self, freq):
        """Generate random position"""

        if freq == 0:
            return None
        elif int(random.random()*(1/freq)) == 0:
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

            return x, y
        else:
            return None


    def collision_detection(self):
        """Detect collision"""

        # Between enemies and shots
        enemy_collided = pygame.sprite.groupcollide(self.enemies, self.shots, False, True)
        for enemy, shots in enemy_collided.items():
            #EColi.kill_sound.play() #FIXME

            # Bomb!
            if not enemy.hit_once():
                enemy.kill()                    # Kill an enemy
                self.gamedata.killed_enemies(1)       # FIXME
                Explosion(shots[0].rect.center) # Draw explosion

        # Between player and E.Colis
        player_collided = pygame.sprite.spritecollide(self.player, self.enemies, True)
        if player_collided:
            if not self.player.is_invincible():
                #Player.bomb_sound.play()  #FIXME
                pass
            if not self.player.killed_once(): # die once
                self.gamedata.result = self.gamedata.LOSE
                self.gameover = True

    def hasfinished(self):
        return self.gameover


class BackgroundPlay():
    """Background follows player's move"""

    mag = 0.2

    def __init__(self, level):

        magged_size = (int(SCR_RECT.width*(1+self.mag)), int(SCR_RECT.height*(1+self.mag)))

        self.image = self.images[level-1]  # FIXME some images in one level
        self.image = pygame.transform.scale(self.image, (magged_size[0], magged_size[1]))
        self.rect = self.image.get_rect()

        self.startx = -magged_size[0]*(self.mag/(1+self.mag))/2.0
        self.starty = -magged_size[1]*(self.mag/(1+self.mag))/2.0

    def update(self):
        pos = player_pos
        start = SCR_RECT.center

        self.rect.x = self.startx + (start[0] - pos[0])*self.mag
        self.rect.y = self.starty + (start[1] - pos[1])*self.mag


class Player(pygame.sprite.Sprite):
    """Own ship"""

    speed = 2
    accel = 0.15
    dynamic_fc = 0.05
    max_speed = 4
    # When the object is static, its friction coefficient is 0

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
        self.rect = Rect(0, 0, self.rect.width*3/4, self.rect.height*3/4)  #FIXME TEST
        self.rect.center = CENTER

        self.hearts = [HeartMark((SCR_RECT.width - (60+60*x), SCR_RECT.height - 45)) for x in range(self.lives)]

        self.fpx = float(self.rect.x)
        self.fpy = float(self.rect.y)
        self.fpvx = 0
        self.fpvy = 0

        self.frame = 0L

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
                #self.image.set_alpha(128)
                set_transparency_to_surf(self.image, 128) #FIXME
            else:
                #self.image.set_alpha(255)
                set_transparency_to_surf(self.image, 255) #FIXME
        elif self.invincible == 0:
            self.invincible -= 1

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

        self.fpx += self.fpvx
        self.fpy += self.fpvy
        self.rect.x = int(self.fpx)
        self.rect.y = int(self.fpy)
        self.rect.clamp_ip(SCR_RECT)        

        player_pos = self.rect.center



#########################################################################################
#                     WEAPONS                                                           #
#########################################################################################


class Shot(pygame.sprite.Sprite):
    """プレイヤーが発射するビーム"""

    speed = 9  # 移動速度

    def __init__(self, start, target=None, degree=None):
        pygame.sprite.Sprite.__init__(self, self.containers)

        # Rotate image
        if degree is None:
            direction = math.atan2(target[1]-start[1], target[0]-start[0])
            self.image = pygame.transform.rotate(self.shot_image, -180*direction/math.pi)
        else:
            direction = -degree*math.pi/180.0
            self.image = pygame.transform.rotate(self.shot_image, degree)

        self.rect = self.image.get_rect()
        self.rect.center = start
        self.fpx = float(self.rect.x)
        self.fpy = float(self.rect.y)

        self.fpvx = math.cos(direction) * self.speed
        self.fpvy = math.sin(direction) * self.speed

    def init(self, start, target=None, degree=None):
        # Rotate image
        if degree is None:
            direction = math.atan2(target[1]-start[1], target[0]-start[0])
            self.image = pygame.transform.rotate(self.shot_image, -180*direction/math.pi)
        else:
            direction = -degree*math.pi/180.0
            self.image = pygame.transform.rotate(self.shot_image, degree)

        self.rect = self.image.get_rect()
        self.rect.center = start
        self.fpx = float(self.rect.x)
        self.fpy = float(self.rect.y)

        self.fpvx = math.cos(direction) * self.speed
        self.fpvy = math.sin(direction) * self.speed

        # Reborn
        self.add(self.containers)

    def update(self):
        # Move
        self.fpx += self.fpvx
        self.fpy += self.fpvy
        self.rect.x = int(self.fpx)
        self.rect.y = int(self.fpy)

        # 画面外に出たらオブジェクトを破棄
        if not SCR_RECT.contains(self.rect):
            self.kill()

    def kill(self):
        pygame.sprite.Sprite.kill(self)
        self.__class__.recyclebox.append(self)


class TripleShot():
    """プレイヤーが発射するビーム"""

    def __init__(self, start, target):
        direction = math.atan2(target[1]-start[1], target[0]-start[0])
        degree = -180*direction/math.pi
        recycle_or_gen_object(Shot, start, None, degree)
        recycle_or_gen_object(Shot, start, None, degree+120 if degree+120<180 else degree-240)
        recycle_or_gen_object(Shot, start, None, degree+240 if degree+240<180 else degree-120)
        del self
        

class EColi(pygame.sprite.Sprite):
    """E.Coli"""

    speed = 1.2  # 移動速度
    animecycle = 18  # アニメーション速度

    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self, self.containers)

        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.center = pos

        # 速度を計算
        self.fpx = float(self.rect.x)
        self.fpy = float(self.rect.y)

        self.hp = 1
        self.frame = 0

    def init(self, pos):
        self.frame = 0
        # set pos
        self.rect.center = pos
        self.fpx = float(self.rect.x)
        self.fpy = float(self.rect.y)
        self.add(self.containers)

    def update(self):

        # Character Animation FIXME
        self.frame += 1
        self.image = self.images[self.frame/self.animecycle%len(self.images)]

        # 終点の角度を計算
        target = player_pos
        start = self.rect.center
        direction = math.atan2(float(target[1]-start[1]), float(target[0]-start[0]))

        # rotate
        self.image = pygame.transform.rotate(self.image, -180*direction/math.pi)

        # Move
        fpvx = math.cos(direction) * self.speed
        fpvy = math.sin(direction) * self.speed
        self.fpx += fpvx
        self.fpy += fpvy
        self.rect.x = int(self.fpx)
        self.rect.y = int(self.fpy)

    def hit_once(self):

        # Player's shot hit me!
        self.hp -= 1
        return self.hp > 0

    def kill(self):
        pygame.sprite.Sprite.kill(self)
        self.__class__.recyclebox.append(self)


class EColi2(pygame.sprite.Sprite):
    """E.Coli2"""

    speed = 0.4  # 移動速度

    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self, self.containers)

        self.original_image = self.image.copy()
        self.rect = self.image.get_rect()
        self.rect.center = pos

        # 速度を計算
        self.fpx = float(self.rect.x)
        self.fpy = float(self.rect.y)

        self.hp = 3

    def init(self, pos):
        # set pos
        self.rect.center = pos
        self.fpx = float(self.rect.x)
        self.fpy = float(self.rect.y)
        self.add(self.containers)

    def update(self):

        # 終点の角度を計算
        target = player_pos
        start = self.rect.center
        direction = math.atan2(float(target[1]-start[1]), float(target[0]-start[0]))

        # rotate
        self.image = self.original_image.copy()
        self.image = pygame.transform.rotate(self.image, -180*direction/math.pi)

        # Move
        fpvx = math.cos(direction) * self.speed
        fpvy = math.sin(direction) * self.speed
        self.fpx += fpvx
        self.fpy += fpvy
        self.rect.x = int(self.fpx)
        self.rect.y = int(self.fpy)

    def hit_once(self):

        # Player's shot hit me!
        self.hp -= 1
        return self.hp > 0

    def kill(self):
        pygame.sprite.Sprite.kill(self)
        self.__class__.recyclebox.append(self)


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
        #self.rect = Rect(0, 0, self.rect.width*3/4, self.rect.height*2/3)  #FIXME test
        self.rect.center = (-self.rect.width/2, -self.rect.height/2)

        # Calculate speed
        self.fpx = float(self.rect.center[0])
        self.fpy = float(self.rect.center[1])

        # 終点の角度を計算
        self.target = self.point1
        self.start = self.rect.center
        self.direction = math.atan2(float(self.target[1]-self.start[1]), float(self.target[0]-self.start[0]))

        # Move
        self.fpvx = math.cos(self.direction) * self.speed
        self.fpvy = math.sin(self.direction) * self.speed

        # Calculate Angular Velocity
        self.av = self.speed/(2*math.pi*self.roundr/360.0)

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
            
    def hit_once(self):

        # Player's shot hit me!
        self.hp -= 1
        return self.hp > 0


class HeartMark(pygame.sprite.Sprite):
    """Life remains"""

    animecycle = 1
    destroy_limit = 60

    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self, self.containers)

        self.image = self.images[0]

        self.rect = self.image.get_rect()
        self.rect.center = pos

        self.frame = 0
        self.max_frame = len(self.images) * self.animecycle  # a frame to rewind

        self.destroyed = False
        self.destroy_frame = 0

    def update(self):
        # Character Animation
        self.image = self.images[self.frame/self.animecycle]
        self.frame += 1
        if self.frame == self.max_frame:
            self.frame = 0

        if self.destroyed:
            if self.destroy_frame >= self.destroy_limit:
                self.kill()

            self.image = self.image.copy()
            #self.image.set_alpha(255*(1- self.destroy_frame/float(self.destroy_limit)))
            set_transparency_to_surf(self.image, 255*(1- self.destroy_frame/float(self.destroy_limit)))

            self.destroy_frame += 1

    def destroy(self):
        self.destroyed = True

class Explosion(pygame.sprite.Sprite):
    """Explosion effect"""

    animecycle = 2  # アニメーション速度
    max_frame = 16 * animecycle  # a frame to disappear

    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self, self.containers)

        self.image = self.images[0]

        self.rect = self.image.get_rect()
        self.rect.center = pos

        self.frame = 0

    def update(self):
        # Character Animation
        self.image = self.images[self.frame/self.animecycle]
        self.frame += 1
        if self.frame == self.max_frame:
            self.kill()  # disappear


class Gage(pygame.sprite.Sprite):
    """Score Gage"""

    pos = (21, 705)

    def __init__(self, gamedata):
        pygame.sprite.Sprite.__init__(self, self.containers)

        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos

        GageMask.containers = self.containers
        GageMask(gamedata, self.pos)

    def update(self):
        pass


class GageMask(pygame.sprite.Sprite):

    max_width = 387
    max_height = 17

    killedlimit = 100

    def __init__(self, gamedata, pos):
        pygame.sprite.Sprite.__init__(self, self.containers)

        self.image = pygame.Surface((self.max_width, self.max_height))
        self.image.fill((0,0,0))
        self.none_image = pygame.Surface((0,0))
        self.rect = self.image.get_rect()
        self.rect.topright = (pos[0]+2+self.max_width, pos[1]+2)

        self.topright = (pos[0]+2+self.max_width, pos[1]+2)
        self.gamedata = gamedata

    def update(self):

        if self.gamedata.weapon_mode == self.gamedata.SHOT:

            counter = self.gamedata.subshot_counter
            if counter >= self.killedlimit:
                self.image = self.none_image
                pressed_keys = pygame.key.get_pressed()
                if pressed_keys[K_SPACE]:
                    self.gamedata.weapon_mode = self.gamedata.SUBSHOT
                    self.gamedata.subshot_timer = self.gamedata.subshot_timelimit
            else:
                self.image = pygame.Surface((self.max_width*(1-float(counter)/self.killedlimit), self.max_height))
                self.image.fill((0,0,0))
                self.rect = self.image.get_rect()
                self.rect.topright = self.topright

        elif self.gamedata.weapon_mode == self.gamedata.SUBSHOT:

            counter = self.gamedata.subshot_timer
            self.image = pygame.Surface((self.max_width*(1-float(counter)/self.gamedata.subshot_timelimit), self.max_height))
            self.image.fill((0,0,0))
            self.rect = self.image.get_rect()
            self.rect.topright = self.topright

            if counter <= 0:
                self.gamedata.weapon_mode = self.gamedata.SHOT

