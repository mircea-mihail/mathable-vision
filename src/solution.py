import cv2 as cv

from image_processing import *
from constants import *

def get_board_change(prev_board, cur_board):
    diff_board = cv.absdiff(prev_board, cur_board)

    changed_square = [0, 0] 
    best_score = 0
    for i in range(TOTAL_SQUARES):
        for j in range(TOTAL_SQUARES):
            cur_score = np.sum(get_square(diff_board, j, i))
            if cur_score > best_score:
                best_score = cur_score
                changed_square[X] = j
                changed_square[Y] = i
    return changed_square

# returns the adnotations written in the _turns file, when each player's move starts, offset by one to start from 0
def get_players_moves(turns_file):
    players_moves = []

    with open(os.path.join(INPUT_DIR, turns_file), "r") as file:
        for line in file.readlines():
            players_moves.append(int(line.split(" ")[1].replace("\n", "")) - 1)

    return players_moves

# initialises the move matrix with minus ones and places 1 2 3 4 in the middle
def init_move_matrix():
    mat = np.full((14, 14), -1)
    mat[6][6] = 1
    mat[6][7] = 2
    mat[7][6] = 3
    mat[7][7] = 4

    return mat

# checks every ecuation between a and b and returns true if any matches the result using the constraint 
def check_ecuations(a, b, res, constraint):
    if constraint == NC:
        if a + b == res or abs(a - b) == res or a * b == res:
            return True
        if a != 0 and b != 0 and max(a, b) / min(a, b) == res:
            return True

    if constraint == PL and a + b == res:
        return True
    if constraint == MI and abs(a - b) == res:
        return True
    if constraint == MU and a * b == res:
        return True
    if constraint == DV: 
        if a != 0 and b != 0 and max(a, b) / min(a, b) == res:
            return True
    
    return False

# returns the score generated by placing a piece on the board at x and y locations
def get_score(x, y, val, board_mat):
    ecuations_found = 0
    # sus:
    if y > 1:
        a = board_mat[y - 1][x] 
        b = board_mat[y - 2][x]
        if a != -1 and b != -1:
            if check_ecuations(a, b, val, CONSTRAINTS[y][x]):
                ecuations_found += 1
    if y < 12:
        a = board_mat[y + 1][x] 
        b = board_mat[y + 2][x]
        if a != -1 and b != -1: 
            if check_ecuations(a, b, val, CONSTRAINTS[y][x]):
                ecuations_found += 1
    if x > 1:
        a = board_mat[y][x - 1] 
        b = board_mat[y][x - 2]
        if a != -1 and b != -1:
            if check_ecuations(a, b, val, CONSTRAINTS[y][x]):
                ecuations_found += 1
    if x < 12:
        a = board_mat[y][x + 1] 
        b = board_mat[y][x + 2]
        if a != -1 and b != -1:
            if check_ecuations(a, b, val, CONSTRAINTS[y][x]):
                ecuations_found += 1

    return val * ecuations_found * BONUSES[y][x]

