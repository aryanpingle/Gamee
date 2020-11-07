# SETUP
# 
# Open the Chrome tab with the game started to the left half of the screen
# Run this program
# As simple as that

import time
import numpy as np
import pyautogui as gui
import math

# HELPERS

def pixel_difference(val, target, multiple=True):
    if multiple:
        return min([sum([abs(val[i]-t[i]) for i in range(3)]) for t in target])
    else:
        return sum([abs(val[i]-target[i]) for i in range(3)])

onblue = [[6, 145, 146], [53, 126, 205], [8, 133, 251], [0, 148, 254], [1, 144, 255]]
boxes = [[[150, 347], [162, 367]], [[127, 345], [140, 367]], [[105, 346], [118, 367]]]
boxes.reverse()
def get_speeds():
    permissible_diff = 20

    speeds = []
    for box in boxes:
        img = np.array(gui.screenshot( region=(*box[0], *[box[1][i]-box[0][i] for i in range(2)])))
        for i in img:
            found = False
            for j in i:
                if pixel_difference(list(j), onblue) < permissible_diff:
                    speeds.append(True)
                    found = True
                    break
            if found:
                break
        if not found:
            speeds.append(False)
    return speeds

# Consts
SW, SH = gui.size()

px = 170
py = 817

H = 100

hoop_colour_red = [255, 53, 53]
skin_colour = [255, 175, 159]

auto_targeting = True

while True:
    tx = -1
    ty = -1

    gay = 0
    speeds = [False, False, False]
    while gay < 5 and speeds == [False, False, False]:
        speeds = get_speeds()
        gay += 1

    direction = sum([1 if i else 0 for i in speeds])
    direction *= -1 if speeds[2] else (1 if speeds[0] else 0)

    if auto_targeting:
        img = np.array(gui.screenshot(region=(0, 0, SW/2, SH-50)))

        # Searching from up to down, column wise
        for i in range(len(img[0])):
            for j in range(len(img)):
                if list(img[j][i]) == hoop_colour_red:
                    tx = i+39
                    ty = j
                    gui.moveTo(x=tx, y=ty)
                    break
            if tx != -1:
                break

        if tx == -1:
            print("Something went wrong, exiting")
            break
    else:
        input("Place mouse over the middle of the hoop and press [ENTER]")
        (tx, ty) = gui.position()
    
    a = (( tx-px )/( 2*( math.sqrt(H) + math.sqrt( py + H - ty ) )))**2
    mx = tx - math.sqrt( 4*a*H )
    my = ty - H + 2*a

    gui.click(x=mx-direction*40, y=my)
    if auto_targeting:
        time.sleep(7)