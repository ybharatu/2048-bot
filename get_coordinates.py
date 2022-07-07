#################################################################
# Used to get the coordinates of the tiles on the screen
#################################################################

#################################################################
# Import Packages
#################################################################

import pyautogui
from pynput.mouse import Listener

#################################################################
# Function: get_click_loc()
# Description: Gets X and Y coordinates of clicked location
#################################################################

def get_click_loc(x,y,button,pressed):
    #print("Point: (X: " + str(x) + " , Y: " + str(y) + " )")
    print(pyautogui.position())
    return

#################################################################
# Main function
#################################################################

if __name__ == "__main__":

    with Listener(on_click=get_click_loc) as listener:
        listener.join()
