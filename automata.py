import sys
import argparse
import math
import pygame 
from pygame.locals import *

from typing import Collection


class GuiApp:
    def __init__(self):
        self.running = False
        self.drawing_surface = None
        self.size = (800, 600)
        self.color_pixel = [255, 255, 255]
        self.color_background = [0, 0, 0]
        self.pixel_size = 10

    def on_init(self):
        pygame.init()
        self.drawing_surface = pygame.display.set_mode(self.size, pygame.HWSURFACE)
        self.running = True

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False

    def on_draw(self):
        self.drawing_surface.fill(self.color_background)

        x = 0
        y = 0

        # Draw every row
        for row in self.row:
            for col in row:
                pygame.draw.rect(self.drawing_surface, self.color_pixel if col == 1 else self.color_background, pygame.Rect(x, y, self.pixel_size, self.pixel_size))
                x += self.pixel_size
            y += self.pixel_size
            x = 0
            
        pygame.display.flip()

    def on_close(self):
        pygame.quit()

    def display(self, row):
        self.row = row
        if self.on_init() == False:
            self.running = False
        while(self.running):
            for event in pygame.event.get():
                self.on_event(event)

            self.on_draw()
            
            # do something
        self.on_close()


def print_row(row, t="*", f="-"):
    """
    Prints a list to the standard output where a 1 is written as a *, everything else as -.
    """
    for x in row:
        print(t if x == 1 else f, end='')

    print()


def generate_ruleset(rule):
    """
    Generates a ruleset (a list of 8 rules) from a wolfram rule number.
    """
    rule = "{:08b}".format(rule)  
    ruleset =  []
  
    for n in range(8):
        ruleset.append(int(rule[7-n]))

    return ruleset


def calculate_row(row, ruleset):
    """
    Generates a new row based on the given row and ruleset.
    """
    newrow = []

    for x in range(len(row)):
        xl = 0 if x == 0 else row[x-1]             # if at the left edge, xl is 0. Else it is the value in x-1
        xr = 0 if x >= len(row) - 1 else row[x+1]   # if at the right edge, xr = 0. Else it is the value in x+1
        xc = row[x]

        # convert the binary xl, xc, xr to a number
        val = (xl << 2) + (xc << 1) + xr
        newrow.append(ruleset[val])

    return newrow


def main(argv):
    parser = argparse.ArgumentParser(description="Shows an cellular automata.")
    parser.add_argument('--rule', type=int, help="Rule to use, using wolfram rulenumber", default=30)
    parser.add_argument('--rows', type=int, help="Amount of rows to print", default=80)
    parser.add_argument('--cols', type=int, help="The width of each row", default=64)
    parser.add_argument('--gui', action='store_true', help="Print using graphics")
    args = parser.parse_args()

    rule = args.rule
    height = args.rows
    width = args.cols

    col = [ 0 ] * width
    col[math.floor(width/2)] = 1
    row = []

    ruleset = generate_ruleset(rule)
    row.append(col)

    print("Generating %i rows using rule %i." % (height, rule))
    for n in range(1,height):
        row.append(calculate_row(row[n-1], ruleset))

    # print
    if args.gui:
        window = GuiApp()
        window.display(row)
    else:
        for n in row:
            print_row(n)


if __name__ == '__main__':
    main(sys.argv)

    