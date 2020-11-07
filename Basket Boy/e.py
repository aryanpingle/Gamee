import time
import numpy as np
import pyautogui as gui
import math

def pixel_difference(val, target, multiple=True):
    if multiple:
        return min([sum([abs(val[i]-t[i]) for i in range(3)]) for t in target])
    else:
        return sum([abs(val[i]-target[i]) for i in range(3)])

def get_speeds():
    # bkg = [[66, 53, 106]]
    onblue = [[6, 145, 146], [53, 126, 205], [8, 133, 251], [0, 148, 254], [1, 144, 255]]
    # offblue = [[71, 69, 132], [74, 70, 131], [75, 71, 130]]

    permissible_diff = 20

    # If even one of these is bkg, then either normal or speeding up
    neutrals = [[115, 347], [158, 346]]

    # box1 = [[105, 346], [118, 367]]
    # box2 = [[127, 345], [140, 367]]
    # box3 = [[150, 347], [162, 366]]

    # Point where if its bkg, its either back or empty

    boxes = [[[150, 347], [162, 367]], [[127, 345], [140, 367]], [[105, 346], [118, 367]]]
    boxes.reverse()

    speeds = []
    for box in boxes:
        img = gui.screenshot( region=(*box[0], *[box[1][i]-box[0][i] for i in range(2)]))
        # img.show()
        img = np.array(img)
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

        # input()

    return speeds

print(get_speeds())