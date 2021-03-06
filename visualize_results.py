from tkinter import *
from tkinter import ttk
from random import choice
from getters import get_voter_parties

def paint_results(grids, ratio_stats):
    """ Displays redistricting results in a tkinter GUI """

    rv = Redistricting_Visualization(grids, ratio_stats)

    rv.visualize()

class Redistricting_Visualization():
    def __init__(self, grids, ratio_stats):
        """ Initializes the class """
        self.board = Board()
        self.root = self.get_root()
        self.canvas = Canvas(self.root, width=self.board.window_width, height=self.board.window_height, borderwidth=5, background='white')
        self.canvas.grid(row=0, column=0, columnspan=6, rowspan=5)
        self.add_buttons()

        self.color_by_party = False
        self.pie_is_hidden = False

        self.grid = Grid(grids)
        self.grid.create_rectangles(self.canvas, self.color_by_party)
        self.grid.hide_grid(self.canvas)
        self.pie = Pie_Chart(self.root, self.canvas, ratio_stats)

    def btn_show_pie_clicked(self):
        """ Show pie button on_click event handler """
        if self.pie_is_hidden:
            self.show_pie()
        else:
            self.hide_pie()

    def show_pie(self):
        """ Shows pie chart. hides grid """
        self.btn_next.configure(state=DISABLED)
        self.btn_prev.configure(state=DISABLED)
        self.btn_show_pie.configure(text="Hide pie chart")
        self.btn_color_by.configure(state=DISABLED)
        self.pie.show_pie(self.canvas)
        self.grid.hide_grid(self.canvas)
        self.pie_is_hidden = False

    def hide_pie(self):
        """ Hides pie chart, shows grid """
        self.enable_disable_next_prev_btns()
        self.btn_show_pie.configure(text="Show pie chart")
        self.btn_color_by.configure(state=NORMAL)
        self.pie.hide_pie(self.canvas)
        self.grid.show_grid(self.canvas)
        self.pie_is_hidden = True

    def btn_next_clicked(self):
        """ Next button event handler """
        self.grid.grid_num += 1
        self.color_by_party = False
        self.btn_color_by.configure(text='Color by Party')
        self.grid.create_rectangles(self.canvas, self.color_by_party)
        self.enable_disable_next_prev_btns()

    def btn_previous_clicked(self):
        """ Previous button event handler """
        self.grid.grid_num -= 1
        self.color_by_party = False
        self.btn_color_by.configure(text='Color by Party')
        self.grid.create_rectangles(self.canvas, self.color_by_party)
        self.enable_disable_next_prev_btns()

    def btn_color_by_clicked(self):
        """ Color by button event handler """
        if not self.color_by_party:
            self.color_by_party = True
            self.btn_color_by.configure(text='Color by District')
            self.grid.create_rectangles(self.canvas, self.color_by_party)
        else:
            self.color_by_party = False
            self.btn_color_by.configure(text='Color by Party')
            self.grid.create_rectangles(self.canvas, self.color_by_party)

    def enable_disable_next_prev_btns(self):
        """ Enables or disables next and previous buttons """
        if self.grid.grid_num == len(self.grid.grids)-1:
            self.btn_next.config(state=DISABLED)
        else:
            self.btn_next.config(state=NORMAL)

        if self.grid.grid_num == 0:
            self.btn_prev.config(state=DISABLED)
        else:
            self.btn_prev.config(state=NORMAL)

    def get_root(self):
        """ Returns a tkinter root """
        root = Tk()
        root.title("Redistricting Results")
        root.grid_columnconfigure(2, weight=1)
        root.grid_columnconfigure(3, weight=1)
        return root
            
    def add_buttons(self):
        """ Adds buttons to the GUI """
        self.btn_show_pie = Button(self.root, text="Hide pie chart", command=self.btn_show_pie_clicked)
        self.btn_show_pie.grid(row=5, column=0, columnspan=6, sticky=W+E)
        self.btn_color_by = Button(self.root, text="Color by Party", command=self.btn_color_by_clicked, state=DISABLED)
        self.btn_color_by.grid(row=6, column=0, columnspan=6, sticky=W+E)
        self.btn_prev = Button(self.root, text="Previous", command=self.btn_previous_clicked, state=DISABLED)
        self.btn_prev.grid(row=7, column=2, sticky=W+E)
        self.btn_next = Button(self.root, text="Next", command=self.btn_next_clicked, state=DISABLED)
        self.btn_next.grid(row=7, column=3, sticky=W+E)

    def visualize(self):
        """ Launches the visualization """
        self.root.mainloop()

class Grid:
    def __init__(self, grids):
        """ Initializes the class """
        self.grids = grids
        self.grid_num = 0
        self.voter_parties = get_voter_parties()
        self.board = Board()
        color_list = ['limegreen', 'red', 'dodgerblue', 'yellow', 'orange']
        self.colors = {k: v  for k, v in zip(range(1,6), color_list)}
        self.rectangle_ids = []
        self.district_label_ids = []

    def create_rectangles(self, canvas, color_by_party):
        """ Creates squares that represent districts """
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
        """ Returns color of the square - either by party or by district """
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
        """ Shows the grid """
        Canvas_Helper.hide_canvas_items(canvas, self.rectangle_ids, hide=False)
        Canvas_Helper.hide_canvas_items(canvas, self.district_label_ids, hide=False)

    def hide_grid(self, canvas):
        """ Hides the grid """
        Canvas_Helper.hide_canvas_items(canvas, self.rectangle_ids)
        Canvas_Helper.hide_canvas_items(canvas, self.district_label_ids)

class Pie_Chart:
    def __init__(self, root, canvas, ratio_stats):
        """ Initializes the class """
        self.board = Board()
        self.arc_ids = []
        self.label_ids = []

        x0, y0, x1, y1 = 100, 20, (self.board.width/8)*7, (self.board.height/4)*3
        coords = [x0, y0, x1, y1]
        green_list = ['limegreen', 'green', 'yellowgreen', 'olive', 'palegreen']

        start_degree = 0

        # test data
        # ratio_stats[(4, 1)] = .4333
        # ratio_stats[(3, 2)] = .4667
        # ratio_stats[(5, 0)] = .0667
        # ratio_stats[(2, 3)] = .0333

        i = 0

        x = 20
        y_start = (self.board.height/20)*16
        new_line = 22

        width = 15

        label_text = '{:<{width}} {:<{width}} {:<{width}} {:<{width}}'.format('Winner', 'Ratio', 'Percent', 'Color', width=width)
        self.label_ids.append(canvas.create_text(x, y_start, text=label_text, font="times 12 bold", anchor='w'))

        for k, v in ratio_stats.items():
            green_wins = k[0]
            purple_wins = k[1]

            color = green_list[i]

            if green_wins > purple_wins:
                winner = 'Green'
                i += 1
            else:
                winner = 'Purple'
                color = 'magenta'
            

            pct = v
            extent = self.prop(pct)

            self.arc_ids.append(canvas.create_arc(*coords, fill=color, outline='black', start=start_degree, extent=extent))
            ratio = 'G: {} P: {}'.format(green_wins, purple_wins)
            pct = round(float(pct*100), 2)
            pct = str(pct).zfill(5) + '%'
            label_text = '{:<{width}} {:<{width}}  {:<{width}} {:<{width}}'.format(winner, ratio, pct, color, width=width)
            self.label_ids.append(canvas.create_text(x, (y_start + new_line), text=label_text, font="times 12", anchor='w'))
            
            start_degree += extent
            y_start += new_line

            

    def prop(self, pct):
        """ Returns percentage of 360 degrees """
        return 359.99 * pct

    def show_pie(self, canvas):
        """ Shows the pie chart """
        Canvas_Helper.hide_canvas_items(canvas, self.arc_ids, hide=False)
        Canvas_Helper.hide_canvas_items(canvas, self.label_ids, hide=False)

    def hide_pie(self, canvas):
        """ Hides the pie chart """
        Canvas_Helper.hide_canvas_items(canvas, self.arc_ids)
        Canvas_Helper.hide_canvas_items(canvas, self.label_ids)

class Board:
    def __init__(self):
        """ Initializes the class """
        self.width = self.height = 500
        self.offset = 10

    @property
    def window_width(self):
        """ Returns the width of the window """
        return self.width + self.offset
    
    @property
    def window_height(self):
        """ Returns the height of the window """
        return self.height + self.offset

class Canvas_Helper:
    @staticmethod
    def hide_canvas_items(canvas, items, hide=True):
        """ Hides items on the canvas """
        if hide:
            state = HIDDEN
        else:
            state = NORMAL

        for item in items:
            canvas.itemconfigure(item, state=state)