import numpy as np
import cv2 as cv
import os 

from constants import *

def get_max_countour(mask):
    contours, _ = cv.findContours(mask,  cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    max_area = 0
   
    for i in range(len(contours)):
        if(len(contours[i]) > 3):
            possible_top_left = None
            possible_bottom_right = None

            for point in contours[i].squeeze():
                if possible_top_left is None or point[0] + point[1] < possible_top_left[0] + possible_top_left[1]:
                    possible_top_left = point

                if possible_bottom_right is None or point[0] + point[1] > possible_bottom_right[0] + possible_bottom_right[1] :
                    possible_bottom_right = point

            diff = np.diff(contours[i].squeeze(), axis = 1)
            possible_top_right = contours[i].squeeze()[np.argmin(diff)]
            possible_bottom_left = contours[i].squeeze()[np.argmax(diff)]

            if cv.contourArea(np.array([[possible_top_left],[possible_top_right],[possible_bottom_right],[possible_bottom_left]])) > max_area:
                max_area = cv.contourArea(np.array([[possible_top_left],[possible_top_right],[possible_bottom_right],[possible_bottom_left]]))
                top_left = possible_top_left
                bottom_right = possible_bottom_right
                top_right = possible_top_right
                bottom_left = possible_bottom_left

    return [top_left, top_right, bottom_right, bottom_left]

def get_trimmed(photo):
    board = cv.imread(os.path.join(INPUT_DIR, photo))
    hsv_board = cv.cvtColor(board, cv.COLOR_BGR2HSV)

    mask = np.zeros((board.shape[0], board.shape[1]), np.uint8)
    _, mask = cv.threshold(hsv_board[:, :, HUE], BOARD_MIN_HUE, BOARD_MAX_HUE, cv.THRESH_BINARY)

    bounds = get_max_countour(mask)
    bounds = np.array(bounds, dtype="float32")

    destination_of_puzzle = np.array(
    [
        [0,0],
        [BOARD_WIDTH,0],
        [BOARD_WIDTH,BOARD_WIDTH],
        [0,BOARD_WIDTH]
    ], dtype = "float32")

    mapping = cv.getPerspectiveTransform(bounds, destination_of_puzzle)
    board = cv.warpPerspective(board, mapping, (BOARD_WIDTH, BOARD_WIDTH))

    board = board[TOP_TRIM:board.shape[0] - BOTTOM_TRIM, LEFT_TRIM:board.shape[0] - RIGHT_TRIM].copy()
    board = cv.resize(board, (BOARD_WIDTH, BOARD_WIDTH))

    return board

    
def print_lines(board):
    thickness = SQUARE_TRIM_PX * 2 
    color = [0, 0, 255]
    for i in range(1, int(TOTAL_SQUARES)):
        board = cv.line(board, 
            [int(SQUARE_WIDTH * i), 0],
            [int(SQUARE_WIDTH * i), int(BOARD_WIDTH-1)],
            color=color, 
            thickness=thickness
        )
        board = cv.line(board, 
            [0, int(SQUARE_WIDTH * i)],
            [int(BOARD_WIDTH-1), int(SQUARE_WIDTH * i)],
            color=color, 
            thickness=thickness
        )
    return board

def get_square(board, p_x_pos, p_y_pos):
    return board[
        int(p_y_pos*SQUARE_WIDTH + SQUARE_TRIM_PX) : int((p_y_pos+1) * SQUARE_WIDTH - SQUARE_TRIM_PX), 
        int(p_x_pos*SQUARE_WIDTH + SQUARE_TRIM_PX) : int((p_x_pos+1) * SQUARE_WIDTH - SQUARE_TRIM_PX)
    ].copy()

