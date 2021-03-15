import math
import tkinter as tk
from cng import *

def __move_right():
    x = 10
    y = 0
    obj_move(rect, x, y)
    ox, oy = canv.coords(rect)[0], canv.coords(rect)[1]
    print(ox, oy)


def __move_left():
    x = -10
    y = 0
    obj_move(rect, x, y)
    ox, oy = canv.coords(rect)[0], canv.coords(rect)[1]
    print(ox, oy)


def __move_up():
    x = 0
    y = -10
    obj_move(rect, x, -y)
    ox, oy = canv.coords(rect)[0], canv.coords(rect)[1]
    print(ox, oy)


def __move_down():
    x = 0
    y = -10
    obj_move(rect, x, y)
    ox, oy = canv.coords(rect)[0], canv.coords(rect)[1]
    print(ox, oy)


def drawRectangle(x, y, dimx, dimy):
    rect = rectangle(x, y, x+dimx, x+dimy)
    return rect

def drawLine(ox, oy, length):
    vx =  int(dVx  * ( (px - wx_o ) / dWx ) + vx_o)       # new point x-coordinate in viewport
    vy =  int(-dVy * ( (py - wy_o ) / dWy ) + vy_o + dVy) # new point y-coordinate in viewport
    for i in range(length):
        if i == 0:
            print(vx, vy)
        point(vx+i, vy+i)


def update(ox, oy):
    clear_screen()
    rect = drawRectangle(ox, oy , ox+dVx, oy+dVy)
    drawLine(ox, oy, 300)

if __name__ == "__main__":
    global hadVx
    global rect
    global root
    global canv
    global px, pyv_height
    global x, y
    global v_width, v_height
    global dVx, dVy
    global vx_o, vy_o


    width, height = 1024, 768
    root, canv = init_window("EXERCICES TP1", width, height)
    ha = root.winfo_screenheight()
    w_width, w_height = width, height # Dimensions de la window
    vx_o, vy_o = 380, 280 # Origine de la viewport
    v_width, v_height = w_width - vx_o , w_height - vy_o # Dimensions de la viewport
    assoc_key('d', __move_right)
    assoc_key('q', __move_left)
    assoc_key('z', __move_up)
    assoc_key('s', __move_down)

    current_color('green')
    px, py = 0,0 # point ou la droite commence
    # World Coordinate :
    # Origine : wx_o, wy_o
    # Dimensions : width, height
    # Delta W : dWx, dWy
    wx_o, wy_o = -1, -3 # world origin
    dWx = 6 # world Dimensions (x axis)
    dWy = 1 # world Dimensions (y axis)
    # ----
    # DC :
    # Origine : vx_o, vy_o
    # Dimensions : v_width, v_height
    # Delta V : dVx, dVy
    dVx = v_width  - vx_o - 200 # viewport Dimensions (x axis)
    dVy = v_height - vy_o - 200 # viewport Dimensions (y axis)

    rect = drawRectangle(vx_o, vy_o , vx_o+dVx, vy_o+dVy)
    drawLine(vx_o, vy_o, 350)


    main_loop()
