import matplotlib.pyplot as plt 
import numpy as np

# --------------------------- IMAGE PROCESSING
TOP_LEFT = 0
TOP_RIGHT = 1
BOTTOM_LEFT = 2
BOTTOM_RIGHT = 3

BLUE_WIDTH = 2000

# --------------------------- FILTERS
BOARD_MIN_HUE = 89
BOARD_MAX_HUE = 115

HUE = 0
SATURATION = 1
VALUE = 2

# --------------------------- PATHS
INPUT_DIR = "../antrenare"

NC = 0 # no constraint
PL = 1 # plus
MI = 2 # minus
MU = 3 # multiply
DV = 4 # divide

CONSTRAINTS = \
[
    [NC, NC, NC, NC, NC, NC, NC, NC, NC, NC, NC, NC, NC, NC],
    [NC, NC, NC, NC, DV, NC, NC, NC, NC, DV, NC, NC, NC, NC],
    [NC, NC, NC, NC, NC, MI, NC, NC, MI, NC, NC, NC, NC, NC],
    [NC, NC, NC, NC, NC, NC, PL, MU, NC, NC, NC, NC, NC, NC],
    [NC, DV, NC, NC, NC, NC, MU, PL, NC, NC, NC, NC, DV, NC],
    [NC, NC, MI, NC, NC, NC, NC, NC, NC, NC, NC, MI, NC, NC],
    [NC, NC, NC, MU, PL, NC, NC, NC, NC, MU, PL, NC, NC, NC],
    [NC, NC, NC, PL, MU, NC, NC, NC, NC, PL, MU, NC, NC, NC],
    [NC, NC, MI, NC, NC, NC, NC, NC, NC, NC, NC, MI, NC, NC],
    [NC, DV, NC, NC, NC, NC, PL, MU, NC, NC, NC, NC, DV, NC],
    [NC, NC, NC, NC, NC, NC, MU, PL, NC, NC, NC, NC, NC, NC],
    [NC, NC, NC, NC, NC, MI, NC, NC, MI, NC, NC, NC, NC, NC],
    [NC, NC, NC, NC, DV, NC, NC, NC, NC, DV, NC, NC, NC, NC],
    [NC, NC, NC, NC, NC, NC, NC, NC, NC, NC, NC, NC, NC, NC],
]

BONUSES = \
[ 
    [3, 1, 1, 1, 1, 1, 3, 3, 1, 1, 1, 1, 1, 3], 
    [1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1], 
    [1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1], 
    [1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1], 
    [1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1], 
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3], 
    [3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3], 
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1], 
    [1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1], 
    [1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1], 
    [1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1], 
    [3, 1, 1, 1, 1, 1, 3, 3, 1, 1, 1, 1, 1, 3], 
]

NUMBERS = \
[ 
    0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 
    10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 
    20, 21, 24, 25, 27, 28, 
    30, 32, 35, 36, 
    40, 42, 45, 48, 49, 
    50, 54, 56, 
    60, 63, 64, 
    70, 72, 
    80, 81, 
    90
]


def testConsts():
    mat = []
    for i in range(len(BONUSES)):
        line = []
        for j in range(len(BONUSES[0])):
            c = CONSTRAINTS[i][j]
            b = BONUSES[i][j]
            if c != 0:
                if c == PL:
                    line.append('+')
                if c == MI:
                    line.append('-')
                if c == MU:
                    line.append('*')
                if c == DV:
                    line.append('/')
            elif b != 1:
                if b == 2:
                    line.append('2')
                if b == 3:
                    line.append('3')
            else:
                line.append(' ')

        mat.append(line)

    for i in range(len(BONUSES)):
        for j in range(len(BONUSES[0])):
            print(mat[i][j], end = " ")
        print()
    
    plt.imshow(CONSTRAINTS)
    plt.show()
    plt.imshow(BONUSES)
    plt.show()
 
# testConsts()