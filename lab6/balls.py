import random
import numpy
import pygame
import csv

from random import randint
from operator import itemgetter
from LIB_colors import *
from pygame.draw import *

pygame.init()

FPS = 60
WIDTH = 900
MENU_WIDTH = 300
HEIGHT = 700
LIMIT = 10
R_MIN = 30
R_MAX = 40
TYPE_SQ = 1
TYPE_C = 0
CHECK = 100


def set_screen():
    """
    устанавоиваем фон и разметку
    """

    screen.fill(BLACK)
    line(screen, WHITE, (WIDTH, 0), (WIDTH, HEIGHT))


def sign(x):
    """
    просто удобная функция которая определяет знак числа
    """

    if x != 0:
        return abs(x) / x
    else:
        return 0


def rand_sign():
    """
    просто удобная функция, которая выдает рандомный знак +/-
    """

    return randint(1, 2) % 2 * 2 - 1


def create_nice_ball():
    """
    создаем "хороший" шарик, в рандомном месте и т.п.
    """

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


def create_nice_square():
    """
    создаем "хороший" квадратик, в рандомном месте на краю карты
    он появляется когда очки достигают степени 10 начиная с 100,
    (100, 1000, 10000, и тд) и при нажатии на них дают количество
    очков равное отметке появления умноженной на два
    100 -> 200
    1000 -> 2000
    и т.д.
    """

    r = randint(3, 6) * 10
    t = randint(0, 1)
    x = t * randint(0, WIDTH - r)
    y = (not t) * randint(0, HEIGHT - r)
    v_x = (not t) * randint(5, 8)
    v_y = t * randint(5, 8)
    color = COLORS[randint(0, len(COLORS) - 1)]

    return {
        'x': x,
        'y': y,
        'vx': v_x,
        'vy': v_y,
        'r': r,
        'color': color
    }


def update_pos(objects, type):
    """
    просчитываем позицию объектов "objects" в новом кадре
    """

    for i, obj in enumerate(objects):
        objects[i]['x'] += objects[i]['vx']
        objects[i]['y'] += objects[i]['vy']

        if type == TYPE_C:
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

    if type == TYPE_C:
        for i, obj in enumerate(objects):
            if obj['r'] > R_MAX + 10:
                objects[i] = create_nice_ball()


def update_canvas(objects, type):
    """
    перерисовываем объекты
    """

    for i, obj in enumerate(objects):
        x, y, r = obj['x'], obj['y'], obj['r']
        if type == TYPE_C:
            circle(screen, objects[i]['color'],
                   (int(x), int(y)), int(r))
        elif type == TYPE_SQ:
            rect(screen, objects[i]['color'],
                 [int(x), int(y), int(r), int(r)])


def is_clicked(event, object, type):
    """
    проверяем нажатие на объект
    """

    mx, my = event.pos
    x, y, r = object['x'], object['y'], object['r']

    if type == TYPE_C:
        return abs(x - mx) < r and abs(y - my) < r
    elif type == TYPE_SQ:
        return (x < mx < x + r) and (y < my < y + r)


def leaderboard():
    file = open('leaderboard.txt', 'r')
    board = file.readlines()
    file.close()
    n = len(board)
    font1 = pygame.font.Font(None, 30)
    text = [font1.render('LEADERBOARD:', 1, YELLOW)]
    font1 = pygame.font.Font(None, 24)
    for i in range(min(n, 10)):
        text.append(font1.render(board[i][:-1], 1, BLUE))
    screen.blit(text[0], (WIDTH + 10, 10))
    for i in range(min(n, 10)):
        screen.blit(text[i + 1], (WIDTH + 10, i * 20 + 30))


def update_leaderboard(name, score):
    file = open('leaderboard.txt', 'r')
    board = file.readlines()
    file.close()
    board.append(str(score) + ' ' + name + '\n')
    n = len(board)
    board = [board[i].split() for i in range(n)]
    board = [[int(board[i][0]), board[i][1]] for i in range(n)]
    board.sort(reverse=True)
    board = [str(board[i][0]) + ' ' + str(board[i][1]) + '\n' for i in range(n)]
    board = board[:min(10, n)]
    file = open('leaderboard.txt', 'w')
    file.writelines(board)
    file.close()


name = str(input('Name your fighter(No more than 15 symbols): \n'))
name = name[:15]

screen = pygame.display.set_mode((WIDTH + MENU_WIDTH, HEIGHT))

balls = [create_nice_ball() for i in range(LIMIT)]
squares = []
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
                if is_clicked(event, ball, TYPE_C):
                    balls[i] = create_nice_ball()
                    points += int((2 * (ball['vx'] ** 2 + ball['vy'] ** 2) ** 0.5 +
                                   0.3 * (R_MAX + 10 - ball['r'])))
            if squares and is_clicked(event, squares[0], TYPE_SQ):
                squares = []
                points += (CHECK // 5)

    if points > CHECK:
        squares.append(create_nice_square())
        CHECK *= 10
    update_pos(squares, TYPE_SQ)
    if squares:
        x, y, r = squares[0]['x'], squares[0]['y'], squares[0]['r']
        if x + r > WIDTH or y + r > HEIGHT:
            squares = []
    update_canvas(squares, TYPE_SQ)

    update_pos(balls, TYPE_C)
    update_canvas(balls, TYPE_C)

    leaderboard()
    pygame.display.set_caption(name + '\'s SCORE:    ' + str(points))
    pygame.display.update()

    set_screen()

update_leaderboard(name, points)
pygame.quit()
