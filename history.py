from tkinter import *
from tkinter import ttk
import tkinter.font as tkfont
from PIL import Image, ImageTk
from tkinter import filedialog
from tkinter.filedialog import askopenfile
import os, table

class History():
    def __init__(self, root):
        self.root = root
        self.history_asset_name = StringVar()
        self.history_location = StringVar()
        self.history_owner = StringVar()
        self.history_status = StringVar()

    def filterTable(self):
        # Where filtering would happen
        print("Filter button clicked")

    def displayHistory(self, history_form_frame, field_label, buttonA):
        Label(history_form_frame, text="Filter by Asset Name", bg="#DDDDDD", fg="#363636", font=field_label).place(relx=.5, rely=0.200, anchor="c")
        Entry(history_form_frame, textvariable=self.history_asset_name, bd=0).place(height=20, width=225, relx=.5, rely=0.250, anchor="c")

        Label(history_form_frame, text="Filter by Location", bg="#DDDDDD", fg="#363636", font=field_label).place(relx=.5, rely=0.325, anchor="c")
        Entry(history_form_frame, textvariable=self.history_location, bd=0).place(height=20, width=225, relx=.5, rely=0.375, anchor="c")

        Label(history_form_frame, text="Filter by Owner", bg="#DDDDDD", fg="#363636", font=field_label).place(relx=.5, rely=0.450, anchor="c")
        Entry(history_form_frame, textvariable=self.history_owner, bd=0).place(height=20, width=225, relx=.5, rely=0.500, anchor="c")

        Label(history_form_frame, text="Filter by Status", bg="#DDDDDD", fg="#363636", font=field_label).place(relx=.5, rely=0.575, anchor="c")
        Entry(history_form_frame, textvariable=self.history_status, bd=0).place(height=20, width=225, relx=.5, rely=0.625, anchor="c")

        filter_btn = Button(history_form_frame, text="Filter", width=13, command=lambda: self.filterTable(), bg="#FE5F55", fg="#FFFFFF", bd=0, font=buttonA)
        filter_btn.place(relx=.5, rely=0.725, anchor="c")

    def displayTable(self, history_table_frame):
        history_canvas = Canvas(history_table_frame, bg="#191919", width=825, height=500)

        history_measurements = {
            "cell_width": 150,
            "cell_height": 75,
            "rows": 100,
            "columns": 10
        }
        history_table_header = ["Photo", "Asset Name", "Company", "Owner", "Location",
                                "Price", "Payment Status", "Amount", "Status", "Operation"]

        history_table_contents = []
        self.root.table_image = []
        for row in range(100):
            curr_row = []
            for column in range(10):
                if row == 0:
                    curr_row.append(history_table_header[column])
                else:
                    if column == 0:
                        image = Image.open(os.getcwd() + r'\assets\img\sample_photo.png')
                        resized_img = image.resize((50, 50), Image.ANTIALIAS)
                        table_image = ImageTk.PhotoImage(resized_img)
                        self.root.table_image.append(table_image)
                        curr_row.append(table_image)
                    else:
                        curr_row.append("Testing Text")
            history_table_contents.append(curr_row)

        history_table = table.Table(history_measurements, history_canvas, history_table_contents)
        history_table.setScrollbars(history_table_frame)
        history_table.createTable()
        history_canvas.configure(scrollregion=history_canvas.bbox("all"))