from tkinter import *
import tkinter.font as tkfont
from PIL import Image, ImageTk
from tkinter import filedialog
import user, asset, history, table, db

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


def approvedMessage(frames, message, success):
    for i in frames:
        i.destroy()

    approved_bg = Frame(root, bg="#DDDDDD", width=300, height=300)
    approved_bg.columnconfigure(0, weight=1)
    approved_bg.place(relx=.5, rely=.5, anchor="center")

    displayHeader(approved_bg, 0.15, 0.25)

    approved_font = tkfont.Font(family='Oswald', weight="bold", size=25)
    approved_label = Label(approved_bg, text=message, bg="#DDDDDD", fg="#6B9A39", font=approved_font)
    approved_label.place(relx=.5, rely=0.5, anchor="center")

    if not success:
        approved_label.config(fg="#DC5047")

    approved_frames = [approved_bg]
    approved_btn = Button(approved_bg, text="Back to Home", height=1, width=15,
                                 command=lambda: goToNext(approved_frames, 2), bg="#2D2E2E", fg="#FFFFFF", bd=0,
                                 font=buttonB)
    approved_btn.place(relx=.5, rely=0.850, anchor="center")


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
            findAsset()
        elif nextFunc == 9:  # History
            historyPage()
        elif nextFunc == 10:  # Receive
            receiveAsset()
        elif nextFunc == 11:  # Update Asset
            updateAsset()
        elif nextFunc == 12:  # Update Asset Page
            updatePage()
        elif nextFunc == 13:  # Import & Export
            importExport()
        elif nextFunc == 14:  # Import
            importOption()
        elif nextFunc == 15:  # Export
            exportOption()
        elif nextFunc == 16:  # Delete
            deleteAsset()
        elif nextFunc == 17:  # Receipt
            receiptPage()
        elif nextFunc == 18:  # Summary
            summaryPage()
        elif nextFunc == 19:  # Receipt for update
            updateReceipt()
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
        global valid_login, role
        if login_credentials.checkLoginCredentials():
            role = login_credentials.getRole()
            valid_login = True
            goToNext(frames, nextFunc)
        else:
            valid_login = False

    frames = [login_bg]
    login_btn = Button(login_bg, text="Login", height=1, width=13, command=lambda:checkCredentials(frames, 2), bg="#6D94AA", fg="#FFFFFF", bd=0, font=buttonA)
    login_btn.place(relx=.5, rely=0.8, anchor="center")


def nav():
    if role == "manager":
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
    import_btn = Button(nav_bg, text="Import & Export", width=15, command=lambda: goToNext(frames, 13), bg="#3C4648", fg="#FFFFFF", bd=0, font=buttonA)
    delete_btn = Button(nav_bg, text="Delete", width=15, command=lambda: goToNext(frames, 16), bg="#FE5F55", fg="#FFFFFF", bd=0, font=buttonA)
    logout_btn = Button(nav_bg, text="Logout", width=10, command=lambda: goToNext(frames, 1), bg="#363636", fg="#FFFFFF", bd=0, font=buttonB)

    if role == "manager":
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
    elif role == "clerk":
        displayHeader(nav_bg, 0.15, 0.20)

        create_asset_btn.place(relx=.5, rely=0.350, anchor="center")
        find_btn.place(relx=.5, rely=0.450, anchor="center")
        receive_btn.place(relx=.5, rely=0.550, anchor="center")
        update_btn.place(relx=.5, rely=0.650, anchor="center")
        import_btn.place(relx=.5, rely=0.750, anchor="center")
        logout_btn.place(relx=.5, rely=0.850, anchor="center")


def createAsset():
    global photo_filename
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
    create_form = asset.createAsset(root)
    create_form.displayUploadImage(create_left, buttonA, field_label)
    create_form.displayCreate(create_right, field_label)
    back_btn = Button(create_left, text="Back", width=10, command=lambda: goToNext(frames, 2), bg="#2D2E2E", fg="#FFFFFF", bd=0, font=buttonB)
    back_btn.place(relx=.15, rely=0.950, anchor="center")

    def checkCreateAsset(frames):
        success_submit = create_form.submitForm(login_credentials.username.get())
        if success_submit is True:
            approvedMessage(frames, "Asset Created\nSuccessfully!", True)
        elif success_submit is not None:
            approvedMessage(frames, "Error Creating\nAsset!", False)

    create_btn = Button(create_right, text="Create", width=15, command=lambda: checkCreateAsset(frames),
                        bg="#B8D8D8", fg="#FFFFFF", bd=0, font=buttonA)
    create_btn.place(relx=.250, rely=0.975, anchor="center")


def manageUser():
    global manage_page
    manage_bg = Frame(root, bg="#DDDDDD", width=1000, height=600)
    manage_bg.pack()
    manage_bg.columnconfigure(0, weight=1)
    manage_bg.place(relx=.5, rely=.5, anchor="center")

    manage_form_frame = Frame(manage_bg, bg="#DDDDDD", width=300, height=550)
    manage_form_frame.place(relx=.175, rely=.5, anchor="center")

    manage_table_frame = Frame(manage_bg, bg="#191919", width=605, height=500)
    manage_table_frame.place(relx=.665, rely=.5, anchor="center")

    displayHeader(manage_form_frame, 0.050, 0.100)

    manage_page = user.manageUser(root)
    manage_page.displayUsers(manage_form_frame, field_label, buttonA, buttonB)
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
            approvedMessage(frames, "User Created\nSuccessfully!", True)
        else:
            approvedMessage(frames, "Error\nCreating User!", False)

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

    operation_table_frame = Frame(operation_user_bg, bg="#DDDDDD", width=450, height=150)
    operation_table_frame.place(relx=.5, rely=.5, anchor="center")

    displayHeader(operation_user_bg, 0.10, 0.15)
    manage_page.displaySelectedUser(operation_user_bg, operation_table_frame)

    frames = [operation_user_bg, operation_table_frame]

    def deleteUser(frames):
        if manage_page.deleteUser():
            approvedMessage(frames, "Successfully\nDeleted\nUser!", True)
        else:
            approvedMessage(frames, "Error\nDeleting User!", False)

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
            approvedMessage(frames, "Password Updated\nSuccessfully!", True)
        else:
            approvedMessage(frames, "Error Updating\nPassword!", False)

    frames = [change_pass_bg]
    change_pass_btn = Button(change_pass_bg, text="Change Password", height=1, width=15, command=lambda: validateChangePassword(frames), bg="#8EB8CF", fg="#FFFFFF", bd=0, font=buttonA)
    change_pass_btn.place(relx=.5, rely=0.800, anchor="center")

    back_btn = Button(change_pass_bg, text="Back", width=10, command=lambda: goToNext(frames, 6), bg="#2D2E2E", fg="#FFFFFF", bd=0, font=buttonB)
    back_btn.place(relx=.5, rely=0.900, anchor="center")


def summaryPage():

    global findAsset_page

    summary_bg = Frame(root, bg="#DDDDDD", width=1200, height=600)
    summary_bg.pack()
    summary_bg.columnconfigure(0, weight=1)
    summary_bg.place(relx=.5, rely=.5, anchor="c")

    summary_form_frame = Frame(summary_bg, bg="#DDDDDD", width=300, height=550)
    summary_form_frame.place(relx=.135, rely=.5, anchor="c")

    displayHeader(summary_form_frame, 0.050, 0.100)

    findAsset_page.displaySummaryDetails(summary_bg, summary_form_frame, field_label)
    findAsset_page.displaySummaryAssets(summary_bg)

    def confirmAssets(frames):
        findAsset_page.operationSuccess()
        approvedMessage(frames, "Operation performed", True)

    frames = [summary_bg]

    confirm_btn = Button(summary_form_frame, text="Confirm", width=13, command=lambda: confirmAssets(frames), bg="#24434D",
                        fg="#FFFFFF", bd=0, font=buttonA)
    confirm_btn.place(relx=.25, rely=0.850, anchor="c")

    back_btn = Button(summary_form_frame, text="Back", width=10, command=lambda: goToNext(frames, 8), bg="#2D2E2E", fg="#FFFFFF", bd=0, font=buttonB)
    back_btn.place(relx=.15, rely=0.950, anchor="c")


def receiptPage():

    global findAsset_page

    receipt_bg = Frame(root, bg="#DDDDDD", width=500, height=550)
    receipt_bg.columnconfigure(0, weight=1)
    receipt_bg.place(relx=.5, rely=.5, anchor="center")

    displayHeader(receipt_bg, 0.10, 0.15)
    findAsset_page.displayReceipt(receipt_bg, field_label)

    frames = [receipt_bg]

    def operationSuccess(frames):
        if findAsset_page.assetOperationSuccess():
            #approvedMessage(frames, "Successful operation", True)
            goToNext(frames, 18)

    confirm_btn = Button(receipt_bg, text="Confirm", height=1, width=15,
                             command=lambda: operationSuccess(frames), bg="#8EB8CF", fg="#FFFFFF", bd=0, font=buttonA)
    confirm_btn.place(relx=.5, rely=0.800, anchor="center")

    back_btn = Button(receipt_bg, text="Back", width=10, command=lambda: goToNext(frames, 8), bg="#2D2E2E",
                      fg="#FFFFFF", bd=0, font=buttonB)
    back_btn.place(relx=.5, rely=0.900, anchor="center")


def findAsset():

    global findAsset_page

    findAsset_bg = Frame(root, bg="#DDDDDD", width=1200, height=600)
    findAsset_bg.pack()
    findAsset_bg.columnconfigure(0, weight=1)
    findAsset_bg.place(relx=.5, rely=.5, anchor="c")

    findAsset_form_frame = Frame(findAsset_bg, bg="#DDDDDD", width=300, height=550)
    findAsset_form_frame.place(relx=.135, rely=.5, anchor="c")

    displayHeader(findAsset_form_frame, 0.050, 0.100)

    findAsset_page = asset.findAsset(root)
    findAsset_page.displayFind(findAsset_form_frame, field_label, buttonA, buttonB)
    findAsset_page.displayTable(findAsset_bg)

    def confirmAssets(frames):
        if findAsset_page.getSelected():
            for widget in findAsset_form_frame.winfo_children():
                widget.destroy()

            displayHeader(findAsset_form_frame, 0.050, 0.100)

            move_btn = Button(findAsset_form_frame, text="Move", width=13, command=lambda: performOperations(frames, 1), bg="#6D94AA",
                              fg="#FFFFFF", bd=0, font=buttonA)
            move_btn.place(relx=.5, rely=0.25, anchor="center")

            lend_btn = Button(findAsset_form_frame, text="Lend", width=13, command=lambda: performOperations(frames, 2), bg="#6D94AA",
                              fg="#FFFFFF", bd=0, font=buttonA)
            lend_btn.place(relx=.5, rely=0.35, anchor="center")

            store_btn = Button(findAsset_form_frame, text="Store", width=13, command=lambda: performOperations(frames, 3), bg="#6D94AA",
                              fg="#FFFFFF", bd=0, font=buttonA)
            store_btn.place(relx=.5, rely=0.45, anchor="center")

            sell_btn = Button(findAsset_form_frame, text="Sell", width=13, command=lambda: performOperations(frames, 4), bg="#6D94AA",
                              fg="#FFFFFF", bd=0, font=buttonA)
            sell_btn.place(relx=.5, rely=0.55, anchor="center")

            dispose_btn = Button(findAsset_form_frame, text="Dispose", width=13, command=lambda: performOperations(frames, 5), bg="#6D94AA",
                              fg="#FFFFFF", bd=0, font=buttonA)
            dispose_btn.place(relx=.5, rely=0.65, anchor="center")

            
            back_btn = Button(findAsset_form_frame, text="Back", width=10, command=lambda: goToNext(frames, 8), bg="#2D2E2E",
                              fg="#FFFFFF", bd=0, font=buttonB)
            back_btn.place(relx=.15, rely=0.950, anchor="center")

    def performOperations(frames, operation_no):
        ## Check
        findAsset_page.setOperation(operation_no, login_credentials.username.get())
        goToNext(frames, 17)

    frames = [findAsset_bg, findAsset_form_frame, findAsset_page.findAsset_table_frame]

    operation_btn = Button(findAsset_form_frame, text="Operations", width=13, command=lambda: confirmAssets(frames), bg="#24434D",
                        fg="#FFFFFF", bd=0, font=buttonA)
    operation_btn.place(relx=.25, rely=0.850, anchor="c")

    back_btn = Button(findAsset_form_frame, text="Back", width=10, command=lambda: goToNext(frames, 2), bg="#2D2E2E", fg="#FFFFFF", bd=0, font=buttonB)
    back_btn.place(relx=.15, rely=0.950, anchor="c")


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
    history_page.displayHistory(history_form_frame, field_label, buttonA, buttonB)
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
    receive_page.displayReceive(receive_form_frame, field_label, buttonA, buttonB)
    receive_page.displayTable(receive_table_frame)

    def confirmSelected(frames, operation):
        if receive_page.checkAssets():
            for widget in receive_form_frame.winfo_children():
                widget.destroy()

            displayHeader(receive_form_frame, 0.050, 0.100)
            filter_ins = Label(receive_form_frame, text="Confirm Assets to " + operation, bg="#DDDDDD", fg="#363636", font=header)
            filter_ins.place(relx=.5, rely=.5, anchor="center")
            current_font = tkfont.Font(filter_ins, filter_ins.cget("font"))
            current_font.configure(size=18, slant="italic")
            filter_ins.config(font=current_font)

            back_btn = Button(receive_form_frame, text="Confirm", width=13, command=lambda: validReceiveAssets(frames), bg="#FE5F55",
                              fg="#FFFFFF", bd=0, font=buttonA)
            back_btn.place(relx=.20, rely=0.850, anchor="center")

            if operation.lower() == "cancel":
                back_btn.config(command=lambda: validCancelAssets(frames))

            back_btn = Button(receive_form_frame, text="Back", width=10, command=lambda: goToNext(frames, 10), bg="#2D2E2E",
                              fg="#FFFFFF", bd=0, font=buttonB)
            back_btn.place(relx=.15, rely=0.950, anchor="center")

    def validReceiveAssets(frames):
        if receive_page.receiveAssets():
            approvedMessage(frames, "Assets Received!", True)
        else:
            approvedMessage(frames, "Error\nReceiving Assets!", False)

    def validCancelAssets(frames):
        if receive_page.cancelAssets():
            approvedMessage(frames, "Assets Cancelled!", True)
        else:
            approvedMessage(frames, "Error\nCancelling Assets!", False)

    frames = [receive_bg, receive_form_frame, receive_table_frame]
    receive_btn = Button(receive_form_frame, text="Receive", width=13, command=lambda: confirmSelected(frames, "Receive"), bg="#24434D",
                        fg="#FFFFFF", bd=0, font=buttonA)
    receive_btn.place(relx=.25, rely=0.750, anchor="center")
    cancel_btn = Button(receive_form_frame, text="Cancel", width=13, command=lambda: confirmSelected(frames, "Cancel"), bg="#FFFFFF",
                         fg="#24434D", bd=0, font=buttonA)
    cancel_btn.place(relx=.25, rely=0.850, anchor="center")

    back_btn = Button(receive_form_frame, text="Back", width=10, command=lambda: goToNext(frames, 2), bg="#2D2E2E",
                      fg="#FFFFFF", bd=0, font=buttonB)
    back_btn.place(relx=.15, rely=0.950, anchor="center")


def updateAsset():

    global update_page

    update_bg = Frame(root, bg="#DDDDDD", width=1200, height=600)
    update_bg.pack()
    update_bg.columnconfigure(0, weight=1)
    update_bg.place(relx=.5, rely=.5, anchor="c")

    update_form_frame = Frame(update_bg, bg="#DDDDDD", width=300, height=550)
    update_form_frame.place(relx=.135, rely=.5, anchor="c")

    displayHeader(update_form_frame, 0.050, 0.100)

    update_page = asset.updateAsset(root)
    update_page.displayFind(update_form_frame, field_label, buttonA, buttonB)
    update_page.displayTable(update_bg)

    def confirmUpdate(frames, nextFunc):
        if update_page.getSelected():
            goToNext(frames, nextFunc)
        else: print("Fail")

    def validUpdateAssets(frames):
        if update_page.updateAssets():
            approvedMessage(frames, "Assets Updated\nSuccessfully!", True)
        else:
            approvedMessage(frames, "Error Updating\nAssets!", False)

    frames = [update_bg, update_form_frame, update_page.update_table_frame]

    update_btn = Button(update_form_frame, text="Update", width=13, command=lambda: confirmUpdate(frames, 12), bg="#24434D",
                        fg="#FFFFFF", bd=0, font=buttonA)
    update_btn.place(relx=.25, rely=0.850, anchor="c")

    back_btn = Button(update_form_frame, text="Back", width=10, command=lambda: goToNext(frames, 2), bg="#2D2E2E", fg="#FFFFFF", bd=0, font=buttonB)
    back_btn.place(relx=.15, rely=0.950, anchor="c")


def updatePage():

    global update_page
    global photo_filename

    update_selected_bg = Frame(root, bg="#DDDDDD", width=950, height=600)
    update_selected_bg.columnconfigure(0, weight=1)
    update_selected_bg.place(relx=.5, rely=.5, anchor="center")

    update_left = Frame(update_selected_bg, bg="#DDDDDD", width=300, height=575)
    update_left.columnconfigure(0, weight=1)
    update_left.place(relx=.175, rely=.5, anchor="center")

    update_right = Frame(update_selected_bg, bg="#DDDDDD", width=575, height=550)
    update_right.place(relx=.675, rely=.5, anchor="center")

    frames = [update_selected_bg, update_left, update_right]

    displayHeader(update_left, 0.050, 0.100)
    update_page.displayUploadedImage(update_left, buttonA, field_label)
    update_page.displayDetails(update_right, field_label)


    def checkUpdateAsset(frames, form):

        '''
        if form.submitForm(login_credentials.username.get()):
            ## Check inputs
            approvedMessage(frames, "Changes successfully\nsent for approval", True)
        '''

        if form.checkForm(login_credentials.username.get()):
            goToNext(frames, 19) 

    back_btn = Button(update_left, text="Back", width=10, command=lambda: goToNext(frames, 2), bg="#2D2E2E", fg="#FFFFFF", bd=0, font=buttonB)
    back_btn.place(relx=.15, rely=0.950, anchor="center")

    update_btn = Button(update_right, text="Update", width=15, command=lambda: checkUpdateAsset(frames, update_page),
                        bg="#B8D8D8", fg="#FFFFFF", bd=0, font=buttonA)
    update_btn.place(relx=.250, rely=0.975, anchor="center")
    update_page.setButton(update_btn)


def updateReceipt():

    global update_page

    receipt_bg = Frame(root, bg="#DDDDDD", width=500, height=550)
    receipt_bg.columnconfigure(0, weight=1)
    receipt_bg.place(relx=.5, rely=.5, anchor="center")

    displayHeader(receipt_bg, 0.10, 0.15)
    update_page.displayReceipt(receipt_bg, field_label)

    frames = [receipt_bg]

    def operationSuccess(frames):
        if update_page.assetOperationSuccess():
            approvedMessage(frames, "Successful operation", True)
            #approvedMessage(frames, "Changes successfully\nsent for approval", True)
        else:
            approvedMessage(frames, "Try Again", False)

    confirm_btn = Button(receipt_bg, text="Confirm", height=1, width=15,
                             command=lambda: operationSuccess(frames), bg="#8EB8CF", fg="#FFFFFF", bd=0, font=buttonA)
    confirm_btn.place(relx=.5, rely=0.800, anchor="center")

    back_btn = Button(receipt_bg, text="Back", width=10, command=lambda: goToNext(frames, 11), bg="#2D2E2E",
                      fg="#FFFFFF", bd=0, font=buttonB)
    back_btn.place(relx=.5, rely=0.900, anchor="center")


def importExport():
    import_bg = Frame(root, bg="#DDDDDD", width=300, height=300)
    import_bg.columnconfigure(0, weight=1)
    import_bg.place(relx=.5, rely=.5, anchor="center")

    frames = [import_bg]
    displayHeader(import_bg, 0.15, 0.25)

    import_btn = Button(import_bg, text="Import", width=15, command=lambda: goToNext(frames, 14), bg="#3C4648", fg="#FFFFFF", bd=0, font=buttonA)
    import_btn.place(relx=.5, rely=0.450, anchor="center")

    export_btn = Button(import_bg, text="Export", width=15, command=lambda: goToNext(frames, 15), bg="#3C4648", fg="#FFFFFF", bd=0, font=buttonA)
    export_btn.place(relx=.5, rely=0.650, anchor="center")

    back_btn = Button(import_bg, text="Back", width=10, command=lambda: goToNext(frames, 2), bg="#2D2E2E",
                      fg="#FFFFFF", bd=0, font=buttonB)
    back_btn.place(relx=.5, rely=0.850, anchor="center")


def importOption():
    import_bg = Frame(root, bg="#DDDDDD", width=300, height=550)
    import_bg.columnconfigure(0, weight=1)
    import_bg.place(relx=.5, rely=.5, anchor="center")

    displayHeader(import_bg, 0.075, 0.125)
    frames = [import_bg]
    import_user = table.ImportExport()
    import_user.displayImport(import_bg, sub)

    def importFile(frames):
        import_files = import_user.importFile()
        if import_files is True:
            approvedMessage(frames, "Successfully\nImported Files!", True)
        elif import_files is not None:
            approvedMessage(frames, "Error Importing\nFiles!", False)

    import_btn = Button(import_bg, text="Import", width=15, command=lambda: importFile(frames), bg="#3C4648", fg="#FFFFFF", bd=0, font=buttonA)
    import_btn.place(relx=.5, rely=0.850, anchor="center")

    back_btn = Button(import_bg, text="Back", width=10, command=lambda: goToNext(frames, 2), bg="#2D2E2E",
                      fg="#FFFFFF", bd=0, font=buttonB)
    back_btn.place(relx=.5, rely=0.925, anchor="center")


def exportOption():
    export_bg = Frame(root, bg="#DDDDDD", width=300, height=400)
    export_bg.columnconfigure(0, weight=1)
    export_bg.place(relx=.5, rely=.5, anchor="center")

    export_frames = [export_bg]
    displayHeader(export_bg, 0.15, 0.25)
    export_user = table.ImportExport()

    export_font = tkfont.Font(family='Oswald', weight="bold", size=25)
    export_label = Label(export_bg, text="Successfully\nExported!", bg="#DDDDDD", fg="#6B9A39", font=export_font)
    open_btn = Button(export_bg, text="Open Folder", height=1, width=15,
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

    displayHeader(delete_form_frame, 0.050, 0.100)

    delete_page = asset.deleteAsset(root)
    delete_page.displayDelete(delete_form_frame, field_label, buttonA, buttonB)
    delete_page.displayTable(delete_bg)

    def confirmDelete(frames):
        if delete_page.getSelected():
            for widget in delete_form_frame.winfo_children():
                widget.destroy()

            displayHeader(delete_form_frame, 0.050, 0.100)
            filter_ins = Label(delete_form_frame, text="Confirm Assets to Delete", bg="#DDDDDD", fg="#363636", font=header)
            filter_ins.place(relx=.5, rely=.5, anchor="center")
            current_font = tkfont.Font(filter_ins, filter_ins.cget("font"))
            current_font.configure(size=18, slant="italic")
            filter_ins.config(font=current_font)

            back_btn = Button(delete_form_frame, text="Confirm", width=13, command=lambda: validDeleteAssets(frames), bg="#FE5F55",
                              fg="#FFFFFF", bd=0, font=buttonA)
            back_btn.place(relx=.20, rely=0.850, anchor="center")
            back_btn = Button(delete_form_frame, text="Back", width=10, command=lambda: goToNext(frames, 15), bg="#2D2E2E",
                              fg="#FFFFFF", bd=0, font=buttonB)
            back_btn.place(relx=.15, rely=0.950, anchor="center")

    def validDeleteAssets(frames):
        if delete_page.deleteAssets():
            approvedMessage(frames, "Assets Deleted\nSuccessfully!", True)
        else:
            approvedMessage(frames, "Error Deleting\nAssets!", False)

    frames = [delete_bg, delete_form_frame, delete_page.delete_table_frame]
    delete_btn = Button(delete_form_frame, text="Delete", width=13, command=lambda: confirmDelete(frames), bg="#FE5F55",
                        fg="#FFFFFF", bd=0, font=buttonA)
    delete_btn.place(relx=.25, rely=0.850, anchor="center")

    back_btn = Button(delete_form_frame, text="Back", width=10, command=lambda: goToNext(frames, 2), bg="#2D2E2E",
                      fg="#FFFFFF", bd=0, font=buttonB)
    back_btn.place(relx=.15, rely=0.950, anchor="center")


login()
root.mainloop()