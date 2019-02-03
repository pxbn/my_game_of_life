from graphics import *
import numpy as np
from math import ceil
from time import sleep

# Initialize the window with everything
def init_window(win, tile_size, window_size, num_of_tiles):
    # win.setCoords(0.0, 0.0, 10.0, 10.0)
    win.setBackground("gray")


    # draw grid
    for i in range(1, num_of_tiles):
        line = Line(Point(i*tile_size, 0), Point(i*tile_size, window_size))
        line.draw(win)

        line = Line(Point(0,i*tile_size), Point(window_size, i*tile_size))
        line.draw(win)

def populate_on_mouse(mp, data, tile_size, window_size):
    x = int(ceil(mp.getX() / tile_size)) -1
    y = int(ceil(mp.getY() / tile_size)) -1

    # Populate
    data[x][y] = not data[x][y]
    print("spalte: " + str(x) + " zeile: " + str(y) + " population: "
        + str(data[x][y]))
    
def animate(win, data, tile_size):
    for x in range(0, data.shape[0]):
        for y in range(0, data.shape[1]):
            rect = Rectangle(Point(x*tile_size, y*tile_size),
                Point(x*tile_size + tile_size, y*tile_size+tile_size))
            if data[x, y] == True:
                rect.setFill("yellow")
            elif data[x, y] == False:
                rect.setFill("gray")
            
            rect.draw(win)

def do_stuff(data):
    # copy data so that current and next generation dont interfer
    next_gen = np.copy(data)

    for x in range(0, data.shape[0]):
        for y in range(0, data.shape[1]):
            #check surrounding tiles
            num_of_neighbours = 0
            # print('at x: ' + str(x) + " y: " + str(y))

            for x_off in range(-1, 2):
                for y_off in range(-1, 2):
                    # ignore out of bounds
                    curr_x = x+x_off
                    curr_y = y+y_off
                    
                    if  curr_x < 0 or curr_x >= data.shape[0]:
                        continue
                    if curr_y < 0 or curr_y >= data.shape[1]:
                        continue
                    if curr_x == x and curr_y == y:
                        continue

                    if data[curr_x, curr_y] == True:
                        num_of_neighbours += 1
            #             print('added neighbor at x:' + str(curr_x) + 
            #                 " y: " + str(curr_y))

            # print("num_of_neighbours: " + str(num_of_neighbours))
            
            # die from isolation
            if num_of_neighbours < 2:
                next_gen[x, y] = False
            # die from overpopulation
            elif num_of_neighbours > 3:
                next_gen[x, y] = False
            #getting reborn
            if num_of_neighbours == 3:
                next_gen[x,y] = True

    return next_gen



def new_tile_clicked(old_click, click_point, tile_size):
    if old_click == None or click_point == None:
        return True

    oldX = old_click.getX()
    oldY = old_click.getY()

    newX = click_point.getX()
    newY = click_point.getY()

    diffX = abs(oldX - newX)
    diffY = abs(oldY - newY)

    if diffX > tile_size or diffY > tile_size:
        return True
    else:
        return False

def main():
    # init data
    tile_size = 25
    window_size = 500
    num_of_tiles = int(window_size / tile_size)
    data = np.zeros((num_of_tiles,num_of_tiles), dtype=bool)

    # init window
    win = GraphWin('Game of life', window_size, window_size)
    init_window(win, tile_size, window_size, num_of_tiles)

    run = False

    data[2,2] = True
    data[2,3] = True
    data[3,2] = True
    data[3,3] = True
    data[3,4] = True
    animate(win, data, tile_size)
    sleep(1)

    old_click = None
    old_key = ""


    while True:
        click_point = win.checkMouse()
        key = win.checkKey()

        # clicked new grid element? -> populate
        if (click_point != old_click and
         new_tile_clicked(old_click, click_point, tile_size)):
            populate_on_mouse(click_point, data, tile_size, window_size)
            old_click = None
            click_point = None

            animate(win,data,tile_size)
        
        # new key pres? start simulation
        if key != old_key:
            run = not run
            old_key = ''
            key = ''

        if run:
            data = do_stuff(data)
            sleep(0.5)
            animate(win,data,tile_size)


main()
