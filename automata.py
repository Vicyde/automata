import sys
import argparse
import math
import pygame 
import random 

from pygame.locals import *

from typing import Collection


class GuiApp:
    def __init__(self):
        self.running = False
        self.drawing_surface = None
        self.automata_surface = None
        self.size = (800, 600)
        self.automata_size = ()
        self.color_pixel = [255, 255, 255]
        self.color_background = [0, 0, 0]
        self.pixel_size = 0
        self.row = []
        self.dx = 0
        self.dy = 0

    def set_title(self, title):
        pygame.display.set_caption(title)

    def on_init(self):
        pygame.init()
        self.drawing_surface = pygame.display.set_mode(self.size, pygame.HWSURFACE)

        print("Automata Size: ", self.automata_size)
        
        self.running = True

        if self.pixel_size == 0:
            self.pixel_size = math.floor(min(
                self.size[0] / len(self.row[0]),
                self.size[1] / len(self.row)
            ))

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_KP_PLUS:
                self.pixel_size += 1
            elif event.key == pygame.K_KP_MINUS:
                self.pixel_size -= 1 if self.pixel_size > 1 else 0
            elif event.key == pygame.K_DOWN:
                self.dy += 5
            elif event.key == pygame.K_UP:
                self.dy += -5
            elif event.key == pygame.K_RIGHT:
                self.dx += 5
            elif event.key == pygame.K_LEFT:
                self.dx += -5


    def create_automata_surface(self):
        self.automata_size = (self.pixel_size * len(self.row[0]), self.pixel_size * len(self.row))
        self.automata_surface = pygame.Surface(self.automata_size)
        print(self.automata_size)

        x = 0
        y = 0
        for row in self.row:
            for col in row:
                pygame.draw.rect(self.automata_surface, self.color_pixel if col == 1 else self.color_background, pygame.Rect(x, y, self.pixel_size, self.pixel_size))   
                x += self.pixel_size
            y += self.pixel_size
            x = 0         

    def on_draw(self):
        self.drawing_surface.fill(self.color_background)
        self.drawing_surface.blit(self.automata_surface, (self.dx,self.dy))
            
        pygame.display.update()

    def on_close(self):
        pygame.quit()

    def display(self, row, pixel_size):
        self.row = row      
        self.pixel_size = pixel_size

        if self.on_init() == False:
            self.running = False

        self.create_automata_surface()
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
    print()
    parser = argparse.ArgumentParser(description="Shows a cellular automata.")
    parser.add_argument('--rule', type=int, help="Rule to use, using wolfram rulenumber", default=30)
    parser.add_argument('--rows', type=int, help="Amount of rows to print", default=80)
    parser.add_argument('--cols', type=int, help="The width of each row", default=64)
    parser.add_argument('--gui', action='store_true', help="Print using graphics")
    parser.add_argument('--size', type=int, help="GUI only: Size of each pixel", default=0)
    parser.add_argument('--random', action='store_true', help="Starting row will be randomized")
    args = parser.parse_args()

    rule = args.rule
    height = args.rows
    width = args.cols

    if rule > 255:
        print("Rule can't exceed 256.")
        exit(1)

    col = [ 0 ] * width

    if args.random:
        for n in range(0, len(col)):
            col[n] = random.randrange(0, 2)
    else:
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
        window.set_title("Showing rule %i" % rule)
        window.display(row, args.size)
    else:
        for n in row:
            print_row(n)


if __name__ == '__main__':
    main(sys.argv)

    