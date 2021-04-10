import pygame
import random
import tkinter as tk
from tkinter import messagebox

class Cube:

    def __init__(self, start, dirx=1, diry=0, color=(255, 0, 0)):
        self.pos = start
        self.dir_x = 1
        self.dir_y = 0
        self.rows= rows
        self.color = color
    def move(self, dirx, diry):
        self.dir_x = dirx
        self.dir_y = diry
        self.pos = (self.pos[0] + self.dir_x, self.pos[1]+ self.dir_y)
    def draw(self, surf, eyes=False):
        i = self.pos[0]
        j = self.pos[1]
        pygame.draw.rect(surf, self.color, (i*block_size+1, j*block_size+1, block_size-2, block_size-2))

        if eyes:
            center = block_size // 2
            r = block_size/6
            circle_mid = (i*block_size+center-r, j*block_size+8)
            circle_mid_2 = (i*block_size +block_size-r*2, j*block_size+8)
            pygame.draw.circle(surf, (255, 255, 255), circle_mid, r)
            pygame.draw.circle(surf, (255, 255, 255), circle_mid_2, r)



class Snake:
    body = []
    turns = {}
    def __init__(self, color, pos):
        self.color = color
        self.head = Cube(pos)
        self.body.append(self.head)
        self.dir_x = 0
        self.dir_y = 0
    
    def reset(self):
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dir_y = 1
        self.dir_x = 0

    def poisioned(self):
        self.body = self.body[:-4]

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            keys = pygame.key.get_pressed()

            for key in keys:
                if keys[pygame.K_LEFT] and self.dir_x != 1:
                    self.dir_x = -1
                    self.dir_y = 0
                    self.turns[self.head.pos[:]] = [self.dir_x, self.dir_y]
                elif keys[pygame.K_RIGHT] and self.dir_x != -1:
                    self.dir_x = 1
                    self.dir_y = 0
                    self.turns[self.head.pos[:]] = [self.dir_x, self.dir_y]
                elif keys[pygame.K_UP] and self.dir_y != 1:
                    self.dir_x = 0
                    self.dir_y = -1
                    self.turns[self.head.pos[:]] = [self.dir_x, self.dir_y]
                elif keys[pygame.K_DOWN] and self.dir_y != -1:
                    self.dir_x = 0
                    self.dir_y = 1
                    self.turns[self.head.pos[:]] = [self.dir_x, self.dir_y]
        
        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body) - 1:
                    self.turns.pop(p)
            else:
                if c.dir_x == -1 and c.pos[0] <= 0:
                    c.pos = (c.rows-1, c.pos[1])
                elif c.dir_x == 1 and c.pos[0] >= c.rows-1:
                    c.pos = (0, c.pos[1])
                elif c.dir_y == 1 and c.pos[1] >= c.rows-1:
                    c.pos = (c.pos[0], 0)
                elif c.dir_y == -1 and c.pos[1] <= 0:
                    c.pos = (c.pos[0], c.rows-1)
                else:
                    c.move(c.dir_x, c.dir_y)

    def draw(self, surf):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surf, eyes=True)
            else:
                c.draw(surf)

    def add_cube(self):
        tail = self.body[-1]
        new_x, new_y = tail.dir_x, tail.dir_y
        if new_x == 1 and new_y == 0:
            self.body.append(Cube((tail.pos[0]-1, tail.pos[1])))
        elif new_x == -1 and new_y == 0:
            self.body.append(Cube((tail.pos[0]+1, tail.pos[1])))
        elif new_x == 0 and new_y == 1:
            self.body.append(Cube((tail.pos[0], tail.pos[1]-1)))
        elif new_x == 0 and new_y == -1:
            self.body.append(Cube((tail.pos[0], tail.pos[1]+1)))
    
        self.body[-1].dir_x = new_x
        self.body[-1].dir_y = new_y

    def add_5_cubes(self):
        for i in range(5):
            self.add_cube()

def make_snack(rows, item):
    positions = item.body
    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda  z: z.pos==(x,y), positions))) > 0:
            continue
        else:
            break
    return (x,y)

def make_grid(surf):
    size_block = width / rows
    x, y = 0, 0
    for line in range(rows):
        x += size_block
        y += size_block
        pygame.draw.line(surf, (255, 255, 255), (x, 0), (x, width))
        pygame.draw.line(surf, (255, 255, 255),(0, y), (width, y))

def print_message(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass

def re_make_window(surf, snake, snack, snack_extra, poision):
    surf.fill((0, 0, 0))
    snake.draw(surf)
    snack.draw(surf)
    if len(snake.body) > 5:
        snack_extra.draw(surf)
        poision.draw(surf)
    make_grid(surf)
    pygame.display.update()

def game():
    #init_window = pygame.display.set_mode(500, 500)
    global width, rows, block_size
    width = 500
    rows = 20
    block_size = width / rows
    window = pygame.display.set_mode((width, width))
    snake = Snake((255, 0, 0), (rows/2, rows/2))
    snack = Cube(make_snack(rows, snake), color=(255,69,0))
    snack_extra = Cube(make_snack(rows, snake), color=(0, 255, 0))
    poision = Cube(make_snack(rows, snake), color=(0, 0, 255))
    game_on = True
    clock = pygame.time.Clock()
    blocks_traveled_from_last = 0
    timing = 10
    while game_on:
        blocks_traveled_from_last += 1
        pygame.event.pump()
        pygame.time.delay(5)
        clock.tick(timing)
        snake.move()
        if snake.body[0].pos == snack.pos:
            snake.add_cube()
            snack = Cube(make_snack(rows, snake), color=(255,69,0))
            poision = Cube(make_snack(rows, snake), color=(0, 0, 255))
            snack_extra = Cube(make_snack(rows, snake), color=(0, 255, 0))
            blocks_traveled_from_last = 0
        elif len(snake.body) > 5 and snake.body[0].pos == snack_extra.pos:
            snake.add_5_cubes()
            snack = Cube(make_snack(rows, snake), color=(255,69,0))
            snack_extra = Cube(make_snack(rows, snake), color=(0, 255, 0))
            poision = Cube(make_snack(rows, snake), color=(0, 0, 255))
            blocks_traveled_from_last = 0
        elif len(snake.body) > 5 and snake.body[0].pos == poision.pos:
            snack = Cube(make_snack(rows, snake), color=(255,69,0))
            snack_extra = Cube(make_snack(rows, snake), color=(0, 255, 0))
            snake.poisioned()
            poision = Cube(make_snack(rows, snake), color=(0, 0, 255))
            blocks_traveled_from_last = 0
        for x in range(len(snake.body)):
            if snake.body[x].pos in list(map(lambda z: z.pos, snake.body[x+1:])):
                print(f"Score: {len(snake.body)}")
                print_message("You done fucked up", "try again")
                snake.reset()
                break

        if len(snake.body) > 5:
            timing = 15
        elif len(snake.body) > 10:
            timing = 20
        else:
            timing = 10

        if blocks_traveled_from_last >= rows*1.5:
            snack_extra = Cube(make_snack(rows, snake), color=(0, 255, 0))
            blocks_traveled_from_last = 0

        re_make_window(window, snake, snack, snack_extra, poision)




game()