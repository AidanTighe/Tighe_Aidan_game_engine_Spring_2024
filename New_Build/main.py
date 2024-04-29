# This file was created by: Chris Cozort

# import libraries and modules
import pygame as pg
from settings import *
from sprites import *
from random import randint
import sys
from os import path
import time
from tilemap import *


'''
BETA GOAL:
Primary:
-Add Levels
Secondary
-Fix wall collisions
-Make good spritesdddd
'''
LEVEL1 = "level1.txt"
LEVEL2 = "level2.txt"
LEVEL3 = "level3.txt"
LEVEL4 = "level4.txt"
LEVEL5 = "level5.txt"
LEVEL6 = "level6.txt"
LEVEL7 = "level7.txt"


levels = [LEVEL1, LEVEL2, LEVEL3, LEVEL4,LEVEL5,LEVEL6,LEVEL7]

# Define game class...
class Game:
    # Define a special method to init the properties of said class...
    def __init__(self):
        # init pygame
        pg.init()
        pg.mixer.init()
        # set size of screen and be the screen
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        # setting game clock 
        self.clock = pg.time.Clock()
        self.load_data()
        #self.running = True
        self.death = False
        self.current_level = 0
    def load_data(self):
        self.game_folder = path.dirname(__file__)
        self.img_folder = path.join(self.game_folder, 'images')
        self.map = Map(path.join(game_folder, 'level1.txt'))
        self.coin_img = pg.image.load(path.join(self.img_folder, 'CoiN.png')).convert_alpha()
        self.wblock_img = pg.image.load(path.join(self.img_folder, 'finish.png')).convert_alpha()
        self.spotion_img = pg.image.load(path.join(self.img_folder, 'SPotion.png')).convert_alpha()
        # self.lvl1_data = []
        '''
        The with statement is a context manager in Python. 
        It is used to ensure that a resource is properly closed or released 
        after it is used. This can help to prevent errors and leaks.
        '''
        # with open(path.join(self.game_folder, 'lvl1.txt'), 'rt') as f:
        #     for line in f:
        #         print(line)
        #         self.lvl1_data.append(line)

    # Create run method which runs the whole GAME
    def change_level(self, lvl):
        for s in self.all_sprites:
            s.kill()
        self.player.moneybag = 0
        self.map_data = []
        with open(path.join(self.game_folder, lvl), 'rt') as f:
            for line in f:
                print(line)
                self.map_data.append(line)
        for row, tiles in enumerate(self.map.data):
            print(row)
            for col, tile in enumerate(tiles):
                print(col)
                if tile == '1':
                    print("a wall at", row, col)
                    Wall(self, col, row)
                if tile == '2':
                    print("a wallie at", row, col)
                    Wallie(self, col, row)
                if tile == 'P':
                    self.player = Player(self, col, row)
                if tile == 'C':
                    Coin(self, col, row)
                if tile == 'S':
                   SPotion(self, col, row)
                if tile == 'M':
                    LWall(self, col, row)
                if tile == 'w':
                    CWall(self, col, row)
                if tile == 'W':
                    WBlock1(self, col, row)
                if tile == 'B':
                    WBlock2(self, col, row)
                if tile == 'b':
                    WBlock3(self, col, row)
    def new(self):
        self.load_data()
        print("create new game...")
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.wallies = pg.sprite.Group()
        self.coins = pg.sprite.Group()
        self.spotions = pg.sprite.Group()
        self.lwalls = pg.sprite.Group()
        self.wblock1s = pg.sprite.Group()
        self.wblock2s = pg.sprite.Group()
        self.wblock3s = pg.sprite.Group()
        self.cwalls = pg.sprite.Group()
        # self.player1 = Player(self, 1, 1)
        # for x in range(10, 20):
        #     Wall(self, x, 5)
        for row, tiles in enumerate(self.map.data):
            print(row)
            for col, tile in enumerate(tiles):
                print(col)
                if tile == '1':
                    print("a wall at", row, col)
                    Wall(self, col, row)
                if tile == '2':
                    print("a wallie at", row, col)
                    Wallie(self, col, row)
                if tile == 'P':
                    self.player = Player(self, col, row)
                if tile == 'C':
                    Coin(self, col, row)
                if tile == 'S':
                   SPotion(self, col, row)
                if tile == 'M':
                    LWall(self, col, row)
                if tile == 'w':
                    CWall(self, col, row)
                if tile == 'W':
                    WBlock1(self, col, row)
                if tile == 'B':
                    WBlock2(self, col, row)
                if tile == 'b':
                    WBlock3(self, col, row)

    def run(self):
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def quit(self):
         pg.quit()
         sys.exit()
    

    def update(self):
        self.all_sprites.update()
        if self.player.moneybag > 2:
                self.current_level += 1
                self.change_level(levels[self.current_level])
                
    
    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
              pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
              pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))
    def draw_text(self, surface, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        surface.blit(text_surface, text_rect)
    def draw(self):
        self.screen.fill(BGCOLOR)
        #self.screen.blit(self.background_img, self.background_rect)
        self.draw_grid()
        self.all_sprites.draw(self.screen)
        self.draw_text(self.screen, str(self.player.moneybag), 64, WHITE, 1, 1)

        pg.display.flip()

    def events(self):
         for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            # if event.type == pg.KEYDOWN:
            #     if event.key == pg.K_LEFT:
            #         self.player.move(dx=-1)
            #     if event.key == pg.K_RIGHT:
            #         self.player.move(dx=1)
            #     if event.key == pg.K_UP:
            #         self.player.move(dy=-1)
            #     if event.key == pg.K_DOWN:
            #         self.player.move(dy=1)

    def show_start_screen(self):
        self.screen.fill(BGCOLOR)
        self.draw_text(self.screen, "To Begin the Game click any key", 24, WHITE, WIDTH/2, HEIGHT/2)
        pg.display.flip()
        self.wait_for_key()

    def show_end_screen(self):
        self.screen.fill(RED)
        self.draw_text(self.screen, "You Died a Horrifically Painful Death", 24, BLACK, WIDTH/2, HEIGHT/2)
        pg.display.flip()
        self.wait_for_losekey()
        sys.exit()
    
    def show_win_screen(self):
        self.screen.fill(GREEN)
        self.draw_text(self.screen, "You beat the level, congrats", 24, BLACK, WIDTH/2, HEIGHT/2)
        pg.display.flip()
        self.wait_for_winkey()
        sys.exit()

    def wait_for_winkey(self):
        waiting = True
        while waiting:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.quit()
    
    def wait_for_losekey(self):
        waiting = True
        while waiting:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.quit()

    def wait_for_key(self):
        waiting = True
        while waiting:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.quit()
                if event.type == pg.KEYUP:
                    waiting = False

# Instantiate the game... 
g = Game()
# use game method run to run
g.show_start_screen()
while True:
    g.new()
    
    g.run()

