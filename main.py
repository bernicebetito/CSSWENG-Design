from tkinter import *
import tkinter.font as tkfont
from PIL import Image, ImageTk
from tkinter import filedialog
import credentials, asset, history

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

login_credentials = credentials.User()
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


def approvedMessage(frames, message):
    for i in frames:
            i.destroy()

    approved_create_bg = Frame(root, bg="#DDDDDD", width=300, height=300)
    approved_create_bg.columnconfigure(0, weight=1)
    approved_create_bg.place(relx=.5, rely=.5, anchor="c")

    displayHeader(approved_create_bg, 0.15, 0.25)

    approved_create_label = tkfont.Font(family='Oswald', weight="bold", size=25)
    Label(approved_create_bg, text=message, bg="#DDDDDD", fg="#6B9A39", font=approved_create_label).place(relx=.5, rely=0.5, anchor="c")

    approved_frames = [approved_create_bg]
    approved_create_btn = Button(approved_create_bg, text="Back to Home", height=1, width=15,
                                 command=lambda: goToNext(approved_frames, 2), bg="#2D2E2E", fg="#FFFFFF", bd=0,
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
            createUser()
        elif nextFunc == 5:  # Find
            nav()
        elif nextFunc == 6:  # History
            historyPage()
        elif nextFunc == 7:  # Receive
            nav()
        elif nextFunc == 8:  # Update
            nav()
        elif nextFunc == 9:  # Delete
            deleteAsset()
        elif nextFunc == 10:  # Change Password
            changePassword()
    else:
        login()


def login():
    global login_credentials
    login_bg = Frame(root, bg="#DDDDDD", width=300, height=450)
    login_bg.columnconfigure(0, weight=1)
    login_bg.place(relx=.5, rely=.5, anchor="c")

    displayHeader(login_bg, 0.20, 0.25)
    login_credentials = credentials.User()
    login_credentials.setLogin(login_bg, field_label)

    def checkCredentials(frames, nextFunc):
        global valid_login, username
        if login_credentials.checkLoginCredentials():
            username = login_credentials.getUsername()
            valid_login = True
            goToNext(frames, nextFunc)
        else:
            valid_login = False

    frames = [login_bg]
    login_btn = Button(login_bg, text="Login", height=1, width=13, command=lambda:checkCredentials(frames, 2), bg="#6D94AA", fg="#FFFFFF", bd=0, font=buttonA)
    login_btn.place(relx=.5, rely=0.8, anchor="c")


def nav():
    if username == "manager":
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
    change_btn = Button(nav_bg, text="Change Password", width=15, command=lambda: goToNext(frames, 10), bg="#8C241E", fg="#FFFFFF", bd=0, font=buttonA)
    logout_btn = Button(nav_bg, text="Logout", width=10, command=lambda: goToNext(frames, 1), bg="#363636", fg="#FFFFFF", bd=0, font=buttonB)

    if username == "manager":
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
    elif username == "clerk":
        displayHeader(nav_bg, 0.15, 0.20)

        create_asset_btn.place(relx=.5, rely=0.350, anchor="c")
        find_btn.place(relx=.5, rely=0.450, anchor="c")
        receive_btn.place(relx=.5, rely=0.550, anchor="c")
        update_btn.place(relx=.5, rely=0.650, anchor="c")
        change_btn.place(relx=.5, rely=0.750, anchor="c")
        logout_btn.place(relx=.5, rely=0.900, anchor="c")


def createAsset():
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

    create_form = asset.createAsset(root)
    create_form.setCreate(create_right, field_label)

    def checkCreateAsset(frames, form):
        if form.submitForm():
            approvedMessage(frames, "Asset Created\nSuccessfully!")

    create_btn = Button(create_right, text="Create", width=15, command=lambda: checkCreateAsset(frames, create_form),
                        bg="#B8D8D8", fg="#FFFFFF", bd=0, font=buttonA)
    create_btn.place(relx=.250, rely=0.975, anchor="c")
    create_form.setButton(create_btn)


def createUser():
    create_user_bg = Frame(root, bg="#DDDDDD", width=300, height=450)
    create_user_bg.columnconfigure(0, weight=1)
    create_user_bg.place(relx=.5, rely=.5, anchor="c")

    displayHeader(create_user_bg, 0.10, 0.15)
    create_user = credentials.createNewUser()
    create_user.setCreateNewUser(create_user_bg, field_label)

    def validateCreateUser(frames):
        if create_user.checkNewUser():
            approvedMessage(frames, "User Created\nSuccessfully!")

    frames = [create_user_bg]
    change_pass_btn = Button(create_user_bg, text="Create User", height=1, width=15,
                             command=lambda: validateCreateUser(frames), bg="#8EB8CF", fg="#FFFFFF", bd=0,
                             font=buttonA)
    change_pass_btn.place(relx=.5, rely=0.800, anchor="c")

    back_btn = Button(create_user_bg, text="Back", width=10, command=lambda: goToNext(frames, 2), bg="#2D2E2E", fg="#FFFFFF", bd=0, font=buttonB)
    back_btn.place(relx=.5, rely=0.900, anchor="c")


def historyPage():
    history_bg = Frame(root, bg="#DDDDDD", width=1200, height=600)
    history_bg.pack()
    history_bg.columnconfigure(0, weight=1)
    history_bg.place(relx=.5, rely=.5, anchor="c")

    history_form_frame = Frame(history_bg, bg="#DDDDDD", width=300, height=550)
    history_form_frame.place(relx=.135, rely=.5, anchor="c")

    history_table_frame = Frame(history_bg, bg="#191919", width=825, height=500)
    history_table_frame.place(relx=.625, rely=.5, anchor="c")

    displayHeader(history_form_frame, 0.050, 0.100)

    history_page = history.History(root)
    history_page.displayHistory(history_form_frame, field_label, buttonA)
    history_page.displayTable(history_table_frame)

    frames = [history_bg, history_form_frame, history_table_frame]
    back_btn = Button(history_form_frame, text="Back", width=10, command=lambda: goToNext(frames, 2), bg="#2D2E2E", fg="#FFFFFF", bd=0, font=buttonB)
    back_btn.place(relx=.15, rely=0.950, anchor="c")


def deleteAsset():
    delete_bg = Frame(root, bg="#DDDDDD", width=1200, height=600)
    delete_bg.pack()
    delete_bg.columnconfigure(0, weight=1)
    delete_bg.place(relx=.5, rely=.5, anchor="c")

    delete_form_frame = Frame(delete_bg, bg="#DDDDDD", width=300, height=550)
    delete_form_frame.place(relx=.135, rely=.5, anchor="c")

    delete_table_frame = Frame(delete_bg, bg="#191919", width=825, height=500)
    delete_table_frame.place(relx=.625, rely=.5, anchor="c")

    displayHeader(delete_form_frame, 0.050, 0.100)

    delete_page = asset.deleteAsset(root)
    delete_page.displayDelete(delete_form_frame, field_label, buttonA)
    delete_page.displayTable(delete_table_frame)

    def validDeleteAssets(frames):
        if delete_page.checkAssets():
            approvedMessage(frames, "Assets Deleted\nSuccessfully!")

    frames = [delete_bg, delete_form_frame, delete_table_frame]
    delete_btn = Button(delete_form_frame, text="Delete", width=13, command=lambda: validDeleteAssets(frames), bg="#FE5F55",
                        fg="#FFFFFF", bd=0, font=buttonA)
    delete_btn.place(relx=.25, rely=0.850, anchor="c")

    back_btn = Button(delete_form_frame, text="Back", width=10, command=lambda: goToNext(frames, 2), bg="#2D2E2E",
                      fg="#FFFFFF", bd=0, font=buttonB)
    back_btn.place(relx=.15, rely=0.950, anchor="c")


def changePassword():
    change_pass_bg = Frame(root, bg="#DDDDDD", width=300, height=450)
    change_pass_bg.columnconfigure(0, weight=1)
    change_pass_bg.place(relx=.5, rely=.5, anchor="c")

    displayHeader(change_pass_bg, 0.10, 0.15)
    login_credentials.setChangePassword(change_pass_bg, field_label)

    def validateChangePassword(frames):
        if login_credentials.checkChangePassword():
            approvedMessage(frames, "Password Updated\nSuccessfully!")

    frames = [change_pass_bg]
    change_pass_btn = Button(change_pass_bg, text="Change Password", height=1, width=15, command=lambda: validateChangePassword(frames), bg="#8C241E", fg="#FFFFFF", bd=0, font=buttonA)
    change_pass_btn.place(relx=.5, rely=0.800, anchor="c")

    back_btn = Button(change_pass_bg, text="Back", width=10, command=lambda: goToNext(frames, 2), bg="#2D2E2E", fg="#FFFFFF", bd=0, font=buttonB)
    back_btn.place(relx=.5, rely=0.900, anchor="c")


login()
root.mainloop()