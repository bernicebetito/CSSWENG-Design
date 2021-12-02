from tkinter import *
from tkinter import ttk
import tkinter.font as tkfont

root = Tk()
root.title('Prime Properties - Inventory Management System')
root.geometry('1366x768')
root.configure(bg="#191919")
root.state('zoomed')

header = tkfont.Font(family='Oswald', weight='bold', size=20)
sub = tkfont.Font(family='Open Sans', size=12)


def goToNext(currentFrames, nextFunc):
    for i in currentFrames:
        i.destroy()

    if nextFunc == 1:
        login()
    elif nextFunc == 2:
        nav()


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

    nav_text = tkfont.Font(family='Open Sans', weight="bold", size=15)
    logout_text = tkfont.Font(family='Open Sans', weight="bold", size=10)

    create_asset_btn = Button(nav_bg, text="Create Asset", width=15, command=nav, bg="#B8D8D8", fg="#FFFFFF", bd=0, font=nav_text)
    create_user_btn = Button(nav_bg, text="Create User", width=15, command=nav, bg="#8EB8CF", fg="#FFFFFF", bd=0, font=nav_text)
    find_btn = Button(nav_bg, text="Find", width=15, command=nav, bg="#7A9E9F", fg="#FFFFFF", bd=0, font=nav_text)
    history_btn = Button(nav_bg, text="History", width=15, command=nav, bg="#3D626D", fg="#FFFFFF", bd=0, font=nav_text)
    receive_btn = Button(nav_bg, text="Receive", width=15, command=nav, bg="#24434D", fg="#FFFFFF", bd=0, font=nav_text)
    update_btn = Button(nav_bg, text="Update", width=15, command=nav, bg="#4F6367", fg="#FFFFFF", bd=0, font=nav_text)
    delete_btn = Button(nav_bg, text="Delete", width=15, command=nav, bg="#FE5F55", fg="#FFFFFF", bd=0, font=nav_text)
    logout_btn = Button(nav_bg, text="Logout", width=10, command=lambda: goToNext(frames, 1), bg="#EEF5DB", fg="#363636", bd=0, font=logout_text)

    frames = [nav, nav_bg]
    if username.get() == "manager":
        Label(nav_bg, text="PRIME PROPERTIES", bg="#DDDDDD", fg="#3E3E3E", font=header).place(relx=.5, rely=0.05, anchor="c")
        Label(nav_bg, text="Inventory Management System", bg="#DDDDDD", fg="#6A6A6A", font=sub).place(relx=.5, rely=0.1, anchor="c")

        create_asset_btn.place(relx=.5, rely=0.2, anchor="c")
        create_user_btn.place(relx=.5, rely=0.3, anchor="c")
        find_btn.place(relx=.5, rely=0.4, anchor="c")
        history_btn.place(relx=.5, rely=0.5, anchor="c")
        receive_btn.place(relx=.5, rely=0.6, anchor="c")
        update_btn.place(relx=.5, rely=0.7, anchor="c")
        delete_btn.place(relx=.5, rely=0.8, anchor="c")
        logout_btn.place(relx=.5, rely=0.9, anchor="c")
    elif username.get() == "clerk":
        Label(nav_bg, text="PRIME PROPERTIES", bg="#DDDDDD", fg="#3E3E3E", font=header).place(relx=.5, rely=0.15, anchor="c")
        Label(nav_bg, text="Inventory Management System", bg="#DDDDDD", fg="#6A6A6A", font=sub).place(relx=.5, rely=0.2, anchor="c")

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

    Label(login_bg, text="PRIME PROPERTIES", bg="#DDDDDD", fg="#3E3E3E", font=header).place(relx=.5, rely=0.2, anchor="c")
    Label(login_bg, text="Inventory Management System", bg="#DDDDDD", fg="#6A6A6A", font=sub).place(relx=.5, rely=0.25, anchor="c")

    login_label = tkfont.Font(family='Oswald', weight="bold", size=15)
    Label(login_bg, text="LOGIN", bg="#DDDDDD", fg="#3E3E3E", font=login_label).place(relx=.5, rely=0.375, anchor="c")

    credentials_label = tkfont.Font(family='Open Sans', size=10)
    username = StringVar()
    password = StringVar()
    Label(login_bg, text="Username", bg="#DDDDDD", fg="#363636", font=credentials_label).place(relx=.5, rely=0.45, anchor="c")
    username_field = Entry(login_bg, textvariable=username, bd=0)
    username_field.focus()
    username_field.place(height=20, width=225, relx=.5, rely=0.5, anchor="c")

    Label(login_bg, text="Password", bg="#DDDDDD", fg="#363636", font=credentials_label).place(relx=.5, rely=0.6, anchor="c")
    Entry(login_bg, textvariable=password, show="*", width=35, bd=0).place(height=20, width=225, relx=.5, rely=0.65, anchor="c")

    frames = [login, login_bg]
    Button(login_bg, text="Login", height=1, width=10, command=lambda:goToNext(frames, 2), bg="#6D94AA", fg="#FFFFFF", bd=0).place(relx=.5, rely=0.8, anchor="c")


login()
root.mainloop()