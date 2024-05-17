# This file was created by: Aidan Tighe
import pygame as pg
from settings import *
from utils import *
from random import choice
from random import randint
from os import path
from math import *
from math import degrees

vec =pg.math.Vector2


game_folder = path.dirname(__file__)
img_folder = path.join(game_folder, 'images')

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        # init super class
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.spritesheet = Spritesheet(path.join(img_folder, 'Player.png'))
        self.load_images()
        # self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.vx, self.vy = 0, 0
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.moneybag = 0
        self.current_frame = 0
        self.last_update = 0
        self.speed = 210
        self.can_collide = True

    def load_images(self):
        self.standing_frames = [self.spritesheet.get_image(0, 0, 32, 32), 
                                self.spritesheet.get_image(32, 0, 32, 32)]
            
    def animate(self):
        now = pg.time.get_ticks()
        if now - self.last_update > 350:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
            bottom = self.rect.bottom
            self.image = self.standing_frames[self.current_frame]
            self.rect = self.image.get_rect()
            self.rect.bottom = bottom
    
    def get_keys(self):
        self.vx, self.vy = 0, 0
        keys = pg.key.get_pressed()
            
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vx = -self.speed  
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vx = self.speed  
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vy = -self.speed  
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vy = self.speed
        if self.vx != 0 and self.vy != 0:
            self.vx *= 0.7071
            self.vy *= 0.7071

    # def move(self, dx=0, dy=0):
    #     if not self.collide_with_walls(dx, dy):
    #         self.x += dx
    #         self.y += dy

    # def collide_with_walls(self, dx=0, dy=0):
    #     for wall in self.game.walls:
    #         if wall.x == self.x + dx and wall.y == self.y + dy:
    #             return True
    #     return False
            
    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y

    def collide_with_wallies(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.wallies, False)
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.wallies, False)
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y

    def collide_with_group(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits:
            if str(hits[0].__class__.__name__) == "Coin":
                self.moneybag += 1         
        if hits:
            if str(hits[0].__class__.__name__) == "SPotion":
                self.speed += 500
        if hits:
            if str(hits[0].__class__.__name__) == "LWall":
                self.game.show_end_screen()
        if hits:
            if str(hits[0].__class__.__name__) == "WBlock1":
                self.moneybag += 1 
        if hits:
            if str(hits[0].__class__.__name__) == "Mob":
                self.game.show_end_screen()
                
                
                

    def update(self):
        self.animate()
        self.get_keys()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        if self.can_collide == True:
            self.collide_with_walls('x')
        self.rect.y = self.y
        if self.can_collide == True:
            self.collide_with_walls('y')
            
        self.rect.y = self.y
        if self.can_collide == True:
            self.collide_with_wallies('y')
        self.rect.x = self.x
        if self.can_collide == True:
            self.collide_with_wallies('x')
        

        self.collide_with_group(self.game.coins, True)
        self.collide_with_group(self.game.spotions, True)
        self.collide_with_group(self.game.lwalls, True)
        self.collide_with_group(self.game.wblock1s, True)
        self.collide_with_group(self.game.mobs, True)
        self.collide_with_group(self.game.wallies, True)


    # def update(self):
    #     self.animate()
    #     self.get_keys()
    #     self.x += self.vx * self.game.dt
    #     self.y += self.vy * self.game.dt

    #     self.rect.x = self.x
    #     self.collide_with_wallies('x')
    #     self.rect.y = self.y
    #     self.collide_with_wallies('y')

class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Wallie(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.wallies
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class CWall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.ad = 1
        self.speed = 0

    def move(self):  
        if self.game.player.moneybag >= 2:
            while self.ad != 50:
                self.rect.x += self.ad
                self.ad += 1

    def update(self):
        self.move()

class Coin(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.coins
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        # self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image = self.game.coin_img
        # self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class SPotion(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.spotions
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        # self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image = self.game.spotion_img
        # self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE


class WBlock1(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.wblock1s
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        # self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image = self.game.wblock_img
        # self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class LWall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.lwalls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE * 5, TILESIZE))
        self.surface = pg.Surface((TILESIZE * 5, TILESIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.ad = -7.5

    def move(self):
        self.y += self.ad

    def collide_with_walls(self, dir):
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                self.ad = self.ad * -1
                self.y = self.rect.y
                self.move()


    def update(self):
        self.move()
        self.rect.x = self.x
        self.collide_with_walls('x')
        self.rect.y = self.y
        self.collide_with_walls('y')

class Mob(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        # self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image = self.game.invisable_img
        # self.image.fill(BGCOLOR)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.pos = vec(x, y) * TILESIZE
        
    def move(self):
            #pythag formula for making enemy
            self.distance_x = self.game.player.x - self.rect.x
            self.distance_y = self.game.player.y - self.rect.y
            self.distance = (self.distance_x ** 2 + self.distance_y ** 2) ** 0.5
   
            #make stop chasing
            if self.distance >= 250 or self.distance <= 5:
                self.speed = 0
            elif self.distance <= 200:
                self.speed = 1
   
            #make enemy "chase" player
            if self.distance != 0:
                self.rect.x += self.speed * self.distance_x / self.distance
                self.rect.y += self.speed * self.distance_y / self.distance
 
    def move(self):
            #pythag formula for making enemy
            self.distance_x = self.game.player.x - self.rect.x
            self.distance_y = self.game.player.y - self.rect.y
            self.distance = (self.distance_x ** 2 + self.distance_y ** 2) ** 0.5
   
            #make stop chasing
            if self.distance >= 250 or self.distance <= 5:
                self.speed = 0
            elif self.distance <= 200:
                self.speed = 4
   
            #make enemy "chase" player
            if self.distance != 0:
                self.rect.x += self.speed * self.distance_x / self.distance
                self.rect.y += self.speed * self.distance_y / self.distance
 
    def update(self):
        self.x = self.rect.x
        self.y = self.rect.y
        self.move()
