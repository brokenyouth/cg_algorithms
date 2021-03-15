import math
import tkinter as tk
from cng import *

def __move_right():
    x = 10
    y = 0
    obj_move(rect, x, y)

def __move_left():
    x = -10
    y = 0
    obj_move(rect, x, y)

def __move_up():
    x = 0
    y = -10
    obj_move(rect, x, -y)

def __move_down():
    x = 0
    y = -10
    obj_move(rect, x, y)

def drawRectangle(x, y, dimx, dimy):
    rect = rectangle(x, y, x+dimx, y+dimy)
    return rect

if __name__ == "__main__":
    global rect
    global root
    width, height = 1024, 768
    init_window("EXERCICES TP1", width, height)

    w_width, w_height = get_screen_width(), get_screen_height() # Dimensions de la window
    vx_o, vy_o = 380, 280 # Origine de la viewport
    v_width, v_height = w_width - vx_o , w_height - vy_o # Dimensions de la viewport

    rect = drawRectangle(vx_o, vy_o , v_width, v_height)
    assoc_key('d', __move_right)
    assoc_key('q', __move_left)
    assoc_key('z', __move_up)
    assoc_key('s', __move_down)
    
    current_color('green')
    px, py = 40,20
    # WC : 
    # Origine : 0, 0
    # Dimensions : width, height
    # Delta W : dWx, dWy
    dWx = w_width
    dWy = w_height
    # ----
    # DC : 
    # Origine : vx_o, vy_o
    # Dimensions : v_width, v_height
    # Delta V : dVx, dVy
    dVx = v_width  - vx_o
    dVy = v_height - vy_o

    vy =  int(dVx  * ( (px - 0 ) / dWx ) + vx_o)
    vx =  int(-dVy * ( (py - 0 ) / dWy ) + vy_o + dVy)

    for i in range(50):
        point(px+i, py)
        point(vx+i, vy)
        #print(vx)
    
    

    

    main_loop()