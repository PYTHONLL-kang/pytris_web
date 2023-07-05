from inspect import stack
from re import L
import pygame as pg
import time as t
import random as rand

black = (0, 0, 0)
white = (255, 255, 255)
yellow = (255, 255, 0)
light_blue = (0, 255, 255)
purple = (255, 0, 255)
blue = (30, 128, 255)
orange = (255, 140, 0)
green = (0, 221, 0)
red = (255, 0, 0)

size = [640, 640]
screen = pg.display.set_mode(size)

BLOCK_SIZE = 25

def return_loc(block_x, block_y, x, y):
    return [(block_x+x)*BLOCK_SIZE, (block_y+y)*BLOCK_SIZE]

class Block:
    def __init__(self, shape, color, type):
        self.X = 9
        self.Y = 0
        self.posit = 0
        self.last_decent = t.time()
        self.shape = shape
        self.spin = 0
        self.color = color

    def go_to(self, x, y):
        self.X = x
        self.Y = y

    def move(self, x_m, y_m):
        self.X = self.X + x_m
        self.Y = self.Y + y_m

    def draw_mino(self, spin):
        self.spin = spin
        for shape in self.shape[self.spin]:
            loc = return_loc(shape[0], shape[1], self.X, self.Y)
            pg.draw.rect(screen, self.color, [loc[0], loc[1], BLOCK_SIZE, BLOCK_SIZE])

    def mino_to_block(self):
        obj = []

        for shape in self.shape[self.spin]:
            obj.append({"X" : self.X + shape[0], "Y" : self.Y + shape[1], "color": self.color})

        return obj

class Block_I(Block):
    def __init__(self):
        super().__init__(
            [
                [
                    [0, 1],
                    [1, 1],
                    [2, 1],
                    [3, 1]
                ],
                [
                    [2, 0],
                    [2, 1],
                    [2, 2],
                    [2, 3]
                ],
                [
                    [0, 2],
                    [1, 2],
                    [2, 2],
                    [3, 2]
                ],
                [
                    [1, 0],
                    [1, 1],
                    [1, 2],
                    [1, 3]
                ]
            ], color=light_blue, type='I')

class Block_J(Block):
    def __init__(self):
        super().__init__(
            [
                [
                    [0, 0],
                    [0, 1],
                    [1, 1],
                    [2, 1]
                ],
                [
                    [1, 0],
                    [2, 0],
                    [1, 1],
                    [1, 2]
                ],
                [
                    [0, 1],
                    [1, 1],
                    [2, 1],
                    [2, 2]
                ],
                [
                    [1, 0],
                    [1, 1],
                    [0, 2],
                    [1, 2]
                ]
            ], color=blue, type='J')

class Block_L(Block):
    def __init__(self):
        super().__init__(
            [
                [
                    [2, 0],
                    [0, 1],
                    [1, 1],
                    [2, 1]
                ],
                [
                    [1, 0],
                    [1, 1],
                    [1, 2],
                    [2, 2]
                ],
                [
                    [0, 1],
                    [1, 1],
                    [2, 1],
                    [0, 2]
                ],
                [
                    [0, 0],
                    [1, 0],
                    [1, 1],
                    [1, 2]
                ]
            ], color=orange, type='L')

class Block_O(Block):
    def __init__(self):
        super().__init__(
            [
                [
                    [1, 0],
                    [2, 0],
                    [1, 1],
                    [2, 1]
                ],
                [
                    [1, 0],
                    [2, 0],
                    [1, 1],
                    [2, 1]
                ],
                [
                    [1, 0],
                    [2, 0],
                    [1, 1],
                    [2, 1]
                ],
                [
                    [1, 0],
                    [2, 0],
                    [1, 1],
                    [2, 1]
                ]
            ], color=yellow, type='O')

class Block_S(Block):
    def __init__(self):
        super().__init__(
            [
                [
                    [1, 0],
                    [2, 0],
                    [0, 1],
                    [1, 1]
                ],
                [
                    [1, 0],
                    [1, 1],
                    [2, 1],
                    [2, 2]
                ],
                [
                    [1, 1],
                    [2, 1],
                    [0, 2],
                    [1, 2]
                ],
                [
                    [0, 0],
                    [0, 1],
                    [1, 1],
                    [1, 2]
                ]
            ], color=green, type='S')

class Block_T(Block):
    def __init__(self):
        super().__init__(
            [
                [
                    [1, 0],
                    [0, 1],
                    [1, 1],
                    [2, 1]
                ],
                [
                    [1, 0],
                    [1, 1],
                    [2, 1],
                    [1, 2]
                ],
                [
                    [0, 1],
                    [1, 1],
                    [2, 1],
                    [1, 2]
                ],
                [
                    [1, 0],
                    [0, 1],
                    [1, 1],
                    [1, 2]
                ]
            ], color=purple, type='T')

class Block_Z(Block):
    def __init__(self):
        super().__init__(
            [
                [
                    [0, 0],
                    [1, 0],
                    [1, 1],
                    [2, 1]
                ],
                [
                    [2, 0],
                    [1, 1],
                    [2, 1],
                    [1, 2]
                ],
                [
                    [0, 1],
                    [1, 1],
                    [1, 2],
                    [2, 2]
                ],
                [
                    [1, 0],
                    [0, 1],
                    [1, 1],
                    [0, 2]
                ]
            ], color=red, type='Z')

class Bag:
    def __init__(self):
        self.bag = [
            Block_I(),
            Block_J(),
            Block_L(),
            Block_O(),
            Block_S(),
            Block_T(),
            Block_Z()
        ]

    def pop_(self):
        if len(self.bag) == 0:
            self.__init__()
            return self.pop_()

        return self.bag.pop(rand.randrange(0, len(self.bag)))

class Hold:
    def __init__(self):
        self.holding = None

    def change(self, block):
        hold_block = self.holding
        self.holding = block
        if hold_block:
            hold_block.X = 9
            hold_block.Y = 0
        return hold_block

    def draw_holding_block(self):
        if self.holding == None:
            return None

        self.holding.X = 0
        self.holding.Y = 0
        self.holding.draw_mino(0)

class Stack:
    def __init__(self):
        self.stack_objects = [[] for i in range(25)]
        self.cleared_line = []

    def add(self, current_block):
        for block in current_block.mino_to_block():
            y_line = block["Y"]
            self.stack_objects[y_line].append({"X" : block["X"], "Y" : y_line, "color" : block["color"]})

    def draw_stack(self):
        for blockY in self.stack_objects:
            for block in blockY:
                if block != []:
                    pg.draw.rect(screen, block["color"], [block["X"]*BLOCK_SIZE, block["Y"]*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE])

    def clear_line(self):
        c = 0
        for i, stack_line in enumerate(self.stack_objects):
            if len(stack_line) > 9:
                self.stack_objects.pop(i)
                self.stack_objects.insert(0, [])
                self.cleared_line.append(i)
                c += 1

        for i, stack_line in enumerate(self.stack_objects):
            for j in range(len(self.stack_objects[i])):
                self.stack_objects[i][j]["Y"] = i

        return c
