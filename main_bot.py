# Using https://medium.com/@bartoszzadrony/beginners-guide-to-ai-and-writing-your-own-bot-for-the-2048-game-4b8083faaf53 as a guide

#################################################################
# Import Packages
#################################################################
import sys
import pyautogui
from PIL import ImageGrab, ImageOps, Image
from common import *
import time
# Need to do: brew install tesseract
import pytesseract
import pytesser

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 2.5
#################################################################
# Main Function
#################################################################

def main():
    print("START!")
    time.sleep(1)
    # Really useful for bbox: http://chayanvinayak.blogspot.com/2013/03/bounding-box-in-pilpython-image-library.html
    # Bbox = (left, upper, right, lower)
    screenshot = ImageGrab.grab()

    im_list = []
    for i in range(16):
        im_list.append(screenshot.crop(coord_list[i]))
        board.append(pytesseract.image_to_string(im_list[i]))

    print(board)

#################################################################
# Print's the current values of the board
#################################################################
def print_board():
    for i in range(0,15,4):
        print("%6s %6s %6s %6s" % board[i], board[i+1], board[i+2], board[i+3])


#################################################################
# Merge all pictures to show the board (Verification Function)
#################################################################
def display_board_img(im_list):

    four_img = []
    two_img = []

    for i in range(0,15,2):
        temp_img = Image.new('RGB', (2*im_list[i].size[0], im_list[i].size[1]), (250,250,250))
        temp_img.paste(im_list[i], (0, 0))
        temp_img.paste(im_list[i+1], (im_list[i].size[0], 0))
        two_img.append(temp_img)

    for i in range(0,7,2):
        temp_img = Image.new('RGB', (2 * two_img[i].size[0], two_img[i].size[1]), (250, 250, 250))
        temp_img.paste(two_img[i], (0, 0))
        temp_img.paste(two_img[i+1], (two_img[i].size[0], 0))
        four_img.append(temp_img)

    final_image = Image.new('RGB', (four_img[0].size[0], 4 * four_img[0].size[1]), (250, 250, 250))
    final_image.paste(four_img[0], (0, 0))
    final_image.paste(four_img[1], (0, four_img[1].size[1]))
    final_image.paste(four_img[2], (0, 2 * four_img[1].size[1]))
    final_image.paste(four_img[3], (0, 3 * four_img[1].size[1]))
    final_image.show()

#################################################################
# Wrapper for Main
#################################################################

if __name__ == "__main__":
   #main(sys.argv[1:])
    main()

