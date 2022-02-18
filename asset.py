from tkinter import *
from PIL import Image, ImageTk
import tkinter.font as tkfont
from tkinter import filedialog
import os, datetime
import table, db


class createAsset():
    def __init__(self, root):
        self.root = root
        self.database = db.Database()

        self.create_name = StringVar()
        self.create_company = StringVar()
        self.create_status = StringVar()
        self.create_location = StringVar()
        self.create_price = StringVar()
        self.create_quantity = StringVar()
        self.create_ownership = StringVar()
        self.create_payment_status = StringVar()
        self.create_payment_status_int = IntVar()
        self.create_photo_filename = ""

        self.create_fields = []
        self.create_all_invalid = False

        self.reg_validDouble = root.register(self.validDouble)
        self.reg_invalidDouble = root.register(self.invalidDouble)

    def displayUploadImage(self, create_left, buttonA, field_label):
        self.create_photo_preview = Canvas(create_left, bg="#FFFFFF", width=250, height=250)
        self.create_photo_preview.place(relx=.5, rely=0.450, anchor="center")
        self.create_photo_text = self.create_photo_preview.create_text((125, 125), text="No Photo Uploaded", font=field_label)

        upload_btn = Button(create_left, text="Upload", width=13, command=lambda: self.uploadImage(), bg="#B3D687",
                            fg="#FFFFFF", bd=0, font=buttonA)
        upload_btn.place(relx=.5, rely=0.725, anchor="center")

    def displayCreate(self, create_right, field_label):
        Label(create_right, text="Asset Name", bg="#DDDDDD", fg="#363636", font=field_label).place(relx=.100,
                                                                                                   rely=0.200,
                                                                                                   anchor="center")
        self.create_name_field = Entry(create_right, textvariable=self.create_name, width=35, bd=0)
        self.create_name_field.place(height=25, width=250, relx=.245, rely=0.250, anchor="center")
        self.create_fields.append(self.create_name_field)

        Label(create_right, text="Company", bg="#DDDDDD", fg="#363636", font=field_label).place(relx=.590, rely=0.200,
                                                                                                anchor="center")
        self.create_company_field = Entry(create_right, textvariable=self.create_company, width=35, bd=0)
        self.create_company_field.place(height=25, width=250, relx=.750, rely=0.250, anchor="center")
        self.create_fields.append(self.create_company_field)

        Label(create_right, text="Status", bg="#DDDDDD", fg="#363636", font=field_label).place(relx=.070, rely=0.350,
                                                                                               anchor="center")
        self.create_status_field = Label(create_right, text="Available", width=35, bg="#FFFFFF", fg="#000000")
        self.create_status_field.place(height=25, width=250, relx=.245, rely=0.400, anchor="center")

        Label(create_right, text="Unit Location", bg="#DDDDDD", fg="#363636", font=field_label).place(relx=.605,
                                                                                                      rely=0.350,
                                                                                                      anchor="center")
        self.create_location_field = Entry(create_right, textvariable=self.create_location, width=35, bd=0)
        self.create_location_field.place(height=25, width=250, relx=.750, rely=0.400, anchor="center")
        self.create_fields.append(self.create_location_field)

        Label(create_right, text="Price", bg="#DDDDDD", fg="#363636", font=field_label).place(relx=.065, rely=0.500,
                                                                                              anchor="center")
        self.create_price_field = Entry(create_right, textvariable=self.create_price, width=35, bd=0)
        self.create_price_field.place(height=25, width=250, relx=.245, rely=0.550, anchor="center")
        self.create_price_field.config(validate="focusout", validatecommand=(self.reg_validDouble, '%P'),
                                       invalidcommand=(self.reg_invalidDouble,))
        self.create_fields.append(self.create_price_field)

        Label(create_right, text="Quantity", bg="#DDDDDD", fg="#363636", font=field_label).place(relx=.585, rely=0.500,
                                                                                                 anchor="center")
        self.create_quantity_field = Entry(create_right, textvariable=self.create_quantity, width=35, bd=0)
        self.create_quantity_field.place(height=25, width=250, relx=.750, rely=0.550, anchor="center")
        self.create_quantity_field.config(validate="focusout", validatecommand=(self.reg_validDouble, '%P'),
                                          invalidcommand=(self.reg_invalidDouble,))
        self.create_fields.append(self.create_quantity_field)

        Label(create_right, text="Ownership", bg="#DDDDDD", fg="#363636", font=field_label).place(relx=.090, rely=0.650,
                                                                                                  anchor="center")
        self.create_owner_field = Entry(create_right, textvariable=self.create_ownership, width=35, bd=0)
        self.create_owner_field.place(height=25, width=250, relx=.245, rely=0.700, anchor="center")
        self.create_fields.append(self.create_owner_field)

        Label(create_right, text="Payment Status", bg="#DDDDDD", fg="#363636", font=field_label).place(relx=.625,
                                                                                                       rely=0.650,
                                                                                                       anchor="center")
        self.create_payment_paid = Radiobutton(create_right, text="Paid", bg="#DDDDDD",
                                               variable=self.create_payment_status_int, value=1)
        self.create_payment_paid.place(relx=.650, rely=0.700, anchor="center")
        self.create_payment_paid = Radiobutton(create_right, text="Unpaid", bg="#DDDDDD",
                                               variable=self.create_payment_status_int, value=2)
        self.create_payment_paid.place(relx=.850, rely=0.700, anchor="center")

        self.create_error_label = Label(create_right, bg="#DDDDDD", fg="#D64000", font=field_label)
        self.create_error_label.place(relx=.5, rely=0.750, anchor="center")

    def validDouble(self, value):
        for i in self.create_fields:
            i.configure(highlightthickness=0, highlightbackground="#D64000", highlightcolor="#D64000")
        self.create_error_label.config(text="")
        try:
            float(value)
            return True
        except :
            return False

    def invalidDouble(self):
        if not self.create_all_invalid:
            for i in self.create_fields:
                i.configure(highlightthickness=0, highlightbackground="#D64000", highlightcolor="#D64000")
            self.create_error_label.config(text="Price and Quantity should be Numbers")
            self.create_price_field.configure(highlightthickness=2, highlightbackground="#D64000", highlightcolor="#D64000")
            self.create_quantity_field.configure(highlightthickness=2, highlightbackground="#D64000", highlightcolor="#D64000")

    def uploadImage(self):
        fileTypes = [('JPG Files', '*.jpg'),
                     ('JPEG Files', '*.jpeg'),
                     ('PNG Files', '*.png')]
        self.create_photo_filename = filedialog.askopenfilename(filetypes=fileTypes)
        if len(self.create_photo_filename) > 0:
            image = Image.open(self.create_photo_filename)
            resized_img = image.resize((250, 250), Image.ANTIALIAS)
            upload_img = ImageTk.PhotoImage(resized_img)
            self.root.create_photo = upload_img

            self.create_photo_preview.create_image(0, 0, image=upload_img, anchor=NW)
            self.create_photo_preview.delete(self.create_photo_text)

    def submitForm(self, username):
        for i in self.create_fields:
            i.configure(highlightthickness=0, highlightbackground="#D64000", highlightcolor="#D64000")
        valid_first = len(self.create_name.get()) > 1 and len(self.create_company.get()) > 1
        valid_second = len(self.create_location.get()) > 1 and len(self.create_ownership.get()) > 1 and self.create_payment_status_int.get() > 0
        valid_third = len(self.create_price.get()) > 0 and len(self.create_quantity.get()) > 0 and len(self.create_photo_filename) > 0
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
            image = self.database.convertToBinaryData(self.create_photo_filename)

            if (str(price)[0] == "0" and str(price).find(".") < 0) or (str(quantity)[0] == "0" and str(quantity).find(".") < 0):
                self.create_error_label.config(text="Price and Quantity should follow the following format: 12.34")
                self.create_price_field.configure(highlightthickness=2, highlightbackground="#D64000", highlightcolor="#D64000")
                self.create_quantity_field.configure(highlightthickness=2, highlightbackground="#D64000", highlightcolor="#D64000")
                return None
            if not self.validDouble(price) or not self.validDouble(quantity):
                self.invalidDouble()
                return None
            if float(price) <= 0 or float(quantity) <= 0:
                self.create_error_label.config(text="Price and Quantity should be Higher than 0.00")
                self.create_price_field.configure(highlightthickness=2, highlightbackground="#D64000", highlightcolor="#D64000")
                self.create_quantity_field.configure(highlightthickness=2, highlightbackground="#D64000", highlightcolor="#D64000")
                return None
            if not image:
                self.create_error_label.config(text="Please Upload A Photo")
                return None

            try:
                currTime = datetime.datetime.now()
                self.database.createAsset("assets", username, name, company, owner, status, unit_loc, float(price), float(quantity), payment_stat, image, currTime)
                return True
            except:
                return False
        else:
            for i in self.create_fields:
                i.configure(highlightthickness=0, highlightbackground="#D64000", highlightcolor="#D64000")

            if not valid_first and not valid_second and not valid_third:
                for i in self.create_fields:
                    i.configure(highlightthickness=2, highlightbackground="#D64000", highlightcolor="#D64000")
                self.create_error_label.config(text="Please Fill Up All Fields")
            elif not valid_first or not valid_second:
                for i in self.create_fields:
                    i.configure(highlightthickness=2, highlightbackground="#D64000", highlightcolor="#D64000")
                self.create_error_label.config(text="Please Fill Up All Fields")
            elif len(self.create_photo_filename) <= 0:
                self.create_error_label.config(text="Please Upload A Photo")
            elif not os.path.isfile(self.create_photo_filename):
                self.create_error_label.config(text="Please Upload A Valid Photo")
            elif len(self.create_price.get()) > 0 and len(self.create_quantity.get()) > 0:
                price = self.create_price.get()
                quantity = self.create_quantity.get()
                invalid_float = False
                if (str(self.create_price.get())[0] == 0 and str(price).find(".") > 0) or (str(quantity)[0] == 0 and str(quantity).find(".") > 0):
                    self.create_error_label.config(text="Price and Quantity follow the following format: 12.34")
                    invalid_float = True
                elif not self.validDouble(price) or not self.validDouble(quantity):
                    self.invalidDouble()
                    invalid_float = True
                elif float(price) <= 0 or float(quantity) <= 0:
                    self.create_error_label.config(text="Price and Quantity should be Higher than 0.00")
                    invalid_float = True
                if invalid_float:
                    self.create_price_field.configure(highlightthickness=2, highlightbackground="#D64000", highlightcolor="#D64000")
                    self.create_quantity_field.configure(highlightthickness=2, highlightbackground="#D64000", highlightcolor="#D64000")

            return None


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


class findAsset():
    def __init__(self, root):

        # Database
        self.database = db.Database()
        self.root = root

        # Search variables
        self.find_asset_name = StringVar()
        self.findAsset_location = StringVar()
        self.findAsset_owner = StringVar()
        self.findAsset_status = StringVar()
        self.findAsset_payment_status_int = IntVar()

        # Receipt Variables
        self.receipt_no_field = Entry() 
        self.receipt_no = IntVar()

        self.recipient_field = Entry()
        self.recipient = StringVar()

        self.operation_field = Entry()
        self.operation = StringVar()

        self.user_field = Entry()
        self.user = StringVar()

        self.location_field = Entry()
        self.location = StringVar()

        self.company_field = Entry()
        self.company = StringVar()

        self.owner_field = Entry()
        self.owner = StringVar()

        self.status_field = Entry()
        self.status = StringVar()

        # Selected Assets
        self.selected_assets_int = IntVar()
        self.find_assets = [] # Array of selected assets
        self.find_assets_rows = [] 
        self.find_assets_cols = []
        self.photo_filepaths = []
        self.photo_id = []
        self.quantity = []

        # New 
        self.new_company = StringVar()
        self.new_owner = StringVar()
        self.new_location = StringVar()

    def displayFind(self, findAsset_form_frame, field_label, buttonA, buttonB):

        Label(findAsset_form_frame, text="Search by Asset Name", bg="#DDDDDD", fg="#363636", font=field_label).place(relx=.5, rely=0.200, anchor="center")
        Entry(findAsset_form_frame, textvariable=self.find_asset_name, bd=0).place(height=20, width=225, relx=.5, rely=0.245, anchor="center")

        Label(findAsset_form_frame, text="Search by Location", bg="#DDDDDD", fg="#363636", font=field_label).place(relx=.5, rely=0.295, anchor="center")
        Entry(findAsset_form_frame, textvariable=self.findAsset_location, bd=0).place(height=20, width=225, relx=.5, rely=0.340, anchor="center")

        Label(findAsset_form_frame, text="Search by Owner", bg="#DDDDDD", fg="#363636", font=field_label).place(relx=.5, rely=0.390, anchor="center")
        Entry(findAsset_form_frame, textvariable=self.findAsset_owner, bd=0).place(height=20, width=225, relx=.5, rely=0.435, anchor="center")

        Label(findAsset_form_frame, text="Filter by Status", bg="#DDDDDD", fg="#363636", font=field_label).place(relx=0.300, rely=0.500, anchor="center")                     
        
        paid_on = Radiobutton(findAsset_form_frame, text="Paid", bg="#DDDDDD", variable=self.findAsset_payment_status_int, value=1)
        paid_on.place(relx=.60, rely=0.500, anchor="center")

        paid_off = Radiobutton(findAsset_form_frame, text="Unpaid", bg="#DDDDDD", variable=self.findAsset_payment_status_int, value=2)
        paid_off.place(relx=.80, rely=0.500, anchor="center")

        filter_btn = Button(findAsset_form_frame, text="Search", width=13, command=lambda: self.filterTable(), bg="#DC5047", fg="#FFFFFF", bd=0, font=buttonA)
        filter_btn.place(relx=.5, rely=0.625, anchor="center")

        clear_btn = Button(findAsset_form_frame, text="Clear Filter", width=13, command=lambda: self.filterTable(), bg="#404040", fg="#FFFFFF", bd=0, font=buttonB)
        clear_btn.place(relx=.5, rely=0.725, anchor="center")

    def displayTable(self, findAsset_bg):
        self.findAsset_bg = findAsset_bg
        self.findAsset_table_frame = Frame(findAsset_bg, bg="#191919", width=825, height=500)
        self.findAsset_table_frame.place(relx=.625, rely=.5, anchor="center")
        self.findAsset_canvas = Canvas(self.findAsset_table_frame, bg="#191919", width=825, height=500)

        findAsset_filter = {"asset_name": "", "company": "", "owner": "", "location": "", "pay_status": "", "status": ""}
        findAsset_measurements = {"cell_width": 150, "cell_height": 75, "rows": self.getContent(findAsset_filter),
                               "columns": 10}

        self.findAsset_table = table.Table(findAsset_measurements, self.findAsset_canvas, self.findAsset_table_contents)
        self.findAsset_table.setScrollbars(self.findAsset_table_frame)
        self.findAsset_table.optionsTable(23, "checkbox")
        self.findAsset_canvas.configure(scrollregion=self.findAsset_canvas.bbox("all"))

    def getContent(self, filter_val):

        findAsset_table_header = ["Select", "Photo", "Asset Name", "Company", "Owner", "Location",
                               "Price", "Quantity", "Payment Status", "Availability"]
        self.findAsset_table_contents = []
        curr_row = []
        for column in findAsset_table_header:
            curr_row.append(column)
        self.findAsset_table_contents.append(curr_row)

        self.root.table_image = []

        findAsset = self.database.viewTable(1, filter_val)
        if type(findAsset) == list:
            for row in range(len(findAsset)):
                curr_row = []
                for column in range(len(findAsset[row])):
                    if type(findAsset[row][column]) == bytes:
                        filepath = self.database.readBLOB(findAsset[row][0])
                        image = Image.open(filepath)
                        resized_img = image.resize((50, 50), Image.ANTIALIAS)
                        table_image = ImageTk.PhotoImage(resized_img)
                        self.root.table_image.append(table_image)
                        curr_row.insert(1, table_image)

                        self.photo_filepaths.append(filepath)

                    else:
                        curr_row.append(findAsset[row][column])
                self.findAsset_table_contents.append(curr_row)
            return len(findAsset) + 1
        return 1

    def filterTable(self):
        self.findAsset_table_frame.destroy()
        self.findAsset_table_frame = Frame(self.findAsset_bg, bg="#191919", width=825, height=500)
        self.findAsset_table_frame.place(relx=.625, rely=.5, anchor="center")
        self.findAsset_canvas = Canvas(self.findAsset_table_frame, bg="#191919", width=825, height=500)

        if len(self.find_asset_name.get()) > 0 or len(self.findAsset_owner.get()) > 0 or len(self.findAsset_location.get()) > 0 or self.findAsset_payment_status_int.get() > 0:
            
            status = ""

            if self.findAsset_payment_status_int.get() == 1:
                status = "Paid"
            elif self.findAsset_payment_status_int.get() == 2:
                status = "Unpaid"            
            else:
                status = ""

            findAsset_filter = {"asset_name": self.find_asset_name.get(), "company": "", "owner": self.findAsset_owner.get(),
                             "location": self.findAsset_location.get(), "pay_status": status, "status": ""}
            self.find_asset_name.set("")
            self.findAsset_owner.set("")
            self.findAsset_location.set("")
            self.findAsset_payment_status_int.set(0)
        else:
            findAsset_filter = {"asset_name": "", "company": "", "owner": "", "location": "", "pay_status": "", "status": ""}

        self.findAsset_table.canvas = self.findAsset_canvas
        self.findAsset_table.rows = self.getContent(findAsset_filter)
        self.findAsset_table.contents = self.findAsset_table_contents
        self.findAsset_table.setScrollbars(self.findAsset_table_frame)
        self.findAsset_table.optionsTable(23, "checkbox")
        self.findAsset_canvas.configure(scrollregion=self.findAsset_canvas.bbox("all"))
 
    def getSelected(self):
        self.find_assets = self.findAsset_table.getSelectedCheckbox()
        self.photo_id = self.find_assets

        if len(self.find_assets) > 0:
            self.findAsset_canvas.delete("all")

            for keep_asset in range(len(self.findAsset_table_contents) - 1, -1, -1):
                if self.findAsset_table_contents[keep_asset][0] not in self.find_assets and keep_asset != 0:
                    del self.findAsset_table_contents[keep_asset]
                else:
                    self.findAsset_table_contents[keep_asset].append(self.findAsset_table_contents[keep_asset][0])

            self.findAsset_table.rows = len(self.findAsset_table_contents)
            self.findAsset_table.cols = len(self.findAsset_table_contents[0]) - 1
            self.findAsset_table.contents = self.findAsset_table_contents

            self.find_assets = self.findAsset_table.contents
            self.find_assets_rows = self.findAsset_table.rows
            self.find_assets_cols = self.findAsset_table.cols  

            self.findAsset_table.optionsTable(23, "quantity")
            self.findAsset_canvas.configure(scrollregion=self.findAsset_canvas.bbox("all"))

            return True
           
        return False

    def displayReceipt(self, receipt_bg, field_label):

        # Editable
        Label(receipt_bg, text="Enter Receipt Number", bg="#DDDDDD", fg="#363636", font=field_label).place(relx=.040, rely=0.250,
                                                                                               anchor="w")
        self.receipt_no_field = Entry(receipt_bg, textvariable=self.receipt_no, width=25, bd=0)
        self.receipt_no_field.delete(0, 'end')
        self.receipt_no_field.place(height=25, width=200, relx=.25, rely=0.300, anchor="center")

        Label(receipt_bg, text="Enter Recipient", bg="#DDDDDD", fg="#363636", font=field_label).place(relx=.540, rely=0.250,
                                                                                               anchor="w")
        self.recipient_field = Entry(receipt_bg, textvariable=self.recipient, width=25, bd=0)
        self.recipient_field.delete(0, 'end')
        self.recipient_field.place(height=25, width=200, relx=.745, rely=0.300, anchor="center")

        Label(receipt_bg, text="Operation", bg="#DDDDDD", fg="#363636", font=field_label).place(relx=.040, rely=0.375,
                                                                                               anchor="w")
        self.operation_field = Entry(receipt_bg, textvariable=self.operation, width=25, bd=0)
        self.operation_field.delete(0, 'end')
        self.operation_field.insert(0, self.operation)
        self.operation_field.config(state='disabled')
        self.operation_field.place(height=25, width=200, relx=.25, rely=0.425, anchor="center")

        Label(receipt_bg, text="Noted By", bg="#DDDDDD", fg="#363636", font=field_label).place(relx=.040, rely=0.500,
                                                                                               anchor="w")
        self.user_field = Entry(receipt_bg, textvariable=self.user, width=25, bd=0)
        self.user_field.delete(0, 'end')
        self.user_field.insert(0, self.user)
        self.user_field.config(state='disabled')
        self.user_field.place(height=25, width=200, relx=.25, rely=0.550, anchor="center")

        Label(receipt_bg, text="Status", bg="#DDDDDD", fg="#363636", font=field_label).place(relx=.040, rely=0.625,
                                                                                               anchor="w")
        self.status_field = Entry(receipt_bg, textvariable=self.status, width=25, bd=0)
        self.status_field.delete(0, 'end')
        self.status_field.insert(0, self.status)
        self.status_field.config(state='disabled')
        self.status_field.place(height=25, width=200, relx=.25, rely=0.675, anchor="center")

        ## EDITABLE
        Label(receipt_bg, text="New Location", bg="#DDDDDD", fg="#363636", font=field_label).place(relx=.540, rely=0.625,
                                                                                               anchor="w")
        self.location_field = Entry(receipt_bg, textvariable=self.new_location, width=25, bd=0)
        self.location_field.delete(0, 'end')
        #self.location_field.insert(0, self.location)
        self.location_field.place(height=25, width=200, relx=.745, rely=0.675, anchor="center")

        Label(receipt_bg, text="New Company", bg="#DDDDDD", fg="#363636", font=field_label).place(relx=.540, rely=0.375,
                                                                                               anchor="w")
        self.company_field = Entry(receipt_bg, textvariable=self.new_company, width=25, bd=0)
        self.company_field.delete(0, 'end')
        #self.company_field.insert(0, self.company)
        self.company_field.place(height=25, width=200, relx=.745, rely=0.425, anchor="center")

        Label(receipt_bg, text="New Owner", bg="#DDDDDD", fg="#363636", font=field_label).place(relx=.540, rely=0.500,
                                                                                               anchor="w")
        self.owner_field = Entry(receipt_bg, textvariable=self.new_owner, width=25, bd=0)
        self.owner_field.delete(0, 'end')
        #self.owner_field.insert(0, self.owner)
        self.owner_field.place(height=25, width=200, relx=.745, rely=0.550, anchor="center")

        self.receipt_error_label = Label(receipt_bg, bg="#DDDDDD", fg="#D64000", font=field_label)
        self.receipt_error_label.place(relx=.5, rely=0.730, anchor="center")

    def setOperation(self, op_no, user):

        self.quantity = self.findAsset_table.getQuantity()
        for x in range(len(self.quantity)):
            if self.quantity[x] > self.findAsset_table.contents[x+1][7]:
                return False
        
        if op_no == 1:
            self.operation = "Move"
            self.status = "In Transit - Move"
        elif op_no == 2: 
            self.operation = "Lend"
            self.status = "In Transit - Lent"
        elif op_no == 3:
            self.operation = "Store"
            self.status = "In Transit - Stored"
        elif op_no == 4:
            self.operation = "Sell"
            self.status = "In Transit - Sold"
        elif op_no == 5:
            self.operation = "Dispose"
            self.status = "In Transit - Disposed"
        else: 
            self.operation = ""

        self.user = user

        return True
        
    def assetOperationSuccess(self):
        ## TODO: Place checkers if receipt values are valid
        if self.receipt_no.get() >= 0 and not self.database.checkReceiptNo(self.receipt_no.get()):
            if len(self.new_location.get()) > 0 and len(self.new_company.get()) > 0 and len(self.new_owner.get()) > 0 and len(self.recipient.get()):
                self.location = self.new_location.get()
                self.owner = self.new_owner.get()
                self.company = self.new_company.get()
                self.receipt_no = self.receipt_no.get()
                self.recipient = self.recipient.get()
                return True
            else:
                self.receipt_error_label.config(text="Please Fill Up All Fields")
        else:
            self.receipt_error_label.config(text="Please Use Another Receipt Number")

    def displaySummaryDetails(self, summary_bg, summary_form_frame, field_label):

        Label(summary_form_frame, text="Receipt Number", bg="#DDDDDD", fg="#363636", font=field_label).place(relx=.5, rely=0.175, anchor="center")
        Label(summary_form_frame, text=self.receipt_no, bd=0, state='disabled').place(height=20, width=225, relx=.5, rely=0.210, anchor="center")

        Label(summary_form_frame, text="Recipient", bg="#DDDDDD", fg="#363636", font=field_label).place(relx=.5, rely=0.260, anchor="center")
        Label(summary_form_frame, text=self.recipient, bd=0, state='disabled').place(height=20, width=225, relx=.5, rely=0.295, anchor="center")

        Label(summary_form_frame, text="Noted by", bg="#DDDDDD", fg="#363636", font=field_label).place(relx=.5, rely=0.345, anchor="center")
        Label(summary_form_frame, text=self.user, bd=0, state='disabled').place(height=20, width=225, relx=.5, rely=0.380, anchor="center")

        Label(summary_form_frame, text="New Location", bg="#DDDDDD", fg="#363636", font=field_label).place(relx=.5, rely=0.430, anchor="center")
        Label(summary_form_frame, text=self.location, bd=0, state='disabled').place(height=20, width=225, relx=.5, rely=0.465, anchor="center")

        Label(summary_form_frame, text="Payment Status", bg="#DDDDDD", fg="#363636", font=field_label).place(relx=.5, rely=0.515, anchor="center")
        Label(summary_form_frame, textv=self.status, bd=0, state='disabled').place(height=20, width=225, relx=.5, rely=0.550, anchor="center")

        Label(summary_form_frame, text="New Company", bg="#DDDDDD", fg="#363636", font=field_label).place(relx=.5, rely=0.600, anchor="center")
        Label(summary_form_frame, text=self.company, bd=0, state='disabled').place(height=20, width=225, relx=.5, rely=0.635, anchor="center")

        Label(summary_form_frame, text="New Owner", bg="#DDDDDD", fg="#363636", font=field_label).place(relx=.5, rely=0.685, anchor="center")
        Label(summary_form_frame, text=self.owner, bd=0, state='disabled').place(height=20, width=225, relx=.5, rely=0.720, anchor="center")

        return True 

    def displaySummaryAssets(self, summary_bg):

        self.summary_bg = summary_bg
        self.summary_table_frame = Frame(summary_bg, bg="#191919", width=825, height=500)
        self.summary_table_frame.place(relx=.625, rely=.5, anchor="center")

        self.summary_canvas = Canvas(self.summary_table_frame, bg="#191919", width=825, height=500)

        summary_measurements = {"cell_width": 150, "cell_height": 75, "rows": self.find_assets_rows,
                               "columns": 10}

        self.find_assets[0][0] = "Quantity"
        for x in range(len(self.find_assets)-1):
            self.find_assets[x+1][0] = self.quantity[x]

        self.summary_table = table.Table(summary_measurements, self.summary_canvas, self.find_assets)
        self.summary_table.setScrollbars(self.summary_table_frame)
        self.summary_canvas.configure(scrollregion=self.summary_canvas.bbox("all"))

        self.summary_table.createTable()

        return True


    def operationSuccess(self):
       
        find_filepath = []

        for y in range(len(self.photo_id)):
            find_filepath.append("asset_"+str(self.photo_id[y]))
        index = 0
        image_filepath = []

        for z in range(len(self.photo_filepaths)):
            if self.photo_filepaths[z].find(find_filepath[index]) != -1:
                image_filepath.append(self.photo_filepaths[z])
                index = index+1

            if index == len(find_filepath):
                break

        del self.find_assets[0]

        op = self.operation
        self.operation = "In Transit - " + self.operation

        currTime = datetime.datetime.now()

        for x in range(len(self.find_assets)):

            asset_id = self.find_assets[x][10]
            image = image_filepath[x]  
            quantity = self.quantity[x]

            ## Check quantity
            if quantity < self.find_assets[x][7]:
                remaining = self.find_assets[x][7]-quantity
                img = self.database.convertToBinaryData(image)

                self.database.duplicateAsset("assets", self.find_assets[x][2], self.find_assets[x][3], self.find_assets[x][4], self.find_assets[x][9], self.find_assets[x][5], self.find_assets[x][6], remaining, self.find_assets[x][8], img, currTime)

                update_query = "UPDATE assets SET company = '" + self.company + "', owner = '" + self.owner\
                                                                + "', unit_loc = '" + self.location + "', amount = '" + str(quantity) + "', status = '" + self.operation\
                                                                + "' WHERE id = " + str(asset_id)
                self.database.updateAsset(update_query)

            else:
                update_query = "UPDATE assets SET company = '" + self.company + "', owner = '" + self.owner\
                                                                + "', unit_loc = '" + self.location + "', status = '" + self.operation\
                                                                + "' WHERE id = " + str(asset_id)
                self.database.updateAsset(update_query)

            self.database.createReceipt(self.receipt_no, op, self.user, "Authorized", asset_id, self.find_assets[x][2], self.recipient, self.company, self.owner, self.location, quantity, self.find_assets[x][8], image, "Unapproved")

        return False

class updateAsset():
    def __init__(self, root):
        self.database = db.Database()
        self.root = root

        # Update variables
        self.update_photo_filename = ""
        self.update_photo = ""
        self.asset_no = IntVar()
        self.update_name = StringVar()
        self.update_company = StringVar()
        self.update_status = StringVar()
        self.update_location = StringVar()
        self.update_price = DoubleVar()
        self.update_quantity = DoubleVar()
        self.update_ownership = StringVar()
        self.update_payment_status = StringVar()
        self.update_payment_status_int = IntVar()

        # New updated variables
        self.new_name = StringVar()
        self.new_company = StringVar()
        self.new_location = StringVar()
        self.new_price = DoubleVar()
        self.new_quantity = DoubleVar()
        self.new_ownership = StringVar()
        self.new_payment_status = StringVar()
        self.new_payment_status_int = IntVar()

        self.new_photo_filename = ""
        self.new_photo = ""

        # Update entry fields
        self.update_name_field = Entry()
        self.update_company_field = Entry()
        self.update_status_field = Entry()
        self.update_location_field = Entry()
        self.update_price_field = Entry()
        self.update_quantity_field = Entry()
        self.update_owner_field = Entry()
        self.update_payment_field = Radiobutton()

        self.update_fields = []
        self.update_error_label = Label()
        self.update_all_invalid = False

        self.selected_asset = -1

        # Receipt fields
        self.op_type = "Update"

        self.receipt_no_field = Entry() 
        self.receipt_no = IntVar()

        self.operation_field = Entry()
        self.operation = StringVar()

        self.user_field = Entry()
        self.user = StringVar()

        self.location_field = Entry()
        self.location = StringVar()

        self.company_field = Entry()
        self.company = StringVar()

        self.owner_field = Entry()
        self.owner = StringVar()

        self.status_field = Entry()
        self.status = StringVar()

        self.reg_validDouble = root.register(self.validDouble)
        self.reg_invalidDouble = root.register(self.invalidDouble)

        self.asset_index = 0

    def validDouble(self, value):
        for i in self.update_fields:
            i.configure(highlightthickness=0, highlightbackground="#D64000", highlightcolor="#D64000")
        self.update_error_label.config(text="")
        try:
            float(value)
            self.update_button.config(state=NORMAL)
            return True
        except :
            return False

    def invalidDouble(self):
        self.update_button.config(state=DISABLED)
        if not self.update_all_invalid:
            for i in self.find_fields:
                i.configure(highlightthickness=0, highlightbackground="#D64000", highlightcolor="#D64000")
            self.update_error_label.config(text="Price and Quantity should be Numbers")
            self.update_price_field.configure(highlightthickness=2, highlightbackground="#D64000", highlightcolor="#D64000")
            self.update_quantity_field.configure(highlightthickness=2, highlightbackground="#D64000", highlightcolor="#D64000")

    def displayFind(self, update_form_frame, field_label, buttonA, buttonB):

        Label(update_form_frame, text="Search by Asset Name", bg="#DDDDDD", fg="#363636", font=field_label).place(relx=.5, rely=0.200, anchor="center")
        Entry(update_form_frame, textvariable=self.update_name, bd=0).place(height=20, width=225, relx=.5, rely=0.245, anchor="center")

        Label(update_form_frame, text="Search by Location", bg="#DDDDDD", fg="#363636", font=field_label).place(relx=.5, rely=0.295, anchor="center")
        Entry(update_form_frame, textvariable=self.update_location, bd=0).place(height=20, width=225, relx=.5, rely=0.340, anchor="center")

        Label(update_form_frame, text="Search by Owner", bg="#DDDDDD", fg="#363636", font=field_label).place(relx=.5, rely=0.390, anchor="center")
        Entry(update_form_frame, textvariable=self.update_ownership, bd=0).place(height=20, width=225, relx=.5, rely=0.435, anchor="center")

        Label(update_form_frame, text="Filter by Status", bg="#DDDDDD", fg="#363636", font=field_label).place(relx=0.300, rely=0.500, anchor="center")                     
        
        paid_on = Radiobutton(update_form_frame, text="Paid", bg="#DDDDDD", variable=self.update_payment_status_int, value=1)
        paid_on.place(relx=.60, rely=0.500, anchor="center")

        paid_off = Radiobutton(update_form_frame, text="Unpaid", bg="#DDDDDD", variable=self.update_payment_status_int, value=2)
        paid_off.place(relx=.80, rely=0.500, anchor="center")


        filter_btn = Button(update_form_frame, text="Search", width=13, command=lambda: self.filterTable(), bg="#DC5047", fg="#FFFFFF", bd=0, font=buttonA)
        filter_btn.place(relx=.5, rely=0.625, anchor="center")

        clear_btn = Button(update_form_frame, text="Clear Filter", width=13, command=lambda: self.filterTable(), bg="#404040", fg="#FFFFFF", bd=0, font=buttonB)
        clear_btn.place(relx=.5, rely=0.725, anchor="center")

    def displayTable(self, update_bg):
        self.update_bg = update_bg
        self.update_table_frame = Frame(update_bg, bg="#191919", width=825, height=500)
        self.update_table_frame.place(relx=.625, rely=.5, anchor="center")
        self.update_canvas = Canvas(self.update_table_frame, bg="#191919", width=825, height=500)

        update_filter = {"asset_name": "", "company": "", "owner": "", "location": "", "pay_status": "", "status": ""}
        update_measurements = {"cell_width": 150, "cell_height": 75, "rows": self.getContent(update_filter),
                               "columns": 10}

        self.update_table = table.Table(update_measurements, self.update_canvas, self.update_table_contents)
        self.update_table.setScrollbars(self.update_table_frame)
        self.update_table.optionsTable(23, "radio")
        self.update_canvas.configure(scrollregion=self.update_canvas.bbox("all"))

    def getContent(self, filter_val):
        update_table_header = ["Select", "Photo", "Asset Name", "Company", "Owner", "Location",
                               "Price", "Quantity", "Payment Status", "Status"]
        self.update_table_contents = []
        curr_row = []
        for column in update_table_header:
            curr_row.append(column)
        self.update_table_contents.append(curr_row)

        self.root.table_image = []

        update = self.database.viewTable(1, filter_val)
        if type(update) == list:
            for row in range(len(update)):
                curr_row = []
                for column in range(len(update[row])):
                    if type(update[row][column]) == bytes:
                        filepath = self.database.readBLOB(update[row][0])
                        image = Image.open(filepath)
                        resized_img = image.resize((50, 50), Image.ANTIALIAS)
                        table_image = ImageTk.PhotoImage(resized_img)
                        self.root.table_image.append(table_image)
                        curr_row.insert(1, table_image)
                    else:
                        curr_row.append(update[row][column])
                self.update_table_contents.append(curr_row)
            return len(update) + 1
        return 1

    def filterTable(self):
        self.update_table_frame.destroy()
        self.update_table_frame = Frame(self.update_bg, bg="#191919", width=825, height=500)
        self.update_table_frame.place(relx=.625, rely=.5, anchor="center")
        self.update_canvas = Canvas(self.update_table_frame, bg="#191919", width=825, height=500)

        if len(self.update_name.get()) > 0 or len(self.update_ownership.get()) > 0 or len(self.update_location.get()) > 0 or self.update_payment_status_int.get() > 0:
            
            status = ""

            if self.update_payment_status_int.get() == 1:
                status = "Paid"
            elif self.update_payment_status_int.get() == 2:
                status = "Unpaid"            
            else:
                status = ""         

            update_filter = {"asset_name": self.update_name.get(), "company": "", "owner": self.update_ownership.get(),
                             "location": self.update_location.get(), "pay_status": status, "status": ""}
            self.update_name.set("")
            self.update_ownership.set("")
            self.update_location.set("")
            self.update_payment_status_int.set(0)
        else:
            update_filter = {"asset_name": "", "company": "", "owner": "", "location": "", "pay_status": "", "status": ""}

        self.update_table.canvas = self.update_canvas
        self.update_table.rows = self.getContent(update_filter)
        self.update_table.contents = self.update_table_contents
        self.update_table.setScrollbars(self.update_table_frame)
        self.update_table.optionsTable(23, "radio")
        self.update_canvas.configure(scrollregion=self.update_canvas.bbox("all"))
        
    def getSelected(self):
        self.selected_asset = self.update_table.getSelectedRadio()

        if self.selected_asset > -1:
            
            for keep_asset in range(len(self.update_table_contents)):
                if self.selected_asset == self.update_table_contents[keep_asset][0]:
                    self.update_contents = self.update_table_contents[keep_asset]
                    self.asset_index = keep_asset-1
            
            self.asset_no = self.update_contents[0]
            self.update_name = self.update_contents[2]
            self.update_company = self.update_contents[3]
            self.update_ownership = self.update_contents[4]
            self.update_location = self.update_contents[5]
            self.update_price = self.update_contents[6]
            self.update_quantity = self.update_contents[7]
            self.update_payment_status = self.update_contents[8]
            self.update_status = self.update_contents[9]

            return True
        return False

    def setButton(self, update_button):
        self.update_button = update_button
        self.update_button.config(state=NORMAL)

    def displayUploadedImage(self, update_left, buttonA, field_label):

        self.update_photo_preview = Canvas(update_left, bg="#FFFFFF", width=250, height=250)
        self.update_photo_preview.place(relx=.5, rely=0.450, anchor="center")
        self.update_photo_text = self.update_photo_preview.create_text((125, 125), text="No Photo Uploaded", font=field_label)

        filter_val = {"asset_name": "", "company": "", "owner": "", "location": "", "pay_status": "", "status": ""}
        update = self.database.viewTable(1, filter_val)
        filepath = self.database.readBLOB(update[self.asset_index][0])

        self.update_photo_filename = filepath

        image_set = Image.open(filepath)
        resized_img = image_set.resize((250, 250), Image.ANTIALIAS)
        upload_img = ImageTk.PhotoImage(resized_img)
        
        self.root.update_photo = upload_img

        self.update_photo_preview.create_image(0, 0, image=upload_img, anchor=NW)
        self.update_photo_preview.delete(self.update_photo_text)

        upload_btn = Button(update_left, text="Upload", width=13, command=lambda: self.uploadImage(), bg="#B3D687",
                            fg="#FFFFFF", bd=0, font=buttonA)
        upload_btn.place(relx=.5, rely=0.725, anchor="center")

    def displayDetails(self, update_right, field_label):
        
        Label(update_right, text="Asset Name", bg="#DDDDDD", fg="#363636", font=field_label).place(relx=.100,
                                                                                                   rely=0.200,
                                                                                                   anchor="center")
        self.update_name_field = Entry(update_right, textvariable=self.new_name, width=35, bd=0)
        self.update_name_field.delete(0, 'end')
        self.update_name_field.insert(0, self.update_name)
        self.update_name_field.place(height=25, width=250, relx=.245, rely=0.250, anchor="center")
        self.update_fields.append(self.update_name_field)

        Label(update_right, text="Company", bg="#DDDDDD", fg="#363636", font=field_label).place(relx=.590, rely=0.200,
                                                                                                anchor="center")
        self.update_company_field = Entry(update_right, textvariable=self.new_company, width=35, bd=0)
        self.update_company_field.delete(0, 'end')
        self.update_company_field.insert(0, self.update_company)
        self.update_company_field.place(height=25, width=250, relx=.750, rely=0.250, anchor="center")
        self.update_fields.append(self.update_company_field)

        Label(update_right, text="Status", bg="#DDDDDD", fg="#363636", font=field_label).place(relx=.070, rely=0.350,
                                                                                               anchor="center")
        self.update_status_field = Label(update_right, text=self.update_status, width=35, bg="#FFFFFF", fg="#000000")
        self.update_status_field.place(height=25, width=250, relx=.245, rely=0.400, anchor="center")

        Label(update_right, text="Unit Location", bg="#DDDDDD", fg="#363636", font=field_label).place(relx=.605,
                                                                                                      rely=0.350,
                                                                                                      anchor="center")
        self.update_location_field = Entry(update_right, textvariable=self.new_location, width=35, bd=0)
        self.update_location_field.delete(0, 'end')
        self.update_location_field.insert(0, self.update_location)
        self.update_location_field.place(height=25, width=250, relx=.750, rely=0.400, anchor="center")
        self.update_fields.append(self.update_location_field)

        Label(update_right, text="Price", bg="#DDDDDD", fg="#363636", font=field_label).place(relx=.065, rely=0.500,
                                                                                              anchor="center")
        self.update_price_field = Entry(update_right, textvariable=self.new_price, width=35, bd=0)
        self.update_price_field.delete(0, 'end')
        self.update_price_field.insert(0, self.update_price)
        self.update_price_field.place(height=25, width=250, relx=.245, rely=0.550, anchor="center")
        self.update_price_field.config(validate="focusout", validatecommand=(self.reg_validDouble, '%P'),
                                       invalidcommand=(self.reg_invalidDouble,))
        self.update_fields.append(self.update_price_field)

        Label(update_right, text="Quantity", bg="#DDDDDD", fg="#363636", font=field_label).place(relx=.585, rely=0.500,
                                                                                                 anchor="center")
        self.update_quantity_field = Entry(update_right, textvariable=self.new_quantity, width=35, bd=0)
        self.update_quantity_field.delete(0, 'end')
        self.update_quantity_field.insert(0, self.update_quantity)
        self.update_quantity_field.place(height=25, width=250, relx=.750, rely=0.550, anchor="center")
        self.update_quantity_field.config(validate="focusout", validatecommand=(self.reg_validDouble, '%P'),
                                          invalidcommand=(self.reg_invalidDouble,))
        self.update_fields.append(self.update_quantity_field)

        Label(update_right, text="Ownership", bg="#DDDDDD", fg="#363636", font=field_label).place(relx=.090, rely=0.650,
                                                                                                  anchor="center")
        self.update_owner_field = Entry(update_right, textvariable=self.new_ownership, width=35, bd=0)
        self.update_owner_field.delete(0, 'end')
        self.update_owner_field.insert(0, self.update_ownership)
        self.update_owner_field.place(height=25, width=250, relx=.245, rely=0.700, anchor="center")
        self.update_fields.append(self.update_owner_field)

        Label(update_right, text="Payment Status", bg="#DDDDDD", fg="#363636", font=field_label).place(relx=.625,
                                                                                                       rely=0.650,
                                                                                                       anchor="center")
        self.update_payment_paid = Radiobutton(update_right, text="Paid", bg="#DDDDDD",
                                               variable=self.new_payment_status_int, value=1)
        self.update_payment_paid.place(relx=.650, rely=0.700, anchor="center")
        self.update_payment_unpaid = Radiobutton(update_right, text="Unpaid", bg="#DDDDDD",
                                               variable=self.new_payment_status_int, value=2)
        self.update_payment_unpaid.place(relx=.850, rely=0.700, anchor="center")

        self.update_error_label = Label(update_right, bg="#DDDDDD", fg="#D64000", font=field_label)
        self.update_error_label.place(relx=.5, rely=0.750, anchor="center")

    def uploadImage(self):

        fileTypes = [('JPG Files', '*.jpg'),
                     ('JPEG Files', '*.jpeg'),
                     ('PNG Files', '*.png')]
        self.update_photo_filename = filedialog.askopenfilename(filetypes=fileTypes)

        if len(self.update_photo_filename) > 0:
            image = Image.open(self.update_photo_filename)
            resized_img = image.resize((250, 250), Image.ANTIALIAS)
            upload_img = ImageTk.PhotoImage(resized_img)
            self.root.update_photo = upload_img

            self.update_photo_preview.create_image(0, 0, image=upload_img, anchor=NW)
            self.update_photo_preview.delete(self.update_photo_text)

    def checkForm(self, username):
        valid_first = len(self.new_name.get()) > 1 and len(self.new_company.get()) > 1
        valid_second = len(self.new_location.get()) > 1 and len(self.new_ownership.get()) > 1 and len(self.update_photo_filename) > 0
        valid_third = self.new_price.get() > 0 and self.new_quantity.get() > 0 and self.new_payment_status_int.get() > 0

        # Check validity

        if valid_first and valid_second and valid_third:

            self.operation = "Update"
            self.user = username

            self.update_name = self.new_name.get()
            self.update_company = self.new_company.get()
            self.update_location = self.new_location.get()
            self.update_price = self.new_price.get()
            self.update_quantity = self.new_quantity.get()
            self.update_ownership = self.new_ownership.get()


            if self.new_payment_status_int.get() == 1:
                self.update_payment_status = "Paid"
            else:
                self.update_payment_status = "Unpaid"

            return True
        else:
            if self.update_price <= 0 or self.update_quantity <= 0:
                for i in self.update_fields:
                    i.configure(highlightthickness=0, highlightbackground="#D64000", highlightcolor="#D64000")
                self.update_error_label.config(text="Price and Quantity should be Higher than 0.00")
                self.update_price_field.configure(highlightthickness=2, highlightbackground="#D64000", highlightcolor="#D64000")
                self.update_quantity_field.configure(highlightthickness=2, highlightbackground="#D64000", highlightcolor="#D64000")
            else:
                for i in self.update_fields:
                    i.configure(highlightthickness=2, highlightbackground="#D64000", highlightcolor="#D64000")
                self.update_error_label.config(text="Please Fill Up All Fields")
            return False

    def displayReceipt(self, receipt_bg, field_label):

        Label(receipt_bg, text="Enter Receipt Number", bg="#DDDDDD", fg="#363636", font=field_label).place(relx=.5, rely=0.250,
                                                                                               anchor="center")
        self.receipt_no_field = Entry(receipt_bg, textvariable=self.receipt_no, width=25, bd=0)
        self.receipt_no_field.place(height=25, width=200, relx=.5, rely=0.300, anchor="center")

        Label(receipt_bg, text="Operation", bg="#DDDDDD", fg="#363636", font=field_label).place(relx=.040, rely=0.375,
                                                                                               anchor="w")
        self.operation_field = Entry(receipt_bg, textvariable=self.operation, width=25, bd=0)
        self.operation_field.delete(0, 'end')
        self.operation_field.insert(0, self.operation)
        self.operation_field.config(state='disabled')
        self.operation_field.place(height=25, width=200, relx=.25, rely=0.425, anchor="center")

        Label(receipt_bg, text="Noted By", bg="#DDDDDD", fg="#363636", font=field_label).place(relx=.040, rely=0.500,
                                                                                               anchor="w")
        self.user_field = Entry(receipt_bg, textvariable=self.user, width=25, bd=0)
        self.user_field.delete(0, 'end')
        self.user_field.insert(0, self.user)
        self.user_field.config(state='disabled')
        self.user_field.place(height=25, width=200, relx=.25, rely=0.550, anchor="center")

        Label(receipt_bg, text="Location", bg="#DDDDDD", fg="#363636", font=field_label).place(relx=.040, rely=0.625,
                                                                                               anchor="w")
        self.location_field = Entry(receipt_bg, textvariable=self.update_location, width=25, bd=0)
        self.location_field.delete(0, 'end')
        self.location_field.insert(0, self.update_location)
        self.location_field.config(state='disabled')
        self.location_field.place(height=25, width=200, relx=.25, rely=0.675, anchor="center")

        Label(receipt_bg, text="Company", bg="#DDDDDD", fg="#363636", font=field_label).place(relx=.540, rely=0.375,
                                                                                               anchor="w")
        self.company_field = Entry(receipt_bg, textvariable=self.update_company, width=25, bd=0)
        self.company_field.delete(0, 'end')
        self.company_field.insert(0, self.update_company)
        self.company_field.config(state='disabled')
        self.company_field.place(height=25, width=200, relx=.745, rely=0.425, anchor="center")

        Label(receipt_bg, text="Owner", bg="#DDDDDD", fg="#363636", font=field_label).place(relx=.540, rely=0.500,
                                                                                               anchor="w")
        self.owner_field = Entry(receipt_bg, textvariable=self.update_ownership, width=25, bd=0)
        self.owner_field.delete(0, 'end')
        self.owner_field.insert(0, self.update_ownership)
        self.owner_field.config(state='disabled')
        self.owner_field.place(height=25, width=200, relx=.745, rely=0.550, anchor="center")

        Label(receipt_bg, text="Payment Status", bg="#DDDDDD", fg="#363636", font=field_label).place(relx=.540, rely=0.625,
                                                                                               anchor="w")
        self.status_field = Entry(receipt_bg, textvariable=self.update_payment_status, width=25, bd=0)
        self.status_field.delete(0, 'end')
        self.status_field.insert(0, self.update_payment_status)
        self.status_field.config(state='disabled')
        self.status_field.place(height=25, width=200, relx=.745, rely=0.675, anchor="center")

    def assetOperationSuccess(self):


        asset_id = self.asset_no
        name = self.update_name
        company = self.update_company
        owner = self.update_ownership
        status = "Available"
        unit_loc = self.update_location
        price = self.update_price
        quantity = self.update_quantity

        if self.update_payment_status_int.get() == 1:
            payment_stat = "Paid"
        else:
            payment_stat = "Unpaid"

        image = self.database.convertToBinaryData(self.update_photo_filename)
        if not image:
            return False

        query =  "UPDATE assets SET image = %s WHERE id = %s"
        args = (image, str(asset_id))
        self.database.updatePhoto(query,args)
        

        # Check valid receipt number
        if self.receipt_no.get() >= 0 and not self.database.checkReceiptNo(self.receipt_no.get()):
            self.database.createReceipt(self.receipt_no.get(), "Update", self.user, "Authorized", asset_id, name, "None", company, owner, unit_loc, quantity, payment_stat, image, "Unapproved")
            

            # Reflect updates
            update_query = "UPDATE assets SET name = '" + name + "', company = '" + company + "', owner = '" + owner\
                                                             + "', unit_loc = '" + unit_loc + "', price = '" + str(price) + "', amount = '" + str(quantity) + "', payment_stat = '" + payment_stat\
                                                             + "' WHERE id = " + str(asset_id)
            self.database.updateAsset(update_query)

            return True
                                                         
        return False
        