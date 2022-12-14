# AoC 2022 - Day 17 - Mike D
import sys
import os
import string
import copy
from aocd import get_data, submit
from tqdm import tqdm
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from utils import *

input_data = get_data(day=17, year=2022)
testdata = ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"

horizontal = [['#','#','#','#']]
plus = [
    ['.', '#', '.'],
    ['#', '#', '#'],
    ['.', '#', '.']
]
invplus = [
    ['.', '#', '.'],
    ['#', '#', '#'],
    ['#', '.', '#']
]
lshape = [
    ['.','.','#'],
    ['.','.','#'],
    ['#','#','#']
]
line = [
    ['#'],
    ['#'],
    ['#'],
    ['#']
]
square = [
    ['#','#'],
    ['#','#']
]

rocks = [horizontal, plus, lshape, line, square]
width = 7
headroom = 7
limit = 100

class data:
    def __init__(self, wind):
        self.removed = 0
        self.chamber = make_grid(width, headroom, ".")
        self.wind = wind
        self.cycle = 0
        self.x = 0
        self.y = 0
        self.falling = False
        self.shape = None
        self.startcycle = 0
        self.rockid = 0
        self.additional_height = 0
        self.states = []

def add_rows(d, n):
    for i in range(n):
        row = ['.'] * width
        d.chamber.insert(0, row)

def check_headroom(d):
    h = 0
    if not d.falling:
        for j in range(headroom):
            if d.chamber[j].count('#') > 0:
                h += 1
        add_rows(d, h)

def check_next_shape(d, rock):
    # do we have a shape?
    if not d.falling:
        d.rockid = rock % len(rocks)
        d.shape = rocks[rock % len(rocks)]
        d.x = 2
        d.y = 4 - len(d.shape)
        d.falling = True
        d.startcycle = d.cycle
        
def blow_wind(d):
    action = d.wind[d.cycle % len(d.wind)]
    d.cycle += 1
    good = False
    right = action == '>'

    if right and not d.x + 1 > width - len(d.shape[0]):
        good = True
    elif not right and not d.x - 1 < 0:
        good = True
       
    # check every point in d.shape can move in d.chamber
    if good:
        for i in range (len(d.shape)):
            for j in range (len(d.shape[i])):
                chamber_x = d.x+j+1 if right else d.x+j-1

                if d.shape[i][j] == '#' and d.chamber[d.y+i][chamber_x] == '#':
                    good = False
                    break
            if not good:
                break

    if good and right:
        d.x += 1
    elif good and not right:
        d.x -= 1

def handle_gravity(d):
    gravity = d.y + len(d.shape) < len(d.chamber)
    if gravity: 
        for i in range (len(d.shape)):
            for j in range (len(d.shape[i])):
                if d.shape[i][j] == '#':
                    if d.chamber[d.y+i+1][d.x+j] != '.':
                        gravity = False
    if gravity:
        d.y += 1
    else:
        d.falling = False
        for l in range(len(d.shape)):
            for m in range(len(d.shape[l])):
                if d.shape[l][m] == '#':
                    d.chamber[d.y+l][d.x+m] = '#'

def handle_collision(d):
    for j in range(len(d.shape)):
        for k in range(len(d.shape[j])):
            if d.shape[j][k] == '#':
                if d.chamber[d.y+j][d.x+k] == '#':
                    d.falling = False
                    for l in range(len(d.shape)):
                        for m in range(len(d.shape[l])):
                            if d.shape[l][m] == '#':
                                d.chamber[d.y+l][d.x+m] = '#'
                    break
        if not d.falling:
            break

def print_debug(d):
    action = d.wind[d.cycle % len(d.wind)]
    print(d.cycle, d.falling, action)
    c = copy.deepcopy(d.chamber)
    if d.falling:
        for j in range(0, min(25, len(d.shape))):
            for k in range(len(d.shape[j])):
                if d.shape[j][k] == '#':
                    c[d.y+j][d.x+k] = '@'
    print_grid(c)

def check_for_cycles(d: data, total_rocks, rock):
    if d.additional_height == 0:
        cols = []
        for column in range(len(d.chamber[0])):
            max_col = -1
            for row in range(len(d.chamber)):
                if d.chamber[row][column] == '#':
                    max_col = row
                    break
            cols.append(max_col)

        height = len(d.chamber) - headroom
        smol = min(cols)
        cols = [c - smol for c in cols]

        cols.append(rock % len(rocks))
        cols.append(d.cycle % len(d.wind))
        cols = tuple(cols)

        if cols in d.states:
            remaining = total_rocks - rock
            cycles = remaining//rock
            leftover = remaining % rock
            d.additional_height = height * cycles
            return total_rocks - leftover

        else:
            d.states.append(cols)
    return rock + 1

def cycle(total_rocks, d: data, debug):
    rock = 0
    while rock < total_rocks + 1:
        check_headroom(d)
        check_next_shape(d, rock)
        
        while d.falling:
            blow_wind(d)
            handle_gravity(d)
            handle_collision(d)
            if debug:
                print_debug(d)

        rock = check_for_cycles(d, total_rocks, rock)
    return len(d.chamber) - headroom + d.removed + d.additional_height

def part1():
    d = data(input_data)
    return cycle(2022, d, False)
    
def part2():
    d = data(input_data)
    return cycle(1000000000000, d, False) 

if __name__ == "__main__":
    print("-- AoC 2022 - Day 17 --\n")
    # part("One", 17, 2022, part1, False)
    part("Two", 17, 2022, part2, False)
