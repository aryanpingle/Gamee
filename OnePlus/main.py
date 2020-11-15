# Quick Setup

# Open the gamee.com window to the left half of the screen, so that its width is half of the monitor 
# It's important to note that this game gets fukt up on pc if the window is wider than it is tall
# Umm yeah, run this code. That's all there is to it. Oh, and change the `max_plays` value to however many times you want the game to run. 

# EXPLANATION

# The code reads the box given by the variable `monitor`, so it keeps checking one specific part of the screen to read the equation, derives the answer through simple maths, and clicks on the button to progress. Then it waits some time for the next question to load, and repeats.

# WARNING

# This code is VERY BAD, NO GOOD< TRASH. There are many better ways to do it, and I chose the easiest path that I could understand.

max_plays = 20

import pyautogui as gui
import numpy as np
import time
import mss

buttons = [[481, 748], [481, 868], [481, 984]]

def identify(img):
    """
    This function returns the type of token shown in `img`, so it can be "1", "2", "3", "-" or "+".

    I have carefully (yeah right) analysed the look of each token, so I've made some approximations regarding their heights and widths.
    """
    if len(img) < 40:
        return "-"

    height = len(img)
    width = len(img[0])
    
    if height < 60 or abs(height/width - 1) < 0.05:
        return "+"
    
    if width < 40:
        return "1"

    total = sum(sum(img[:-len(img)//6, -len(img[0])//6:]))

    val = img[24][24]
    if round(val, 2) == 1.68:
        return "2"
    return "3"

ox = 130
oy = 545
ex = 797
ey = 667

# Rectangle representing the area to be watched
monitor = {"top": oy, "left": 155, "width": ex-ox, "height":ey-oy}
# (NOT USED ANYMORE) A dictionary to easily access the save files
# save_dict = {"1": "digits/1.npy", "2": "digits/2.npy", "3": "digits/3.npy", "-": "operators/minus.npy", "+": "operators/plus.npy"}
# This is a dictionary to easily convert the string to its number part... Fuck, I should've used int(value) instead of a fucking dictionary but I'm too tired to change it so deal with it.
values = {"1": 1, "2": 2, "3": 3}

with mss.mss() as sct:
    counter = 0
    while counter < max_plays:
        img = np.asarray(sct.grab(monitor))
        img = np.delete(img, 3, 2)/255

        img = np.array([[sum(x) for x in i] for i in img])

        # bruh stores lists like this: [startx, endx, start_index, height]
        bruh = []

        i = 0
        startx = -1
        while i < len(img[0]):
            if len(set(img[:, i])) != 1: # Some disturbance
                if startx == -1:
                    startx = i
            else:
                if startx != -1: # End of shape
                    bruh.append([startx, i])
                    startx = -1

            i += 1

        bruh = bruh[:-2]

        for index in range(len(bruh)):
            indices = bruh[index]
            shape = img[:, indices[0]:indices[1]]

            top_found = False
            bottom_found = False
            startindex = 0
            endindex = 0
            for i in range(len(shape)):
                if not top_found:
                    if len(set(shape[i])) != 1:
                        top_found = True
                        startindex = i
                if not bottom_found:
                    if len(set(shape[len(shape)-1-i])) != 1:
                        bottom_found = True
                        endindex = len(shape)-i
                if top_found and bottom_found:
                    break
            
            bruh[index].extend([startindex, endindex])
        
        # fix contains the tokens of the equation, except '=' and '?'
        fix = [identify(img[shape[2]:shape[3], shape[0]:shape[1]]) for shape in bruh]

        # For debugging
        # print(fix)
    
        # Time to calculate the answer of the equation, stored in `running`
        i = 0
        running = 0
        while i < len(fix):
            g = fix[i]

            if g == "-":
                running -= values[fix[i+1]]
                i += 1
            elif g == "+":
                running += values[fix[i+1]]
                i += 1
            else:
                running += values[g]

            i += 1

        if running == 0:
            break
        
        # Click on the corresponding button
        gui.click(*buttons[running-1])
        
        # Pause for the next question to load
        time.sleep(2)
        counter += 1

        # In case you're running the program many times, this is helpful
        if counter % 25 == 0:
            print(counter)