from tkinter import *
import tkinter.font as tkfont
from PIL import Image, ImageTk
from tkinter import filedialog
import user, asset, history, table

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

login_credentials = user.User()
valid_login = True


def displayHeader(frame, header_y, sub_y):
    Label(frame, text="PRIME PROPERTIES", bg="#DDDDDD", fg="#3E3E3E", font=header).place(relx=.5, rely=header_y, anchor="center")
    Label(frame, text="Inventory Management System", bg="#DDDDDD", fg="#6A6A6A", font=sub).place(relx=.5, rely=sub_y, anchor="center")


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

    approved_bg = Frame(root, bg="#DDDDDD", width=300, height=300)
    approved_bg.columnconfigure(0, weight=1)
    approved_bg.place(relx=.5, rely=.5, anchor="center")

    displayHeader(approved_bg, 0.15, 0.25)

    approved_font = tkfont.Font(family='Oswald', weight="bold", size=25)
    approved_label = Label(approved_bg, text=message, bg="#DDDDDD", fg="#6B9A39", font=approved_font)
    approved_label.place(relx=.5, rely=0.5, anchor="center")

    approved_frames = [approved_bg]
    approved_btn = Button(approved_bg, text="Back to Home", height=1, width=15,
                                 command=lambda: goToNext(approved_frames, 2), bg="#2D2E2E", fg="#FFFFFF", bd=0,
                                 font=buttonB)
    approved_btn.place(relx=.5, rely=0.8, anchor="center")


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
        elif nextFunc == 4:  # Manage Users
            manageUser()
        elif nextFunc == 5:  # Create Users
            createUser()
        elif nextFunc == 6:  # Perform Operation (Users)
            performUsers()
        elif nextFunc == 7:  # Change Password
            changePassword()
        elif nextFunc == 8:  # Find
            nav()
        elif nextFunc == 9:  # History
            historyPage()
        elif nextFunc == 10:  # Receive
            receiveAsset()
        elif nextFunc == 11:  # Update
            nav()
        elif nextFunc == 12:  # Import & Export
            importExport()
        elif nextFunc == 13:  # Import
            importOption()
        elif nextFunc == 14:  # Export
            exportOption()
        elif nextFunc == 15:  # Delete
            deleteAsset()
    else:
        login()


def login():
    global login_credentials
    login_bg = Frame(root, bg="#DDDDDD", width=300, height=450)
    login_bg.columnconfigure(0, weight=1)
    login_bg.place(relx=.5, rely=.5, anchor="center")

    displayHeader(login_bg, 0.20, 0.25)
    login_credentials = user.User()
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
    login_btn.place(relx=.5, rely=0.8, anchor="center")


def nav():
    if username == "manager":
        nav_bg = Frame(root, bg="#DDDDDD", width=300, height=600)
    else:
        nav_bg = Frame(root, bg="#DDDDDD", width=300, height=500)

    nav_bg.columnconfigure(0, weight=1)
    nav_bg.place(relx=.5, rely=.5, anchor="center")

    frames = [nav_bg]
    create_asset_btn = Button(nav_bg, text="Create Asset", width=15, command=lambda: goToNext(frames, 3), bg="#B8D8D8", fg="#FFFFFF", bd=0, font=buttonA)
    manage_user_btn = Button(nav_bg, text="Manage Users", width=15, command=lambda: goToNext(frames, 4), bg="#8EB8CF", fg="#FFFFFF", bd=0, font=buttonA)
    find_btn = Button(nav_bg, text="Find", width=15, command=lambda: goToNext(frames, 8), bg="#7A9E9F", fg="#FFFFFF", bd=0, font=buttonA)
    history_btn = Button(nav_bg, text="History", width=15, command=lambda: goToNext(frames, 9), bg="#3D626D", fg="#FFFFFF", bd=0, font=buttonA)
    receive_btn = Button(nav_bg, text="Receive", width=15, command=lambda: goToNext(frames, 10), bg="#24434D", fg="#FFFFFF", bd=0, font=buttonA)
    update_btn = Button(nav_bg, text="Update", width=15, command=lambda: goToNext(frames, 11), bg="#4F6367", fg="#FFFFFF", bd=0, font=buttonA)
    import_btn = Button(nav_bg, text="Import & Export", width=15, command=lambda: goToNext(frames, 12), bg="#3C4648", fg="#FFFFFF", bd=0, font=buttonA)
    delete_btn = Button(nav_bg, text="Delete", width=15, command=lambda: goToNext(frames, 15), bg="#FE5F55", fg="#FFFFFF", bd=0, font=buttonA)
    logout_btn = Button(nav_bg, text="Logout", width=10, command=lambda: goToNext(frames, 1), bg="#363636", fg="#FFFFFF", bd=0, font=buttonB)

    if username == "manager":
        displayHeader(nav_bg, 0.05, 0.10)

        create_asset_btn.place(relx=.5, rely=0.225, anchor="center")
        manage_user_btn.place(relx=.5, rely=0.310, anchor="center")
        find_btn.place(relx=.5, rely=0.395, anchor="center")
        history_btn.place(relx=.5, rely=0.480, anchor="center")
        receive_btn.place(relx=.5, rely=0.565, anchor="center")
        update_btn.place(relx=.5, rely=0.650, anchor="center")
        import_btn.place(relx=.5, rely=0.735, anchor="center")
        delete_btn.place(relx=.5, rely=0.820, anchor="center")
        logout_btn.place(relx=.5, rely=0.905, anchor="center")
    elif username == "clerk":
        displayHeader(nav_bg, 0.15, 0.20)

        create_asset_btn.place(relx=.5, rely=0.350, anchor="center")
        find_btn.place(relx=.5, rely=0.450, anchor="center")
        receive_btn.place(relx=.5, rely=0.550, anchor="center")
        update_btn.place(relx=.5, rely=0.650, anchor="center")
        import_btn.place(relx=.5, rely=0.750, anchor="center")
        logout_btn.place(relx=.5, rely=0.850, anchor="center")


def createAsset():
    create_bg = Frame(root, bg="#DDDDDD", width=950, height=600)
    create_bg.columnconfigure(0, weight=1)
    create_bg.place(relx=.5, rely=.5, anchor="center")

    create_left = Frame(create_bg, bg="#DDDDDD", width=300, height=575)
    create_left.columnconfigure(0, weight=1)
    create_left.place(relx=.175, rely=.5, anchor="center")

    create_right = Frame(create_bg, bg="#DDDDDD", width=575, height=550)
    create_right.place(relx=.675, rely=.5, anchor="center")

    frames = [create_bg, create_left, create_right]

    displayHeader(create_left, 0.050, 0.100)
    create_photo_preview = Canvas(create_left, bg="#FFFFFF", width=250, height=250)
    create_photo_preview.place(relx=.5, rely=0.450, anchor="center")
    create_photo_text = create_photo_preview.create_text((125, 125), text="No Photo Uploaded", font=field_label)

    upload_btn = Button(create_left, text="Upload", width=13, command=lambda: uploadImage(create_photo_preview, create_photo_text), bg="#B3D687", fg="#FFFFFF", bd=0, font=buttonA)
    upload_btn.place(relx=.5, rely=0.725, anchor="center")
    back_btn = Button(create_left, text="Back", width=10, command=lambda: goToNext(frames, 2), bg="#2D2E2E", fg="#FFFFFF", bd=0, font=buttonB)
    back_btn.place(relx=.15, rely=0.950, anchor="center")

    create_form = asset.createAsset(root)
    create_form.setCreate(create_right, field_label)

    def checkCreateAsset(frames, form):
        if form.submitForm():
            approvedMessage(frames, "Asset Created\nSuccessfully!")

    create_btn = Button(create_right, text="Create", width=15, command=lambda: checkCreateAsset(frames, create_form),
                        bg="#B8D8D8", fg="#FFFFFF", bd=0, font=buttonA)
    create_btn.place(relx=.250, rely=0.975, anchor="center")
    create_form.setButton(create_btn)


def manageUser():
    global manage_page
    manage_bg = Frame(root, bg="#DDDDDD", width=825, height=600)
    manage_bg.pack()
    manage_bg.columnconfigure(0, weight=1)
    manage_bg.place(relx=.5, rely=.5, anchor="center")

    manage_form_frame = Frame(manage_bg, bg="#DDDDDD", width=300, height=550)
    manage_form_frame.place(relx=.200, rely=.5, anchor="center")

    manage_table_frame = Frame(manage_bg, bg="#191919", width=455, height=500)
    manage_table_frame.place(relx=.675, rely=.5, anchor="center")

    displayHeader(manage_form_frame, 0.050, 0.100)

    manage_page = user.manageUser(root)
    manage_page.displayUsers(manage_form_frame, field_label, buttonA)
    manage_page.displayTable(manage_table_frame)

    frames = [manage_bg, manage_form_frame, manage_table_frame]

    def performOperationsUser(frames, nextFunc):
        if manage_page.getSelected():
            goToNext(frames, nextFunc)

    create_user_btn = Button(manage_form_frame, text="Create New User", width=15, command=lambda: goToNext(frames, 5), bg="#8EB8CF",
                      fg="#FFFFFF", bd=0, font=buttonA)
    create_user_btn.place(relx=.30, rely=0.750, anchor="center")
    operation_user_btn = Button(manage_form_frame, text="Perform Operation", width=15, command=lambda: performOperationsUser(frames, 6), bg="#8EB8CF",
                      fg="#FFFFFF", bd=0, font=buttonA)
    operation_user_btn.place(relx=.30, rely=0.850, anchor="center")
    back_btn = Button(manage_form_frame, text="Back", width=10, command=lambda: goToNext(frames, 2), bg="#2D2E2E",
                      fg="#FFFFFF", bd=0, font=buttonB)
    back_btn.place(relx=.15, rely=0.950, anchor="center")


def createUser():
    global manage_page
    create_user_bg = Frame(root, bg="#DDDDDD", width=300, height=450)
    create_user_bg.columnconfigure(0, weight=1)
    create_user_bg.place(relx=.5, rely=.5, anchor="center")

    displayHeader(create_user_bg, 0.10, 0.15)
    create_user = manage_page
    create_user.setCreateNewUser(create_user_bg, field_label)

    def validateCreateUser(frames):
        if create_user.checkNewUser():
            approvedMessage(frames, "User Created\nSuccessfully!")

    frames = [create_user_bg]
    change_pass_btn = Button(create_user_bg, text="Create User", height=1, width=15,
                             command=lambda: validateCreateUser(frames), bg="#8EB8CF", fg="#FFFFFF", bd=0,
                             font=buttonA)
    change_pass_btn.place(relx=.5, rely=0.800, anchor="center")

    back_btn = Button(create_user_bg, text="Back", width=10, command=lambda: goToNext(frames, 4), bg="#2D2E2E", fg="#FFFFFF", bd=0, font=buttonB)
    back_btn.place(relx=.5, rely=0.900, anchor="center")


def performUsers():
    global manage_page
    operation_user_bg = Frame(root, bg="#DDDDDD", width=500, height=550)
    operation_user_bg.columnconfigure(0, weight=1)
    operation_user_bg.place(relx=.5, rely=.5, anchor="center")

    operation_table_frame = Frame(operation_user_bg, bg="#DDDDDD", width=300, height=150)
    operation_table_frame.place(relx=.5, rely=.5, anchor="center")

    displayHeader(operation_user_bg, 0.10, 0.15)
    manage_page.displaySelectedUser(operation_user_bg, operation_table_frame)

    frames = [operation_user_bg, operation_table_frame]

    def deleteUser(frames):
        if manage_page.deleteUser():
            approvedMessage(frames, "Successfully\nDeleted\nUser!")

    change_pass_btn = Button(operation_user_bg, text="Change Password", height=1, width=15,
                             command=lambda: goToNext(frames, 7), bg="#8EB8CF", fg="#FFFFFF", bd=0, font=buttonA)
    change_pass_btn.place(relx=.25, rely=0.750, anchor="center")

    delete_btn = Button(operation_user_bg, text="Delete", height=1, width=15,
                             command=lambda: deleteUser(frames), bg="#8EB8CF", fg="#FFFFFF", bd=0, font=buttonA)
    delete_btn.place(relx=.75, rely=0.750, anchor="center")

    back_btn = Button(operation_user_bg, text="Back", width=10, command=lambda: goToNext(frames, 4), bg="#2D2E2E",
                      fg="#FFFFFF", bd=0, font=buttonB)
    back_btn.place(relx=.5, rely=0.900, anchor="center")


def changePassword():
    global manage_page
    change_pass_bg = Frame(root, bg="#DDDDDD", width=300, height=450)
    change_pass_bg.columnconfigure(0, weight=1)
    change_pass_bg.place(relx=.5, rely=.5, anchor="center")

    displayHeader(change_pass_bg, 0.10, 0.15)
    manage_page.setChangePassword(change_pass_bg, field_label)

    def validateChangePassword(frames):
        if manage_page.checkChangePassword():
            approvedMessage(frames, "Password Updated\nSuccessfully!")

    frames = [change_pass_bg]
    change_pass_btn = Button(change_pass_bg, text="Change Password", height=1, width=15, command=lambda: validateChangePassword(frames), bg="#8EB8CF", fg="#FFFFFF", bd=0, font=buttonA)
    change_pass_btn.place(relx=.5, rely=0.800, anchor="center")

    back_btn = Button(change_pass_bg, text="Back", width=10, command=lambda: goToNext(frames, 6), bg="#2D2E2E", fg="#FFFFFF", bd=0, font=buttonB)
    back_btn.place(relx=.5, rely=0.900, anchor="center")


def historyPage():
    history_bg = Frame(root, bg="#DDDDDD", width=1200, height=600)
    history_bg.pack()
    history_bg.columnconfigure(0, weight=1)
    history_bg.place(relx=.5, rely=.5, anchor="center")

    history_form_frame = Frame(history_bg, bg="#DDDDDD", width=300, height=550)
    history_form_frame.place(relx=.135, rely=.5, anchor="center")

    history_table_frame = Frame(history_bg, bg="#191919", width=825, height=500)
    history_table_frame.place(relx=.625, rely=.5, anchor="center")

    displayHeader(history_form_frame, 0.050, 0.100)

    history_page = history.History(root)
    history_page.displayHistory(history_form_frame, field_label, buttonA)
    history_page.displayTable(history_table_frame)

    frames = [history_bg, history_form_frame, history_table_frame]
    back_btn = Button(history_form_frame, text="Back", width=10, command=lambda: goToNext(frames, 2), bg="#2D2E2E", fg="#FFFFFF", bd=0, font=buttonB)
    back_btn.place(relx=.15, rely=0.950, anchor="center")


def receiveAsset():
    receive_bg = Frame(root, bg="#DDDDDD", width=1200, height=600)
    receive_bg.pack()
    receive_bg.columnconfigure(0, weight=1)
    receive_bg.place(relx=.5, rely=.5, anchor="center")

    receive_form_frame = Frame(receive_bg, bg="#DDDDDD", width=300, height=550)
    receive_form_frame.place(relx=.135, rely=.5, anchor="center")

    receive_table_frame = Frame(receive_bg, bg="#191919", width=825, height=500)
    receive_table_frame.place(relx=.625, rely=.5, anchor="center")

    displayHeader(receive_form_frame, 0.050, 0.100)

    receive_page = asset.receiveAsset(root)
    receive_page.displayReceive(receive_form_frame, field_label, buttonA)
    receive_page.displayTable(receive_table_frame)

    def validReceiveAssets(frames):
        if receive_page.checkAssets():
            approvedMessage(frames, "Assets Received!")

    frames = [receive_bg, receive_form_frame, receive_table_frame]
    receive_btn = Button(receive_form_frame, text="Receive", width=13, command=lambda: validReceiveAssets(frames), bg="#24434D",
                        fg="#FFFFFF", bd=0, font=buttonA)
    receive_btn.place(relx=.25, rely=0.750, anchor="center")
    cancel_btn = Button(receive_form_frame, text="Cancel", width=13, command=lambda: validReceiveAssets(frames), bg="#FFFFFF",
                         fg="#24434D", bd=0, font=buttonA)
    cancel_btn.place(relx=.25, rely=0.850, anchor="center")

    back_btn = Button(receive_form_frame, text="Back", width=10, command=lambda: goToNext(frames, 2), bg="#2D2E2E",
                      fg="#FFFFFF", bd=0, font=buttonB)
    back_btn.place(relx=.15, rely=0.950, anchor="center")


def importExport():
    import_bg = Frame(root, bg="#DDDDDD", width=300, height=300)
    import_bg.columnconfigure(0, weight=1)
    import_bg.place(relx=.5, rely=.5, anchor="center")

    frames = [import_bg]
    displayHeader(import_bg, 0.15, 0.25)

    import_btn = Button(import_bg, text="Import", width=15, command=lambda: goToNext(frames, 13), bg="#3C4648", fg="#FFFFFF", bd=0, font=buttonA)
    import_btn.place(relx=.5, rely=0.450, anchor="center")

    export_btn = Button(import_bg, text="Export", width=15, command=lambda: goToNext(frames, 14), bg="#3C4648", fg="#FFFFFF", bd=0, font=buttonA)
    export_btn.place(relx=.5, rely=0.650, anchor="center")

    back_btn = Button(import_bg, text="Back", width=10, command=lambda: goToNext(frames, 2), bg="#2D2E2E",
                      fg="#FFFFFF", bd=0, font=buttonB)
    back_btn.place(relx=.5, rely=0.850, anchor="center")


def importOption():
    import_bg = Frame(root, bg="#DDDDDD", width=300, height=400)
    import_bg.columnconfigure(0, weight=1)
    import_bg.place(relx=.5, rely=.5, anchor="center")

    displayHeader(import_bg, 0.15, 0.25)
    frames = [import_bg]
    import_user = table.ImportExport()
    import_user.displayImport(import_bg, sub)

    def importFile(frames):
        if import_user.importFile():
            approvedMessage(frames, "Successfully\nImported File!")

    import_btn = Button(import_bg, text="Import", width=15, command=lambda: importFile(frames), bg="#3C4648", fg="#FFFFFF", bd=0, font=buttonA)
    import_btn.place(relx=.5, rely=0.725, anchor="center")

    back_btn = Button(import_bg, text="Back", width=10, command=lambda: goToNext(frames, 12), bg="#2D2E2E",
                      fg="#FFFFFF", bd=0, font=buttonB)
    back_btn.place(relx=.5, rely=0.850, anchor="center")


def exportOption():
    export_bg = Frame(root, bg="#DDDDDD", width=300, height=400)
    export_bg.columnconfigure(0, weight=1)
    export_bg.place(relx=.5, rely=.5, anchor="center")

    export_frames = [export_bg]
    displayHeader(export_bg, 0.15, 0.25)
    export_user = table.ImportExport()

    export_font = tkfont.Font(family='Oswald', weight="bold", size=25)
    export_label = Label(export_bg, text="Successfully\nExported!", bg="#DDDDDD", fg="#6B9A39", font=export_font)
    open_btn = Button(export_bg, text="Open File", height=1, width=15,
                      command=export_user.openExport, bg="#3C4648", fg="#FFFFFF", bd=0,
                      font=buttonA)

    if not export_user.exportFile():
        export_label.config(text="Error in\nExporting!", fg="#DC5047")
        open_btn.config(state="disabled")

    export_label.place(relx=.5, rely=0.475, anchor="center")
    open_btn.place(relx=.5, rely=0.725, anchor="center")

    back_btn = Button(export_bg, text="Back to Home", height=1, width=15,
                                 command=lambda: goToNext(export_frames, 2), bg="#2D2E2E", fg="#FFFFFF", bd=0,
                                 font=buttonB)
    back_btn.place(relx=.5, rely=0.850, anchor="center")


def deleteAsset():
    delete_bg = Frame(root, bg="#DDDDDD", width=1200, height=600)
    delete_bg.pack()
    delete_bg.columnconfigure(0, weight=1)
    delete_bg.place(relx=.5, rely=.5, anchor="center")

    delete_form_frame = Frame(delete_bg, bg="#DDDDDD", width=300, height=550)
    delete_form_frame.place(relx=.135, rely=.5, anchor="center")

    delete_table_frame = Frame(delete_bg, bg="#191919", width=825, height=500)
    delete_table_frame.place(relx=.625, rely=.5, anchor="center")

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
    delete_btn.place(relx=.25, rely=0.850, anchor="center")

    back_btn = Button(delete_form_frame, text="Back", width=10, command=lambda: goToNext(frames, 2), bg="#2D2E2E",
                      fg="#FFFFFF", bd=0, font=buttonB)
    back_btn.place(relx=.15, rely=0.950, anchor="center")


login()
root.mainloop()