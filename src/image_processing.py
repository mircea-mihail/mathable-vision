import numpy as np
import cv2 as cv
import os 

from constants import *

# --------------------------------------------------- related to the whole board
def get_board(photo_path):
    board = cv.imread(os.path.join(photo_path))
    board = get_trimmed(board)
    return board

# returns the biggest contour in the immage (to get the board from the image)
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

            current_area = cv.contourArea(np.array([[possible_top_left],[possible_top_right],[possible_bottom_right],[possible_bottom_left]])) 

            if current_area > max_area:
                max_area = current_area

                top_left = possible_top_left
                bottom_right = possible_bottom_right
                top_right = possible_top_right
                bottom_left = possible_bottom_left

    return [top_left, top_right, bottom_right, bottom_left]

# remaps the board using the blue on brown contrast between the board and the table
def get_trimmed(board):
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

# prints red lines to mark the squares (for debug)
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

# processes the board for better extraction of digits
def process_board(board):
    board = cv.medianBlur(board, 5)

    alpha = 2
    beta = -0.5
    gamma = 0
    flt_board = cv.addWeighted(src1=board, src2=board, alpha=alpha, beta=beta, gamma=gamma)
    flt_board = 255 - flt_board

    return flt_board

# --------------------------------------------------- digit squares

# returns a trimmed matrix of a square
def get_square(board, p_x_pos, p_y_pos):
    return board[
        int(p_y_pos*SQUARE_WIDTH + SQUARE_TRIM_PX) : int((p_y_pos+1) * SQUARE_WIDTH - SQUARE_TRIM_PX), 
        int(p_x_pos*SQUARE_WIDTH + SQUARE_TRIM_PX) : int((p_x_pos+1) * SQUARE_WIDTH - SQUARE_TRIM_PX)
    ].copy()

# returns the points that border the actual digits for a remapping
def get_digits_contour(mask):
    contours, _ = cv.findContours(mask,  cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    
    populated_corners = False
    top_left = [0, 0]
    top_right = [0, 0]
    bottom_left = [0, 0]
    bottom_right = [0, 0]
   
    for i in range(len(contours)):
        top = None
        bottom = None
        left = None
        right = None

        for point in contours[i].squeeze():
            if top is None or point[1] < top:
                top = point[1] 

            if bottom is None or point[1] > bottom:
                bottom = point[1]

            if left is None or point[0] < left:
                left = point[0]

            if right is None or point[0] > right:
                right = point[0]

        current_contour = np.array([[top, left],[top, right],[bottom, right],[bottom, left]])
        # print("current contour: ", current_contour)

        current_area = cv.contourArea(current_contour)

        if  current_area > DIGIT_FILTER_SIZE:
            if populated_corners:
                top = min(top, top_left[1])
                bottom = max(bottom, bottom_right[1])
                left = min(left, top_left[0])
                right = max(right, bottom_right[0])

            top_left = [left, top]
            bottom_right = [right, bottom] 
            top_right = [right, top]
            bottom_left = [left, bottom]

            populated_corners = True

    return [top_left, top_right, bottom_right, bottom_left]
 

# remaps the square to only contain the inner digit, no white border around it
def remap_square(mask):
    bounds = np.array(get_digits_contour(mask), dtype = "float32")
    square_destination = np.array(
    [
        [0,0],
        [SQUARE_WIDTH,0],
        [SQUARE_WIDTH,SQUARE_WIDTH],
        [0,SQUARE_WIDTH]
    ], dtype = "float32")

    mapping = cv.getPerspectiveTransform(bounds, square_destination)
    mask = cv.warpPerspective(mask, mapping, (SQUARE_WIDTH, SQUARE_WIDTH))

    mask = mask == MAX_PX_VAL
    mask = mask * MAX_PX_VAL
    return mask

# filters noise, thickens and remaps the digit to fit the whole square
def process_square(p_sq):
    hsv_sq = cv.cvtColor(p_sq, cv.COLOR_BGR2HSV)
    sat_mask = np.zeros((p_sq.shape[0], p_sq.shape[1]), np.uint8)
    val_mask = np.zeros((p_sq.shape[0], p_sq.shape[1]), np.uint8)

    _, val_mask = cv.threshold(hsv_sq[:, :, VALUE], SQUARE_MIN_VALUE, 256, cv.THRESH_BINARY)
    _, sat_mask = cv.threshold(hsv_sq[:, :, VALUE], 256, SQUARE_MAX_SATURATION, cv.THRESH_BINARY)

    mask = cv.bitwise_or(sat_mask, val_mask)

    filter_size = 3
    kill_noise_kernel = np.ones((filter_size, filter_size), np.uint8)
    mask = cv.erode(mask, kill_noise_kernel, iterations=1)
    # mask = cv2.dilate(mask, kill_noise_kernel, iterations=1)

    inflation = 4
    kernel = np.ones((inflation, inflation), np.uint8) 
    mask = cv.dilate(mask, kernel, iterations=1) 
    # mask = cv.threshold(mask, 255/2, 256, cv.THRESH_BINARY)

    return remap_square(mask)
   
# --------------------------------------------------- templates

# generates the template files using the best of the provided refference photos
def generate_templates():
    tpl = cv.imread(TEMPLATE_PATH)

    board = get_trimmed(tpl)
    board = process_board(board)
    idx = 0

    # sq = get_square(board, 0, 0)
    # mask = process_square(sq)
    # print(mask[0, 50])
    # plt.imshow(mask)

    for i in range(0, 13, 2):
        for j in range(0, 13, 2):
            if i == 12 and j > 6:
                return 

            sq = get_square(board, j, i)
            mask = process_square(sq)

            cv.imwrite(os.path.join(RAW_TEMPLATE_DIR, str(NUMBERS[idx]) + ".png"), mask)

            idx += 1 

# loads the templates from the template directory
def load_templates():
    tpl_names = os.listdir(TEMPLATE_DIR)
    tpl_names = sorted([template for template in tpl_names], key=lambda x: int(os.path.splitext(x)[0]))
    templates = {}

    for tpl in tpl_names:
       templates[int(os.path.splitext(tpl)[0])] = cv.cvtColor(cv.imread(os.path.join(TEMPLATE_DIR, tpl)), cv.COLOR_BGR2GRAY)

    return templates

# returns the best match between the given image and a template
def get_similitude(img, templates):
    best_score = 0
    best_number = -1
    for cur_nr in NUMBERS:
        template = templates[cur_nr]
        sim_score = 0
        # for i in range(SQUARE_WIDTH):
        #     for j in range(SQUARE_WIDTH):
        #         if template[i][j] == img[i][j]:
        #             sim_score += 1
        
        sim_score = np.sum(img == template)
        # if cur_nr == 28:
        #     print(sim_score/(SQUARE_WIDTH ** 2), cur_nr)

        if sim_score > best_score:  
            # print(sim_score/(SQUARE_WIDTH ** 2), cur_nr)
            best_score = sim_score
            best_number = cur_nr

    if best_score / (SQUARE_WIDTH * SQUARE_WIDTH) < MIN_SIMILITUDE:
        return -1
    return best_number
