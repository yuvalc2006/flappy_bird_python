from constants import *
from math import sqrt

import pygame as pg
import random as rnd
from sys import exit


def check_if_quit(events):
    for event in events:
        if event.type == pg.QUIT:
            pg.quit()
            exit()


def jump_if_asked(keys, keys_last_tick):
    if keys[pg.K_SPACE] and not keys_last_tick[pg.K_SPACE]:
        bird.vy = -sqrt(2 * const.gravity * bird.JUMP_HEIGHT)


def left_if_asked(keys):
    if keys[pg.K_LEFT] and bird.x > 0:
        bird.x -= 2.5


def right_if_asked(keys):
    if keys[pg.K_RIGHT] and bird.x < const.game_screen_width - bird.BIRD_WIDTH:
        bird.x += 2.5


def has_touched_ground():
    if bird.y >= (const.game_screen_height - bird.BIRD_HEIGHT):
        pg.quit()
        exit()


def has_touched_ceiling():
    if bird.y <= 0:
        bird.vy = 0
        bird.y = 0


def check_for_collisions(pipe):
    if (bird.x + bird.BIRD_WIDTH >= pipe.x and bird.x <= pipe.x + pipe.PIPE_WIDTH and (
            bird.y + bird.BIRD_HEIGHT >= pipe.bottom_pipe_y or bird.y <= pipe.top_pipe_y)):
        return True


def update_score(pipe):
    if pipe.x + pipe.PIPE_WIDTH < bird.x:
        pipe.did_bird_pass = 1


def movement(keys, keys_last_tick):
    has_touched_ground()
    has_touched_ceiling()
    jump_if_asked(keys, keys_last_tick)
    left_if_asked(keys)
    right_if_asked(keys)
    bird.y += bird.vy + const.gravity / 2


def shoot_if_asked(arrows, keys, keys_last_tick):
    if keys[pg.K_UP] and bird.arrows_count > 0 and not keys_last_tick[pg.K_UP]:
        arrows.append(Arrow())
        bird.arrows_count -= 1


def paint_and_collide_arrows(arrows, pipes):
    if len(arrows) == 0:
        return
    index = 0
    while index < len(arrows):
        print(f"index: {index}")
        print(f"len: {len(arrows)}")
        arrow = arrows[index]
        if arrow.x > const.game_screen_width:
            arrows.pop(index)
            index -= 1
        arrow.paint()
        for pipe in pipes:
            if pipe.x <= arrow.x <= pipe.x + pipe.PIPE_WIDTH and (
                    pipe.top_pipe_y >= arrow.y or pipe.bottom_pipe_y <= arrow.y):
                pipes.remove(pipe)
                arrows.pop(index)
                const.pipes_gone += 1
                index -= 1
                break
        index += 1


def move_all_ob_y(pipes, arrows):
    for pipe in pipes:
        pipe.x += pipe.vx
    for arrow in arrows:
        arrow.x += arrow.vx


def generate_and_paint_pipes(pipes):
    if len(pipes) == 0:
        pipes.append(Pipe())
    time_since_last_pipe = pg.time.get_ticks() - pipes[-1].when_created
    if time_since_last_pipe > 800 and rnd.randint(0, 30) == 0:
        pipes.append(Pipe())

    was_collisions = False
    index = 0
    print(pipes[0].x)
    while index < len(pipes):
        pipe = pipes[index]
        update_score(pipe)
        if not was_collisions:
            was_collisions = check_for_collisions(pipe)
        bird.score += pipe.did_bird_pass
        pipe.paint()
        if pipe.x + pipe.PIPE_WIDTH < 0:
            const.pipes_gone += 1
            pipes.pop(index)
            index -= 1
        index += 1

    return was_collisions


def run():
    keys = pg.key.get_pressed()
    bird.paint(200, 100)
    pipes = [Pipe()]
    arrows = []
    score_font = pg.font.Font(None, const.score_font_size)
    ammo_font = pg.font.Font(None, const.ammo_font_size)
    added_ammo_yet = False

    while True:
        bird.score = const.pipes_gone

        check_if_quit(pg.event.get())

        game_screen.fill('Black')
        bird.vy += const.gravity

        keys_last_tick = keys
        keys = pg.key.get_pressed()

        move_all_ob_y(pipes, arrows)

        movement(keys, keys_last_tick)
        shoot_if_asked(arrows, keys, keys_last_tick)

        bird.paint(bird.x, bird.y)
        was_collisions = generate_and_paint_pipes(pipes)
        if bird.score % 10 == 0 and bird.score != 0:
            if not added_ammo_yet:
                bird.arrows_count += 1
                added_ammo_yet = True
        else:
            added_ammo_yet = False
        paint_and_collide_arrows(arrows, pipes)

        score_text = score_font.render(f"{bird.score}", True, 'White')
        game_screen.blit(score_text, (0, 0))
        ammo_text = ammo_font.render(f"{bird.arrows_count}", True, 'Gray')
        game_screen.blit(ammo_text, (0, const.game_screen_height - const.ammo_font_size))

        pg.display.update()
        clock.tick(60)

        if was_collisions:
            exit()
