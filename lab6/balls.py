import random
import numpy
import pygame

from random import randint
from LIB_colors import *
from pygame.draw import *

pygame.init()

FPS = 60
WIDTH = 900
MENU_WIDTH = 300
HEIGHT = 700
LIMIT = 10
R_MIN = 30
R_MAX = 50

screen = pygame.display.set_mode((WIDTH + MENU_WIDTH, HEIGHT))


def set_screen():
    '''
    устанавоиваем фон и разметку
    '''

    screen.fill(BLACK)
    line(screen, WHITE, (WIDTH, 0), (WIDTH, HEIGHT))


def sign(x):
    '''
    просто удобная функция которая определяет знак числа
    '''

    if x != 0:
        return abs(x) / x
    else:
        return 0


def rand_sign():
    '''
    просто удобная функция, которая выдает рандомный знак +/-
    '''

    return randint(1, 2) % 2 * 2 - 1


def create_nice_ball():
    '''
    создаем "хороший" шарик, в рандомном месте и т.п.
    '''

    r = randint(R_MIN, R_MAX)
    x = randint(r, WIDTH - r)
    y = randint(r, HEIGHT - r)
    v_x = rand_sign() * randint(3, 7)
    v_y = rand_sign() * randint(3, 7)
    color = COLORS[randint(0, len(COLORS) - 1)]

    return {
        'x': x,
        'y': y,
        'vx': v_x,
        'vy': v_y,
        'r': r,
        'color': color
    }


def update_pos(objects):
    '''
    просчитываем позицию объектов "objects" в новом кадре
    '''

    for i in range(len(objects)):
        objects[i]['x'] += objects[i]['vx']
        objects[i]['y'] += objects[i]['vy']

        x = objects[i]['x']
        y = objects[i]['y']
        r = objects[i]['r']
        v_x = objects[i]['vx']
        v_y = objects[i]['vy']

        if x - r < 0 or x + r > WIDTH:
            objects[i]['vx'] *= -1
            objects[i]['vy'] = sign(v_y) * randint(3, 7)
            objects[i]['x'] += objects[i]['vx']
        if y - r < 0 or y + r > HEIGHT:
            objects[i]['vy'] *= -1
            objects[i]['vx'] = sign(v_x) * randint(3, 7)
            objects[i]['y'] += objects[i]['vy']

        objects[i]['r'] += 0.1

    for i, object in enumerate(objects):
        if object['r'] > R_MAX + 10:
            objects[i] = create_nice_ball()
        x, y = object['x'], object['y']


def update_canvas(objects):
    '''
    перерисовываем объекты
    '''

    for i in range(len(objects)):
        circle(screen, objects[i]['color'],
               (int(objects[i]['x']), int(objects[i]['y'])),
               int(objects[i]['r']))


def is_clicked(event, object):
    '''
    проверяем нажатие на объект
    '''

    mx, my = event.pos
    x, y, r = object['x'], object['y'], object['r']

    return abs(x - mx) < r and abs(y - my) < r


balls = [create_nice_ball() for i in range(LIMIT)]
points = 0

set_screen()
pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for i, ball in enumerate(balls):
                if is_clicked(event, ball):
                    balls[i] = create_nice_ball()
                    points += int((2 * (ball['vx'] ** 2 + ball['vy'] ** 2) ** 0.5 +
                                   0.3 * (R_MAX + 10 - ball['r'])))

    update_pos(balls)
    update_canvas(balls)

    pygame.display.set_caption('SCORE:    ' + str(points))
    pygame.display.update()

    set_screen()

pygame.quit()
