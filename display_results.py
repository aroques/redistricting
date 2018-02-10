from tkinter import *
from tkinter import ttk
from random import choice


def paint_results(grids):

    dsv = District_Scheme_Visualization(grids)

    dsv.create_rectangles()

    dsv.visualize()


class District_Scheme_Visualization():
    def __init__(self, grids):
        self.board = Board()
        self.root = self.get_root()
        self.canvas = Canvas(self.root, width=self.board.window_width, height=self.board.window_height, borderwidth=5, background='white')
        self.canvas.grid(row=0, column=0, columnspan=6, rowspan=5, sticky=N+E+S+W)
        self.add_buttons()
        self.grids = grids
        self.grid_num = 0

    def btn_next_clicked(self):
        self.grid_num += 1
        self.create_rectangles()
        self.enable_disable_buttons()

    def btn_previous_clicked(self):
        self.grid_num -= 1
        self.create_rectangles()
        self.enable_disable_buttons()

    def enable_disable_buttons(self):
        if self.grid_num == len(self.grids)-1:
            self.btn_next.config(state=DISABLED)
        else:
            self.btn_next.config(state=NORMAL)

        if self.grid_num == 0:
            self.btn_prev.config(state=DISABLED)
        else:
            self.btn_prev.config(state=NORMAL)

    def get_root(self):
        root = Tk()
        root.title("Redistricting Results")
        root.grid_columnconfigure(2, weight=1)
        root.grid_columnconfigure(3, weight=1)
        return root
            
    def add_buttons(self):
        self.btn_prev = Button(self.root, text="Previous", command=self.btn_previous_clicked, state=DISABLED)
        self.btn_prev.grid(row=5, column=2, sticky=W+E)
        self.btn_next = Button(self.root, text="Next", command=self.btn_next_clicked)
        self.btn_next.grid(row=5, column=3, sticky=W+E)

    def create_rectangles(self):
        col_width = self.board.width/len(self.grids[self.grid_num])
        row_height = self.board.height/len(self.grids[self.grid_num][0])

        color_list = ['limegreen', 'red', 'dodgerblue', 'yellow', 'orange']
        colors = {k: v  for k, v in zip(range(1,6), color_list)}

        for i, row in enumerate(self.grids[self.grid_num]):
            for j, col in enumerate(row):
                district = self.grids[self.grid_num][i][j]
                x0, y0, x1, y1 = j*col_width, (i*row_height), (j+1)*col_width , (i+1)*row_height
                rect_coords = [x0, y0, x1, y1]
                rect_coords = [ (coord + self.board.offset) for coord in rect_coords ]
                self.canvas.create_rectangle(*rect_coords, fill=colors[district], width=2.0)
                self.canvas.create_text(x0 + col_width/2  + self.board.offset, y0 + row_height/2 + self.board.offset, text=str(district), font="times 28 bold")
    
    def visualize(self):
        self.root.mainloop()

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