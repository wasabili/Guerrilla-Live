#!/usr/bin/env python
#-*- coding:utf-8 -*-

import pygame
from pygame.locals import *
import math
import random
import time
from collections    import deque

from lib.sprite     import *
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

    shot_reload_time = 5  #FIXME move to gamedata
    select_weapon_wait = 0.12

    def __init__(self, gamedata):
        # Create sprite groups
        self.play_all   = LayeredUpdates()          # Play screen
        self.enemies    = Group()                   # Enemy Group
        self.shots      = Group()                   # Beam Group
        self.bosses     = Group()                   # Bosses Group

        # Assign default sprite groups
        BackgroundPlay.containers   = self.play_all
        Player.containers           = self.play_all
        EColi.containers            = self.play_all, self.enemies
        EColi2.containers           = self.play_all, self.enemies
        BigEColi.containers         = self.play_all, self.enemies, self.bosses
        Shot.containers             = self.play_all, self.shots
        Bomb.containers             = self.play_all
        Explosion.containers        = self.play_all
        HeartMark.containers        = self.play_all
        Gage.containers             = self.play_all
        WeaponPanel.containers      = self.play_all
        DisplayWeapon.containers    = self.play_all

        # Create recycle boxes
        EColi.recyclebox        = deque()
        EColi2.recyclebox       = deque()
        Shot.recyclebox         = deque()
        Explosion.recyclebox    = deque()

        # Set Layer
        BackgroundPlay._layer   = -100
        Player._layer           = 100
        HeartMark._layer        = 200
        Explosion._layer        = 100
        Gage._layer             = 200
        GageMask._layer         = 201
        GageSeparator._layer    = 202
        WeaponPanel._layer      = 200
        DisplayWeapon._layer    = 200

        self.player = Player()
        self.bg_play = BackgroundPlay(gamedata.level)
        self.gage = Gage(gamedata)
        self.weaponpanel = WeaponPanel()
        self.dispweapon = DisplayWeapon(gamedata)

        self.gamedata = gamedata
        self.boss = None
        self.gameover = False
        self.gameend_timer = 150
        self.select_weapon_timer = 0
        self.bomb = None

        # Shot reloading
        self.shot_reload_timer = 0

    def update(self):
        self.play_all.update()


        # Manage game system
        if not self.gameover:
            self.manage_weapon_system()
            self.manage_enemies()
        else:
            self.gameend_timer -= 1


    def draw(self, screen):
        return self.play_all.draw(screen)

    def manage_weapon_system(self):
        """ Manage Weapon System"""

        if self.gamedata.weapon_mode == self.gamedata.SHOT:
            counter = self.gamedata.subweapon_counter

            # Weapon Panels
            if counter >= self.gamedata.gage_limit:
                self.weaponpanel.set_enable(0, True)
                self.weaponpanel.set_enable(1, True)
                self.weaponpanel.set_enable(2, True)
            elif counter*3 >= self.gamedata.gage_limit*2:
                self.weaponpanel.set_enable(0, True)
                self.weaponpanel.set_enable(1, True)
                self.weaponpanel.set_enable(2, False)
            elif counter*3 >= self.gamedata.gage_limit:
                self.weaponpanel.set_enable(0, True)
                self.weaponpanel.set_enable(1, False)
                self.weaponpanel.set_enable(2, False)

            # Select
            if time.clock() - self.select_weapon_timer > self.select_weapon_wait:
                if pygame.mouse.get_pressed()[2]:
                    self.weaponpanel.select_next()
                    self.select_weapon_timer = time.clock()

            # Launch
            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[K_SPACE]:
                selection = self.weaponpanel.get_selected()
                if selection == -1:
                    pass
                elif selection == 0:
                    self.gamedata.weapon_mode = self.gamedata.SUBSHOT
                    self.gamedata.subweapon_limiter = counter - self.gamedata.gage_limit/3
                    self.weaponpanel.set_enable(0, False)
                    self.weaponpanel.set_enable(1, False)
                    self.weaponpanel.set_enable(2, False)
                elif selection == 1:
                    self.gamedata.weapon_mode = self.gamedata.MACHINEGUN
                    self.gamedata.subweapon_limiter = counter - self.gamedata.gage_limit*2/3
                    self.weaponpanel.set_enable(0, False)
                    self.weaponpanel.set_enable(1, False)
                    self.weaponpanel.set_enable(2, False)
                elif selection == 2:
                    self.gamedata.weapon_mode = self.gamedata.BOMB
                    self.gamedata.subweapon_limiter = 0
                    self.weaponpanel.set_enable(0, False)
                    self.weaponpanel.set_enable(1, False)
                    self.weaponpanel.set_enable(2, False)
                    self.bomb = Bomb()

            # Reload
            self.shot_reload_timer -= 1

            # Shoot
            if pygame.mouse.get_pressed()[0] and self.shot_reload_timer <= 0:  # Not while reloading
                recycle_or_gen_object(Shot, player_pos, pygame.mouse.get_pos())
                self.shot_reload_timer = self.shot_reload_time

        elif self.gamedata.weapon_mode == self.gamedata.SUBSHOT:

            # Reload
            self.shot_reload_timer -= 1

            # Shoot
            if pygame.mouse.get_pressed()[0] and self.shot_reload_timer <= 0:  # Not while reloading
                TripleShot(player_pos, pygame.mouse.get_pos())
                self.shot_reload_timer = self.shot_reload_time

            # Time limit which a player is able to use this weapon
            self.gamedata.subweapon_counter -= 0.3
            if self.gamedata.subweapon_counter <= self.gamedata.subweapon_limiter:
                self.gamedata.subweapon_counter = self.gamedata.subweapon_limiter
                self.gamedata.weapon_mode = self.gamedata.SHOT
                self.weaponpanel.set_enable(0, False)

        elif self.gamedata.weapon_mode == self.gamedata.MACHINEGUN:

            # Reload
            self.shot_reload_timer -= 1

            # Shoot
            if pygame.mouse.get_pressed()[0] and self.shot_reload_timer <= 0:  # Not while reloading
                SextupleShot(player_pos, pygame.mouse.get_pos())
                self.shot_reload_timer = self.shot_reload_time

            # Time limit which a player is able to use this weapon
            self.gamedata.subweapon_counter -= 0.6
            if self.gamedata.subweapon_counter <= self.gamedata.subweapon_limiter:
                self.gamedata.subweapon_counter = self.gamedata.subweapon_limiter
                self.gamedata.weapon_mode = self.gamedata.SHOT
                self.weaponpanel.set_enable(1, False)

        elif self.gamedata.weapon_mode == self.gamedata.BOMB:

            if not self.bomb.alive():
                for enemy in self.enemies:
                    if not enemy.hit(30):  #FIXME
                        enemy.kill()
                        self.gamedata.killed_enemies(1)       # FIXME
                        recycle_or_gen_object(Explosion, enemy.rect.center) # Draw explosion
                self.gamedata.subweapon_counter = 0

            # Time limit which a player is able to use this weapon
            if self.gamedata.subweapon_counter <= self.gamedata.subweapon_limiter:
                self.gamedata.subweapon_counter = self.gamedata.subweapon_limiter
                self.gamedata.weapon_mode = self.gamedata.SHOT
                self.weaponpanel.set_enable(2, False)

    def manage_enemies(self):
        """ Manage enemies """

        # detect collision
        self.collision_detection()

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

    def collision_detection(self):
        """Detect collision"""

        """ Between enemies and shots """
        enemy_collided = groupcollide(self.enemies, self.shots, False, True)
        for enemy, shots in enemy_collided.items():
            if not enemy.hit(1):  #FIXME
                enemy.kill()                    # Kill an enemy
                self.gamedata.killed_enemies(1)       # FIXME
                recycle_or_gen_object(Explosion, shots[0].rect.center) # Draw explosion

        """ Between player and E.Colis """
        player_collided = spritecollide(self.player, self.enemies, True)
        if player_collided:
            if not self.player.killed_once(): # die once
                self.gamedata.result = self.gamedata.LOSE
                self.gameover = True

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

    def hasfinished(self):
        return self.gameover and self.gameend_timer < 0


class BackgroundPlay(Sprite):
    """Background follows player's move"""

    mag = 0.2

    def __init__(self, level):
        Sprite.__init__(self, self.containers)

        magged_size = (int(SCR_RECT.width*(1+self.mag)), int(SCR_RECT.height*(1+self.mag)))

        self.image = self.images[level-1]  # FIXME
        self.image = pygame.transform.scale(self.image, (magged_size[0], magged_size[1]))
        self.rect = self.image.get_rect()

        self.startx = -magged_size[0]*(self.mag/(1+self.mag))/2.0
        self.starty = -magged_size[1]*(self.mag/(1+self.mag))/2.0

    def update(self):
        pos = player_pos
        start = SCR_RECT.center

        self.rect.x = self.startx + (start[0] - pos[0])*self.mag
        self.rect.y = self.starty + (start[1] - pos[1])*self.mag


#########################################################################################
#                     PLAYER                                                            #
#########################################################################################


class Player(Sprite):
    """Own ship"""

    speed = 2
    accel = 0.15
    dynamic_fc = 0.05
    max_speed = 4
    # When the object is static, its friction coefficient is 0

    frame = 0L
    animecycle = 2

    lives = 0 #FIXME FIXME
    hearts = []
    invincible = -1
    blink_interval = 10

    def __init__(self):
        Sprite.__init__(self, self.containers)
        
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect = Rect(0, 0, self.rect.width*3/4, self.rect.height*3/4)  #FIXME TEST
        self.rect.center = CENTER

        self.hearts = [HeartMark((SCR_RECT.width - (60+60*x), SCR_RECT.height - (45+20))) for x in range(self.lives)]

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
        if self.lives >= 0:
            self.hearts.pop().destroy()                 # remove one heart
            self.invincible = 300                    # invincible time
            return True
        else:        # remains no life
            self.player_explosion = PlayerExplosion(player_pos)
            return False


    def is_invincible(self):
        return self.invincible >= 0

    def update(self):
        global player_pos

        # Character Animation
        self.image = self.images[self.frame/self.animecycle%len(self.images)]
        self.frame += 1

        if self.lives >= 0:

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
            elif SCR_RECT.left >= self.rect.left and self.fpvx < 0:
                self.fpvx = 0
            if SCR_RECT.top >= self.rect.top and self.fpvy < 0:
                self.fpvy = 0
            elif SCR_RECT.bottom <= self.rect.bottom and self.fpvy > 0:
                self.fpvy = 0

            self.fpx += self.fpvx
            self.fpy += self.fpvy
            self.rect.x = int(self.fpx)
            self.rect.y = int(self.fpy)
            self.rect.clamp_ip(SCR_RECT)

            player_pos = self.rect.center

        else:

            self.player_explosion.update()


#########################################################################################
#                     WEAPONS                                                           #
#########################################################################################


class Shot(Sprite):
    """プレイヤーが発射するビーム"""

    speed = 9  # 移動速度

    def __init__(self, start, target=None, degree=None):
        Sprite.__init__(self, self.containers)

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
        Sprite.kill(self)
        self.__class__.recyclebox.append(self)


class TripleShot():
    """プレイヤーが発射するビーム x3"""

    def __init__(self, start, target):
        direction = math.atan2(target[1]-start[1], target[0]-start[0])
        degree = -180*direction/math.pi
        recycle_or_gen_object(Shot, start, None, degree)
        recycle_or_gen_object(Shot, start, None, degree+120 if degree+120<180 else degree-240)
        recycle_or_gen_object(Shot, start, None, degree+240 if degree+240<180 else degree-120)
        del self
        

class SextupleShot():
    """プレイヤーが発射するビーム x6"""

    def __init__(self, start, target):
        direction = math.atan2(target[1]-start[1], target[0]-start[0])
        degree = -180*direction/math.pi
        recycle_or_gen_object(Shot, start, None, degree)
        recycle_or_gen_object(Shot, start, None, degree+60 if degree+60<180 else degree-300)
        recycle_or_gen_object(Shot, start, None, degree+120 if degree+120<180 else degree-240)
        recycle_or_gen_object(Shot, start, None, degree+180 if degree+180<180 else degree-180)
        recycle_or_gen_object(Shot, start, None, degree+240 if degree+240<180 else degree-120)
        recycle_or_gen_object(Shot, start, None, degree+300 if degree+300<180 else degree-60)
        del self

class Bomb(Sprite):

    speed = 30

    def __init__(self):
        Sprite.__init__(self, self.containers)

        self.base_img = pygame.Surface(SCR_RECT.size, SRCALPHA|HWSURFACE)
        self.image = self.base_img.copy()
        self.rect = SCR_RECT    

        self.start = player_pos
        self.radius = 5
        self.width = 1

    def update(self):
        self.image = self.base_img.copy()
        pygame.draw.circle(self.image, (255,255,255), self.start, self.radius, self.width)

        self.radius += self.speed

        if self.radius > 1280:
            self.kill()


#########################################################################################
#                     ENEMIES                                                           #
#########################################################################################


class EColi(Sprite):
    """E.Coli"""

    speed = 1.2  # 移動速度
    animecycle = 18  # アニメーション速度

    def __init__(self, pos):
        Sprite.__init__(self, self.containers)

        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.center = pos

        # 速度を計算
        self.fpx = float(self.rect.x)
        self.fpy = float(self.rect.y)

        self.hp = 1
        self.frame = 0

    def init(self, pos):
        # set pos
        self.frame = 0
        self.rect.center = pos
        self.fpx = float(self.rect.x)
        self.fpy = float(self.rect.y)

        # reborn
        self.add(self.containers)

    def update(self):

        # Character Animation FIXME
        self.frame += 1
        self.image = self.images[self.frame/self.animecycle%len(self.images)]

        # 終点の角度を計算
        target = player_pos
        start = self.rect.center
        direction = math.atan2(target[1]-start[1], target[0]-start[0])

        # rotate
        self.image = pygame.transform.rotate(self.image, -180*direction/math.pi)

        # Move
        fpvx = math.cos(direction) * self.speed
        fpvy = math.sin(direction) * self.speed
        self.fpx += fpvx
        self.fpy += fpvy
        self.rect.x = int(self.fpx)
        self.rect.y = int(self.fpy)

    def hit(self, p):

        # Player's shot hit me!
        self.hp -= p
        return self.hp > 0

    def kill(self):
        Sprite.kill(self)
        self.__class__.recyclebox.append(self)


class EColi2(Sprite):
    """E.Coli2"""

    start_hp = 3
    speed = 0.4  # 移動速度

    animecycle = 10

    def __init__(self, pos):
        Sprite.__init__(self, self.containers)

        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.center = pos

        # 速度を計算
        self.fpx = float(self.rect.x)
        self.fpy = float(self.rect.y)

        self.frame = 0
        self.blink_timer = -1
        self.hp = self.start_hp

    def init(self, pos):
        # set pos
        self.rect.center = pos
        self.fpx = float(self.rect.x)
        self.fpy = float(self.rect.y)
        self.hp = self.start_hp

        self.blink_timer = 0
        self.frame = 0

        # reborn
        self.add(self.containers)

    def update(self):

        if self.blink_timer > 0:
            self.frame += 1
            self.blink_timer -= 1
            self.image = self.images[(self.frame/self.animecycle)%2]
        elif self.blink_timer == 0:
            self.image = self.images[0]
            self.blink_timer -= 1
        else:
            self.image = self.images[0]

        # 終点の角度を計算
        target = player_pos
        start = self.rect.center
        direction = math.atan2(target[1]-start[1], target[0]-start[0])

        # rotate
        self.image = pygame.transform.rotate(self.image.copy(), -180*direction/math.pi)

        # Move
        fpvx = math.cos(direction) * self.speed
        fpvy = math.sin(direction) * self.speed
        self.fpx += fpvx
        self.fpy += fpvy
        self.rect.x = int(self.fpx)
        self.rect.y = int(self.fpy)

    def hit(self, p):

        # Player's shot hit me!
        self.hp -= p
        self.blink_timer = 40
        return self.hp > 0

    def kill(self):
        Sprite.kill(self)
        self.__class__.recyclebox.append(self)


class BigEColi(Sprite):
    """Sample Boss: no attaching and no animation"""

    speed = 2  # 移動速度
    hp = 100
    animecycle = 10
    angle = 180
    animechap = 0
    roundr = 100
    point1 = (150, SCR_RECT.height/2)
    point2 = (point1[0]+roundr, point1[1])  # The center of the round
    av = 0  # Angular velocity

    def __init__(self):
        Sprite.__init__(self, self.containers)

        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect = Rect(self.rect.width*1/8, self.rect.height*1/8, self.rect.width*3/4, self.rect.height*3/4)  #TODO test
        self.rect.center = (-self.rect.width/2, -self.rect.height/2)

        # Calculate speed
        self.fpx = float(self.rect.center[0])
        self.fpy = float(self.rect.center[1])

        # 終点の角度を計算
        self.target = self.point1
        self.start = self.rect.center
        self.direction = math.atan2(self.target[1]-self.start[1], self.target[0]-self.start[0])

        # Move
        self.fpvx = math.cos(self.direction) * self.speed
        self.fpvy = math.sin(self.direction) * self.speed

        # Calculate Angular Velocity
        self.av = self.speed/(2*math.pi*self.roundr/360.0)

        self.frame = 0
        self.blink_timer = -1

    def update(self):

        # Blinking
        if self.blink_timer > 0:
            self.frame += 1
            self.blink_timer -= 1
            self.image = self.images[(self.frame/self.animecycle)%2]
        elif self.blink_timer == 0:
            self.image = self.images[0]
            self.blink_timer -= 1
        else:
            self.image = self.images[0]


        if self.animechap == 0:

            self.fpx = min(self.fpx + self.fpvx, self.point1[0])
            self.fpy = min(self.fpy + self.fpvy, self.point1[1])
            self.rect.center = (int(self.fpx), int(self.fpy))

            if self.rect.center == (int(self.point1[0]), int(self.point1[1])):
                self.animechap = 1

        elif self.animechap == 1:

            vx = math.cos(self.angle/180.0*math.pi) * self.roundr
            vy = math.sin(self.angle/180.0*math.pi) * self.roundr

            self.rect.center = (int(self.point2[0] + vx), int(self.point2[1] - vy))

            self.angle += self.av
            
    def hit(self, p):

        # Player's shot hit me!
        self.hp -= p
        self.blink_timer = 40
        return self.hp > 0


#########################################################################################
#                     EFFECT                                                            #
#########################################################################################


class Explosion(Sprite):
    """Explosion effect"""

    animecycle = 2  # アニメーション速度
    max_frame = 16 * animecycle  # a frame to disappear

    def __init__(self, pos):
        Sprite.__init__(self, self.containers)

        self.image = self.images[0]

        self.rect = self.image.get_rect()
        self.rect.center = pos

        self.frame = 0

    def init(self, pos):
        self.image = self.images[0]
        self.rect.center = pos
        self.frame = 0
        self.add(self.containers)

    def update(self):
        # Character Animation
        self.image = self.images[self.frame/self.animecycle]
        self.frame += 1
        if self.frame == self.max_frame:
            self.kill()  # disappear

    def kill(self):
        Sprite.kill(self)
        self.__class__.recyclebox.append(self)


class PlayerExplosion():
    """Player Explosion"""

    step = 10 #24
    side = 30

    def __init__(self, pos):
        self.pos = pos
        self.frames = 0

    def update(self):

        if self.frames % self.step == 0:
            v = int(random.random()*self.side)-10
            h = int(random.random()*self.side)-10
            e = Explosion((self.pos[0]+v, self.pos[1]+h))

        self.frames += 1


#########################################################################################
#                     SYSTEM                                                            #
#########################################################################################


class HeartMark(Sprite):
    """Life remains"""

    animecycle = 1
    destroy_limit = 60

    def __init__(self, pos):
        Sprite.__init__(self, self.containers)
        self.dirty = 2

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
            set_transparency_to_surf(self.image, 255*(1- self.destroy_frame/float(self.destroy_limit)))

            self.destroy_frame += 1

    def destroy(self):
        self.destroyed = True


class Gage(Sprite):
    """Score Gage"""

    pos = (28, 738)

    def __init__(self, gamedata):
        Sprite.__init__(self, self.containers)

        self.image = self.image_red
        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos

        # Mask
        GageMask.containers = self.containers
        self.gagemask = GageMask(gamedata, self.pos)

        # Separators
        GageSeparator.containers = self.containers
        self.gagesep1 = GageSeparator((350, self.pos[1]+1))
        self.gagesep2 = GageSeparator((671, self.pos[1]+1))

        self.gamedata = gamedata
        self.lastweapon = self.gamedata.SHOT

    def update(self):
        if self.gamedata.weapon_mode == self.lastweapon:
            return

        elif self.gamedata.weapon_mode == self.gamedata.SHOT:
            self.image = self.image_red
            self.lastweapon = self.gamedata.weapon_mode
            self.dirty = 1
        else:
            self.image = self.image_blue
            self.lastweapon = self.gamedata.weapon_mode
            self.dirty = 1


class GageMask(Sprite):

    max_width = 964
    max_height = 5
    border_length = 2

    def __init__(self, gamedata, pos):
        Sprite.__init__(self, self.containers)

        self.image = pygame.Surface((self.max_width, self.max_height))
        self.image.fill((0,0,0))
        self.none_image = pygame.Surface((0,0))
        self.rect = self.image.get_rect()
        self.topright = (pos[0]+self.border_length+self.max_width, pos[1]+self.border_length)
        self.rect.topright = self.topright

        self.percent = 0
        self.gamedata = gamedata

    def update(self):
        self.dirty = 1

        self.percent = float(self.gamedata.subweapon_counter)/self.gamedata.gage_limit

        self.image = pygame.Surface((self.max_width*(1-self.percent), self.max_height))
        self.image.fill((0,0,0))
        self.rect = self.image.get_rect()
        self.rect.topright = self.topright


class GageSeparator(Sprite):

    def __init__(self, pos):
        Sprite.__init__(self, self.containers)

        self.rect = self.image.get_rect()
        self.rect.topleft = pos


class WeaponPanel():

    pos = (638, 638-40, 638-40*2)

    def __init__(self):
        WeaponPanelPart.containers  = self.containers
        WeaponPanelPart._layer      = self._layer

        self.parts = []
        self.parts.append(WeaponPanelPart(self.images[0], self.pos[0]))
        self.parts.append(WeaponPanelPart(self.images[1], self.pos[1]))
        self.parts.append(WeaponPanelPart(self.images[2], self.pos[2]))

        WeaponSelector.containers   = self.containers
        WeaponSelector._layer       = self._layer

        self.selector = WeaponSelector()
        self.selection = -1

    def set_enable(self, index, enable):
        self.parts[index].set_enable(enable)
        if not enable and index == self.selection:
            self.select_next()

    def get_enable(self, index):
        return self.parts[index].get_enable()

    def select_next(self):
        print 'called: select_next()'
        for i in range(1, 4):
            self.selection = (self.selection+1)%3
            if self.get_enable(self.selection):
                print 'selected: '+str(self.selection)
                self.selector.change(self.pos[self.selection])
                break        
        else:
            print 'none is selected'
            self.selection = -1
            self.selector.hide()

    def get_selected(self):
        return self.selection


class WeaponPanelPart(DirtySprite):

    speed = 5

    def __init__(self, image, y):
        DirtySprite.__init__(self, self.containers)

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topright = (0, y)

        self.max_x = self.image.get_width()
        self.min_x = 0

        self.x = self.min_x
        self.vx = 0

        self.enabled = False

    def get_enable(self):
        return self.enabled

    def set_enable(self, enable):
        self.enabled = enable
        if enable:
            self.vx = self.speed
        else:
            self.vx = -self.speed

    def update(self):
        self.dirty = 1

        self.rect.right = self.x

        if self.vx != 0:
            self.dirty = 1

            n = self.x + self.vx
            if n < self.min_x:
                self.x = self.min_x
                self.vx = 0
            elif n > self.max_x:
                self.x = self.max_x
                self.vx = 0
            else:
                self.x = n


class WeaponSelector(DirtySprite):

    animecycle = 4
    x = 160

    def __init__(self):
        DirtySprite.__init__(self, self.containers)
        self.dirty = 2

        # Create images
        self.arrow_dark = self.image.copy()
        self.arrow_none = pygame.Surface((0,0), HWSURFACE)

        self.rect = self.image.get_rect()
        self.image = self.arrow_none
        self.frame = 0
        self.visible = False

    def update(self):

        if self.visible:
            if self.frame/self.animecycle%2 == 0:
                self.image = self.arrow_dark
            else:
                self.image = self.arrow_none
            self.frame += 1

    def change(self, y):

        self.rect.x = self.x
        self.rect.y = y
        self.visible = True

    def hide(self):
        self.image = self.arrow_none
        self.visible = False

class DisplayWeapon(Sprite):

    pos = (20, 738-70)

    def __init__(self, gamedata):
        Sprite.__init__(self, self.containers)
        self.dirty = 2

        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos

        self.gamedata = gamedata

    def update(self):
        if self.gamedata.weapon_mode == self.gamedata.SHOT:
            self.image = self.images[0]
        elif self.gamedata.weapon_mode == self.gamedata.SUBSHOT:
            self.image = self.images[1]
        elif self.gamedata.weapon_mode == self.gamedata.MACHINEGUN:
            self.image = self.images[2]
        elif self.gamedata.weapon_mode == self.gamedata.BOMB:
            self.image = self.images[3]

