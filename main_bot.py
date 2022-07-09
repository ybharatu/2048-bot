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
import colorthief
import cv2
import numpy


pyautogui.FAILSAFE = True
pyautogui.PAUSE = 2.5

#################################################################
# Main Function
#################################################################

def main():

    #################################################################
    # Lets me switch screens to 2048
    #################################################################
    time.sleep(1)

    #################################################################
    # Gets a screenshot and populates the values of the board
    #################################################################
    screencap_board()

    #################################################################
    # Print's the value of the board to the terminal
    #################################################################
    print_board()

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
    display_board_img(im_list)


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
    for i in range(16):
        im_list.append(screenshot.crop(coord_list[i]))
        np_image = numpy.array(im_list[i])
        blur = cv2.GaussianBlur(np_image, (5, 5), 0)
        ret3, th3 = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        #th3 = cv2.adaptiveThreshold(numpy.array(im_list[i]), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        im_pil = Image.fromarray(th3)
        im_list[i] = im_pil
        t_value = pytesseract.image_to_string(im_list[i], config=custom_config).strip()
        if t_value.isnumeric():
            board.append(t_value)
        else:
            np_image = numpy.array(im_list[i])
            invert = numpy.invert(np_image)
            pil_image = Image.fromarray(invert)
            t_value = pytesseract.image_to_string(pil_image, config=custom_config).strip()
            if t_value.isnumeric():
                im_list[i] = pil_image
                board.append(t_value)
            else:
                board.append("-")

    return im_list

#################################################################
# Print's the current values of the board
#################################################################
def print_board():

    print(board[0] + " " + board[1] + " " + board[2] + " " + board[3])
    print(board[4] + " " + board[5] + " " + board[6] + " " + board[7])
    print(board[8] + " " + board[9] + " " + board[10] + " " + board[11])
    print(board[12] + " " + board[13] + " " + board[14] + " " + board[15])



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
# Wrapper for Main
#################################################################

if __name__ == "__main__":
   #main(sys.argv[1:])
    main()

