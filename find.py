from tkinter import *
from PIL import Image, ImageTk
import os, table

class FindAsset():
    def __init__(self, root):
        self.root = root
        self.findAsset_asset_name = StringVar()
        self.findAsset_location = StringVar()
        self.findAsset_owner = StringVar()
        self.findAsset_status = StringVar()

    def filterTable(self):
        # Where filtering would happen
        print("Filter button clicked")

    def displayAssets(self, findAsset_form_frame, field_label, buttonA):
        Label(findAsset_form_frame, text="Search by Asset Name", bg="#DDDDDD", fg="#363636", font=field_label).place(relx=.5, rely=0.200, anchor="c")
        Entry(findAsset_form_frame, textvariable=self.findAsset_asset_name, bd=0).place(height=20, width=225, relx=.5, rely=0.250, anchor="c")

        Label(findAsset_form_frame, text="Search by Location", bg="#DDDDDD", fg="#363636", font=field_label).place(relx=.5, rely=0.325, anchor="c")
        Entry(findAsset_form_frame, textvariable=self.findAsset_location, bd=0).place(height=20, width=225, relx=.5, rely=0.375, anchor="c")

        Label(findAsset_form_frame, text="Search by Owner", bg="#DDDDDD", fg="#363636", font=field_label).place(relx=.5, rely=0.450, anchor="c")
        Entry(findAsset_form_frame, textvariable=self.findAsset_owner, bd=0).place(height=20, width=225, relx=.5, rely=0.500, anchor="c")

        Label(findAsset_form_frame, text="Search by Status", bg="#DDDDDD", fg="#363636", font=field_label).place(relx=.5, rely=0.575, anchor="c")
        Entry(findAsset_form_frame, textvariable=self.findAsset_status, bd=0).place(height=20, width=225, relx=.5, rely=0.625, anchor="c")

        filter_btn = Button(findAsset_form_frame, text="Search", width=13, command=lambda: self.filterTable(), bg="#DC5047", fg="#FFFFFF", bd=0, font=buttonA)
        filter_btn.place(relx=.5, rely=0.725, anchor="c")

    def displayTable(self, findAsset_table_frame):
        findAsset_canvas = Canvas(findAsset_table_frame, bg="#191919", width=825, height=500)

        findAsset_measurements = {
            "cell_width": 150,
            "cell_height": 75,
            "rows": 100,
            "columns": 10
        }
        findAsset_table_header = ["Photo", "Asset Name", "Company", "Owner", "Location",
                                "Price", "Payment Status", "Amount", "Status", "Operation"]

        findAsset_table_contents = []
        self.root.table_image = []
        for row in range(100):
            curr_row = []
            for column in range(10):
                if row == 0:
                    curr_row.append(findAsset_table_header[column])
                else:
                    if column == 0:
                        image = Image.open(os.getcwd() + r'\assets\img\sample_photo.png')
                        resized_img = image.resize((50, 50), Image.ANTIALIAS)
                        table_image = ImageTk.PhotoImage(resized_img)
                        self.root.table_image.append(table_image)
                        curr_row.append(table_image)
                    else:
                        curr_row.append("Testing Text")
            findAsset_table_contents.append(curr_row)

        findAsset_table = table.Table(findAsset_measurements, findAsset_canvas, findAsset_table_contents)
        findAsset_table.setScrollbars(findAsset_table_frame)
        findAsset_table.createTable()
        findAsset_canvas.configure(scrollregion=findAsset_canvas.bbox("all"))