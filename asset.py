from tkinter import *
from PIL import Image, ImageTk
import tkinter.font as tkfont
import os, table
import db


class createAsset():
    def __init__(self, root):
        self.database = db.Database()

        self.create_photo = ""
        self.create_name = StringVar()
        self.create_company = StringVar()
        self.create_status = StringVar()
        self.create_location = StringVar()
        self.create_price = DoubleVar()
        self.create_quantity = DoubleVar()
        self.create_ownership = StringVar()
        self.create_payment_status = StringVar()
        self.create_payment_status_int = IntVar()

        self.create_name_field = Entry()
        self.create_company_field = Entry()
        self.create_status_field = Entry()
        self.create_location_field = Entry()
        self.create_price_field = Entry()
        self.create_quantity_field = Entry()
        self.create_owner_field = Entry()
        self.create_payment_field = Radiobutton()

        self.create_fields = []
        self.create_error_label = Label()
        self.create_all_invalid = False

        self.reg_validDouble = root.register(self.validDouble)
        self.reg_invalidDouble = root.register(self.invalidDouble)

    def setButton(self, create_button):
        self.create_button = create_button
        self.create_button.config(state=DISABLED)

    def validDouble(self, value):
        for i in self.create_fields:
            i.configure(highlightthickness=0, highlightbackground="#D64000", highlightcolor="#D64000")
        self.create_error_label.config(text="")
        try:
            float(value)
            self.create_button.config(state=NORMAL)
            return True
        except :
            return False

    def invalidDouble(self):
        self.create_button.config(state=DISABLED)
        if not self.create_all_invalid:
            for i in self.create_fields:
                i.configure(highlightthickness=0, highlightbackground="#D64000", highlightcolor="#D64000")
            self.create_error_label.config(text="Price and Quantity should be Numbers")
            self.create_price_field.configure(highlightthickness=2, highlightbackground="#D64000", highlightcolor="#D64000")
            self.create_quantity_field.configure(highlightthickness=2, highlightbackground="#D64000", highlightcolor="#D64000")

    def setImage(self, filepath):
        self.create_photo = self.database.convertToBinaryData(filepath)
        if self.create_photo == False:
            return False
        return True

    def submitForm(self, username):
        valid_first = len(self.create_name.get()) > 1 and len(self.create_company.get()) > 1
        valid_second = len(self.create_location.get()) > 1 and len(self.create_ownership.get()) > 1
        valid_third = self.create_price.get() > 0 and self.create_quantity.get() > 0 and self.create_payment_status_int.get() > 0
        if valid_first and valid_second and valid_third:
            name = self.create_name.get()
            company = self.create_company.get()
            owner = self.create_ownership.get()
            status = "Available"
            unit_loc = self.create_location.get()
            price = self.create_price.get()
            quantity = self.create_quantity.get()
            if self.create_payment_status_int.get() == 1:
                payment_stat = "Paid"
            else:
                payment_stat = "Unpaid"
            image = self.create_photo

            self.database.createAsset("assets", username, name, company, owner, status, unit_loc, price, quantity, payment_stat, image)
            return True
        else:
            if self.create_price.get() <= 0 or self.create_quantity.get() <= 0:
                for i in self.create_fields:
                    i.configure(highlightthickness=0, highlightbackground="#D64000", highlightcolor="#D64000")
                self.create_error_label.config(text="Price and Quantity should be Higher than 0.00")
                self.create_price_field.configure(highlightthickness=2, highlightbackground="#D64000", highlightcolor="#D64000")
                self.create_quantity_field.configure(highlightthickness=2, highlightbackground="#D64000", highlightcolor="#D64000")
            else:
                for i in self.create_fields:
                    i.configure(highlightthickness=2, highlightbackground="#D64000", highlightcolor="#D64000")
                self.create_error_label.config(text="Please Fill Up All Fields")
            return False

    def setCreate(self, create_right, field_label):
        Label(create_right, text="Asset Name", bg="#DDDDDD", fg="#363636", font=field_label).place(relx=.100, rely=0.200, anchor="center")
        self.create_name_field = Entry(create_right, textvariable=self.create_name, width=35, bd=0)
        self.create_name_field.place(height=25, width=250, relx=.245, rely=0.250, anchor="center")
        self.create_fields.append(self.create_name_field)

        Label(create_right, text="Company", bg="#DDDDDD", fg="#363636", font=field_label).place(relx=.590, rely=0.200, anchor="center")
        self.create_company_field = Entry(create_right, textvariable=self.create_company, width=35, bd=0)
        self.create_company_field.place(height=25, width=250, relx=.750, rely=0.250, anchor="center")
        self.create_fields.append(self.create_company_field)

        Label(create_right, text="Status", bg="#DDDDDD", fg="#363636", font=field_label).place(relx=.070, rely=0.350, anchor="center")
        self.create_status_field = Label(create_right, text="Available", width=35, bg="#FFFFFF", fg="#000000")
        self.create_status_field.place(height=25, width=250, relx=.245, rely=0.400, anchor="center")

        Label(create_right, text="Unit Location", bg="#DDDDDD", fg="#363636", font=field_label).place(relx=.605, rely=0.350, anchor="center")
        self.create_location_field = Entry(create_right, textvariable=self.create_location, width=35, bd=0)
        self.create_location_field.place(height=25, width=250, relx=.750, rely=0.400, anchor="center")
        self.create_fields.append(self.create_location_field)

        Label(create_right, text="Price", bg="#DDDDDD", fg="#363636", font=field_label).place(relx=.065, rely=0.500, anchor="center")
        self.create_price_field = Entry(create_right, textvariable=self.create_price, width=35, bd=0)
        self.create_price_field.place(height=25, width=250, relx=.245, rely=0.550, anchor="center")
        self.create_price_field.config(validate="focusout", validatecommand=(self.reg_validDouble, '%P'), invalidcommand=(self.reg_invalidDouble,))
        self.create_fields.append(self.create_price_field)

        Label(create_right, text="Quantity", bg="#DDDDDD", fg="#363636", font=field_label).place(relx=.585, rely=0.500, anchor="center")
        self.create_quantity_field = Entry(create_right, textvariable=self.create_quantity, width=35, bd=0)
        self.create_quantity_field.place(height=25, width=250, relx=.750, rely=0.550, anchor="center")
        self.create_quantity_field.config(validate="focusout", validatecommand=(self.reg_validDouble, '%P'), invalidcommand=(self.reg_invalidDouble,))
        self.create_fields.append(self.create_quantity_field)

        Label(create_right, text="Ownership", bg="#DDDDDD", fg="#363636", font=field_label).place(relx=.090, rely=0.650, anchor="center")
        self.create_owner_field = Entry(create_right, textvariable=self.create_ownership, width=35, bd=0)
        self.create_owner_field.place(height=25, width=250, relx=.245, rely=0.700, anchor="center")
        self.create_fields.append(self.create_owner_field)

        Label(create_right, text="Payment Status", bg="#DDDDDD", fg="#363636", font=field_label).place(relx=.625, rely=0.650, anchor="center")
        self.create_payment_paid = Radiobutton(create_right, text="Paid", bg="#DDDDDD", variable=self.create_payment_status_int, value=1)
        self.create_payment_paid.place(relx=.650, rely=0.700, anchor="center")
        self.create_payment_paid = Radiobutton(create_right, text="Unpaid", bg="#DDDDDD", variable=self.create_payment_status_int, value=2)
        self.create_payment_paid.place(relx=.850, rely=0.700, anchor="center")

        self.create_error_label = Label(create_right, bg="#DDDDDD", fg="#D64000", font=field_label)
        self.create_error_label.place(relx=.5, rely=0.750, anchor="center")


class receiveAsset():
    def __init__(self, root):
        self.database = db.Database()
        self.root = root
        self.receive_receipt_num = StringVar()
        self.receive_asset_name = StringVar()
        self.receive_owner = StringVar()
        self.receive_assets = []

    def displayReceive(self, receive_form_frame, field_label, buttonA, buttonB):
        Label(receive_form_frame, text="Search by Receipt Number", bg="#DDDDDD", fg="#363636", font=field_label).place(relx=.5, rely=0.200, anchor="center")
        Entry(receive_form_frame, textvariable=self.receive_receipt_num, bd=0).place(height=20, width=225, relx=.5, rely=0.250, anchor="center")

        Label(receive_form_frame, text="Search by Asset Name", bg="#DDDDDD", fg="#363636", font=field_label).place(relx=.5, rely=0.325, anchor="center")
        Entry(receive_form_frame, textvariable=self.receive_asset_name, bd=0).place(height=20, width=225, relx=.5, rely=0.375, anchor="center")

        Label(receive_form_frame, text="Search by Owner", bg="#DDDDDD", fg="#363636", font=field_label).place(relx=.5, rely=0.450, anchor="center")
        Entry(receive_form_frame, textvariable=self.receive_owner, bd=0).place(height=20, width=225, relx=.5, rely=0.500, anchor="center")

        filter_btn = Button(receive_form_frame, text="Search", width=13, command=lambda: self.filterTable(), bg="#DC5047", fg="#FFFFFF", bd=0, font=buttonA)
        filter_btn.place(relx=.5, rely=0.600, anchor="center")

        clear_btn = Button(receive_form_frame, text="Clear Filter", width=13, command=lambda: self.filterTable(), bg="#404040", fg="#FFFFFF", bd=0, font=buttonB)
        clear_btn.place(relx=.5, rely=0.665, anchor="center")

    def displayTable(self, receive_table_frame):
        self.receive_canvas = Canvas(receive_table_frame, bg="#191919", width=825, height=500)

        receive_filter = {"receipt_num": "", "recipient": "", "asset_name": "", "owner": "", "location": "", "op_type": "", "in_transit": True}
        receive_measurements = {"cell_width": 150, "cell_height": 75, "rows": self.getContent(receive_filter),
                                "columns": 12}

        self.receive_table = table.Table(receive_measurements, self.receive_canvas, self.receive_table_contents)
        self.receive_table.setScrollbars(receive_table_frame)
        self.receive_table.optionsTable(25, "checkbox")
        self.receive_canvas.configure(scrollregion=self.receive_canvas.bbox("all"))

    def getContent(self, filter_val):
        receive_table_header = ["Receive", "Receipt #", "Operation", "Username", "Photo", "Asset Name",
                                "Recipient", "Company", "Owner", "Location", "Amount", "Payment Status"]
        curr_row = []
        self.receive_table_contents = []
        for column in receive_table_header:
            curr_row.append(column)
        self.receive_table_contents.append(curr_row)

        self.root.table_image = []
        receive = self.database.viewTable(2, filter_val)
        if type(receive) == list:
            for row in range(len(receive)):
                curr_row = []
                for column in range(1, len(receive[row]) - 1):
                    if type(receive[row][column]) == bytes:
                        filepath = self.database.readBLOB(receive[row][5])
                        image = Image.open(filepath)
                        resized_img = image.resize((50, 50), Image.ANTIALIAS)
                        table_image = ImageTk.PhotoImage(resized_img)
                        self.root.table_image.append(table_image)
                        curr_row.append(table_image)
                    elif column < 4 or column > 6:
                        curr_row.append(receive[row][column])
                curr_row.insert(0, [receive[row][0], receive[row][5]])
                self.receive_table_contents.append(curr_row)
            return len(receive) + 1
        return 1

    def filterTable(self):
        self.receive_canvas.delete("all")

        if len(self.receive_receipt_num.get()) > 0 or len(self.receive_asset_name.get()) > 0 or len(self.receive_owner.get()) > 0:
            receive_filter = {"receipt_num": self.receive_receipt_num.get(), "asset_name": self.receive_asset_name.get(),
                              "owner": self.receive_owner.get(), "location": "", "op_type": "", "in_transit": True}
            self.receive_receipt_num.set("")
            self.receive_asset_name.set("")
            self.receive_owner.set("")
        else:
            receive_filter = {"receipt_num": "", "asset_name": "", "owner": "", "location": "", "op_type": "", "in_transit": True}

        self.receive_table.rows = self.getContent(receive_filter)
        self.receive_table.contents = self.receive_table_contents
        self.receive_table.optionsTable(25, "checkbox")
        self.receive_canvas.configure(scrollregion=self.receive_canvas.bbox("all"))

    def checkAssets(self):
        self.receive_assets = self.receive_table.getSelectedCheckbox()
        if len(self.receive_assets) > 0:
            self.receive_canvas.delete("all")

            for keep_asset in range(len(self.receive_table_contents) - 1, -1, -1):
                if self.receive_table_contents[keep_asset][0] not in self.receive_assets and keep_asset != 0:
                    del self.receive_table_contents[keep_asset]
                else:
                    self.receive_table_contents[keep_asset].append(self.receive_table_contents[keep_asset][0])
                    del self.receive_table_contents[keep_asset][0]

            self.receive_table.rows = len(self.receive_table_contents)
            self.receive_table.cols = len(self.receive_table_contents[0]) - 1
            self.receive_table.contents = self.receive_table_contents
            self.receive_table.createTable()
            self.receive_canvas.configure(scrollregion=self.receive_canvas.bbox("all"))
            return True
        return False

    def receiveAssets(self):
        try:
            self.receive_table_contents.pop(0)
            for asset in self.receive_table_contents:
                self.database.receiveAsset(asset[len(asset) - 1][0], asset[len(asset) - 1][1])
            return True
        except:
            return False

    def cancelAssets(self):
        try:
            self.receive_table_contents.pop(0)
            for asset in self.receive_table_contents:
                self.database.delOperation(asset[len(self.receive_table_contents[0]) - 1][0])
            return True
        except:
            return False


class deleteAsset():
    def __init__(self, root):
        self.database = db.Database()
        self.root = root
        self.delete_asset_name = StringVar()
        self.delete_disposed_int = IntVar()
        self.delete_assets = []

    def displayDelete(self, delete_form_frame, field_label, buttonA, buttonB):
        Label(delete_form_frame, text="Filter by Asset Name", bg="#DDDDDD", fg="#363636", font=field_label).place(relx=0.325, rely=0.200, anchor="center")
        Entry(delete_form_frame, textvariable=self.delete_asset_name, bd=0).place(height=20, width=225, relx=.5, rely=0.250, anchor="center")

        Label(delete_form_frame, text="Disposed Filter", bg="#DDDDDD", fg="#363636", font=field_label).place(relx=0.300, rely=0.325, anchor="center")
        delete_disposed_on = Radiobutton(delete_form_frame, text="On", bg="#DDDDDD", variable=self.delete_disposed_int, value=1)
        delete_disposed_on.place(relx=.60, rely=0.325, anchor="center")

        delete_disposed_off = Radiobutton(delete_form_frame, text="Off", bg="#DDDDDD", variable=self.delete_disposed_int, value=2)
        delete_disposed_off.place(relx=.80, rely=0.325, anchor="center")

        filter_btn = Button(delete_form_frame, text="Filter", width=13, command=lambda: self.filterTable(), bg="#DC5047", fg="#FFFFFF", bd=0, font=buttonA)
        filter_btn.place(relx=.5, rely=0.425, anchor="center")

        clear_btn = Button(delete_form_frame, text="Clear Filter", width=13, command=lambda: self.filterTable(), bg="#404040", fg="#FFFFFF", bd=0, font=buttonB)
        clear_btn.place(relx=.5, rely=0.515, anchor="center")

        filter_ins = Label(delete_form_frame, text="Choose Assets to Delete", bg="#DDDDDD", fg="#363636", font=field_label)
        filter_ins.place(relx=.5, rely=0.575, anchor="center")

        current_font = tkfont.Font(filter_ins, filter_ins.cget("font"))
        current_font.configure(weight="bold", slant="italic")
        filter_ins.config(font=current_font)

    def displayTable(self, delete_bg):
        self.delete_bg = delete_bg
        self.delete_table_frame = Frame(delete_bg, bg="#191919", width=825, height=500)
        self.delete_table_frame.place(relx=.625, rely=.5, anchor="center")
        self.delete_canvas = Canvas(self.delete_table_frame, bg="#191919", width=825, height=500)

        delete_filter = {"asset_name": "", "company": "", "owner": "", "location": "", "pay_status": "", "status": ""}
        delete_measurements = {"cell_width": 150, "cell_height": 75, "rows": self.getContent(delete_filter),
                               "columns": 10}
        self.delete_table = table.Table(delete_measurements, self.delete_canvas, self.delete_table_contents)
        self.delete_table.setScrollbars(self.delete_table_frame)
        self.delete_table.optionsTable(23, "checkbox")
        self.delete_canvas.configure(scrollregion=self.delete_canvas.bbox("all"))

    def getContent(self, filter_val):
        delete_table_header = ["Delete?", "Photo", "Asset Name", "Company", "Owner", "Location",
                               "Price", "Amount", "Payment Status", "Status"]
        self.delete_table_contents = []
        curr_row = []
        for column in delete_table_header:
            curr_row.append(column)
        self.delete_table_contents.append(curr_row)

        self.root.table_image = []

        delete = self.database.viewTable(1, filter_val)
        if type(delete) == list:
            for row in range(len(delete)):
                curr_row = []
                for column in range(len(delete[row])):
                    if type(delete[row][column]) == bytes:
                        filepath = self.database.readBLOB(delete[row][0])
                        image = Image.open(filepath)
                        resized_img = image.resize((50, 50), Image.ANTIALIAS)
                        table_image = ImageTk.PhotoImage(resized_img)
                        self.root.table_image.append(table_image)
                        curr_row.insert(1, table_image)
                    else:
                        curr_row.append(delete[row][column])
                self.delete_table_contents.append(curr_row)
            return len(delete) + 1
        return 1

    def filterTable(self):
        self.delete_table_frame.destroy()
        self.delete_table_frame = Frame(self.delete_bg, bg="#191919", width=825, height=500)
        self.delete_table_frame.place(relx=.625, rely=.5, anchor="center")
        self.delete_canvas = Canvas(self.delete_table_frame, bg="#191919", width=825, height=500)

        if len(self.delete_asset_name.get()) > 0 or self.delete_disposed_int.get() > 0:
            status = ""
            if self.delete_disposed_int.get() == 1:
                status = "Disposed"
            delete_filter = {"asset_name": self.delete_asset_name.get(), "company": "", "owner": "",
                             "location": "", "pay_status": "", "status": status}
            self.delete_asset_name.set("")
            self.delete_disposed_int.set(0)
        else:
            delete_filter = {"asset_name": "", "company": "", "owner": "", "location": "", "pay_status": "", "status": ""}

        self.delete_table.canvas = self.delete_canvas
        self.delete_table.rows = self.getContent(delete_filter)
        self.delete_table.contents = self.delete_table_contents
        self.delete_table.setScrollbars(self.delete_table_frame)
        self.delete_table.optionsTable(23, "checkbox")
        self.delete_canvas.configure(scrollregion=self.delete_canvas.bbox("all"))

    def getSelected(self):
        self.delete_assets = self.delete_table.getSelectedCheckbox()
        if len(self.delete_assets) > 0:
            self.delete_canvas.delete("all")

            for keep_asset in range(len(self.delete_table_contents) - 1, -1, -1):
                if self.delete_table_contents[keep_asset][0] not in self.delete_assets and keep_asset != 0:
                    del self.delete_table_contents[keep_asset]
                else:
                    self.delete_table_contents[keep_asset].append(self.delete_table_contents[keep_asset][0])
                    del self.delete_table_contents[keep_asset][0]

            self.delete_table.rows = len(self.delete_table_contents)
            self.delete_table.cols = len(self.delete_table_contents[0]) - 1
            self.delete_table.contents = self.delete_table_contents
            self.delete_table.createTable()
            self.delete_canvas.configure(scrollregion=self.delete_canvas.bbox("all"))
            return True
        return False

    def deleteAssets(self):
        delete_assets = []
        for assets in range(1, len(self.delete_table_contents)):
            delete_assets.append(self.delete_table_contents[assets][len(self.delete_table_contents[assets]) - 1])

        self.database.delAsset(delete_assets)
        return True
