import pygame as pg
import random as rnd


class Bird:
    BIRD_WIDTH = 50
    BIRD_HEIGHT = 50
    JUMP_HEIGHT = 100
    surface = None
    score = 0
    x = 0
    y = 0
    vy = 0
    arrows_count = 3

    def __init__(self):
        self.surface = pg.Surface((self.BIRD_WIDTH, self.BIRD_HEIGHT))
        self.surface.fill('White')

    def paint(self, x, y):
        self.x = x
        self.y = y
        game_screen.blit(self.surface, (x, y))


class Arrow:
    ARROW_WIDTH = 20
    ARROW_HEIGHT = 20
    x = None
    y = None
    vx = None
    surface = None

    def __init__(self):
        self.x = bird.x + bird.BIRD_WIDTH + 10
        self.y = bird.y + (bird.BIRD_HEIGHT / 2)
        self.vx = 4
        self.surface = pg.Surface((self.ARROW_WIDTH, self.ARROW_HEIGHT))
        self.surface.fill('Red')

    def paint(self):
        game_screen.blit(self.surface, (self.x, self.y))


class Pipe:
    PIPE_WIDTH = 100
    x = 1600
    vx = -5
    bottom_pipe_y = None
    top_pipe_y = None
    top_pipe = None
    bottom_pipe = None
    when_created = 0
    did_bird_pass = 0

    def __init__(self):
        gap_start = rnd.randint(100, 500)
        gap_length = rnd.randint(200, 300)

        self.when_created = pg.time.get_ticks()

        self.bottom_pipe_y = gap_start + gap_length
        self.top_pipe_y = gap_start

        top_pipe_height = gap_start
        self.top_pipe = pg.Surface((self.PIPE_WIDTH, top_pipe_height))
        self.top_pipe.fill('Green')

        bottom_pipe_height = const.game_screen_height - self.bottom_pipe_y
        self.bottom_pipe = pg.Surface((self.PIPE_WIDTH, bottom_pipe_height))
        self.bottom_pipe.fill('Green')

    def paint(self):
        game_screen.blit(self.top_pipe, (self.x, 0))
        game_screen.blit(self.bottom_pipe, (self.x, self.bottom_pipe_y))


class const:
    pipes_gone = 0
    gravity = 0.2
    game_screen_width = 1600
    game_screen_height = 800
    score_font_size = 70
    ammo_font_size = 100


game_screen = pg.display.set_mode((const.game_screen_width, const.game_screen_height))
clock = pg.time.Clock()
bird = Bird()
