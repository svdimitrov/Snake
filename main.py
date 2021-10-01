import pygame
import tkinter
from tkinter import messagebox
import random
import os

x = 400
y = 150
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x, y)
WIDTH = 600
length = 0
screen = pygame.display.set_mode((WIDTH, WIDTH))
is_running = True
image_up = pygame.image.load(r'img/HeadUp.png')
image_left = pygame.image.load(r'img/HeadLeft.png')
image_right = pygame.image.load(r'img/HeadRight.png')
image_down = pygame.image.load(r'img/HeadDown.png')


class Cube:

    def __init__(self, pos, color='green', head=False):
        self.pos = pos
        self.color = color
        self.head = head
        self.dirnx = 1
        self.dirny = 0

    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + 30 * self.dirnx,
                    self.pos[1] + 30 * self.dirny)

    def draw(self):
        i = self.pos[0]
        j = self.pos[1]
        if self.color == 'green':
            if self.head:
                if (self.dirnx, self.dirny) == (1, 0):
                    screen.blit(image_right, (i, j))
                elif (self.dirnx, self.dirny) == (-1, 0):
                    screen.blit(image_left, (i, j))
                elif (self.dirnx, self.dirny) == (0, 1):
                    screen.blit(image_down, (i, j))
                elif (self.dirnx, self.dirny) == (0, -1):
                    screen.blit(image_up, (i, j))
            else:
                pygame.draw.rect(screen, (0, 220, 0), (i + 1, j + 1, 29, 29))
        else:
            pygame.draw.rect(screen, (255, 0, 0), (i + 1, j + 1, 29, 29))


class Snake:
    body = []
    turns = {}

    def __init__(self, pos, color='green'):
        self.pos = pos
        self.color = color
        self.head = Cube(self.pos, head=True)
        self.body.append(self.head)
        self.dirx = 1
        self.diry = 0

    def move(self):
        global is_running
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                is_running = False
                break
            keys = pygame.key.get_pressed()
            for key in keys:
                if keys[pygame.K_UP]:
                    self.dirx = 0
                    self.diry = -1
                    self.turns[self.head.pos] = (self.dirx, self.diry)
                if keys[pygame.K_DOWN]:
                    self.dirx = 0
                    self.diry = 1
                    self.turns[self.head.pos] = (self.dirx, self.diry)
                if keys[pygame.K_RIGHT]:
                    self.dirx = 1
                    self.diry = 0
                    self.turns[self.head.pos] = (self.dirx, self.diry)
                if keys[pygame.K_LEFT]:
                    self.dirx = -1
                    self.diry = 0
                    self.turns[self.head.pos] = (self.dirx, self.diry)

        for index, cube in enumerate(self.body):
            p = cube.pos
            if p in self.turns:
                turn = self.turns[p]
                cube.move(turn[0], turn[1])
                if index == len(self.body) - 1:
                    self.turns.pop(p)
            else:
                if cube.pos[0] <= 0 and (cube.dirnx, cube.dirny) == (-1, 0):
                    is_running = False
                elif cube.pos[0] >= 570 and (cube.dirnx, cube.dirny) == (1, 0):
                    is_running = False
                elif cube.pos[1] <= 0 and (cube.dirnx, cube.dirny) == (0, -1):
                    is_running = False
                elif cube.pos[1] >= 570 and (cube.dirnx, cube.dirny) == (0, 1):
                    is_running = False
                else:
                    cube.move(cube.dirnx, cube.dirny)

    def draw(self):
        for index, cube in enumerate(self.body):
            cube.draw()

    def add_cube(self):
        last = self.body[-1]
        if last.dirnx == 1 and last.dirny == 0:
            tail = Cube(pos=(last.pos[0] - 30, last.pos[1]))
        elif last.dirnx == -1 and last.dirny == 0:
            tail = Cube(pos=(last.pos[0] + 30, last.pos[1]))
        elif last.dirnx == 0 and last.dirny == 1:
            tail = Cube(pos=(last.pos[0], last.pos[1] - 30))
        elif last.dirnx == 0 and last.dirny == -1:
            tail = Cube(pos=(last.pos[0], last.pos[1] + 30))

        tail.dirnx = last.dirnx
        tail.dirny = last.dirny
        self.body.append(tail)


def random_pos(snake):
    f_list = []
    for i in range(0, 600, 30):
        f_list.append(i)
    f_random = random.choice(f_list)
    s_random = random.choice(f_list)
    if (f_random, s_random) in snake.body:
        random_pos(snake)
    return f_random, s_random


def redraw_window(snake, snack):
    screen.fill((20, 20, 20))
    snake.draw()
    snack.draw()
    pygame.display.set_caption('Snake                                               '
                               '                    Score: {0}'.format(len(snake.body)))
    pygame.display.update()


def main():
    global is_running, length
    snake = Snake((0, 0))
    snack = Cube(random_pos(snake), color='red')
    clock = pygame.time.Clock()

    while is_running:
        length = len(snake.body)
        clock.tick(10)
        pygame.time.delay(50)
        for index, cube in enumerate(snake.body):
            if index != 0 and cube.pos == snake.head.pos:
                pygame.quit()
                is_running = False
                break
        if is_running:
            if snake.head.pos == snack.pos:
                snake.add_cube()
                snack = Cube(random_pos(snake), color='red')
            snake.move()
            redraw_window(snake, snack)


main()

root = tkinter.Tk()
root.withdraw()
messagebox.showinfo('Game Over!', 'Your length was: {0}'.format(length))
