# Using https://medium.com/@bartoszzadrony/beginners-guide-to-ai-and-writing-your-own-bot-for-the-2048-game-4b8083faaf53 as a guide

#################################################################
# Import Packages
#################################################################
import sys
import pyautogui
from PIL import ImageGrab, ImageOps, Image
from common import *
from matrix_functions import *
import time
# Need to do: brew install tesseract
import pytesseract
import cv2
import numpy as np
import random
import timeit

pyautogui.FAILSAFE = False
pyautogui.PAUSE = .1

#################################################################
# Main Function
#################################################################

def main():
    #global valid_dirs_weights
    #global valid_dirs
    #################################################################
    # Lets me switch screens to 2048
    #################################################################
    time.sleep(1)
    valid = 0
    while not valid:

        #################################################################
        # Gets a screenshot and populates the values of the board
        #################################################################
        screencap_board()

        #################################################################
        # Get's the direction for the next move
        #################################################################
        direction = get_heuristic_move()
        #direction = get_weighted_direction_move()

        #################################################################
        # Emulates the keyboard press to make the move
        #################################################################
        make_move(direction)


        #valid_dirs_weights = [1, 40, 40, 19]
        #valid_dirs = [UP, DOWN, RIGHT, LEFT]

#################################################################
# Takes a screen shot and sets up the board
#################################################################
def screencap_board():

    #################################################################
    # Takes screenshot
    # Really useful for bbox explanation:
    # http://chayanvinayak.blogspot.com/2013/03/bounding-box-in-pilpython-image-library.html
    # Bbox = (left, upper, right, lower)
    #################################################################
    screenshot = ImageGrab.grab()

    #################################################################
    # Gray scales the image
    #################################################################
    grayscaled = screenshot.convert('L')

    #################################################################
    # Takes the image and crops each individual tile into an array.
    # Also populates the board with values
    #################################################################
    im_list = get_values_by_number(grayscaled)

    #################################################################
    # Debug Function, that shows the image with all the cropped
    # tiles stitched together.
    #################################################################
    #display_board_img(im_list)

#################################################################
# Obtain values based on reading the number
#################################################################
def get_values_by_number(screenshot):

    im_list = []

    #################################################################
    # Config string for pytesseract:
    # '--psm 6' will indicate it is a single block of text
    # '-c tessedit_char_whitelist=0123456789 'will look number values
    #################################################################
    custom_config = r'--psm 6 -c tessedit_char_whitelist=0123456789'

    #################################################################
    # Iterates through all the tiles on the board
    # For each tile:
    #   - Applies a Gaussian Blur
    #   - Applies a Threshold Function
    #   - Tries to read the number
    # If the number cannot be read, tries the same steps, but
    # inverts the image
    #################################################################
    for i in range(NUM_TILES):
        im_list.append(screenshot.crop(coord_list[i]))
        np_image = np.array(im_list[i])
        blur = cv2.GaussianBlur(np_image, (5, 5), 0)
        ret3, th3 = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        im_pil = Image.fromarray(th3)
        t_value = pytesseract.image_to_string(im_pil, config=custom_config).strip()
        if t_value.isnumeric():
            im_list[i] = im_pil
            board[i] = t_value
        else:
            np_image = np.array(im_pil)
            invert = np.invert(np_image)
            pil_image = Image.fromarray(invert)
            t_value = pytesseract.image_to_string(pil_image, config=custom_config).strip()
            if t_value.isnumeric():
                im_list[i] = pil_image
                board[i] = t_value
            else:
                board[i] = "-"

    # print("DEBUG: Get_values_by_number()")
    # print(board)

    return im_list

#################################################################
# Print's the current values of the board
#################################################################
def print_board():

    print(board[0] + " " + board[1] + " " + board[2] + " " + board[3])
    debug_log(board[0] + " " + board[1] + " " + board[2] + " " + board[3] + "\n", DEBUG)
    print(board[4] + " " + board[5] + " " + board[6] + " " + board[7])
    debug_log(board[4] + " " + board[5] + " " + board[6] + " " + board[7] + "\n", DEBUG)
    print(board[8] + " " + board[9] + " " + board[10] + " " + board[11])
    debug_log(board[8] + " " + board[9] + " " + board[10] + " " + board[11] + "\n", DEBUG)
    print(board[12] + " " + board[13] + " " + board[14] + " " + board[15])
    debug_log(board[12] + " " + board[13] + " " + board[14] + " " + board[15] + "\n", DEBUG)
    debug_log("-----------------\n", DEBUG)

#################################################################
# Merge all pictures to show the board (Verification Function)
#################################################################
def display_board_img(im_list):

    four_img = []
    two_img = []

    #################################################################
    # Merges all single pictures into an array of two side-by-side
    # images.
    #################################################################
    for i in range(0,15,2):
        temp_img = Image.new('RGB', (2*im_list[i].size[0], im_list[i].size[1]), (250,250,250))
        temp_img.paste(im_list[i], (0, 0))
        temp_img.paste(im_list[i+1], (im_list[i].size[0], 0))
        two_img.append(temp_img)

    #################################################################
    # Merges all side-by-side images to an image of the row
    #################################################################
    for i in range(0,7,2):
        temp_img = Image.new('RGB', (2 * two_img[i].size[0], two_img[i].size[1]), (250, 250, 250))
        temp_img.paste(two_img[i], (0, 0))
        temp_img.paste(two_img[i+1], (two_img[i].size[0], 0))
        four_img.append(temp_img)

    #################################################################
    # Vertically stacks all four row images into a board image
    #################################################################
    final_image = Image.new('RGB', (four_img[0].size[0], 4 * four_img[0].size[1]), (250, 250, 250))
    final_image.paste(four_img[0], (0, 0))
    final_image.paste(four_img[1], (0, four_img[1].size[1]))
    final_image.paste(four_img[2], (0, 2 * four_img[1].size[1]))
    final_image.paste(four_img[3], (0, 3 * four_img[1].size[1]))
    final_image.show()

#################################################################
# Swipes the screen to the given direction
#################################################################
def make_move(direction):
    if direction == UP:
        print("Swiping UP")
        pyautogui.press("up")
    elif direction == DOWN:
        print("Swiping DOWN")
        pyautogui.press("down")
    elif direction == RIGHT:
        print("Swiping RIGHT")
        pyautogui.press("right")
    elif direction == LEFT:
        print("Swiping LEFT")
        pyautogui.press("left")
    else:
        print("Uh oh, direction cannot be: " + str(direction))
        exit()

#################################################################
# Heuristic Based Decision making. Listed a variety of factors
# and the bot should try to optimize using these heuristics
#################################################################
def get_heuristic_move():
    max_score = -1
    max_direction = DOWN

    # TODO: Can do all the np.reshapes up here to save some time?
    up_board, changed_up = calc_next_board(UP)
    down_board, changed_down = calc_next_board(DOWN)
    right_board, changed_right = calc_next_board(RIGHT)
    left_board, changed_left = calc_next_board(LEFT)

    if changed_down:
        down_score = calc_total_score(down_board)
        print("Down Score: " + str(down_score))
        debug_log("Down Score: " + str(down_score) + "\n", DEBUG)
        if down_score > max_score:
            max_score = down_score
            max_direction = DOWN
    else:
        print("Can't go Down")
        debug_log("Can't go Down\n", DEBUG)
    if changed_up:
        up_score = calc_total_score(up_board)
        up_score += UPSCORE_PENALTY
        print("Up Score: " + str(up_score))
        debug_log("Up Score: " + str(up_score) + "\n", DEBUG)
        if up_score > max_score:
            max_score = up_score
            max_direction = UP
    else:
        print("Can't go Up")
        debug_log("Can't go Up\n", DEBUG)
    if changed_right:
        right_score = calc_total_score(right_board)
        print("Right Score: " + str(right_score))
        debug_log("Right Score: " + str(right_score) + "\n", DEBUG)
        if right_score > max_score:
            max_score = right_score
            max_direction = RIGHT
    else:
        print("Can't go Right")
        debug_log("Can't go Right\n", DEBUG)
    if changed_left:
        left_score = calc_total_score(left_board)
        print("Left Score: " + str(left_score))
        debug_log("Left Score: " + str(left_score) + "\n", DEBUG)
        if left_score > max_score:
            max_score = left_score
            max_direction = LEFT
    else:
        print("Can't go Left")
        debug_log("Can't go Left\n", DEBUG)

    if not changed_down and not changed_up and not changed_right and not changed_left:
        print("Game over. Can't do anything")
        debug_log("Game over. Can't do anything", DEBUG)
        exit()

    print_board()
    return max_direction

#################################################################
# Calculates the board given a direction
#################################################################
def calc_max_value_score(temp_board):
    max_tile = max_value(temp_board)
    new_board = np.reshape(temp_board, (16,))

    if new_board[15] == str(max_tile):
        return 10000
    else:
        return -10000

#################################################################
# Finds max value of the board
#################################################################
def max_value(temp_board):
    max_tile = -1
    new_board = np.reshape(temp_board, (16,))

    for i in range(16):
        if new_board[i] != "-":
            if max_tile < int(new_board[i]):
                max_tile = int(new_board[i])

    return max_tile

#################################################################
# Calculates heuristic score based on tile position
#################################################################
def calc_tile_heuristic_score(temp_board):
    score = 0
    new_board = np.reshape(temp_board, (16,))
    for i in range(16):
        if new_board[i] != "-":
            score += tile_heuristic_grid[i] * int(new_board[i])

    return score

#################################################################
# Calculates heuristic score based on number of empty tiles
#################################################################
def calc_empty_tile_score(temp_board):
    zeros = 0
    new_board = np.reshape(temp_board, (16,))

    for i in range(16):
        if new_board[i] == "-":
            zeros += 1

    return zeros*500

#################################################################
# Calculates heuristic score based on Monotonicity
#################################################################
def calc_monotonicity_score(temp_board):

    row_score = 0
    col_score = [0, 0]
    #################################################################
    # Checks monotonicity for rows
    #################################################################
    for i in range(4):
        for j in range(4):
            if temp_board[i][j] == "-" or j == 3 or temp_board[i][j+1] == "-":
                continue
            # if first row or third row
            if i == 0 or i == 2:
                #if int(temp_board[i][j]) > int(temp_board[i][j+1]):
                row_score += int(temp_board[i][j]) - int(temp_board[i][j+1])
            # if second or last row
            if i == 1 or i == 3:
                #if int(temp_board[i][j+1]) > int(temp_board[i][j]):
                row_score += int(temp_board[i][j+1]) - int(temp_board[i][j])

    return row_score * 100

#################################################################
# Calculates Smoothness (similar value tiles)
#################################################################


#################################################################
# Calculates the score given a state of the board
#################################################################
def calc_total_score(temp_board):

    total_score = calc_tile_heuristic_score(temp_board)
    total_score += calc_max_value_score(temp_board)
    total_score += calc_empty_tile_score(temp_board)
    total_score += calc_monotonicity_score(temp_board)

    return total_score

#################################################################
# Debug log function
#################################################################
def debug_log(message, enable):
    if enable:
        with open(DEBUG_FILE,"a") as f:
            f.write(message)

#################################################################
# Calculates the board given a direction
#################################################################
def calc_next_board(direction):

    temp_board = np.array(board)
    temp_board = np.reshape(temp_board, (4, 4))

    if direction == UP:
        new_board, changed = move_up(temp_board)
    elif direction == RIGHT:
        new_board, changed = move_right(temp_board)
    elif direction == LEFT:
        new_board, changed = move_left(temp_board)
    elif direction == DOWN:
        new_board, changed = move_down(temp_board)
    else:
        print("calc_next_board messed up")
        return False

    return new_board, changed

#################################################################
# Weighted Direction moving. Tries to keep max value in bottom
# right, by using random number generation
#################################################################
def get_weighted_direction_move():
    valid = False
    while not valid:
        direction = random.choices(valid_dirs, weights=valid_dirs_weights, k=1)[0]

        valid = check_direction(direction)

    return direction

#################################################################
# Verifies if the direction is valid
#################################################################
def check_direction(direction):

    if direction == UP:
        for i in range(15, 4, -1):
            if (board[i] != "-" and board[i-4] == "-") or (board[i] != "-" and board[i] == board[i-4]):
                return True
        remove_dir = valid_dirs.index(UP)
        valid_dirs.pop(remove_dir)
        valid_dirs_weights.pop(remove_dir)
        print("Can't go UP")
        return False
    if direction == DOWN:
        for i in range(0, 11, 1):
            if (board[i] != "-" and board[i+4] == "-") or (board[i] != "-" and board[i] == board[i+4]):
                return True
        remove_dir = valid_dirs.index(DOWN)
        valid_dirs.pop(remove_dir)
        valid_dirs_weights.pop(remove_dir)
        print("Can't go DOWN")
        return False
    if direction == RIGHT:
        for i in range(0, 15, 1):
            if i == 3 or i == 7 or i == 11 or i == 15:
                continue
            if (board[i] != "-" and board[i+1] == "-") or (board[i] != "-" and board[i] == board[i+1]):
                return True
        remove_dir = valid_dirs.index(RIGHT)
        valid_dirs.pop(remove_dir)
        valid_dirs_weights.pop(remove_dir)
        print("Can't go RIGHT")
        return False
    if direction == LEFT:
        for i in range(0, 15, 1):
            if i == 0 or i == 4 or i == 8 or i == 12:
                continue
            if (board[i] != "-" and board[i-1] == "-") or (board[i] != "-" and board[i] == board[i-1]):
                return True
        remove_dir = valid_dirs.index(LEFT)
        valid_dirs.pop(remove_dir)
        valid_dirs_weights.pop(remove_dir)
        print("Can't go LEFT")
        return False

    print("Really hope you don't see this message: " + str(direction) + " is not a direction")
    exit()

#################################################################
# Random direction moving
#################################################################
def get_random_direction_move():
    rand_value = random.randrange(4)

    direction = valid_dirs[rand_value]

    return direction

#################################################################
# Wrapper for Main
#################################################################
if __name__ == "__main__":
   #main(sys.argv[1:])
    main()

