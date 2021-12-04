from tkinter import *
from tkinter import ttk
import tkinter as tk
import tkinter.font as tkfont
from PIL import Image, ImageTk
from tkinter import filedialog
from tkinter.filedialog import askopenfile
import os, table, create

root = Tk()
root.title('Prime Properties - Inventory Management System')
root.geometry('1366x768')
root.configure(bg="#191919")
root.state('zoomed')
root.table_image = []

header = tkfont.Font(family='Oswald', weight='bold', size=20)
sub = tkfont.Font(family='Open Sans', size=12)
field_label = tkfont.Font(family='Open Sans', size=10)
buttonA = tkfont.Font(family='Open Sans', weight="bold", size=15)
buttonB = tkfont.Font(family='Open Sans', weight="bold", size=10)

valid_login = True


def displayHeader(frame, header_y, sub_y):
    Label(frame, text="PRIME PROPERTIES", bg="#DDDDDD", fg="#3E3E3E", font=header).place(relx=.5, rely=header_y, anchor="c")
    Label(frame, text="Inventory Management System", bg="#DDDDDD", fg="#6A6A6A", font=sub).place(relx=.5, rely=sub_y, anchor="c")


def uploadImage(canvas, text):
    global upload_img, photo_filename
    fileTypes = [('JPG Files', '*.jpg'),
                 ('JPEG Files', '*.jpeg'),
                 ('PNG Files', '*.png')]
    photo_filename = filedialog.askopenfilename(filetypes=fileTypes)
    if len(photo_filename) > 0:
        image = Image.open(photo_filename)
        resized_img = image.resize((250, 250), Image.ANTIALIAS)
        upload_img = ImageTk.PhotoImage(resized_img)

        canvas.create_image(0, 0, image=upload_img, anchor=NW)
        canvas.delete(text)


def checkCredentials(frames, nextFunc):
    global valid_login

    if len(username.get()) > 1 and len(password.get()) > 1:
        # add other checking stuff
        valid_login = True
        goToNext(frames, nextFunc)
    else:
        valid_login = False
        login()


def checkCreateAsset(frames, create_fields):
    create_asset = create.createAsset(create_fields)
    approved_create = create_asset.submitForm()

    if approved_create:
        for i in frames:
            i.destroy()

        approved_create_bg = Frame(root, bg="#DDDDDD", width=300, height=300)
        approved_create_bg.columnconfigure(0, weight=1)
        approved_create_bg.place(relx=.5, rely=.5, anchor="c")

        displayHeader(approved_create_bg, 0.15, 0.25)

        approved_create_label = tkfont.Font(family='Oswald', weight="bold", size=25)
        Label(approved_create_bg, text="Asset Created\nSuccessfully!", bg="#DDDDDD", fg="#6B9A39", font=approved_create_label).place(
            relx=.5, rely=0.5, anchor="c")

        frames = [approved_create_bg]
        approved_create_btn = Button(approved_create_bg, text="Back to Home", height=1, width=15,
                                     command=lambda: goToNext(frames, 2), bg="#2D2E2E", fg="#FFFFFF", bd=0,
                                     font=buttonA)
        approved_create_btn.place(relx=.5, rely=0.8, anchor="c")


def goToNext(currentFrames, nextFunc):
    for i in currentFrames:
        i.destroy()

    if valid_login:
        if nextFunc == 1:  # Login
            login()
        elif nextFunc == 2:  # Nav
            nav()
        elif nextFunc == 3:  # Create Asset
            createAsset()
        elif nextFunc == 4:  # Create User
            nav()
        elif nextFunc == 5:  # Find
            nav()
        elif nextFunc == 6:  # History
            history()
        elif nextFunc == 7:  # Receive
            nav()
        elif nextFunc == 8:  # Update
            nav()
        elif nextFunc == 9:  # Delete
            nav()
    else:
        login()


def history():
    history_bg = Frame(root, bg="#DDDDDD", width=1200, height=600)
    history_bg.pack()
    history_bg.columnconfigure(0, weight=1)
    history_bg.place(relx=.5, rely=.5, anchor="c")

    history_form_frame = Frame(history_bg, bg="#DDDDDD", width=300, height=550)
    history_form_frame.place(relx=.135, rely=.5, anchor="c")

    history_table_frame = Frame(history_bg, bg="#191919", width=825, height=500)
    history_table_frame.place(relx=.625, rely=.5, anchor="c")

    displayHeader(history_form_frame, 0.050, 0.100)

    asset_name = StringVar()
    location = StringVar()
    owner = StringVar()
    status = StringVar()
    Label(history_form_frame, text="Filter by Asset Name", bg="#DDDDDD", fg="#363636", font=field_label).place(relx=.5, rely=0.200, anchor="c")
    Entry(history_form_frame, textvariable=asset_name, bd=0).place(height=20, width=225, relx=.5, rely=0.250, anchor="c")

    Label(history_form_frame, text="Filter by Location", bg="#DDDDDD", fg="#363636", font=field_label).place(relx=.5, rely=0.325, anchor="c")
    Entry(history_form_frame, textvariable=location, bd=0).place(height=20, width=225, relx=.5, rely=0.375, anchor="c")

    Label(history_form_frame, text="Filter by Owner", bg="#DDDDDD", fg="#363636", font=field_label).place(relx=.5, rely=0.450, anchor="c")
    Entry(history_form_frame, textvariable=owner, bd=0).place(height=20, width=225, relx=.5, rely=0.500, anchor="c")

    Label(history_form_frame, text="Filter by Status", bg="#DDDDDD", fg="#363636", font=field_label).place(relx=.5, rely=0.575, anchor="c")
    Entry(history_form_frame, textvariable=status, bd=0).place(height=20, width=225, relx=.5, rely=0.625, anchor="c")

    filter_btn = Button(history_form_frame, text="Filter", width=13, command=lambda: goToNext(frames, 6), bg="#FE5F55", fg="#FFFFFF", bd=0, font=buttonA)
    filter_btn.place(relx=.5, rely=0.725, anchor="c")

    frames = [history_bg, history_form_frame, history_table_frame]
    back_btn = Button(history_form_frame, text="Back", width=10, command=lambda: goToNext(frames, 2), bg="#2D2E2E", fg="#FFFFFF", bd=0, font=buttonB)
    back_btn.place(relx=.15, rely=0.950, anchor="c")

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
    root.table_image = []
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
                    root.table_image.append(table_image)
                    curr_row.append(table_image)
                else:
                    curr_row.append("Testing Text")
        history_table_contents.append(curr_row)

    history_table = table.Table(history_measurements, history_canvas, history_table_contents)
    history_table.setScrollbars(history_table_frame)
    history_table.createTable()
    history_canvas.configure(scrollregion=history_canvas.bbox("all"))


def createAsset():
    create_name = StringVar()
    create_company = StringVar()
    create_status = StringVar()
    create_location = StringVar()
    create_price = StringVar()
    create_quantity = StringVar()
    create_ownership = StringVar()
    create_payment_status = StringVar()

    create_bg = Frame(root, bg="#DDDDDD", width=950, height=600)
    create_bg.columnconfigure(0, weight=1)
    create_bg.place(relx=.5, rely=.5, anchor="c")

    create_left = Frame(create_bg, bg="#DDDDDD", width=300, height=575)
    create_left.columnconfigure(0, weight=1)
    create_left.place(relx=.175, rely=.5, anchor="c")

    create_right = Frame(create_bg, bg="#DDDDDD", width=575, height=550)
    create_right.place(relx=.675, rely=.5, anchor="c")

    frames = [create_bg, create_left, create_right]

    displayHeader(create_left, 0.050, 0.100)
    create_photo_preview = Canvas(create_left, bg="#FFFFFF", width=250, height=250)
    create_photo_preview.place(relx=.5, rely=0.450, anchor="c")
    create_photo_text = create_photo_preview.create_text((125, 125), text="No Photo Uploaded", font=field_label)

    upload_btn = Button(create_left, text="Upload", width=13, command=lambda: uploadImage(create_photo_preview, create_photo_text), bg="#B3D687", fg="#FFFFFF", bd=0, font=buttonA)
    upload_btn.place(relx=.5, rely=0.725, anchor="c")
    back_btn = Button(create_left, text="Back", width=10, command=lambda: goToNext(frames, 2), bg="#2D2E2E", fg="#FFFFFF", bd=0, font=buttonB)
    back_btn.place(relx=.15, rely=0.950, anchor="c")

    Label(create_right, text="Asset Name", bg="#DDDDDD", fg="#363636", font=field_label).place(relx=.100, rely=0.200, anchor="c")
    create_name_field = Entry(create_right, textvariable=create_name, width=35, bd=0)
    create_name_field.place(height=25, width=250, relx=.245, rely=0.250, anchor="c")

    Label(create_right, text="Company", bg="#DDDDDD", fg="#363636", font=field_label).place(relx=.590, rely=0.200, anchor="c")
    create_company_field = Entry(create_right, textvariable=create_company, width=35, bd=0)
    create_company_field.place(height=25, width=250, relx=.750, rely=0.250, anchor="c")

    Label(create_right, text="Status", bg="#DDDDDD", fg="#363636", font=field_label).place(relx=.070, rely=0.350, anchor="c")
    create_status_field = Entry(create_right, textvariable=create_status, width=35, bd=0)
    create_status_field.place(height=25, width=250, relx=.245, rely=0.400, anchor="c")

    Label(create_right, text="Unit Location", bg="#DDDDDD", fg="#363636", font=field_label).place(relx=.605, rely=0.350, anchor="c")
    create_location_field = Entry(create_right, textvariable=create_location, width=35, bd=0)
    create_location_field.place(height=25, width=250, relx=.750, rely=0.400, anchor="c")

    Label(create_right, text="Price", bg="#DDDDDD", fg="#363636", font=field_label).place(relx=.065, rely=0.500, anchor="c")
    create_price_field = Entry(create_right, textvariable=create_price, width=35, bd=0)
    create_price_field.place(height=25, width=250, relx=.245, rely=0.550, anchor="c")

    Label(create_right, text="Quantity", bg="#DDDDDD", fg="#363636", font=field_label).place(relx=.585, rely=0.500, anchor="c")
    create_quantity_field = Entry(create_right, textvariable=create_quantity, width=35, bd=0)
    create_quantity_field.place(height=25, width=250, relx=.750, rely=0.550, anchor="c")

    Label(create_right, text="Ownership", bg="#DDDDDD", fg="#363636", font=field_label).place(relx=.090, rely=0.650, anchor="c")
    create_owner_field = Entry(create_right, textvariable=create_ownership, width=35, bd=0)
    create_owner_field.place(height=25, width=250, relx=.245, rely=0.700, anchor="c")

    Label(create_right, text="Payment Status", bg="#DDDDDD", fg="#363636", font=field_label).place(relx=.625, rely=0.650, anchor="c")
    create_payment_field = Entry(create_right, textvariable=create_payment_status, width=35, bd=0)
    create_payment_field.place(height=25, width=250, relx=.750, rely=0.700, anchor="c")

    create_fields = {
        "name": create_name,
        "company": create_company,
        "status": create_status,
        "location": create_location,
        "price": create_price,
        "quantity": create_quantity,
        "ownership": create_ownership,
        "payment_status": create_payment_status
    }

    create_btn = Button(create_right, text="Create", width=15, command=lambda: checkCreateAsset(frames, create_fields), bg="#B8D8D8", fg="#FFFFFF", bd=0, font=buttonA)
    create_btn.place(relx=.250, rely=0.975, anchor="c")


def nav():
    if username.get() == "manager":
        nav_bg = Frame(root, bg="#DDDDDD", width=300, height=600)
    else:
        nav_bg = Frame(root, bg="#DDDDDD", width=300, height=450)

    nav_bg.columnconfigure(0, weight=1)
    nav_bg.place(relx=.5, rely=.5, anchor="c")

    frames = [nav_bg]
    create_asset_btn = Button(nav_bg, text="Create Asset", width=15, command=lambda: goToNext(frames, 3), bg="#B8D8D8", fg="#FFFFFF", bd=0, font=buttonA)
    create_user_btn = Button(nav_bg, text="Create User", width=15, command=lambda: goToNext(frames, 4), bg="#8EB8CF", fg="#FFFFFF", bd=0, font=buttonA)
    find_btn = Button(nav_bg, text="Find", width=15, command=lambda: goToNext(frames, 5), bg="#7A9E9F", fg="#FFFFFF", bd=0, font=buttonA)
    history_btn = Button(nav_bg, text="History", width=15, command=lambda: goToNext(frames, 6), bg="#3D626D", fg="#FFFFFF", bd=0, font=buttonA)
    receive_btn = Button(nav_bg, text="Receive", width=15, command=lambda: goToNext(frames, 7), bg="#24434D", fg="#FFFFFF", bd=0, font=buttonA)
    update_btn = Button(nav_bg, text="Update", width=15, command=lambda: goToNext(frames, 8), bg="#4F6367", fg="#FFFFFF", bd=0, font=buttonA)
    delete_btn = Button(nav_bg, text="Delete", width=15, command=lambda: goToNext(frames, 9), bg="#FE5F55", fg="#FFFFFF", bd=0, font=buttonA)
    change_btn = Button(nav_bg, text="Change Password", width=15, command=lambda: goToNext(frames, 10), bg="#363636", fg="#FFFFFF", bd=0, font=buttonA)
    logout_btn = Button(nav_bg, text="Logout", width=10, command=lambda: goToNext(frames, 1), bg="#EEF5DB", fg="#363636", bd=0, font=buttonB)

    if username.get() == "manager":
        displayHeader(nav_bg, 0.05, 0.10)

        create_asset_btn.place(relx=.5, rely=0.225, anchor="c")
        create_user_btn.place(relx=.5, rely=0.310, anchor="c")
        find_btn.place(relx=.5, rely=0.390, anchor="c")
        history_btn.place(relx=.5, rely=0.475, anchor="c")
        receive_btn.place(relx=.5, rely=0.560, anchor="c")
        update_btn.place(relx=.5, rely=0.645, anchor="c")
        delete_btn.place(relx=.5, rely=0.730, anchor="c")
        change_btn.place(relx=.5, rely=0.815, anchor="c")
        logout_btn.place(relx=.5, rely=0.925, anchor="c")
    elif username.get() == "clerk":
        displayHeader(nav_bg, 0.15, 0.20)

        create_asset_btn.place(relx=.5, rely=0.350, anchor="c")
        find_btn.place(relx=.5, rely=0.450, anchor="c")
        receive_btn.place(relx=.5, rely=0.550, anchor="c")
        update_btn.place(relx=.5, rely=0.650, anchor="c")
        change_btn.place(relx=.5, rely=0.750, anchor="c")
        logout_btn.place(relx=.5, rely=0.900, anchor="c")


def login():
    global username, password
    login_bg = Frame(root, bg="#DDDDDD", width=300, height=450)
    login_bg.columnconfigure(0, weight=1)
    login_bg.place(relx=.5, rely=.5, anchor="c")

    displayHeader(login_bg, 0.20, 0.25)

    login_label = tkfont.Font(family='Oswald', weight="bold", size=15)
    Label(login_bg, text="LOGIN", bg="#DDDDDD", fg="#3E3E3E", font=login_label).place(relx=.5, rely=0.375, anchor="c")

    username = StringVar()
    password = StringVar()
    Label(login_bg, text="Username", bg="#DDDDDD", fg="#363636", font=field_label).place(relx=.5, rely=0.45, anchor="c")
    username_field = Entry(login_bg, textvariable=username, bd=0)
    username_field.focus()
    username_field.place(height=20, width=225, relx=.5, rely=0.5, anchor="c")

    Label(login_bg, text="Password", bg="#DDDDDD", fg="#363636", font=field_label).place(relx=.5, rely=0.6, anchor="c")
    password_field = Entry(login_bg, textvariable=password, show="*", width=35, bd=0)
    password_field.place(height=20, width=225, relx=.5, rely=0.65, anchor="c")

    if not valid_login:
        username_field.configure(highlightthickness=2, highlightbackground="#D64000", highlightcolor="#D64000")
        password_field.configure(highlightthickness=2, highlightbackground="#D64000", highlightcolor="#D64000")
        Label(login_bg, text="Invalid Username and / or Password", bg="#DDDDDD", fg="#D64000", font=field_label)\
            .place(relx=.5, rely=0.725, anchor="c")

    frames = [login_bg]
    login_btn = Button(login_bg, text="Login", height=1, width=13, command=lambda:checkCredentials(frames, 2), bg="#6D94AA", fg="#FFFFFF", bd=0, font=buttonA)
    login_btn.place(relx=.5, rely=0.8, anchor="c")


login()
root.mainloop()