from tkinter import *
from tkinter import ttk
from random import choice

def paint_results(grid):

    root = get_root()

    add_rectangles(root, grid)

    root.mainloop()

def btn_next_clicked():
    print("next clicked!")

def btn_previous_clicked():
    print("previous clicked!")

def get_root():
    root = Tk()
    root.title("Redistricting Results")
    root.grid_columnconfigure(2, weight=1)
    root.grid_columnconfigure(3, weight=1)
    return root

def add_rectangles(root, grid):

    board = Board()

    canvas = Canvas(root, width=board.window_width, height=board.window_height, borderwidth=5, background='white')
    
    add_buttons(root)

    create_rectangles(canvas, grid, board)
            
    canvas.grid(row=0, column=0, columnspan=6, rowspan=5)

def add_buttons(root):
    b = Button(root, text="Previous", command=btn_previous_clicked)
    b.grid(row=5, column=2, sticky=W+E)
    b = Button(root, text="Next", command=btn_next_clicked)
    b.grid(row=5, column=3, sticky=W+E)

def create_rectangles(canvas, grid, board):
    col_width = board.width/len(grid)
    row_height = board.height/len(grid[0])

    color_list = ['green', 'red', 'blue', 'yellow', 'orange']
    colors = {k: v  for k, v in zip(range(1,6), color_list)}

    for i, row in enumerate(grid):
        for j, col in enumerate(row):
            district = grid[i][j]
            x0, y0, x1, y1 = j*col_width, (i*row_height), (j+1)*col_width , (i+1)*row_height
            rect_coords = [x0, y0, x1, y1]
            rect_coords = [ (coord + board.offset) for coord in rect_coords ]
            canvas.create_rectangle(*rect_coords, fill=colors[district], width=2.0)

class Board():
    def __init__(self):
        self.width = self.height = 500
        self.offset = 10

    @property
    def window_width(self):
        return self.width + self.offset
    
    @property
    def window_height(self):
        return self.height + self.offset