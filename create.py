from tkinter import *
from tkinter import ttk
import tkinter as tk
import tkinter.font as tkfont
from PIL import Image, ImageTk
from tkinter import filedialog
from tkinter.filedialog import askopenfile
import os

class createAsset():

    def __init__(self, fields):
        self.create_name = fields["name"]
        self.create_company = fields["company"]
        self.create_status = fields["status"]
        self.create_location = fields["location"]
        self.create_price = fields["price"]
        self.create_quantity = fields["quantity"]
        self.create_ownership = fields["ownership"]
        self.create_payment_status = fields["payment_status"]

    def submitForm(self):
        # checking, validation, and inserting in the DB would happen here
        if len(self.create_name.get()) > 1 and len(self.create_company.get()) > 1:
            if len(self.create_status.get()) > 1 and len(self.create_location.get()) > 1:
                if len(self.create_price.get()) > 1 and len(self.create_quantity.get()) > 1:
                    if len(self.create_ownership.get()) > 1 and len(self.create_payment_status.get()) > 1:
                        return True

        return False