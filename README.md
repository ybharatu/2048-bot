# How I created a 2048 bot

![2048 logo](/Users/yash/projects/Blogs/blog_images/2048.png)


## Introduction

I am definitely late to the party of playing 2048. I remember it becoming extremely popular when I was in high school. I remember not playing it very much though. 

Fast forward to the past couple of months. My partner downloaded the app and was having fun. She was able to get 2048 within the first day of playing. After that, I wanted to try too. So I downloaded the app and began combining powers of two. I was able to get to 2048 soon enough as well, but in that time, my partner just got 4096. Even though the aim is to get to 2048, you can still acheive higher scores by continuing to play after acquiring 2048, surpassing the capped goal. We kept playing, and I was able to consistenly get 2048 and she was consistently getting 4096. One day, she was able to get 8192. 

At this point, I felt like catching up to her was getting harder and harder. So then I wondered if I couldn't get that high, could I write a program that could. 

## First steps: Getting the board

I decided to make my bot in python, a language that I am comfortable and experienced in writing in that will also have plenty of libraries and support that I might need. The main flow of the program, I determined, would be: to take a screenshot of the online game, determine which move would be the best, and to emulate the intended direction. The website I used to test my code can be found [here](https://2048game.com/).

I decided to start work on the first step. I decided to use the pillow library for its image grab function to take a sceenshot of the board after every move, which is necessary because an additional number, a 2 or a 4, gets introduced to the board after each move. The next problem that I faced was getting the numbers from the image. I have read about a library called pytesseract that can do string reads from images and I wanted to explore that. So I manually enetered in coordinates for each tile and cropped the screenshot to the individual tiles. Below is the code for my intial attempt:

```
    for i in range(NUM_TILES):
        im_list.append(screenshot.crop(coord_list[i]))
        t_value = pytesseract.image_to_string(im_list[i], config=custom_config).strip()
        if t_value.isnumeric():
            board[i] = t_value
        else:
            board[i] = "-"
```

This initial naive implementation was not accurate. It often missed numbers, and somtimes mislabled tiles. 
![Bad capture](/Users/yash/projects/Blogs/blog_images/bad_capture.png)
I needed to do some more work pre prossessing the image to make it accurate. After some experimentation, I found that converting the image to grayscale, applying a Gaussian blur and then applying a binary threshold function will allow the pytesseract to read the image with very good accuracy. I also thought about just using the colors of the tile to determine the numbers, but my approach just sounded more fun to me. 

![Really bad capture](/Users/yash/projects/Blogs/blog_images/really_bad_capture.png)
![Better capture](/Users/yash/projects/Blogs/blog_images/closer_capture.png)
![Good capture](/Users/yash/projects/Blogs/blog_images/good_capture.png)


## Step 2: Making a prototype

The next step in the pipeline would be to determine which move would be the best at a given state. However, I wanted to ensure the bot would work before spending large amounts of time on this logic. So I decided to create a completely random move creater to serve as a placeholder. 

```
UP = 500
DOWN = 501
RIGHT = 502
LEFT = 503

valid_dirs = [UP, DOWN, RIGHT, LEFT]

def get_random_direction_move():
    rand_value = random.randrange(4)

    direction = valid_dirs[rand_value]

    return direction
```

Then I wrote the logic to emulate the key presses based on the direction dictated by the get_random_direction_move function. 

```
def make_move(direction):
    if direction == UP:
        pyautogui.press("up")
    elif direction == DOWN:
        pyautogui.press("down")
    elif direction == RIGHT:
        pyautogui.press("right")
    elif direction == LEFT:
        pyautogui.press("left")
    else:
        print("Uh oh, direction cannot be: " + str(direction))
        exit()
```

Then I made a simple main function that envokes all the main functions to get my first initial prototype bot. 

```
def main():

    time.sleep(1)
    while True:

        screencap_board()

        direction = get_random_direction_move

        make_move(direction)
```

And *voila*! I have a functioning 2048 bot. It is awful at the game and cannot get a very high score, but it does work!

## The Meat and Potatoes: Decision Logic

Now that I have a skeleton of the program, I need to put more effort into the decision making logic, the main core of the bot. This is where the I am going to spend almost the entirety of my time. My first thought was to see what would happen if I just give weights to the random directions. I normally play this game by keeping my biggest number in the bottom right and constantly build towards that. I normally only use down and right moves, with ocassional left moves. I only swipe up, if absolutely necessary. So I tried to translate that with weights to see if that would perform better than complete random. The results were ... not that different. It still was losing at roughly the same spot as the complete random move generator. 

So my intial approach was to give each tile position weights, similar to how chess bots work. Then each board state could be given a score by multiplying the board's value with it's position's weight. So effectively, the bot will calculate how the board will look after each move and assign a score with that state. The move with the highest score gets selected. I saw an immediate improvement in the bot's performance. I experimented with different weights and evaluated them, finally ending up with a pattern that worked well for me. 

```
tile_heuristic_grid = [50, 50, 50, 50,
                       500, 500, 500, 500,
                       4000, 4000, 4000, 4000,
                       50000, 50000, 50000, 50000]
```

I also brainstormed other heauristics that I thought could be helpful. Anything to impact the score that could aid in the bot's decision-making process. I came up with the following:

* Max Value Score
* Empty Tile Score
* Smoothness Score
* Combination Priority Score

### Max Value Score:
This heuristic essentially gives a big bonus for the bot to keep the largest number in the bottom right or left corner. It will also give a sizable deduction if the largest number is not in a corner. I find that this is the best strategy for the bot to play with my weights.

### Empty Tile Score:
This heuristic rewards bonus points for boards with empty tiles, by calculating a score by multiplying the amount of empty tiles with a constant value. This score is helpful for the bot to make moves that can combine multiple numbers. 

### Smoothness Score
This score tries to keep numbers next to numbers that are the same as it. This tells the bot to arrange the board to combine the numbers. 

### Combination Priority Score
This is a heuristic I added after seeing the bot make mistakes regarding situations where it can combine scores in its own row vs combining from above. The issue with combining from above is that it creates a larger number than the one next to it. This causes issues as the smaller number will take a long time to raise to that value if ever. 

With all of these heuristics, I was actually able to reach 2048.

![Really bad capture](/Users/yash/projects/Blogs/blog_images/win.png)

## So close, yet still far: Further Optimizations using Minimax Trees

My current approach only picks the best move given the current state. It has no thought about what could happen in the future. That's where minimax trees come in. The concept is fairly simple. The root of the tree is the current state, where as its children nodes are the potential states it could be. Furthermore, each node would have children that represent future game states. Theortetically, you can map all possible gamestates and make the best decision every time. Practically, we are limited by computation, space, and time. But we can create go down a couple of levels so we have some idea of potential future states. 

The pseudo code for minimax (found [here](https://www.cs.cornell.edu/courses/cs312/2002sp/lectures/rec21.htm)) is pretty simple. 

```
fun minimax(n: node): int =
   if leaf(n) then return evaluate(n)
   if n is a max node
      v := L
      for each child of n
         v' := minimax (child)
         if v' > v, v:= v'
      return v
   if n is a min node
      v := W
      for each child of n
         v' := minimax (child)
         if v' < v, v:= v'
      return v
```

This represents the future for this project. I want this bot to be able to go much further than 2048, but it seems like it will be an onging project. I've implemented the minimax algorithm, but I still need to work on the scoring to give the bot a better idea of what moves are the best. 

I've made a lot of changes as this bot evolved. I eventually realized that using the color of the tile is a much better indicator of what the number is, as even if the library misses a single tile, it can really mess up the entire game. Also, I found changing the heuristic weights for any of the heuristics creates significant changes to how the bot plays the game. Experimenting with these values will also prove to be essential if I want it get truly high scores. 

Overall, this was a fun and valuable learning experience. I read a lot of algorithms in order to approach this problem, and it posed to be a good software challence for a primarily hardware developer. I'm going to keep working on this project and update this post whenever I get a breakthrough. 

The code can be found [here](https://github.com/ybharatu/2048-bot)

References:

https://www.cs.cornell.edu/courses/cs312/2002sp/lectures/rec21.htm

https://medium.com/@bartoszzadrony/beginners-guide-to-ai-and-writing-your-own-bot-for-the-2048-game-4b8083faaf53

https://www.geeksforgeeks.org/2048-game-in-python/

