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

        self.color_by_party = False
        
        self.grid = Grid(grids)
        self.grid.create_rectangles(self.canvas, self.color_by_party)
        self.grid.hide_grid(self.canvas)
        self.grid.show_grid(self.canvas)
        #pie = Pie_Chart(self.root, self.canvas)

        #self.create_rectangles(self.color_by_party)

    def btn_show_pie_clicked(self):
        print("show pie clicked!")

    def btn_next_clicked(self):
        self.grid.grid_num += 1
        self.color_by_party = False
        self.btn_color_by.configure(text='Color by Party')
        self.grid.create_rectangles(self.canvas, self.color_by_party)
        self.enable_disable_buttons()

    def btn_previous_clicked(self):
        self.grid.grid_num -= 1
        self.color_by_party = False
        self.btn_color_by.configure(text='Color by Party')
        self.grid.create_rectangles(self.canvas, self.color_by_party)
        self.enable_disable_buttons()

    def btn_color_by_clicked(self):
        if not self.color_by_party:
            self.color_by_party = True
            self.btn_color_by.configure(text='Color by District')
            self.grid.create_rectangles(self.canvas, self.color_by_party)
        else:
            self.color_by_party = False
            self.btn_color_by.configure(text='Color by Party')
            self.grid.create_rectangles(self.canvas, self.color_by_party)


    def enable_disable_buttons(self):
        if self.grid.grid_num == len(self.grid.grids)-1:
            self.btn_next.config(state=DISABLED)
        else:
            self.btn_next.config(state=NORMAL)

        if self.grid.grid_num == 0:
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
        self.btn_show_pie = Button(self.root, text="Show pie chart", command=self.btn_show_pie_clicked)
        self.btn_show_pie.grid(row=5, column=0, columnspan=6, sticky=W+E)
        self.btn_color_by = Button(self.root, text="Color by Party", command=self.btn_color_by_clicked)
        self.btn_color_by.grid(row=6, column=0, columnspan=6, sticky=W+E)
        self.btn_prev = Button(self.root, text="Previous", command=self.btn_previous_clicked, state=DISABLED)
        self.btn_prev.grid(row=7, column=2, sticky=W+E)
        self.btn_next = Button(self.root, text="Next", command=self.btn_next_clicked)
        self.btn_next.grid(row=7, column=3, sticky=W+E)

    def visualize(self):
        self.root.mainloop()

class Grid:

    def __init__(self, grids):
        self.grids = grids
        self.grid_num = 0
        self.voter_parties = get_voter_parties()
        self.board = Board()
        color_list = ['limegreen', 'red', 'dodgerblue', 'yellow', 'orange']
        self.colors = {k: v  for k, v in zip(range(1,6), color_list)}
        self.rectangle_ids = []
        self.district_label_ids = []

    def create_rectangles(self, canvas, color_by_party):
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
                self.rectangle_ids.append(canvas.create_rectangle(*rect_coords, fill=color, width=2.0))
                self.district_label_ids.append(canvas.create_text(x0 + col_width/2  + self.board.offset, y0 + row_height/2 + self.board.offset, text=str(district), font="times 28 bold"))

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

    def show_grid(self, canvas):
        self.hide_canvas_items(False, canvas, self.rectangle_ids)
        self.hide_canvas_items(False, canvas, self.district_label_ids)

    def hide_grid(self, canvas):
        self.hide_canvas_items(True, canvas, self.rectangle_ids)
        self.hide_canvas_items(True, canvas, self.district_label_ids)

    def hide_canvas_items(self, hide, canvas, items):
        if hide:
            state = HIDDEN
        else:
            state = NORMAL

        for item in items:
            canvas.itemconfigure(item, state=state)


class Pie_Chart:
    def __init__(self, root, canvas):
        self.board = Board()
        x0, y0, x1, y1 = 100, 100, (self.board.width/6)*5, (self.board.height/6)*5
        coords = [x0, y0, x1, y1]
        canvas.create_arc(*coords, fill="#FAF402", outline="#FAF402", start=self.prop(0), extent = self.prop(20))
        canvas.create_arc(*coords, fill="#00AC36", outline="#00AC36", start=self.prop(20), extent = self.prop(40))
        canvas.create_arc(*coords, fill="#7A0871", outline="#7A0871", start=self.prop(60), extent = self.prop(5))
        canvas.create_arc(*coords, fill="#E00022", outline="#E00022", start=self.prop(65), extent = self.prop(20))
        canvas.create_arc(*coords, fill="#294994", outline="#294994",  start=self.prop(85), extent = self.prop(15))

    def prop(self, pct): 
        return 360.0 * (pct/100)

class Board:
    def __init__(self):
        self.width = self.height = 500
        self.offset = 10

    @property
    def window_width(self):
        return self.width + self.offset
    
    @property
    def window_height(self):
        return self.height + self.offset