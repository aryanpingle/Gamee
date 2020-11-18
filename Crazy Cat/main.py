import mss
import math
import numpy as np
import time
import pyautogui as gui
import matplotlib.pyplot as plt

def get_positions():
    while input()=="":
        print(gui.position())

def get_pixel_difference(color, targets):
    return min([sum([abs(color[i] - value[i]) for i in range(3)]) for value in targets])

water_height = 921

player_x = 478
player_w = 4 # On either side

# platform = [base_colors, surface colors, ]
rock_platform = [
    [[171, 52, 18], [124, 0, 0], [163, 29, 10]],
    [[204, 204, 204], [153, 153, 153], [128, 128, 128]],
    "ROCK",
    14
]
gold_platform = [
    [[102, 51, 0], [125, 63, 0]],
    [[255, 222, 0], [229, 184, 9]],
    "GOLD",
    14
]
normal_platform = [
    [[102, 102, 102], [77, 77, 77], [51, 51, 51]], # 20 should be diff
    [[175, 212, 1], [144, 78, 13]],
    "NORMAL",
    10
]

platforms = [rock_platform, gold_platform, normal_platform]
bad = [[0, 0, 0], [233, 163, 0], [212, 119, 0], [153, 0, 0], [152, 15, 0], [76, 91, 80]]

platform_pos = 846
monitor = {"top": platform_pos, "left": player_x-player_w, "width": player_w*2, "height": water_height-platform_pos}

time_limit = 360
with mss.mss() as sct:
    starttime = time.time()
    while time.time()-starttime < time_limit:
        img = np.flip(np.delete(np.asarray(sct.grab(monitor)), 3, 2), 2)

        should_click = False
        rejected = False
        for x in range(player_w*2):
            for platform in platforms:
                [base,surface,TYPE,LIMIT] = platform
                # Now the y loop checks from the bottom up
                base_sure = False
                for y in range(water_height-platform_pos-1, -1, -1):
                    rgb = list(img[y][x])
                    if get_pixel_difference(rgb, bad) <= 5:
                        rejected = True
                        break
                    if get_pixel_difference(rgb, base) <= LIMIT:
                        base_sure = True
                        break
                
                if rejected:
                    break

                if not base_sure:
                    continue

                # Here, you've identified the base
                should_click = True
                break
            
            if should_click:
                break
        
        if should_click:
            gui.click(500, 600)
            time.sleep(max(0.005, 0.5 - 0.005*(time.time()-starttime)))
            print("{} seconds left".format(time_limit - time.time() + starttime))