from tkinter import *
import tkinter.font as tkfont
from tkinter import filedialog


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
        self.selectedCheckbox = []
        self.selectedRadio = -1


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
                        col_image = -1
                else:
                    if column == col_image:
                        self.images.append(self.contents[row][column])
                        self.canvas.create_image(x + 50, y + 13, image=self.contents[row][column], anchor=NW)
                    else:
                        self.canvas.create_text((x_text, y_text), text=self.contents[row][column], font=self.data_font)


    def optionsTable(self, num, option):
        self.images = []
        self.checkboxes = {}

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
                        col_image = -1
                else:
                    if column == col_image:
                        self.images.append(self.contents[row][column])
                        self.canvas.create_image(x + 50, y + 13, image=self.contents[row][column], anchor=NW)
                    elif column == 0:
                        if option == "checkbox":
                            self.canvas.create_rectangle(x_text - 9, y_text - 9, x_text + 9, y_text + 9, fill="#191919")
                            self.checkboxes[row] = self.canvas.create_rectangle(x_text - 8, y_text - 8, x_text + 8, y_text + 8, fill="#E8E8E8")
                            self.canvas.tag_bind(self.checkboxes[row], "<Button-1>", lambda e: self.optionClicked(num,option))
                        elif option == "radio":
                            self.canvas.create_oval(x_text - 9, y_text - 9, x_text + 9, y_text + 9, fill="#191919")
                            self.checkboxes[row] = self.canvas.create_oval(x_text - 8, y_text - 8, x_text + 8, y_text + 8, fill="#E8E8E8")
                            self.canvas.tag_bind(self.checkboxes[row], "<Button-1>", lambda e: self.optionClicked(num, option))
                    else:
                        self.canvas.create_text((x_text, y_text), text=self.contents[row][column], font=self.data_font)


    def optionClicked(self, num, option):
        curr_clicked = self.canvas.find_withtag("current")[0] - num
        curr_clicked /= (num - 2)
        curr_clicked = int(curr_clicked)

        if option == "checkbox":
            if curr_clicked in self.selectedCheckbox:
                self.canvas.itemconfig(self.checkboxes[int(curr_clicked + 1)], fill="#E8E8E8")
                self.selectedCheckbox.remove(curr_clicked)
            else:
                self.canvas.itemconfig(self.checkboxes[int(curr_clicked + 1)], fill="#666666")
                self.selectedCheckbox.append(curr_clicked)
        else:
            if curr_clicked == self.selectedRadio:
                self.canvas.itemconfig(self.checkboxes[int(curr_clicked + 1)], fill="#E8E8E8")
                self.selectedRadio = -1
            else:
                if self.selectedRadio == -1:
                    self.selectedRadio += 1
                self.canvas.itemconfig(self.checkboxes[int(self.selectedRadio + 1)], fill="#E8E8E8")
                self.canvas.itemconfig(self.checkboxes[int(curr_clicked + 1)], fill="#666666")
                self.selectedRadio = curr_clicked


    def getSelectedCheckbox(self):
        return self.selectedCheckbox


    def getSelectedRadio(self):
        return self.selectedRadio


class ImportExport():
    def __init__(self):
        self.import_filename = ""
        self.export_filename = "prime_properties_export.txt"

    def uploadFile(self):
        fileTypes = [('All Files', '*.*')]
        self.import_filename = filedialog.askopenfilename(filetypes=fileTypes)
        if len(self.import_filename) > 0:
            display_name = self.import_filename.split('/')[len(self.import_filename.split('/')) - 1]
            self.chosen_header.configure(text=display_name)

    def importFile(self):
        if len(self.import_filename) > 0:
            return True
        return False

    def exportFile(self):
        return True

    def openExport(self):
        print(self.export_filename)

    def displayImport(self, import_bg, sub):
        self.choose_header = Label(import_bg, text="Choose a File to Import", bg="#DDDDDD", fg="#6A6A6A", font=sub)
        self.choose_header.place(relx=.5, rely=0.375, anchor="center")

        self.chosen_header = Label(import_bg, text="No File Chosen", width=25, bg="#EAEAEA", fg="#191919", font=sub)
        self.chosen_header.place(relx=.5, rely=0.450, anchor="center")

        btn_font = tkfont.Font(family='Open Sans', weight="bold", size=13)
        self.choose_btn = Button(import_bg, text="Choose File", width=15, command=lambda: self.uploadFile(),
                            bg="#667275", fg="#FFFFFF", bd=0, font=btn_font)
        self.choose_btn.place(relx=.5, rely=0.550, anchor="center")