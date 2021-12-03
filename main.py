from tkinter import *
from tkinter import ttk
import tkinter as tk
import tkinter.font as tkfont
from PIL import Image, ImageTk
import os, table

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


def displayHeader(frame, header_y, sub_y):
    Label(frame, text="PRIME PROPERTIES", bg="#DDDDDD", fg="#3E3E3E", font=header).place(relx=.5, rely=header_y, anchor="c")
    Label(frame, text="Inventory Management System", bg="#DDDDDD", fg="#6A6A6A", font=sub).place(relx=.5, rely=sub_y, anchor="c")


def goToNext(currentFrames, nextFunc):
    for i in currentFrames:
        i.destroy()

    if nextFunc == 1: # Login
        login()
    elif nextFunc == 2: # Nav
        nav()
    elif nextFunc == 3: # Create Asset
        nav()
    elif nextFunc == 4: # Create User
        nav()
    elif nextFunc == 5: # Find
        nav()
    elif nextFunc == 6: # History
        history()
    elif nextFunc == 7: # Receive
        nav()
    elif nextFunc == 8: # Update
        nav()
    elif nextFunc == 9: # Delete
        nav()


def history():
    history = Frame(root)
    history.pack()
    history.columnconfigure(0, weight=1)
    history.place(relx=.5, rely=.5, anchor="c")

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

    filter_btn = Button(history_form_frame, text="Filter", width=15, command=lambda: goToNext(frames, 6), bg="#FE5F55", fg="#FFFFFF", bd=0, font=buttonA)
    filter_btn.place(relx=.5, rely=0.725, anchor="c")

    frames = [history, history_bg, history_form_frame, history_table_frame]
    back_btn = Button(history_form_frame, text="Back", width=15, command=lambda: goToNext(frames, 2), bg="#2D2E2E", fg="#FFFFFF", bd=0, font=buttonB)
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


def nav():
    nav = Frame(root)
    nav.pack()
    nav.columnconfigure(0, weight=1)
    nav.place(relx=.5, rely=.5, anchor="c")

    if username.get() == "manager":
        nav_bg = Frame(root, bg="#DDDDDD", width=300, height=600)
    else:
        nav_bg = Frame(root, bg="#DDDDDD", width=300, height=450)

    nav_bg.columnconfigure(0, weight=1)
    nav_bg.place(relx=.5, rely=.5, anchor="c")

    frames = [nav, nav_bg]
    create_asset_btn = Button(nav_bg, text="Create Asset", width=15, command=lambda: goToNext(frames, 3), bg="#B8D8D8", fg="#FFFFFF", bd=0, font=buttonA)
    create_user_btn = Button(nav_bg, text="Create User", width=15, command=lambda: goToNext(frames, 4), bg="#8EB8CF", fg="#FFFFFF", bd=0, font=buttonA)
    find_btn = Button(nav_bg, text="Find", width=15, command=lambda: goToNext(frames, 5), bg="#7A9E9F", fg="#FFFFFF", bd=0, font=buttonA)
    history_btn = Button(nav_bg, text="History", width=15, command=lambda: goToNext(frames, 6), bg="#3D626D", fg="#FFFFFF", bd=0, font=buttonA)
    receive_btn = Button(nav_bg, text="Receive", width=15, command=lambda: goToNext(frames, 7), bg="#24434D", fg="#FFFFFF", bd=0, font=buttonA)
    update_btn = Button(nav_bg, text="Update", width=15, command=lambda: goToNext(frames, 8), bg="#4F6367", fg="#FFFFFF", bd=0, font=buttonA)
    delete_btn = Button(nav_bg, text="Delete", width=15, command=lambda: goToNext(frames, 9), bg="#FE5F55", fg="#FFFFFF", bd=0, font=buttonA)
    logout_btn = Button(nav_bg, text="Logout", width=10, command=lambda: goToNext(frames, 1), bg="#EEF5DB", fg="#363636", bd=0, font=buttonB)

    if username.get() == "manager":
        displayHeader(nav_bg, 0.05, 0.10)

        create_asset_btn.place(relx=.5, rely=0.2, anchor="c")
        create_user_btn.place(relx=.5, rely=0.3, anchor="c")
        find_btn.place(relx=.5, rely=0.4, anchor="c")
        history_btn.place(relx=.5, rely=0.5, anchor="c")
        receive_btn.place(relx=.5, rely=0.6, anchor="c")
        update_btn.place(relx=.5, rely=0.7, anchor="c")
        delete_btn.place(relx=.5, rely=0.8, anchor="c")
        logout_btn.place(relx=.5, rely=0.9, anchor="c")
    elif username.get() == "clerk":
        displayHeader(nav_bg, 0.15, 0.20)

        create_asset_btn.place(relx=.5, rely=0.350, anchor="c")
        find_btn.place(relx=.5, rely=0.475, anchor="c")
        receive_btn.place(relx=.5, rely=0.600, anchor="c")
        update_btn.place(relx=.5, rely=0.725, anchor="c")
        logout_btn.place(relx=.5, rely=0.850, anchor="c")


def login():
    global username, password
    login = Frame(root)
    login.pack()
    login.columnconfigure(0, weight=1)
    login.place(relx=.5, rely=.5, anchor="c")

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
    Entry(login_bg, textvariable=password, show="*", width=35, bd=0).place(height=20, width=225, relx=.5, rely=0.65, anchor="c")

    frames = [login, login_bg]
    login_btn = Button(login_bg, text="Login", height=1, width=10, command=lambda:goToNext(frames, 2), bg="#6D94AA", fg="#FFFFFF", bd=0, font=buttonB)
    login_btn.place(relx=.5, rely=0.8, anchor="c")


login()
root.mainloop()