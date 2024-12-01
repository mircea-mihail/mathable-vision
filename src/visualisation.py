from image_processing import *
from constants import *

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