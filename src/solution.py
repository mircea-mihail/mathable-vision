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