import pyautogui as gui
import numpy as np
import time

def mouser():
    while input() == "":
        print(gui.position())

def lwise_gen(arr):
    for i in arr:
        for j in i:
            yield j

def bwise_gen(arr):
    for i in range(len(arr[0])):
        for j in range(len(arr)):
            yield arr[j][i]

ox = 270
oy = 820
width = 670-ox
height = 100

starttime = time.time()
playtime = 15
while time.time() < starttime+playtime:
    img = gui.screenshot(region=(ox, oy, width, height))
    # img.show()
    # break
    img = np.array(img)

    start = -1
    end = 0
    for i in range(len(img)):
        for j in range(len(img[0])):
            rgb = list(img[i][j])

            if rgb == [0, 0, 0]:
                start = j
                break
        if start != -1:
            break

    if start == -1:
        continue
    
    mid = start + 20

    gui.click(x=mid+ox, y=i+oy+100)