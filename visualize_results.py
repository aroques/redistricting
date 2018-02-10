from tkinter import *
from tkinter import ttk
from random import choice
from getters import get_voter_parties

def paint_results(grids):

    rv = Redistricting_Visualization(grids)

    rv.visualize()

class Redistricting_Visualization():
    def __init__(self, grids):
        self.board = Board()
        self.root = self.get_root()
        self.canvas = Canvas(self.root, width=self.board.window_width, height=self.board.window_height, borderwidth=5, background='white')
        self.canvas.grid(row=0, column=0, columnspan=6, rowspan=5)
        self.add_buttons()
        self.grids = grids
        self.grid_num = 0
        self.voter_parties = get_voter_parties()
        self.color_by_party = False


        color_list = ['limegreen', 'red', 'dodgerblue', 'yellow', 'orange']
        self.colors = {k: v  for k, v in zip(range(1,6), color_list)}

        self.create_rectangles(self.color_by_party)

    def btn_next_clicked(self):
        self.grid_num += 1
        self.create_rectangles(False)
        self.enable_disable_buttons()

    def btn_previous_clicked(self):
        self.grid_num -= 1
        self.create_rectangles(False)
        self.enable_disable_buttons()

    def btn_view_voters_clicked(self):
        if not self.color_by_party:
            self.color_by_party = True
            self.btn_view_voters.configure(text='Color by District')
            self.create_rectangles(self.color_by_party)
        else:
            self.color_by_party = False
            self.btn_view_voters.configure(text='Color by Party')
            self.create_rectangles(self.color_by_party)


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
        self.btn_view_voters = Button(self.root, text="Color by Party", command=self.btn_view_voters_clicked)
        self.btn_view_voters.grid(row=5, column=0, columnspan=6, sticky=W+E)
        self.btn_prev = Button(self.root, text="Previous", command=self.btn_previous_clicked, state=DISABLED)
        self.btn_prev.grid(row=6, column=2, sticky=W+E)
        self.btn_next = Button(self.root, text="Next", command=self.btn_next_clicked)
        self.btn_next.grid(row=6, column=3, sticky=W+E)

    def create_rectangles(self, color_by_party):
        col_width = self.board.width/len(self.grids[self.grid_num])
        row_height = self.board.height/len(self.grids[self.grid_num][0])

        for i, row in enumerate(self.grids[self.grid_num]):
            for j, col in enumerate(row):
                district = self.grids[self.grid_num][i][j]
                grid_coord = (i, j)
                color = self.get_color(color_by_party, grid_coord)        
        
                x0, y0, x1, y1 = j*col_width, (i*row_height), (j+1)*col_width , (i+1)*row_height
                rect_coords = [x0, y0, x1, y1]
                rect_coords = [ (coord + self.board.offset) for coord in rect_coords ]
                self.canvas.create_rectangle(*rect_coords, fill=color, width=2.0)
                self.canvas.create_text(x0 + col_width/2  + self.board.offset, y0 + row_height/2 + self.board.offset, text=str(district), font="times 28 bold")
    
    def get_color(self, color_by_party, grid_coord):
        if color_by_party:
            party = self.voter_parties[grid_coord[0]][grid_coord[1]]
            if party == 'P':
                color = '#D050D0'
            else:
                color = '#4FD14F'
        else:
            district = self.grids[self.grid_num][grid_coord[0]][grid_coord[1]]
            color = self.colors[district]
        
        return color


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