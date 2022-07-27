import numpy as np
from matrix_functions import *
from main_bot import *
from common import *

# board = ['-', '-', '2', '2',
#               '-', '-', '-', '-',
#               '-', '8', '32', '8',
#               '2', '8', '4', '2']

UP = 500
DOWN = 501
RIGHT = 502
LEFT = 503
valid_dirs = [UP, DOWN, RIGHT, LEFT]
valid_dirs_weights = [1, 40, 40, 19]

#################################################################
# Calculates the board given a direction
#################################################################
def calc_next_board(direction):
    valid = check_direction(direction)

    if not valid:
        return False

    temp_board = np.array(board)
    temp_board = np.reshape(temp_board, (4, 4))

    if direction == UP:
        new_board, changed = move_up(temp_board)
        print("UP Board")
        print(new_board)
    elif direction == RIGHT:
        new_board, changed = move_right(temp_board)
        print("RIGHT Board")
        print(new_board)
    elif direction == LEFT:
        new_board, changed = move_left(temp_board)
        print("LEFT Board")
        print(new_board)
    elif direction == DOWN:
        new_board, changed = move_down(temp_board)
        print("DOWN Board")
        print(new_board)
    else:
        return False

    return new_board, changed


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
# Print's the current values of the board
#################################################################
def print_board():

    print(board[0] + " " + board[1] + " " + board[2] + " " + board[3])
    print(board[4] + " " + board[5] + " " + board[6] + " " + board[7])
    print(board[8] + " " + board[9] + " " + board[10] + " " + board[11])
    print(board[12] + " " + board[13] + " " + board[14] + " " + board[15])

if __name__ == "__main__":


    direction = get_heuristic_move()
    print(direction)
    print_board()

