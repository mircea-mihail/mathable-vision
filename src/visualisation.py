from image_processing import *
from constants import *
from solution import *

def show_img(p_img):
    plt.figure(dpi = 200)
    plt.imshow(cv.cvtColor(p_img, cv.COLOR_BGR2RGB))
    plt.show()

templates = load_templates()

def show_squares(p_board):
    for i in range(TOTAL_SQUARES):

        plt.figure(dpi = 200)
        for j in range(TOTAL_SQUARES):
            sq = get_square(p_board, j, i)
            mask = process_square(sq)
            match = get_similitude(mask, templates)
            if match == -1:
                print("-", end = ", ")
            else:
                print(match, end = ", ")

            plt.subplot(1, TOTAL_SQUARES, j + 1)
            plt.imshow(mask)
            plt.axis("off")
        print()
        plt.show()

def print_templates():
    templates = load_templates()

    DPI = 300
    plt.figure(dpi=DPI)

    i = 1
    max_i = 5
    for idx in NUMBERS:
        plt.subplot(1, max_i + 1, i + 1)
        plt.axis("off")
        plt.imshow(templates[idx])
        if i >= max_i:
            i = 0
            plt.show()
            plt.figure(dpi=DPI)
        i += 1

def print_mat(mat):
    for i in range(TOTAL_SQUARES):
        for j in range(TOTAL_SQUARES):
            if mat[i][j] == -1:
                print("_\t", end="")
            else:
                print(mat[i][j], end="\t")
        print("\n", end="")

    print()

def print_train_res():
    files = os.listdir(INPUT_DIR)
    solutions = sorted([file for file in files if os.path.splitext(file)[1] == ".txt"])
    photos = sorted([file for file in files if os.path.splitext(file)[1] == ".jpg"])
    
    prev_board = get_board(EMPTY_BOARD_PATH)
    templates = load_templates()

    TRAIN_SET = 0
    offset = TRAIN_SET * 2

    move_matrix = np.full((14, 14), -1)
    start_idx = 0 + int(50 * offset / 2)
    stop_idx = 50 + int(50 * offset / 2)

    idx = start_idx + offset

    for photo in photos[start_idx:stop_idx]: 
        # photo = photos[49]
        board = get_board(os.path.join(INPUT_DIR, photo))
        move_pos = get_board_change(prev_board, board)
        res_string = str(BOARD_Y_VALS[move_pos[Y]]) + str(BOARD_X_VALS[move_pos[X]])

        flt_board = process_board(board)
        move_val = get_similitude(process_square(get_square(flt_board, move_pos[X], move_pos[Y])), templates)
        res_string = res_string + " " + str(move_val)

        move_matrix[move_pos[Y], move_pos[X]] = move_val

        with open(os.path.join(INPUT_DIR, solutions[idx]), 'r') as file:
            first_line = file.readline()
        print(res_string == first_line, "\t", "pos: ", idx - offset, "\t", sep = "", end = "\t")
        print(res_string, "\t", first_line, end = "\n")

        prev_board = board
        idx += 1

    print_mat(move_matrix)

