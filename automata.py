import sys
import argparse
import math

from typing import Collection

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
        pass
    else:
        for n in row:
            print_row(n)


if __name__ == '__main__':
    main(sys.argv)

    