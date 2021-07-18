from pygame import *
import time
import random
import pygame.locals

pygame.init()
size = width, height = 100, 250
screen = pygame.display.set_mode(size)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (220, 0, 0)
GREEN = (0, 180, 0)
ROWS, COLS = 30, 10
CELL_SIZE = 10
offset = -50
d = []
keys = [False, False]
font = pygame.font.Font('freesansbold.ttf', 20)
# text_rect = (120, 20)
# ended_ind = (120, 50)
# ended = font.render('GAME OVER', True, GREEN)
enemies = [[[0, 3], [1, 2], [1, 3], [1, 4], [2, 3], [3, 2], [3, 4]],
           [[0, 6], [1, 5], [1, 6], [1, 7], [2, 6], [3, 5], [3, 7]]]

for i in range(ROWS):
    for j in range(COLS):
        rect = pygame.Rect(j * CELL_SIZE, offset + i * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, WHITE, rect)
        pygame.draw.rect(screen, BLACK, rect, 1)


def default():
    for x, y in enemies[0]:
        player = pygame.Rect(y * CELL_SIZE, offset + (26 + x) * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, GREEN, player)
        pygame.draw.rect(screen, BLACK, player, 1)
    return player


m = default()


def player():
    d = enemies[1]
    for x, y in d:
        enem_plane = pygame.Rect(y * CELL_SIZE, offset + (26 + x) * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, WHITE, enem_plane)
        pygame.draw.rect(screen, BLACK, enem_plane, 1)
    d = enemies[0]
    for x, y in d:
        player = pygame.Rect(y * CELL_SIZE, offset + (26 + x) * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, GREEN, player)
        pygame.draw.rect(screen, BLACK, player, 1)
    return player


def player2():
    d = enemies[0]
    for x, y in d:
        enem_plane = pygame.Rect(y * CELL_SIZE, offset + (26 + x) * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, WHITE, enem_plane)
        pygame.draw.rect(screen, BLACK, enem_plane, 1)
    d = enemies[1]
    for x, y in d:
        player = pygame.Rect(y * CELL_SIZE, offset + (26 + x) * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, GREEN, player)
        pygame.draw.rect(screen, BLACK, player, 1)
    return player


def enemy(i, e, r, m):
    if e[r] != 0:
        for x, y in e[r]:
            if i + x < ROWS:
                enem = pygame.Rect(y * CELL_SIZE, offset + (i + x) * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, RED, enem)
                pygame.draw.rect(screen, BLACK, enem, 1)
            else:
                break
            if enem == m:
                # screen.blit(ended, ended_ind)
                time.sleep(2.0)
                pygame.quit()

    if i >= 9:
        enemy(i - 9, e, r + 1, m)


def enemy_dest(i, e, r):
    if e[r] != 0:
        for x, y in e[r]:
            if i + x < ROWS:
                enem_plane = pygame.Rect(y * CELL_SIZE, offset + (i + x) * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, WHITE, enem_plane)
                pygame.draw.rect(screen, BLACK, enem_plane, 1)
            else:
                break
    if i >= 9:
        enemy_dest(i - 9, e, r + 1)


def border(i):
    while i > ROWS:
        i -= ROWS
    for j in [0, 9]:
        for k in range(-ROWS, ROWS, 5):
            if i + k < ROWS:
                border = pygame.Rect(j * CELL_SIZE, offset + (i + k) * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, BLACK, border)
                border0 = pygame.Rect(j * CELL_SIZE, offset + (i + k + 1) * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, BLACK, border0)
            else:
                break


def border_dest(i):
    while i > ROWS:
        i -= ROWS
    for j in [0, 9]:
        for k in range(-ROWS, ROWS, 5):
            if i + k < ROWS:
                plane = pygame.Rect(j * CELL_SIZE, offset + (i + k) * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                plane0 = pygame.Rect(j * CELL_SIZE, offset + (i + k + 1) * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, WHITE, plane)
                pygame.draw.rect(screen, BLACK, plane, 1)
                pygame.draw.rect(screen, WHITE, plane0)
                pygame.draw.rect(screen, BLACK, plane0, 1)
            else:
                break


def border_run(enemies, m):
    e = []
    i = 0
    r = 0
    z = 0
    while True:
        # text = font.render('Score: ' + str(i), True, GREEN)
        # screen.blit(text, text_rect)
        if i % 9 == 0:
            e.append(enemies[random.randint(0, 1)])
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == K_LEFT:
                    keys[0] = True
                if event.key == K_RIGHT:
                    keys[1] = True
            if event.type == pygame.KEYUP:
                if event.key == K_LEFT:
                    keys[0] = False
                if event.key == K_RIGHT:
                    keys[1] = False
        if keys[0] == True:
            m = player()
        elif keys[1] == True:
            m = player2()
        enemy(i, e, r, m)
        border(i)
        time.sleep(0.15)
        pygame.display.update()
        border_dest(i)
        enemy_dest(i, e, r)
        i += 1
        if i % 45 == 0:
            e[z] = 0
            z += 1

border_run(enemies, m)