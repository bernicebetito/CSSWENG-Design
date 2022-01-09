from tkinter import *
from PIL import Image, ImageTk
import os, table, db

class History():
    def __init__(self, root):
        self.database = db.Database()
        self.root = root
        self.history_asset_name = StringVar()
        self.history_owner = StringVar()
        self.history_location = StringVar()
        self.history_status = StringVar()

    def displayHistory(self, history_form_frame, field_label, buttonA, buttonB):
        Label(history_form_frame, text="Filter by Asset Name", bg="#DDDDDD", fg="#363636", font=field_label).place(relx=.5, rely=0.175, anchor="center")
        Entry(history_form_frame, textvariable=self.history_asset_name, bd=0).place(height=20, width=225, relx=.5, rely=0.225, anchor="center")

        Label(history_form_frame, text="Filter by Owner", bg="#DDDDDD", fg="#363636", font=field_label).place(relx=.5, rely=0.275, anchor="center")
        Entry(history_form_frame, textvariable=self.history_owner, bd=0).place(height=20, width=225, relx=.5, rely=0.325, anchor="center")

        Label(history_form_frame, text="Filter by Location", bg="#DDDDDD", fg="#363636", font=field_label).place(relx=.5, rely=0.375, anchor="center")
        Entry(history_form_frame, textvariable=self.history_location, bd=0).place(height=20, width=225, relx=.5, rely=0.425, anchor="center")

        Label(history_form_frame, text="Filter by Status", bg="#DDDDDD", fg="#363636", font=field_label).place(relx=.5, rely=0.475, anchor="center")
        status_choices = ["Sold", "Disposed", "Borrowed", "Lent"]
        status_menu = OptionMenu(history_form_frame, self.history_status, *status_choices)
        status_menu.place(height=20, width=110, relx=.5, rely=0.525, anchor="center")

        filter_btn = Button(history_form_frame, text="Filter", width=13, command=lambda: self.filterTable(), bg="#DC5047", fg="#FFFFFF", bd=0, font=buttonA)
        filter_btn.place(relx=.5, rely=0.625, anchor="center")

        clear_btn = Button(history_form_frame, text="Clear Filter", width=13, command=lambda: self.filterTable(), bg="#404040", fg="#FFFFFF", bd=0, font=buttonB)
        clear_btn.place(relx=.5, rely=0.715, anchor="center")

    def displayTable(self, history_table_frame):
        self.history_canvas = Canvas(history_table_frame, bg="#191919", width=825, height=500)

        history_filter = {"receipt_num": "", "asset_name": "", "owner": "", "location": "", "op_type": "", "in_transit": False}
        history_measurements = {"cell_width": 150, "cell_height": 75, "rows": self.getContent(history_filter),
                                "columns": 8}
        self.history_table = table.Table(history_measurements, self.history_canvas, self.history_table_contents)
        self.history_table.setScrollbars(history_table_frame)
        self.history_table.createTable()
        self.history_canvas.configure(scrollregion=self.history_canvas.bbox("all"))

    def getContent(self, filter_val):
        history_table_header = ["Photo", "Asset Name", "Company", "Owner", "Location", "Amount", "Payment Status", "Status"]
        curr_row = []
        self.history_table_contents = []
        for column in history_table_header:
            curr_row.append(column)
        self.history_table_contents.append(curr_row)

        self.root.table_image = []
        history = self.database.viewTable(2, filter_val)
        if type(history) == list:
            for row in range(len(history)):
                curr_row = []
                for column in range(6, len(history[row]) - 1):
                    if type(history[row][column]) == bytes:
                        filepath = self.database.readBLOB(history[row][5])
                        image = Image.open(filepath)
                        resized_img = image.resize((50, 50), Image.ANTIALIAS)
                        table_image = ImageTk.PhotoImage(resized_img)
                        self.root.table_image.append(table_image)
                        curr_row.append(table_image)
                    elif column != 8:
                        curr_row.append(history[row][column])
                curr_row.append(history[row][2])
                self.history_table_contents.append(curr_row)
            return len(history) + 1
        return 1

    def filterTable(self):
        self.history_canvas.delete("all")

        if len(self.history_asset_name.get()) > 0 or len(self.history_owner.get()) > 0 or len(self.history_location.get()) > 0 or len(self.history_status.get()) > 0:
            history_filter = {"receipt_num": "", "asset_name": self.history_asset_name.get(),
                              "owner": self.history_owner.get(), "location": self.history_location.get(),
                              "op_type": self.history_status.get(), "in_transit": False}
            self.history_asset_name.set("")
            self.history_owner.set("")
            self.history_location.set("")
            self.history_status.set("")
        else:
            history_filter = {"receipt_num": "", "asset_name": "", "owner": "", "location": "", "op_type": "", "in_transit": False}

        self.history_table.rows = self.getContent(history_filter)
        self.history_table.contents = self.history_table_contents
        self.history_table.optionsTable(11, "radio")
        self.history_canvas.configure(scrollregion=self.history_canvas.bbox("all"))