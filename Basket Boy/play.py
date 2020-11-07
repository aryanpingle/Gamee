import time
import numpy as np
import pyautogui

time.sleep(2.5)

# Consts
SW = 1980
SH = 1080

i = 0
startX = 287
width = 638-startX
startY = 895
height = 5

seconds = 0

while i < seconds:
    # Take Screenshot
    # starttime = time.time()
    img = np.array(pyautogui.screenshot(region=(startX, startY, width, height)))
    # img = sct.grab({'top': startX, 'left': startY, 'width': width, 'height': height})

    found = False
    for row in range(len(img)):
        for col in range(len(img[0])):
            if img[row][col][0] <= img[row][col][1] <= img[row][col][2] < 5:
                found = True
                break
        if found:
            break
    # print(1e3*(time.time()-starttime) // 1)

    if found:
        pyautogui.click(x=startX+col, y=startY+row)

    i += 1
    # break

# For measuring your screen stuff

# while True:
#     if input() == " ":
#         print(pyautogui.position())
#     else:
#         break