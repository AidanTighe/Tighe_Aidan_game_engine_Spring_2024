# this file was create by: Aidan Tighe

# we are importing librarys 
import pygame as pg 
from settings import *
from sprites import *
import sys
from random import randint
from os import path

# added math function for clock
from math import floor
# create a game class
class Game:
    # initializes __init__
    def __init__(self):
        pg.init()
        pg.mixer.init()
        # WIDTH and HEIGHT are varibles imported from settings
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        # makes the string "My first Video Game" the caption
        pg.display.set_caption("My First Video Game")
        # Clock(): class that tracks time using ticks
        self.clock = pg.time.Clock()
        #pg.key.set_repeat(500, 100)
        #self.running = True
        #self.playing = True
        #run Method 
        #later on will store data game info
        self.load_data()
    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'images')
        self.player_img = pg.image.load(path.join(img_folder, 'Coin.png')).convert_alpha()
        self.player_img2 = pg.image.load(path.join(img_folder, 'SpeedPotion.png')).convert_alpha() 
        self.map_data = [] 
        '''
        The with statement is a context manager in Python. 
        It is used to ensure that a resource is properly closed or released 
        after it is used. This can help to prevent errors and leaks.
        '''
        with open(path.join(game_folder, 'map.txt'), 'rt') as f:
            for line in f:
                print(line)
                self.map_data.append(line)
                print(self.map_data)

    def test_method(self):
        print("I can be called from Sprites...")

    def new(self):
        
        self.cooldown = Timer(self)
        print("create new game...")
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.potions = pg.sprite.Group()
        self.coins = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        # self.player = Player(self, 10, 10)
        # self.all_sprites.add(self.player)
        #for x in range(10, 20):
            #Wall(self, x, 5)
        for row, tiles in enumerate(self.map_data):
            print(row)
            for col, tile in enumerate(tiles):
                print(col)
                if tile == '1':
                    print("a wall at", row, col)
                    Wall(self, col, row)
                if tile == 'P':
                    self.player = Player(self, col, row)
                if tile == 'z':
                    self.speedpotion = SpeedPotions(self, col, row)
                if tile == 'C':
                    Coin(self, col, row)
                if tile == 'm':
                    Mob(self, col, row)

            

            
    def run(self):
        self.playing= True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            # this is input
            self.events()
            # this is processing
            # this is output
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()
    # method     
    def update(self):
        self.cooldown.ticking()
        self.all_sprites.update()

    #makes a grid for a square to go between
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
        text_rect.topleft = (x,y)
        surface.blit(text_surface, text_rect)

    def draw(self):
        self.screen.fill(BGCOLOR)
        #self.draw_grid()
        self.all_sprites.draw(self.screen)
        self.draw_text(self.screen, str(self.cooldown.current_time), 24, WHITE, WIDTH/2 - 32, 2)
        self.draw_text(self.screen, str(self.cooldown.event_time), 24, WHITE, WIDTH/2 - 32, 80)
        self.draw_text(self.screen, str(self.cooldown.get_countdown()), 24, WHITE, WIDTH/2 - 32, 120)
        self.draw_text(self.screen, str(self.player.moneybag), 64, WHITE, 1, 1)
        pg.display.flip()
    def events(self):
            # listening for events
            for event in pg.event.get():
                # when you hit the red x the window closes and the game ends
                if event.type == pg.QUIT:
                    self.quit()
                # keyboard events(dictating player's movement)
                # gets inputs from the keyboard arrows and tells it what to do(move)
                # if event.type == pg.KEYDOWN:
                #     if event.key == pg.K_LEFT or event.key == pg.K_a:
                #         self.player.move(dx=-1)
                # if event.type == pg.KEYDOWN:
                #     if event.key == pg.K_RIGHT or event.key == pg.K_d:
                #         self.player.move(dx=1)
                # if event.type == pg.KEYDOWN:
                #     if event.key == pg.K_UP or event.key == pg.K_w:
                #         self.player.move(dy=-1)
                # if event.type == pg.KEYDOWN:
                #     if event.key == pg.K_DOWN or event.key == pg.K_s:
                #         self.player.move(dy=1)
    def show_start_screen(self):
        self.screen.fill(BGCOLOR)
        self.draw_text(self.screen, "This is the start screen - press any key to play", 24, WHITE, WIDTH/2, HEIGHT/2)
        pg.display.flip()
        self.wait_for_key()
    
    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.quit()
                if event.type == pg.KEYUP:
                    waiting = False
    
############################################## Instantiate game... ################################
# assigns Game to a varible, g
g = Game()
# Runs the class Game
# g.show_go_screen()
while True:
    g.new()
    g.run()
    # g.show_go_screen()