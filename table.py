from tkinter import *
from tkinter import ttk
import tkinter as tk
import tkinter.font as tkfont


class Table(object):
    def __init__(self, measurements, canvas, table_contents):
        self.rows = measurements["rows"]
        self.cols = measurements["columns"]
        self.cell_height = measurements["cell_height"]
        self.cell_width = measurements["cell_width"]
        self.canvas = canvas
        self.contents = table_contents
        self.header_font = tkfont.Font(family='Open Sans', weight='bold', size=13)
        self.data_font = tkfont.Font(family='Open Sans', size=10)
        self.images = []


    def setScrollbars(self, frame):
        self.vertical_scroll = Scrollbar(frame, orient=VERTICAL)
        self.vertical_scroll.pack(side=RIGHT, fill=Y)
        self.vertical_scroll.config(command=self.canvas.yview)
        self.horizontal_scroll = Scrollbar(frame, orient=HORIZONTAL)
        self.horizontal_scroll.pack(side=BOTTOM, fill=X)
        self.horizontal_scroll.config(command=self.canvas.xview)

        self.canvas.configure(xscrollcommand=self.horizontal_scroll.set, yscrollcommand=self.vertical_scroll.set)
        self.canvas.pack(expand=True, side=LEFT, fill=BOTH)


    def createTable(self):
        self.images = []
        col_image = 0
        for row in range(self.rows):
            y = row * self.cell_height
            for column in range(self.cols):
                x = column * self.cell_width
                self.canvas.create_rectangle(x, y, x + self.cell_width, y + self.cell_height, fill="#EAEAEA")

                x_text = x + (self.cell_width / 2)
                y_text = y + (self.cell_height / 2)

                if row == 0:
                    self.canvas.create_text((x_text, y_text), text=self.contents[row][column], font=self.header_font)
                    if str(self.contents[row][column]) == "Photo":
                        col_image = column
                else:
                    if column == col_image:
                        self.images.append(self.contents[row][column])
                        self.canvas.create_image(x + 50, y + 13, image=self.contents[row][column], anchor=NW)
                    else:
                        self.canvas.create_text((x_text, y_text), text=self.contents[row][column], font=self.data_font)