import pygame
from pygame.locals import *
import os
import sys
import pickle
import json
import random
import math

FPS = 30.0
DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 600
UFO_RANDRANGE = 1000
INVADER_FALL_DY = 5
INVADER_DY = 20
PLAYER_SHOT_DY = 10
INVADER_SHOT_DY = 5
HORIZONTAL_MARGIN = 25


class Colors:
    """This class stores all game colors"""
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    DARK_GREY = (43, 43, 43)
    LIGHT_GREY = (195, 195, 195)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    BLUE2 = (63, 72, 204)
    CYAN = (153, 217, 234)
    PURPLE = (163, 73, 164)
    YELLOW = (255, 242, 0)


class Resources:
    """This class stores all game resources"""
    ValidChars = "`1234567890-=qwertyuiop[]\\asdfghjkl;'zxcvbnm,./"
    ShiftChars = '~!@#$%^&*()_+QWERTYUIOP{}|ASDFGHJKL:"ZXCVBNM<>?'

    FONT1 = 1
    Fonts = {
        FONT1: {'name': 'Font1', 'file': 'resource/PixelEmulator.otf'}
    }

    PROGRAM_ICON = 1
    Icons = {
        PROGRAM_ICON: {'name': 'Program Icon', 'file': 'resource/red0.png'}
    }

    MAIN_BACKGROUND = 1
    HELP_BACKGROUND = 2
    HIGH_BACKGROUND = 3
    Backgrounds = {
        MAIN_BACKGROUND: {'name': 'Main Background', 'file': 'resource/main.png'},
        HELP_BACKGROUND: {'name': 'Help Background', 'file': 'resource/help.png'},
        HIGH_BACKGROUND: {'name': 'High Background', 'file': 'resource/high.png'}
    }

    INVADER1 = 1
    INVADER2 = 2
    INVADER3 = 3
    UFO1 = 4
    UFO2 = 5
    BRICK = 6
    EXPLOSION = 7
    PLAYER = 8
    Sprites = {
        INVADER1: {'name': 'yellow invader', 'files': ['resource/yellow0.png', 'resource/yellow1.png'], 'color': Colors.YELLOW, 'points': 5, 'step': None},
        INVADER2: {'name': 'purple invader', 'files': ['resource/purple0.png', 'resource/purple1.png'], 'color': Colors.PURPLE, 'points': 10, 'step': None},
        INVADER3: {'name': 'red invader', 'files': ['resource/red0.png', 'resource/red1.png'], 'color': Colors.RED, 'points': 15, 'step': None},
        UFO1: {'name': 'ufo1', 'files': ['resource/ufoa0.png', 'resource/ufoa1.png'], 'color': Colors.CYAN, 'points': 500, 'step': 5},
        UFO2: {'name': 'ufo2', 'files': ['resource/ufob0.png', 'resource/ufob1.png'], 'color': Colors.BLUE2, 'points': 1000, 'step': 7},
        BRICK: {'name': 'brick', 'files': ['resource/brick0.png', 'resource/brick1.png'], 'color': None, 'points': 5, 'step': None},
        EXPLOSION: {'name': 'explosion', 'files': ['resource/explosion0.png', 'resource/explosion1.png'], 'color': None, 'points': 0, 'step': None},
        PLAYER: {'name': 'player', 'files': ['resource/player.png'], 'color': Colors.GREEN, 'points': 0, 'step': 9}
    }


class Data:
    """This class handles game files"""
    SLOT1 = 1
    SLOT2 = 2
    SLOT3 = 3
    SavedGames = {
        SLOT1: {'name': 'Slot 1', 'player': 'Empty', 'level': 1, 'credits:': 0, 'score': 0},
        SLOT2: {'name': 'Slot 2', 'player': 'Empty', 'level': 1, 'credits:': 0, 'score': 0},
        SLOT3: {'name': 'Slot 3', 'player': 'Empty', 'level': 1, 'credits:': 0, 'score': 0}
    }

    HIGHSCORE1 = 1
    HIGHSCORE2 = 2
    HIGHSCORE3 = 3
    HIGHSCORE4 = 4
    Highscores = {
        HIGHSCORE1: {'score': 0, 'name': 'Empty'},
        HIGHSCORE2: {'score': 0, 'name': 'Empty'},
        HIGHSCORE3: {'score': 0, 'name': 'Empty'},
        HIGHSCORE4: {'score': 0, 'name': 'Empty'}
    }

    @staticmethod
    def save_slots():
        file = open('resource/slots.pkl', mode='wb')
        pickle.dump(Data.SavedGames, file)
        file.close()

    @staticmethod
    def load_slots():
        try:
            Data.SavedGames = pickle.load(open('resource/slots.pkl', 'rb'))
        except Exception:
            Data.save_slots()

    @staticmethod
    def save_highscores():
        file = open('resource/highscores.pkl', mode='wb')
        pickle.dump(Data.Highscores, file)
        file.close()

    @staticmethod
    def load_highscores():
        try:
            Data.Highscores = pickle.load(open('resource/highscores.pkl', 'rb'))
        except Exception:
            Data.save_highscores()

    Patterns = {
        1: [
            [1, 1],
            [2, 2],
            [3, 3]
        ],
        2: [
            [1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 1],
            [1, 0, 2, 3, 0, 1],
            [1, 0, 3, 2, 0, 1],
            [1, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1]
        ],
        3: [
            [1, 0, 0, 0, 0, 1],
            [0, 2, 0, 0, 3, 0],
            [0, 0, 2, 3, 0, 0],
            [0, 0, 3, 2, 0, 0],
            [0, 3, 0, 0, 2, 0],
            [1, 0, 0, 0, 0, 1]
        ],
        4: [
            [1, 1, 2, 2, 3, 3],
            [1, 1, 2, 2, 3, 3],
            [1, 1, 2, 2, 3, 3],
            [1, 1, 2, 2, 3, 3],
            [1, 1, 2, 2, 3, 3],
            [1, 1, 2, 2, 3, 3]
        ],
        5: [
            [0, 0, 2, 2, 0, 0],
            [0, 0, 2, 2, 0, 0],
            [0, 0, 2, 2, 0, 0],
            [3, 3, 3, 3, 3, 3],
            [0, 3, 3, 3, 3, 0],
            [0, 0, 3, 3, 0, 0]
        ]
    }

    @staticmethod
    def save_patterns():
        with open('resource/patterns.txt', 'w') as file:
            file.write(json.dumps(Data.Levels, indent=3, separators=(',', ': '))) # use `json.loads` to do the reverse

    @staticmethod
    def load_patterns():
        with open('resource/patterns.txt', 'r') as file:
            Data.Levels = json.load(file)

    """
        Levels define information for each level of game
        copy:
            - 0 for no copy
            - [Number of level] to copy in order to modify some of its elements
        pattern: 
            - [None] for using rectangular formation of rows x cols invaders 
            - [pattern] to use instead of rectangular formation,
        step: player's step in pixels, when None then the default Sprites[PLAYER]['step'] will be used
        top: set starting top in pixels
        rows: the number of horizontal rows for invaders (used when 'pattern'=None)
        cols: the number of invaders per row (used when 'pattern'=None)
        distance: distance in pixels between invaders
        strength: number of hits in order to kill
        min_dx: the minimum pixels per dt (starting speed min_dx/dt)
        max_dx: the maximum pixels per dt (ending speed max_dx/dt)
        dt: elapsed time in milliseconds for evaluation of speed
        bt: elapsed time in milliseconds between bombs
        ut: elapsed time in milliseconds between ufo appearance
        shields: number of shields for level
        h_bricks: number of horizontal bricks per shield
        v_bricks: number of vertical bricks per shield
    """
    Levels = {
        ##############################################################################################################
        1: {'copy': 0, 'pattern': None, 'step': None, 'top': 80, 'rows': 3, 'cols': 6, 'distance': 5, 'strength': 1, 'min_dx': 5, 'max_dx': 40, 'dt': 1000, 'bt': 1000, 'ut': 5000, 'shields': 3, 'h_bricks': 8, 'v_bricks': 6},
        2: {'copy': 1, 'min_dx': 10},
        3: {'copy': 1, 'min_dx': 15},
        4: {'copy': 1, 'min_dx': 20},
        5: {'copy': 1, 'min_dx': 25},
        ##############################################################################################################
        6: {'copy': 1, 'rows': 4, 'cols': 6, 'bt': 800},
        7: {'copy': 6, 'rows': 4, 'cols': 6, 'bt': 800},
        8: {'copy': 6, 'rows': 4, 'cols': 6, 'bt': 800},
        9: {'copy': 6, 'rows': 4, 'cols': 6, 'bt': 800},
        10: {'copy': 6, 'rows': 4, 'cols': 6, 'bt': 800},
        ##############################################################################################################
        11: {'copy': 6, 'rows': 5, 'cols': 6, 'bt': 600},
        12: {'copy': 11, 'rows': 5, 'cols': 6, 'bt': 600},
        13: {'copy': 11, 'rows': 5, 'cols': 6, 'bt': 600},
        14: {'copy': 11, 'rows': 5, 'cols': 6, 'bt': 600},
        15: {'copy': 11, 'rows': 5, 'cols': 6, 'bt': 600},
        ##############################################################################################################
        16: {'copy': 11, 'rows': 6, 'cols': 6, 'bt': 400},
        17: {'copy': 16, 'rows': 6, 'cols': 6, 'bt': 400},
        18: {'copy': 16, 'rows': 6, 'cols': 6, 'bt': 400},
        19: {'copy': 16, 'rows': 6, 'cols': 6, 'bt': 400},
        20: {'copy': 16, 'rows': 6, 'cols': 6, 'bt': 400},
        ##############################################################################################################
        21: {'copy': 0, 'pattern': 5, 'step': None, 'top': 100, 'rows': None, 'cols': None, 'distance': 5, 'strength': 1, 'min_dx': 15, 'max_dx': 60, 'dt': 1000, 'bt': 800, 'ut': 2000, 'shields': 3, 'h_bricks': 8, 'v_bricks': 6},
        22: {'copy': 21, 'min_dx': 20},
        23: {'copy': 21, 'min_dx': 25},
        24: {'copy': 21, 'min_dx': 30},
        25: {'copy': 21, 'min_dx': 35},
        ##############################################################################################################
        26: {'copy': 21, 'min_dx': 40, 'bt': 700},
        27: {'copy': 26, 'bt': 600},
        28: {'copy': 26, 'bt': 500},
        29: {'copy': 26, 'bt': 400},
        30: {'copy': 26, 'bt': 300},
        ##############################################################################################################
        31: {'copy': 26, 'top': 120, 'bt': 700},
        32: {'copy': 31, 'bt': 600},
        33: {'copy': 31, 'bt': 500},
        34: {'copy': 31, 'bt': 400},
        35: {'copy': 31, 'bt': 300},
        ##############################################################################################################
        36: {'copy': 31, 'top': 120, 'min_dx': 45, 'max_dx': 65, 'bt': 700},
        37: {'copy': 36, 'bt': 600},
        38: {'copy': 36, 'bt': 500},
        39: {'copy': 36, 'bt': 400},
        40: {'copy': 36, 'bt': 300}
    }

    @staticmethod
    def save_levels():
        with open('resource/levels.txt', 'w') as file:
            file.write(json.dumps(Data.Levels, indent=3, separators=(',', ': '))) # use `json.loads` to do the reverse

    @staticmethod
    def load_levels():
        with open('resource/levels.txt', 'r') as file:
            Data.Levels = json.load(file)

class Button:
    """A simple button class"""

    def __init__(self, txt, location, action, bg=Colors.DARK_GREY, fg=Colors.WHITE, hbg=Colors.LIGHT_GREY,
                 hfg=Colors.BLUE, size=(200, 50), font_name=Resources.Fonts[Resources.FONT1]['file'], font_size=16):
        self.screen = pygame.display.get_surface()
        self.color = bg  # the static (normal) color
        self.fcolor = fg
        self.bg = bg  # actual background color, can change on mouseover
        self.fg = fg  # text color
        self.hbg = hbg  # highlight / mouse over collor
        self.hfg = hfg  # highlighted text color
        self.size = size
        self.font = pygame.font.Font(font_name, font_size)
        self.txt = txt
        self.txt_surf = self.font.render(self.txt, 1, self.fg)
        self.txt_rect = self.txt_surf.get_rect(center=[s // 2 for s in self.size])
        self.surface = pygame.surface.Surface(size)
        self.rect = self.surface.get_rect(center=location)
        self.call_back_ = action

    def draw(self):
        self.mouseover()
        self.surface.fill(self.bg)
        self.surface.blit(self.txt_surf, self.txt_rect)
        self.screen.blit(self.surface, self.rect)

    def mouseover(self):
        self.bg = self.color
        self.fg = self.fcolor
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            self.bg = self.hbg
            self.fg = self.hfg
            self.txt_surf = self.font.render(self.txt, 1, self.fg)
        else:
            self.txt_surf = self.font.render(self.txt, 1, self.fg)

    def call_back(self):
        self.call_back_()


class TextBox(pygame.sprite.Sprite):
    shiftDown = False

    def __init__(self, screen):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.text = ""
        self.font = pygame.font.Font(Resources.Fonts[Resources.FONT1]['file'], 40)
        #self.image = self.font.render("", True, Colors.YELLOW)
        #self.rect = self.image.get_rect()
        self.text_edit = self.font.render(str(self.text), True, Colors.YELLOW)
        self.rect = self.text_edit.get_rect()
        self.rect.centerx = self.screen.get_rect().centerx
        self.rect.centery = DISPLAY_HEIGHT - 500 #self.screen.get_rect().centery
        self.screen.blit(self.text_edit, self.rect)

    def add_chr(self, char):
        if char in Resources.ValidChars and not TextBox.shiftDown:
            self.text += char
        elif char in Resources.ValidChars and TextBox.shiftDown:
            self.text += Resources.ShiftChars[Resources.ValidChars.index(char)]
        self.update()

    def update(self):
        old_rect_pos = self.rect.center
        #self.image = self.font.render(self.text, True, Colors.YELLOW)
        #self.rect = self.image.get_rect()
        self.text_edit = self.font.render(str(self.text), True, Colors.YELLOW)
        self.rect = self.text_edit.get_rect()
        self.rect.center = old_rect_pos


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, step=Resources.Sprites[Resources.PLAYER]['step']):
        super(Player, self).__init__()
        self.key = Resources.PLAYER
        self.images = []
        try:
            self.images.append(pygame.image.load(Resources.Sprites[Resources.PLAYER]['files'][0]))
        except Exception as ex:
            print('Exception in Ufo.__init__():', ex)
        self.frames = len(Resources.Sprites[Resources.PLAYER]['files'])
        self.name = Resources.Sprites[Resources.PLAYER]['name']
        self.color = Resources.Sprites[Resources.PLAYER]['color']
        self.frame = 0
        self.image = self.images[self.frame]
        self.image.set_colorkey(Colors.BLACK)
        self.rect = self.image.get_rect(center=pos)
        self.dx = 0
        self.step = step

    def update(self):
        super(Player, self).update()
        if (self.dx == self.step and (self.rect.right+self.dx) <= DISPLAY_WIDTH) \
                or (self.dx == -self.step and (self.rect.left+self.dx) >= 0):
            self.rect.move_ip(self.dx, 0)


class Brick(pygame.sprite.Sprite):
    def __init__(self, pos):
        super(Brick, self).__init__()
        self.key = Resources.BRICK
        self.images = []
        try:
            for file in Resources.Sprites[Resources.BRICK]['files']:
                self.images.append(pygame.image.load(file))
        except Exception as ex:
            print('Exception in Brick.__init__():', ex)
        self.frames = len(Resources.Sprites[Resources.BRICK]['files'])
        self.name = Resources.Sprites[Resources.BRICK]['name']
        self.color = Resources.Sprites[Resources.BRICK]['color']
        self.points = Resources.Sprites[Resources.BRICK]['points']
        self.frame = 0
        self.image = self.images[self.frame]
        self.image.set_colorkey(Colors.BLACK)
        self.rect = self.image.get_rect(center=pos)

    def update(self):
        super(Brick, self).update()

    def damage(self, shields: pygame.sprite.Group, damage_radius, destroy_radius):
        for br in shields:
            d = math.sqrt((self.rect.centerx - br.rect.centerx)**2 + (self.rect.centery - br.rect.centery)**2)
            if d <= damage_radius:
                if br.frame == 0:
                    br.frame = 1
                    br.image = br.images[br.frame]
                elif br.frame == 1:
                    shields.remove(br)
            if d <= destroy_radius:
                shields.remove(br)


class Shot(pygame.sprite.Sprite):
    def __init__(self, color, pos):
        super().__init__()
        self.points = 50
        self.color = color
        self.image = pygame.Surface([4, 15])
        self.image.fill(color)
        self.rect = self.image.get_rect(center=pos)

    def update(self):
        super(Shot, self).update()
        if self.color == Colors.GREEN:
            self.rect.y -= PLAYER_SHOT_DY
        else:
            self.rect.y += INVADER_SHOT_DY

    @staticmethod
    def remove_bombs(bombs: pygame.sprite.Group):
        for bm in bombs:
            if bm.rect.bottom >= (DISPLAY_HEIGHT - 10):
                bombs.remove(bm)


class Explosion(pygame.sprite.Sprite):
    def __init__(self, pos):
        super(Explosion, self).__init__()
        self.images = []
        try:
            for file in Resources.Sprites[Resources.EXPLOSION]['files']:
                self.images.append(pygame.image.load(file))
        except Exception as ex:
            print('Exception in Explosion.__init__():', ex)
        self.frames = len(Resources.Sprites[Resources.EXPLOSION]['files'])
        self.frame = 0
        self.image = self.images[self.frame]
        self.image.set_colorkey(Colors.BLACK)
        self.rect = self.image.get_rect(center=pos)
        self.rect.center = pos
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame >= self.frames:
                self.kill()
            else:
                center = self.rect.center
                self.image = self.images[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


class Ufo(pygame.sprite.Sprite):
    """This class handles the ufos"""
    ticks_since_last_ufo = 0
    ticks = 0

    def __init__(self, ship, direction=1):
        super(Ufo, self).__init__()
        self.key = ship
        self.images = []
        try:
            for file in Resources.Sprites[ship]['files']:
                self.images.append(pygame.image.load(file))
        except Exception as ex:
            print('Exception in Ufo.__init__():', ex)
        self.frames = len(Resources.Sprites[ship]['files'])
        self.name = Resources.Sprites[ship]['name']
        self.color = Resources.Sprites[ship]['color']
        self.points = Resources.Sprites[ship]['points']
        self.frame = 0
        self.image = self.images[self.frame]
        self.image.set_colorkey(Colors.BLACK)
        self.direction = direction
        if self.direction == 1:
            pos = (-self.image.get_width(), 45)
        elif self.direction == -1:
            pos = (DISPLAY_WIDTH + self.image.get_width(), 45)
        self.rect = self.image.get_rect(center=pos)
        self.step = Resources.Sprites[ship]['step']

    def update(self):
        super(Ufo, self).update()
        self.frame += 1
        if self.frame >= self.frames:
            self.frame = 0
        self.image = self.images[self.frame]
        self.rect.move_ip(self.direction * self.step, 0)

    @staticmethod
    def appears(level, level_dict, ufos: pygame.sprite.Group):
        ticks = pygame.time.get_ticks()
        Ufo.ticks_since_last_ufo = ticks - Ufo.ticks_since_last_ufo
        if len(ufos.sprites()) == 0 and (not random.randrange(0, UFO_RANDRANGE) or Ufo.ticks_since_last_ufo >= level_dict['ut']):
            Ufo.ticks_since_last_ufo = ticks
            ship = Resources.UFO1 if random.randrange(0, UFO_RANDRANGE) < UFO_RANDRANGE/2 else Resources.UFO2
            direction = 1 if random.randrange(0, UFO_RANDRANGE) < UFO_RANDRANGE/2 else -1
            return ship, direction
        else:
            return 0, 0

    @staticmethod
    def remove_ufos(ufos: pygame.sprite.Group):
        for uf in ufos:
            if uf.direction == 1 and uf.rect.left >= DISPLAY_WIDTH:
                ufos.remove(uf)
            if uf.direction == -1 and uf.rect.right <= 0:
                ufos.remove(uf)


class Invader(pygame.sprite.Sprite):
    """This class handles the invaders"""
    dx = 0                  # horizontal pixels to move
    max_dx = 0              # max horizontal pixels to move per frame
    dy = 0                  # vertical pixels to move
    t = 0                   # current time in ticks
    xt = 0                  # previous time in ticks for position
    xft = 0                 # previous time in ticks for frame
    xbt = 0                 # previous time in ticks for bombs
    dt = 1000               # delta time in ticks for position
    ft = 500                # delta time in ticks for frame
    bt = 2000               # delta time in ticks for bombs
    px = 2                  # pixels to move
    speed = px/dt           # pixels to move per second
    frame = 0               # current frame for invader
    direction = 1           # direction to move
    block = pygame.rect     # rect for block of invaders
    counter = 0             # holds the maximum number of invaders
    level = 0               # holds the level of the game

    def __init__(self, ship, pos):
        super(Invader, self).__init__()
        self.key = ship
        self.images = []
        try:
            for file in Resources.Sprites[ship]['files']:
                self.images.append(pygame.image.load(file))
        except Exception as ex:
            print('Exception in Invader.__init__():', ex)
        self.frames = len(Resources.Sprites[ship]['files'])
        self.name = Resources.Sprites[ship]['name']
        self.color = Resources.Sprites[ship]['color']
        self.points = Resources.Sprites[ship]['points']
        self.frame = 0
        self.image = self.images[self.frame]
        self.image.set_colorkey(Colors.BLACK)
        self.rect = self.image.get_rect(center=pos)
        self.step = Resources.Sprites[ship]['step']
        Invader.counter +=1

    def update(self):
        super(Invader, self).update()
        self.frame = Invader.frame
        self.image = self.images[self.frame]
        if Invader.dx != 0 or Invader.dy != 0:
            self.rect.move_ip(Invader.dx, Invader.dy)

    @staticmethod
    def init_values(level, direction, min_dx=2, max_dx=10, dt=1000, bt=2000, counter=0):
        Invader.level = level
        Invader.direction = direction
        Invader.px = min_dx
        Invader.max_dx = max_dx
        Invader.speed = min_dx/dt
        Invader.dt = dt
        Invader.bt = bt
        Invader.counter = counter

    @staticmethod
    def get_block(invaders: pygame.sprite.Group):
        surface = pygame.display.get_surface()
        left = surface.get_width()
        top = surface.get_height()
        right = 0
        bottom = 0
        for inv in invaders:
            if inv.rect.left <= left:
                left = inv.rect.left
            if inv.rect.top <= top:
                top = inv.rect.top
            if inv.rect.right >= right:
                right = inv.rect.right
            if inv.rect.bottom >= bottom:
                bottom = inv.rect.bottom
        Invader.block.left = left
        Invader.block.top = top
        Invader.block.width = right-left
        Invader.block.height = bottom-top

    @staticmethod
    def get_move(level_dict: dict, invaders: pygame.sprite.Group, bombs: pygame.sprite.Group, player: Player):
        speed_factor = (Invader.counter + 1) / (len(invaders) + 1)

        Invader.t = pygame.time.get_ticks()
        if (Invader.t - Invader.xt) >= Invader.dt:
            Invader.dx = Invader.speed * speed_factor * Invader.dt
            if Invader.dx >= Invader.max_dx:
                Invader.dx = Invader.max_dx
            Invader.xt = Invader.t

        if (Invader.t - Invader.xft) >= Invader.ft:
            Invader.frame += 1
            if Invader.frame >= 2:
                Invader.frame = 0
            Invader.xft = Invader.t

        if Invader.block.top < level_dict['top']:
            Invader.dx = 0
            Invader.dy = INVADER_FALL_DY
            Invader.xbt = Invader.t
            return

        if (Invader.t - Invader.xbt) >= Invader.bt and Invader.block.top >= level_dict['top']:
            inv = Invader.get_bomb(invaders, bombs, player)
            if inv:
                bomb = Shot(inv.color, (inv.rect.left + inv.rect.width / 2, inv.rect.bottom))
                bombs.add(bomb)
            Invader.xbt = Invader.t

        if Invader.direction == -1.0 and Invader.dy == 0 and Invader.block.left <= HORIZONTAL_MARGIN:
            Invader.direction = 1.0
            Invader.dx = Invader.direction * Invader.dx
            Invader.dy = INVADER_DY
        elif Invader.direction == 1.0 and Invader.dy == 0 and (Invader.block.left+Invader.block.width) >= (DISPLAY_WIDTH-HORIZONTAL_MARGIN):
            Invader.direction = -1.0
            Invader.dx = Invader.direction * Invader.dx
            Invader.dy = INVADER_DY
        else:
            Invader.dx = Invader.direction * math.fabs(Invader.dx)
            Invader.dy = 0

    @staticmethod
    def get_bomb(invaders: pygame.sprite.Group, bombs: pygame.sprite.Group, player: Player):
        min_dist = math.sqrt(DISPLAY_WIDTH**2 + DISPLAY_HEIGHT**2)
        min_dist_inv = None
        dist = list()  # list with distance per player
        for i, inv in enumerate(invaders):
            dist.append(math.sqrt((inv.rect.left - player.rect.left)**2 + (inv.rect.right - player.rect.right)**2))
            if dist[i] <= min_dist:
                min_dist = dist[i]
                min_dist_inv = inv

        if min_dist_inv and Invader.direction == 1 and player.rect.left >= Invader.block.left:
            return min_dist_inv
        elif min_dist_inv and Invader.direction == -1 and player.rect.left <= Invader.block.left:
            return min_dist_inv
        else:
            if len(invaders):
                rnd_idx = random.randrange(0, len(invaders))
                for i, inv in enumerate(invaders):
                    if i == rnd_idx:
                        return inv

        return None


class Game:
    """This class controls the Space Invaders game"""

    def __init__(self, width=DISPLAY_WIDTH, height=DISPLAY_HEIGHT):
        self.width = width
        self.height = height
        self.clock = pygame.time.Clock()
        self.icon = None
        self.screen = None
        self.background = None
        self.status = 'Main'
        self.main_window_buttons = list()
        self.help_window_buttons = list()
        self.load_window_buttons = list()
        self.level_text_rect = pygame.rect

        Data.load_slots()
        Data.load_highscores()

        self.credits = 3
        self.level = 1
        self.level_dict = {}
        self.score = 0
        self.highscore = 0
        for hs in Data.Highscores:
            if Data.Highscores[hs]['score'] >= self.highscore:
                self.highscore = Data.Highscores[hs]['score']
        self.player: Player = None
        if Data.Levels[self.level]['step']:
            self.player_step = Data.Levels[self.level]['step']
        else:
            self.player_step = Resources.Sprites[Resources.PLAYER]['step']

        self.invader_width = 50
        self.invader_height = 34
        self.brick_width = 8
        self.brick_height = 8
        self.shield_starting_top = 480

        self.invader_starting_top = Data.Levels[self.level]['top']
        self.invader_rows = Data.Levels[self.level]['rows']
        self.invader_cols = Data.Levels[self.level]['cols']
        self.invader_distance = Data.Levels[self.level]['distance']
        self.invader_strength = Data.Levels[self.level]['strength']
        self.num_shields = Data.Levels[self.level]['shields']
        self.shield_horizontal_bricks = Data.Levels[self.level]['h_bricks']
        self.shield_vertical_bricks = Data.Levels[self.level]['v_bricks']

        self.ufos = pygame.sprite.Group()
        self.invaders = pygame.sprite.Group()
        self.bombs = pygame.sprite.Group()
        self.shots = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()
        self.shields = pygame.sprite.Group()
        self.players = pygame.sprite.Group()
        self.all = pygame.sprite.RenderUpdates()

    def popup_message(self, text, wait_dt=2000, font_color=Colors.YELLOW, font_size=40, font_type=Resources.Fonts[Resources.FONT1]['file']):
        font = pygame.font.Font(font_type, font_size)
        text = font.render(str(text), True, font_color)
        textrect = text.get_rect()
        textrect.centerx = self.screen.get_rect().centerx
        textrect.centery = self.screen.get_rect().centery
        surf = pygame.Surface((textrect.width, textrect.height), pygame.SRCALPHA)
        pygame.draw.rect(surf, (187, 187, 187, 210), (0, 0, textrect.width, textrect.height))
        self.screen.blit(surf, textrect)
        self.screen.blit(text, textrect)
        pygame.display.update()

    def display_text(self, txt, x, y, size=12, color=Colors.WHITE, font_type=Resources.Fonts[Resources.FONT1]['file']):
        font = pygame.font.Font(font_type, size)
        text = font.render(str(txt), True, color)
        self.screen.blit(text, (x, y))

    def display_level(self, txt, font_color=Colors.YELLOW, font_size=40, font_type=Resources.Fonts[Resources.FONT1]['file']):
        font = pygame.font.Font(font_type, font_size)
        text = font.render(str(txt), True, font_color)
        self.level_text_rect = text.get_rect()
        self.level_text_rect.centerx = self.screen.get_rect().centerx
        self.level_text_rect.centery = DISPLAY_HEIGHT - 200 #self.screen.get_rect().centery
        self.screen.blit(text, self.level_text_rect)

    def create_window(self):
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.init()
        pygame.display.set_caption('Space Invaders')
        self.icon = pygame.image.load(Resources.Icons[Resources.PROGRAM_ICON]['file'])
        pygame.display.set_icon(self.icon)
        self.screen = pygame.display.set_mode((self.width, self.height))

    def set_background(self, image: Resources.Backgrounds = None):
        self.background = pygame.Surface(Rect(0, 0, DISPLAY_WIDTH, DISPLAY_HEIGHT).size).convert()
        self.screen.fill(Colors.BLACK)
        if image:
            self.background = pygame.image.load(Resources.Backgrounds[image]['file'])
        self.screen.blit(self.background, (0, 0))
        pygame.display.update()

    #########################################################################
    # Main window handling
    #########################################################################
    def display_main_window_buttons(self):
        self.main_window_buttons.clear()
        new_btn = Button('New', (570, 300), self.main_window_new_click)
        load_btn = Button('Load', (570, 370), self.main_window_load_click)
        help_btn = Button('Help', (570, 440), self.main_window_help_click)
        quit_btn = Button('Quit', (570, 510), self.main_window_quit_click)
        self.main_window_buttons.append(new_btn)
        self.main_window_buttons.append(load_btn)
        self.main_window_buttons.append(help_btn)
        self.main_window_buttons.append(quit_btn)
        for btn in self.main_window_buttons:
            btn.draw()
            pygame.display.update()

    def display_highscores(self):
        self.display_text('High Scores', 600, 10)
        for hs in Data.Highscores:
            self.display_text(str(Data.Highscores[hs]['score']) + ': ' + Data.Highscores[hs]['name'], 600, 10+(hs*15))

    def display_main_window(self):
        self.set_background(Resources.MAIN_BACKGROUND)
        self.display_main_window_buttons()
        self.display_highscores()

    def main_window_new_click(self):
        self.status = 'New'
        self.level = 1
        self.credits = 3
        self.score = 0
        self.display_new_window()

    def main_window_load_click(self):
        self.status = 'Load'
        self.display_load_window()

    def main_window_help_click(self):
        self.status = 'Help'
        self.display_help_window()

    def main_window_quit_click(self):
        self.status = 'Quit'

    def main_window_mousebuttondown(self):
        pos = pygame.mouse.get_pos()
        for btn in self.main_window_buttons:
            if btn.rect.collidepoint(pos):
                btn.call_back()

    def main_window_loop(self):
        while self.status == 'Main':
            self.clock.tick(FPS)
            events = pygame.event.get()
            keys = pygame.key.get_pressed()
            for event in events:
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.main_window_mousebuttondown()
                if event.type == pygame.KEYDOWN:
                    if keys[pygame.K_ESCAPE]:
                        sys.exit()
            for btn in self.main_window_buttons:
                btn.draw()
            pygame.display.flip()

        if self.status == 'Quit':
            sys.exit()

    #########################################################################
    # Help window handling
    #########################################################################
    def display_help_window_buttons(self):
        self.help_window_buttons.clear()
        back_btn = Button('Back', (570, 510), self.help_window_back_click)
        self.help_window_buttons.append(back_btn)
        for btn in self.help_window_buttons:
            btn.draw()
            pygame.display.update()

    def display_help_window(self):
        self.set_background(Resources.HELP_BACKGROUND)
        self.display_help_window_buttons()
        self.help_window_loop()

    def help_window_back_click(self):
        self.status = 'Main'
        self.display_main_window()
        self.main_window_loop()

    def help_window_mousebuttondown(self):
        pos = pygame.mouse.get_pos()
        for btn in self.help_window_buttons:
            if btn.rect.collidepoint(pos):
                btn.call_back()

    def help_window_loop(self):
        while self.status == 'Help':
            self.clock.tick(FPS)
            events = pygame.event.get()
            keys = pygame.key.get_pressed()
            for event in events:
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.help_window_mousebuttondown()
                if event.type == pygame.KEYDOWN:
                    if keys[pygame.K_ESCAPE]:
                        self.status = 'Main'
                        self.display_main_window()
                        self.main_window_loop()
            for btn in self.help_window_buttons:
                btn.draw()
            pygame.display.flip()

    #########################################################################
    # Load window handling
    #########################################################################
    def display_load_window_buttons(self):
        slots = 0
        self.load_window_buttons.clear()
        if Data.SavedGames[Data.SLOT1]['player'] != 'Empty':
            slots += 1
            slot1_btn = Button(Data.SavedGames[Data.SLOT1]['name'] + ': ' + Data.SavedGames[Data.SLOT1]['player'], (570, 300), self.load_window_slot1_click)
            self.load_window_buttons.append(slot1_btn)
        if Data.SavedGames[Data.SLOT2]['player'] != 'Empty':
            slots += 1
            slot2_btn = Button(Data.SavedGames[Data.SLOT2]['name'] + ': ' + Data.SavedGames[Data.SLOT1]['player'], (570, 370), self.load_window_slot2_click)
            self.load_window_buttons.append(slot2_btn)
        if Data.SavedGames[Data.SLOT3]['player'] != 'Empty':
            slots += 1
            slot2_btn = Button(Data.SavedGames[Data.SLOT3]['name'] + ': ' + Data.SavedGames[Data.SLOT3]['player'], (570, 440), self.load_window_slot3_click)
            self.load_window_buttons.append(slot2_btn)
        if slots == 0:
            self.display_text('All slots are empty', 485, 370)
        back_btn = Button('Back', (570, 510), self.load_window_back_click)
        self.load_window_buttons.append(back_btn)
        for btn in self.load_window_buttons:
            btn.draw()
            pygame.display.update()

    def display_load_window(self):
        self.set_background(Resources.MAIN_BACKGROUND)
        self.display_load_window_buttons()
        self.load_window_loop()

    def load_window_slot1_click(self):
        self.status = 'Main'
        self.display_main_window()
        self.main_window_loop()

    def load_window_slot2_click(self):
        self.status = 'Main'
        self.display_main_window()
        self.main_window_loop()

    def load_window_slot3_click(self):
        self.status = 'Main'
        self.display_main_window()
        self.main_window_loop()

    def load_window_back_click(self):
        self.status = 'Main'
        self.display_main_window()
        self.main_window_loop()

    def load_window_mousebuttondown(self):
        pos = pygame.mouse.get_pos()
        for btn in self.load_window_buttons:
            if btn.rect.collidepoint(pos):
                btn.call_back()

    def load_window_loop(self):
        while self.status == 'Load':
            self.clock.tick(FPS)
            events = pygame.event.get()
            keys = pygame.key.get_pressed()
            for event in events:
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.load_window_mousebuttondown()
                if event.type == pygame.KEYDOWN:
                    if keys[pygame.K_ESCAPE]:
                        self.status = 'Main'
                        self.display_main_window()
                        self.main_window_loop()
            for btn in self.load_window_buttons:
                btn.draw()
            pygame.display.flip()

    #########################################################################
    # New game and game window handling
    #########################################################################
    def set_level(self, level):
        if 'step' in level.keys():
            if level['step']:
                self.player_step = level['step']
            else:
                self.player_step = Resources.Sprites[Resources.PLAYER]['step']
        else:
            self.player_step = Resources.Sprites[Resources.PLAYER]['step']
        self.invader_starting_top = level['top']
        if not level['pattern']:
            self.invader_rows = level['rows']
            self.invader_cols = level['cols']
        else:
            self.invader_rows = len(Data.Patterns[level['pattern']])
            self.invader_cols = len(Data.Patterns[level['pattern']][0])
        self.invader_distance = level['distance']
        self.invader_strength = level['strength']
        self.num_shields = level['shields']
        self.shield_horizontal_bricks = level['h_bricks']
        self.shield_vertical_bricks = level['v_bricks']

    def clean_sprites(self):
        self.ufos.empty()
        self.invaders.empty()
        self.bombs.empty()
        self.shots.empty()
        self.explosions.empty()
        self.shields.empty()
        self.players.empty()
        self.player = None

    def load_level(self, lvl):
        pattern = None
        step = None
        top = None
        rows = None
        cols = None
        distance = None
        strength = None
        min_dx = None
        max_dx = None
        dt = None
        bt = None
        ut = None
        shields = None
        h_bricks = None
        v_bricks = None

        copy = Data.Levels[lvl]['copy']
        if 'pattern' in Data.Levels[lvl].keys():
            pattern = Data.Levels[lvl]['pattern']
        if 'step' in Data.Levels[lvl].keys():
            step = Data.Levels[lvl]['step']
        if 'top' in Data.Levels[lvl].keys():
            top = Data.Levels[lvl]['top']
        if 'rows' in Data.Levels[lvl].keys():
            rows = Data.Levels[lvl]['rows']
        if 'cols' in Data.Levels[lvl].keys():
            cols = Data.Levels[lvl]['cols']
        if 'distance' in Data.Levels[lvl].keys():
            distance = Data.Levels[lvl]['distance']
        if 'strength' in Data.Levels[lvl].keys():
            strength = Data.Levels[lvl]['strength']
        if 'min_dx' in Data.Levels[lvl].keys():
            min_dx = Data.Levels[lvl]['min_dx']
        if 'max_dx' in Data.Levels[lvl].keys():
            max_dx = Data.Levels[lvl]['max_dx']
        if 'dt' in Data.Levels[lvl].keys():
            dt = Data.Levels[lvl]['dt']
        if 'bt' in Data.Levels[lvl].keys():
            bt = Data.Levels[lvl]['bt']
        if 'ut' in Data.Levels[lvl].keys():
            ut = Data.Levels[lvl]['ut']
        if 'shields' in Data.Levels[lvl].keys():
            shields = Data.Levels[lvl]['shields']
        if 'h_bricks' in Data.Levels[lvl].keys():
            h_bricks = Data.Levels[lvl]['h_bricks']
        if 'v_bricks' in Data.Levels[lvl].keys():
            v_bricks = Data.Levels[lvl]['v_bricks']

        this = Data.Levels[lvl]
        if copy != 0:
            parent = self.load_level(copy)
            copy = this['copy'] if 'copy' in this.keys() else parent['copy']
            pattern = this['pattern'] if 'pattern' in this.keys() else parent['pattern']
            step = this['step'] if 'step' in this.keys() else parent['step']
            top = this['top'] if 'top' in this.keys() else parent['top']
            rows = this['rows'] if 'rows' in this.keys() else parent['rows']
            cols = this['cols'] if 'cols' in this.keys() else parent['cols']
            distance = this['distance'] if 'distance' in this.keys() else parent['distance']
            strength = this['strength'] if 'strength' in this.keys() else parent['strength']
            min_dx = this['min_dx'] if 'min_dx' in this.keys() else parent['min_dx']
            max_dx = this['max_dx'] if 'max_dx' in this.keys() else parent['max_dx']
            dt = this['dt'] if 'dt' in this.keys() else parent['dt']
            bt = this['bt'] if 'bt' in this.keys() else parent['bt']
            ut = this['ut'] if 'ut' in this.keys() else parent['ut']
            shields = this['shields'] if 'shields' in this.keys() else parent['shields']
            h_bricks = this['h_bricks'] if 'h_bricks' in this.keys() else parent['h_bricks']
            v_bricks = this['v_bricks'] if 'v_bricks' in this.keys() else parent['v_bricks']

        level = {'copy': copy,
                 'pattern': pattern,
                 'step': step,
                 'top': top,
                 'rows': rows,
                 'cols': cols,
                 'distance': distance,
                 'strength': strength,
                 'min_dx': min_dx,
                 'max_dx': max_dx,
                 'dt': dt,
                 'bt': bt,
                 'ut': ut,
                 'shields': shields,
                 'h_bricks': h_bricks,
                 'v_bricks': v_bricks}

        return level

    def create_sprites(self):
        direction = -1 if random.randrange(0, UFO_RANDRANGE) <= UFO_RANDRANGE/2 else 1
        self.level_dict = self.load_level(self.level)
        self.set_level(self.level_dict)

        Invader.init_values(self.level,
                            direction,
                            self.level_dict['min_dx'],
                            self.level_dict['max_dx'],
                            self.level_dict['dt'],
                            self.level_dict['bt'],
                            counter=0)

        starting_top = - self.invader_rows * (self.invader_height + self.invader_distance)
        starting_left = (self.width - (self.invader_cols * self.invader_width + (self.invader_cols - 1) * self.invader_distance)) / 2

        if self.level_dict['pattern'] is None:
            for row in range(0, self.level_dict['rows']):
                for col in range(0, self.level_dict['cols']):
                    invader = Invader(row % 3+1,
                                      (starting_left + col * (self.invader_distance + self.invader_width),
                                       starting_top + row * (self.invader_height + self.invader_distance)))
                    self.invaders.add(invader)
        else:
            pattern = self.level_dict['pattern']
            for row in range(len(Data.Patterns[pattern])):
                for col in range(len(Data.Patterns[pattern][row])):
                    if Data.Patterns[pattern][row][col] != 0:
                        invader = Invader(Data.Patterns[pattern][row][col],
                                          (starting_left + col * (self.invader_distance + self.invader_width),
                                           starting_top + row * (self.invader_height + self.invader_distance)))
                        self.invaders.add(invader)

        h_space = (self.width - (self.num_shields * self.shield_horizontal_bricks * self.brick_width)) / (self.num_shields + 1)
        self.shield_starting_top = self.height - 50 - self.shield_vertical_bricks * self.brick_height
        for s in range(0, self.num_shields):
            starting_left = h_space + s * self.shield_horizontal_bricks * self.brick_width + s * h_space
            for h in range(0, self.shield_horizontal_bricks):
                for v in range(0, self.shield_vertical_bricks):
                    brick = Brick((starting_left + h * self.brick_width, self.shield_starting_top + v * self.brick_height))
                    self.shields.add(brick)

        self.player = Player((self.width / 2.0, (self.height - 25)), self.player_step)
        self.players.add(self.player)

    def process_shots(self):
        for sh in self.shots:
            hits = pygame.sprite.spritecollide(sh, self.invaders, True) + \
                   pygame.sprite.spritecollide(sh, self.ufos, True) + \
                   pygame.sprite.spritecollide(sh, self.shields, True) + \
                   pygame.sprite.spritecollide(sh, self.bombs, True)
            for hit in hits:
                exp = Explosion(hit.rect.center)
                self.explosions.add(exp)
                self.shots.remove(sh)
                if type(hit) == Invader:
                    self.score += (hit.points * hit.speed * 1000)
                    self.invaders.remove(hit)
                elif type(hit) == Ufo:
                    self.score += hit.points
                    self.ufos.remove(hit)
                elif type(hit) == Shot:
                    self.score += hit.points
                    self.shots.remove(hit)
                elif type(hit) == Brick:
                    self.score += hit.points
                    hit.damage(self.shields, 10, 20)
                    self.shields.remove(hit)

    def process_bombs(self):
        for bm in self.bombs:
            hits = pygame.sprite.spritecollide(bm, self.players, True) + \
                   pygame.sprite.spritecollide(bm, self.shields, True) + \
                   pygame.sprite.spritecollide(bm, self.shots, True)
            if len(hits) > 0:
                exp = Explosion(bm.rect.center)
                self.explosions.add(exp)
                self.bombs.remove(bm)
                for hit in hits:
                    if type(hit) == Player:
                        self.players.remove(hit)
                    elif type(hit) == Brick:
                        hit.damage(self.shields, 10, 20)
                        self.shields.remove(hit)
                    elif type(hit) == Shot:
                        self.shots.remove(hit)

    def process_invaders(self):
        for inv in self.invaders:
            hits = pygame.sprite.spritecollide(inv, self.shields, True)
            if len(hits) > 0:
                exp = Explosion(inv.rect.center)
                self.explosions.add(exp)
                self.invaders.remove(inv)
                for hit in hits:
                    exp = Explosion(hit.rect.center)
                    self.explosions.add(exp)
                    hit.damage(self.shields, 10, 20)
                    self.shields.remove(hit)

    def update_sprites(self):
        self.ufos.update()
        self.invaders.update()
        self.bombs.update()
        self.shots.update()
        self.shields.update()
        self.players.update()
        self.explosions.update()

    def draw_sprites(self):
        self.screen.blit(self.background, (0, 0))
        self.ufos.draw(self.screen)
        self.invaders.draw(self.screen)
        self.bombs.draw(self.screen)
        self.shots.draw(self.screen)
        self.shields.draw(self.screen)
        self.players.draw(self.screen)
        self.explosions.draw(self.screen)
        if self.score >= self.highscore:
            self.highscore = self.score
        self.display_text("Credits: {0}, Level: {1}, Score: {2}, Highscore: {3}".format(self.credits, self.level, int(self.score), int(self.highscore)), 5, 0, 16)
        Invader.get_block(self.invaders)
        if len(self.invaders) > 0:
            ship, direction = Ufo.appears(self.level, self.level_dict, self.ufos)
            if ship > 0 and Invader.block.top >= self.level_dict['top']:
                ufo = Ufo(ship, direction)
                self.ufos.add(ufo)
        if Invader.block.top < self.level_dict['top']:
            self.display_level('Level ' + str(self.level))
        pygame.display.update()
        Invader.get_move(self.level_dict, self.invaders, self.bombs, self.player)
        self.process_shots()
        self.process_bombs()
        self.process_invaders()
        Ufo.remove_ufos(self.ufos)

    def check_highscore(self):
        key = 0
        highscore = 0
        for hs in Data.Highscores:
            if self.score >= Data.Highscores[hs]['score']:
                if self.score >= highscore:
                    highscore = self.score
                    key = hs
        if key == 0:
            return

        Data.Highscores[key]['score'] = highscore
        self.clean_sprites()
        self.set_background(Resources.HIGH_BACKGROUND)
        textBox = TextBox(self.screen)
        TextBox.shiftDown = False
        textBox.rect.center = [400, 300]

        running = True
        while running:
            self.display_text('Enter your name: ', 180, 220, 40)
            pygame.draw.rect(self.screen, Colors.BLACK, textBox.rect)
            self.screen.blit(textBox.text_edit, textBox.rect)
            pygame.display.flip()
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    running = False
                if e.type == pygame.KEYUP:
                    if e.key in [pygame.K_RSHIFT, pygame.K_LSHIFT]:
                        TextBox.shiftDown = False
                if e.type == pygame.KEYDOWN:
                    textBox.add_chr(pygame.key.name(e.key))
                    if e.key == pygame.K_SPACE:
                        textBox.text += " "
                        textBox.update()
                    if e.key in [pygame.K_RSHIFT, pygame.K_LSHIFT]:
                        TextBox.shiftDown = True
                    if e.key == pygame.K_BACKSPACE:
                        pygame.draw.rect(self.screen, Colors.BLACK, textBox.rect)
                        textBox.text = textBox.text[:-1]
                        textBox.update()
                    if e.key == pygame.K_RETURN:
                        if len(textBox.text) > 0:
                            Data.Highscores[key]['name'] = textBox.text
                            running = False
        Data.save_highscores()

    def display_new_window(self):
        self.clean_sprites()
        self.set_background()
        self.create_sprites()
        self.update_sprites()
        self.draw_sprites()

        while self.credits > 0:
            self.clock.tick(FPS)
            self.process_events()

            if self.status != 'paused':
                self.update_sprites()
                self.draw_sprites()

            if len(self.invaders) == 0 and len(self.ufos) == 0 and len(self.explosions) == 0:
                if self.level < len(Data.Levels):
                    self.popup_message('Level ' + str(self.level) + ' completed :-)')
                    e = pygame.event.Event(pygame.USEREVENT, {'status': 'level completed', 'pause': 3000})
                    pygame.event.post(e)
                else:
                    self.popup_message('Game completed :-)')
                    e = pygame.event.Event(pygame.USEREVENT, {'status': 'game completed', 'pause': 3000})
                    pygame.event.post(e)
            elif len(self.players) == 0 and len(self.explosions) == 0:
                self.popup_message("Player killed :-(")
                e = pygame.event.Event(pygame.USEREVENT, {'status': 'player killed', 'pause': 3000})
                pygame.event.post(e)
            elif (Invader.block.top + Invader.block.height) >= (self.height - 25):
                self.popup_message("Player invaded :-(")
                e = pygame.event.Event(pygame.USEREVENT, {'status': 'player invaded', 'pause': 3000})
                pygame.event.post(e)

    def process_events(self):
            events = pygame.event.get()
            keys = pygame.key.get_pressed()

            for event in events:
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if keys[pygame.K_ESCAPE]:
                        self.clean_sprites()
                        self.status = 'Main'
                        self.display_main_window()
                        self.main_window_loop()
                    if keys[pygame.K_LEFT]:
                        self.player.dx = -self.player.step
                    if keys[pygame.K_RIGHT]:
                        self.player.dx = self.player.step
                    if keys[pygame.K_SPACE]:
                        if Invader.block.top >= self.level_dict['top']:
                            fire = Shot(self.player.color, (self.player.rect.left + self.player.rect.width / 2, self.player.rect.top))
                            self.shots.add(fire)
                    if keys[pygame.K_p]:
                        if self.status == 'paused':
                            self.status = None
                        else:
                            self.status = 'paused'
                            self.popup_message("Game Paused")

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.player.dx = 0
                    elif event.key == pygame.K_RIGHT:
                        self.player.dx = 0

                if event.type == pygame.USEREVENT:
                    if event.dict['pause']:
                        pygame.time.wait(event.dict['pause'])
                    if event.dict['status'] == 'player killed':
                        if (self.credits-1) > 0:
                            self.credits -= 1
                            self.clean_sprites()
                            self.create_sprites()
                        else:
                            self.clean_sprites()
                            self.check_highscore()
                            self.level = 1
                            self.status = 'Main'
                            self.display_main_window()
                            self.main_window_loop()
                    elif event.dict['status'] == 'player invaded':
                        if (self.credits-1) > 0:
                            self.credits -= 1
                            self.clean_sprites()
                            self.create_sprites()
                        else:
                            self.clean_sprites()
                            self.level = 1
                            self.status = 'Main'
                            self.display_main_window()
                            self.main_window_loop()
                    elif event.dict['status'] == 'level completed':
                        self.clean_sprites()
                        self.level += 1
                        self.display_new_window()
                        self.save()
                    elif event.dict['status'] == 'game completed':
                        self.save()
                        self.clean_sprites()
                        self.level = 1
                        self.status = 'Main'
                        self.display_main_window()
                        self.main_window_loop()

    def save(self):
        data = {'level': self.level, 'credits': self.credits, 'score': self.score, 'highscore': self.highscore}
        file = open('resource/spinv.pkl', mode='wb')
        pickled_data = pickle.dump(data, file)
        file.close()


###########################################################################
# Main
###########################################################################
def main():
    game = Game()
    game.create_window()
    game.display_main_window()
    game.main_window_loop()


###########################################################################
# Module
###########################################################################
if __name__ == '__main__':
    main()
