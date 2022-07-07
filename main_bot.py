# Using https://medium.com/@bartoszzadrony/beginners-guide-to-ai-and-writing-your-own-bot-for-the-2048-game-4b8083faaf53 as a guide

#################################################################
# Import Packages
#################################################################
import sys
import pyautogui
from PIL import ImageGrab, ImageOps, Image
from common import *
import time
import pytesseract

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
    im1 = screenshot.crop(tile1_coord)
    im1.show()


#################################################################
# Wrapper for Main
#################################################################

if __name__ == "__main__":
   #main(sys.argv[1:])
    main()

