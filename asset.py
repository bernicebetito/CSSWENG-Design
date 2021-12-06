from tkinter import *
from tkinter import ttk


class createAsset():

    def __init__(self, root):
        self.create_name = StringVar()
        self.create_company = StringVar()
        self.create_status = StringVar()
        self.create_location = StringVar()
        self.create_price = DoubleVar()
        self.create_quantity = DoubleVar()
        self.create_ownership = StringVar()
        self.create_payment_status = StringVar()

        self.create_name_field = Entry()
        self.create_company_field = Entry()
        self.create_status_field = Entry()
        self.create_location_field = Entry()
        self.create_price_field = Entry()
        self.create_quantity_field = Entry()
        self.create_owner_field = Entry()
        self.create_payment_field = Entry()

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

    def submitForm(self):
        # checking, validation, and inserting in the DB would happen here
        valid_first = len(self.create_name.get()) > 1 and len(self.create_company.get()) > 1
        valid_second = len(self.create_status.get()) > 1 and len(self.create_location.get()) > 1
        valid_third = self.create_price.get() > 0 and self.create_quantity.get() > 0
        valid_fourth = len(self.create_ownership.get()) > 1 and len(self.create_payment_status.get()) > 1
        if valid_first and valid_second and valid_third and valid_fourth:
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
        Label(create_right, text="Asset Name", bg="#DDDDDD", fg="#363636", font=field_label).place(relx=.100, rely=0.200, anchor="c")
        self.create_name_field = Entry(create_right, textvariable=self.create_name, width=35, bd=0)
        self.create_name_field.place(height=25, width=250, relx=.245, rely=0.250, anchor="c")
        self.create_fields.append(self.create_name_field)

        Label(create_right, text="Company", bg="#DDDDDD", fg="#363636", font=field_label).place(relx=.590, rely=0.200, anchor="c")
        self.create_company_field = Entry(create_right, textvariable=self.create_company, width=35, bd=0)
        self.create_company_field.place(height=25, width=250, relx=.750, rely=0.250, anchor="c")
        self.create_fields.append(self.create_company_field)

        Label(create_right, text="Status", bg="#DDDDDD", fg="#363636", font=field_label).place(relx=.070, rely=0.350, anchor="c")
        self.create_status_field = Entry(create_right, textvariable=self.create_status, width=35, bd=0)
        self.create_status_field.place(height=25, width=250, relx=.245, rely=0.400, anchor="c")
        self.create_fields.append(self.create_status_field)

        Label(create_right, text="Unit Location", bg="#DDDDDD", fg="#363636", font=field_label).place(relx=.605, rely=0.350, anchor="c")
        self.create_location_field = Entry(create_right, textvariable=self.create_location, width=35, bd=0)
        self.create_location_field.place(height=25, width=250, relx=.750, rely=0.400, anchor="c")
        self.create_fields.append(self.create_location_field)

        Label(create_right, text="Price", bg="#DDDDDD", fg="#363636", font=field_label).place(relx=.065, rely=0.500, anchor="c")
        self.create_price_field = Entry(create_right, textvariable=self.create_price, width=35, bd=0)
        self.create_price_field.place(height=25, width=250, relx=.245, rely=0.550, anchor="c")
        self.create_price_field.config(validate="focusout", validatecommand=(self.reg_validDouble, '%P'), invalidcommand=(self.reg_invalidDouble,))
        self.create_fields.append(self.create_price_field)

        Label(create_right, text="Quantity", bg="#DDDDDD", fg="#363636", font=field_label).place(relx=.585, rely=0.500, anchor="c")
        self.create_quantity_field = Entry(create_right, textvariable=self.create_quantity, width=35, bd=0)
        self.create_quantity_field.place(height=25, width=250, relx=.750, rely=0.550, anchor="c")
        self.create_quantity_field.config(validate="focusout", validatecommand=(self.reg_validDouble, '%P'), invalidcommand=(self.reg_invalidDouble,))
        self.create_fields.append(self.create_quantity_field)

        Label(create_right, text="Ownership", bg="#DDDDDD", fg="#363636", font=field_label).place(relx=.090, rely=0.650, anchor="c")
        self.create_owner_field = Entry(create_right, textvariable=self.create_ownership, width=35, bd=0)
        self.create_owner_field.place(height=25, width=250, relx=.245, rely=0.700, anchor="c")
        self.create_fields.append(self.create_owner_field)

        Label(create_right, text="Payment Status", bg="#DDDDDD", fg="#363636", font=field_label).place(relx=.625, rely=0.650, anchor="c")
        self.create_payment_field = Entry(create_right, textvariable=self.create_payment_status, width=35, bd=0)
        self.create_payment_field.place(height=25, width=250, relx=.750, rely=0.700, anchor="c")
        self.create_fields.append(self.create_payment_field)

        self.create_error_label = Label(create_right, bg="#DDDDDD", fg="#D64000", font=field_label)
        self.create_error_label.place(relx=.5, rely=0.750, anchor="c")