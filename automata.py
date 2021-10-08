import sys

def print_row(row):
    for x in row:
        print("*" if x == 1 else "-", end='')

    print()


def generate_ruleset(rule):
    rule = "{:08b}".format(rule)  
    ruleset =  []
  
    for n in range(8):
        ruleset.append(int(rule[7-n]))

    return ruleset


def calculate_row(row, ruleset):
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
    rule = 90
    height = 80

    if len(argv) > 1:
        for arg in range(1, len(argv)):
            if argv[arg] == '-r':
                arg += 1
                rule = int(arg)
            if argv[arg] == '-h':
                arg += 1
                height = int(argv[arg])

    row = [ 0 ] * 64
    row[32] = 1

    ruleset = generate_ruleset(rule)

    for n in range(height):
        print_row(row)
        row = calculate_row(row, ruleset)


if __name__ == '__main__':
    main(sys.argv)

    