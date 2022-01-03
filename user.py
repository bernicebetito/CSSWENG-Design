from tkinter import *
import tkinter.font as tkfont
import random
import table
from tkinter import filedialog

class User():
    def __init__(self):
        self.username = StringVar()
        self.password = StringVar()

        self.username_field = Entry()
        self.password_field = Entry()

    def getUsername(self):
        return self.username.get()

    def checkLoginCredentials(self):
        if len(self.username.get()) > 0 and len(self.password.get()) > 0:
            if self.username.get().lower() == "manager" or self.username.get().lower() == "clerk":
                return True

        self.username_field.configure(highlightthickness=2, highlightbackground="#D64000", highlightcolor="#D64000")
        self.password_field.configure(highlightthickness=2, highlightbackground="#D64000", highlightcolor="#D64000")
        self.login_error_label.config(fg="#D64000")
        return False

    def setLogin(self, login_bg, field_label):
        login_label = tkfont.Font(family='Oswald', weight="bold", size=15)
        Label(login_bg, text="LOGIN", bg="#DDDDDD", fg="#3E3E3E", font=login_label).place(relx=.5, rely=0.375, anchor="center")

        Label(login_bg, text="Username", bg="#DDDDDD", fg="#363636", font=field_label).place(relx=.5, rely=0.45, anchor="center")
        self.username_field = Entry(login_bg, textvariable=self.username, bd=0)
        self.username_field.focus()
        self.username_field.place(height=20, width=225, relx=.5, rely=0.5, anchor="center")

        Label(login_bg, text="Password", bg="#DDDDDD", fg="#363636", font=field_label).place(relx=.5, rely=0.6, anchor="center")
        self.password_field = Entry(login_bg, textvariable=self.password, show="*", width=35, bd=0)
        self.password_field.place(height=20, width=225, relx=.5, rely=0.65, anchor="center")

        self.login_error_label = Label(login_bg, text="Invalid Username and / or Password", bg="#DDDDDD", fg="#DDDDDD", font=field_label)
        self.login_error_label.place(relx=.5, rely=0.725, anchor="center")


class manageUser():
    def __init__(self, root):
        self.root = root
        self.manage_username = StringVar()
        self.manage_role_manager = Radiobutton()
        self.manage_role_clerk = Radiobutton()
        self.manage_role_int = IntVar()
        self.manage_table_contents = []
        self.operations_btn = Button()

        # Create New User
        self.create_username = StringVar()
        self.create_password = StringVar()
        self.create_user_role = "clerk"
        self.create_role_int = IntVar()

        self.create_username_field = Entry()
        self.create_password_field = Entry()
        self.create_role_label = Label()
        self.create_role_manager = Radiobutton()
        self.create_role_clerk = Radiobutton()

        # Selected User
        self.selected_user = -1

        # Change Password
        self.curr_password = StringVar()
        self.new_password = StringVar()
        self.confirm_password = StringVar()

        self.current_field = Entry()
        self.new_field = Entry()
        self.confirm_field = Entry()

    def displayUsers(self, manage_form_frame, field_label, buttonA):
        Label(manage_form_frame, text="Search by Username", bg="#DDDDDD", fg="#363636", font=field_label).place(relx=0.325, rely=0.200, anchor="center")
        Entry(manage_form_frame, textvariable=self.manage_username, bd=0).place(height=20, width=225, relx=.5, rely=0.250, anchor="center")

        Label(manage_form_frame, text="Search by Role", bg="#DDDDDD", fg="#363636", font=field_label).place(relx=.5, rely=0.325, anchor="center")
        self.manage_role_manager = Radiobutton(manage_form_frame, text="Manager", bg="#DDDDDD", variable=self.manage_role_int, value=1)
        self.manage_role_manager.place(relx=.30, rely=0.375, anchor="center")

        self.manage_role_clerk = Radiobutton(manage_form_frame, text="Inventory Clerk", bg="#DDDDDD", variable=self.manage_role_int, value=2)
        self.manage_role_clerk.place(relx=.65, rely=0.375, anchor="center")

        search_btn = Button(manage_form_frame, text="Search", width=13, command=lambda: self.filterTable(), bg="#DC5047", fg="#FFFFFF", bd=0, font=buttonA)
        search_btn.place(relx=.5, rely=0.475, anchor="center")

    def displayTable(self, manage_table_frame):
        manage_canvas = Canvas(manage_table_frame, bg="#191919", width=455, height=500)

        manage_measurements = {
            "cell_width": 150,
            "cell_height": 75,
            "rows": 100,
            "columns": 3
        }
        manage_table_header = ["Modify", "Username", "Role", "Password"]

        self.manage_table_contents = []
        self.root.table_image = []
        for row in range(100):
            curr_row = []
            for column in range(4):
                if row == 0:
                    curr_row.append(manage_table_header[column])
                else:
                    if column == 0:
                        curr_row.append("")
                    elif column == 1:
                        curr_row.append("user_" + str(row))
                    elif column == 2:
                        rand_role = random.randint(1, 2)
                        if rand_role == 1:
                            curr_row.append("Manager")
                        else:
                            curr_row.append("Inventory Clerk")
                    else:
                        curr_row.append("p@s5w0rD!_" + str(row))

            self.manage_table_contents.append(curr_row)

        self.manage_table = table.Table(manage_measurements, manage_canvas, self.manage_table_contents)
        self.manage_table.setScrollbars(manage_table_frame)
        self.manage_table.optionsTable(9, 7, "radio")
        manage_canvas.configure(scrollregion=manage_canvas.bbox("all"))

    def filterTable(self):
        # Where filtering would happen
        print("Filter button clicked")

    def getSelected(self):
        self.selected_user = self.manage_table.getSelectedRadio()
        if self.selected_user > -1:
            return True
        return False

    def checkNewUser(self):
        if len(self.create_username.get()) > 0 and len(self.create_password.get()) > 0 and self.create_role_int.get() > 0:
            if self.create_role_int.get() == 1:
                self.create_user_role = "manager"
            else:
                self.create_user_role = "clerk"
            return True
        else:
            self.user_error_label.config(text="Please Fill Up All Fields")
            current_font = tkfont.Font(self.create_role_label, self.create_role_label.cget("font"))
            current_font.configure(underline=True)
            self.create_role_label.config(font=current_font)
            self.create_role_label.config(fg="#D64000")
            self.create_username_field.configure(highlightthickness=2, highlightbackground="#D64000", highlightcolor="#D64000")
            self.create_password_field.configure(highlightthickness=2, highlightbackground="#D64000", highlightcolor="#D64000")
        return False

    def setCreateNewUser(self, create_user_bg, field_label):
        change_pass_label = tkfont.Font(family='Oswald', weight="bold", size=15)
        Label(create_user_bg, text="CREATE A USER", bg="#DDDDDD", fg="#3E3E3E", font=change_pass_label).place(relx=.5, rely=0.275, anchor="center")

        Label(create_user_bg, text="Username", bg="#DDDDDD", fg="#363636", font=field_label).place(relx=.5, rely=0.375, anchor="center")
        self.create_username_field = Entry(create_user_bg, textvariable=self.create_username, width=35, bd=0)
        self.create_username_field.place(height=20, width=225, relx=.5, rely=0.425, anchor="center")

        Label(create_user_bg, text="Password", bg="#DDDDDD", fg="#363636", font=field_label).place(relx=.5, rely=0.500, anchor="center")
        self.create_password_field = Entry(create_user_bg, textvariable=self.create_password, show="*", width=35, bd=0)
        self.create_password_field.place(height=20, width=225, relx=.5, rely=0.550, anchor="center")

        self.create_role_label = Label(create_user_bg, text="User Role", bg="#DDDDDD", fg="#363636", font=field_label)
        self.create_role_label.place(relx=.5, rely=0.625, anchor="center")
        self.create_role_manager = Radiobutton(create_user_bg, text="Manager", bg="#DDDDDD", variable=self.create_role_int, value=1)
        self.create_role_manager.place(relx=.35, rely=0.675, anchor="center")

        self.create_role_clerk = Radiobutton(create_user_bg, text="Clerk", bg="#DDDDDD", variable=self.create_role_int, value=2)
        self.create_role_clerk.place(relx=.65, rely=0.675, anchor="center")

        self.user_error_label = Label(create_user_bg, bg="#DDDDDD", fg="#D64000", font=field_label)
        self.user_error_label.place(relx=.5, rely=0.725, anchor="center")

    def displaySelectedUser(self, operation_frame, operation_table_frame):
        title_label = tkfont.Font(family='Oswald', size=15)
        Label(operation_frame, text="Chosen User", bg="#DDDDDD", fg="#363636", font=title_label).place(
            relx=0.5, rely=0.250, anchor="center")

        operation_canvas = Canvas(operation_table_frame, bg="#191919", width=300, height=150)
        operation_measurements = {
            "cell_width": 150,
            "cell_height": 75,
            "rows": 2,
            "columns": 2
        }
        operation_table_header = ["Username", "Role", "Password"]

        operation_table_contents = []
        for row in range(2):
            curr_row = []
            for column in range(3):
                if row == 0:
                    curr_row.append(operation_table_header[column])
                else:
                    if column == 0:
                        curr_row.append(self.manage_table_contents[self.selected_user + 1][1])
                    else:
                        curr_row.append(self.manage_table_contents[self.selected_user + 1][2])

            operation_table_contents.append(curr_row)

        self.operation_table = table.Table(operation_measurements, operation_canvas, operation_table_contents)
        operation_canvas.pack(expand=True, side=LEFT, fill=BOTH)
        self.operation_table.createTable()

    def checkChangePassword(self):
        self.change_error_label.config(text="")
        self.new_field.configure(highlightthickness=0, highlightbackground="#D64000", highlightcolor="#D64000")
        self.confirm_field.configure(highlightthickness=0, highlightbackground="#D64000", highlightcolor="#D64000")

        if len(self.new_password.get()) > 0 and len(self.confirm_password.get()) > 0:
            if self.new_password.get() == self.confirm_password.get():
                if self.new_password.get() != self.manage_table_contents[self.selected_user + 1][3]:
                    # update the account
                    return True
                else:
                    self.change_error_label.config(text="Password Must Be New")
                    self.new_field.configure(highlightthickness=2, highlightbackground="#D64000", highlightcolor="#D64000")
                    self.confirm_field.configure(highlightthickness=2, highlightbackground="#D64000", highlightcolor="#D64000")
            else:
                self.change_error_label.config(text="Passwords Do Not Match")
                self.new_field.configure(highlightthickness=2, highlightbackground="#D64000", highlightcolor="#D64000")
                self.confirm_field.configure(highlightthickness=2, highlightbackground="#D64000",
                                             highlightcolor="#D64000")

        return False

    def setChangePassword(self, change_pass_bg, field_label):
        change_pass_label = tkfont.Font(family='Oswald', weight="bold", size=15)
        Label(change_pass_bg, text="CHANGE PASSWORD", bg="#DDDDDD", fg="#3E3E3E", font=change_pass_label).place(relx=.5, rely=0.275, anchor="center")

        Label(change_pass_bg, text="Username", bg="#DDDDDD", fg="#363636", font=field_label).place(relx=.5, rely=0.375, anchor="center")
        username = Label(change_pass_bg, text=self.manage_table_contents[self.selected_user + 1][1], bg="#DDDDDD", fg="#363636", font=field_label)
        username.place(relx=.5, rely=0.425, anchor="center")
        current_font = tkfont.Font(username, username.cget("font"))
        current_font.configure(weight="bold", size=13)
        username.config(font=current_font)

        Label(change_pass_bg, text="New Password", bg="#DDDDDD", fg="#363636", font=field_label).place(relx=.5, rely=0.500, anchor="center")
        self.new_field = Entry(change_pass_bg, textvariable=self.new_password, show="*", width=35, bd=0)
        self.new_field.place(height=20, width=225, relx=.5, rely=0.550, anchor="center")

        Label(change_pass_bg, text="Confirm Password", bg="#DDDDDD", fg="#363636", font=field_label).place(relx=.5, rely=0.625, anchor="center")
        self.confirm_field = Entry(change_pass_bg, textvariable=self.confirm_password, show="*", width=35, bd=0)
        self.confirm_field.place(height=20, width=225, relx=.5, rely=0.675, anchor="center")

        self.change_error_label = Label(change_pass_bg, bg="#DDDDDD", fg="#D64000", font=field_label)
        self.change_error_label.place(relx=.5, rely=0.725, anchor="center")

    def deleteUser(self):
        # Account deletion would happen here
        print("Delete User")
        return True


class ImportExport():
    def __init__(self):
        self.import_filename = ""
        self.export_filename = "prime_properties_export.txt"

    def uploadFile(self):
        fileTypes = [('All Files', '*.*')]
        self.import_filename = filedialog.askopenfilename(filetypes=fileTypes)
        if len(self.import_filename) > 0:
            display_name = self.import_filename.split('/')[len(self.import_filename.split('/')) - 1]
            self.chosen_header.configure(text=display_name)

    def importFile(self):
        if len(self.import_filename) > 0:
            return True
        return False

    def exportFile(self):
        return True

    def openExport(self):
        print(self.export_filename)

    def displayImport(self, import_bg, sub):
        self.choose_header = Label(import_bg, text="Choose a File to Import", bg="#DDDDDD", fg="#6A6A6A", font=sub)
        self.choose_header.place(relx=.5, rely=0.375, anchor="center")

        self.chosen_header = Label(import_bg, text="No File Chosen", width=25, bg="#EAEAEA", fg="#191919", font=sub)
        self.chosen_header.place(relx=.5, rely=0.450, anchor="center")

        btn_font = tkfont.Font(family='Open Sans', weight="bold", size=13)
        self.choose_btn = Button(import_bg, text="Choose File", width=15, command=lambda: self.uploadFile(),
                            bg="#667275", fg="#FFFFFF", bd=0, font=btn_font)
        self.choose_btn.place(relx=.5, rely=0.550, anchor="center")