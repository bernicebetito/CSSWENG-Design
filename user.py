from tkinter import *
import tkinter.font as tkfont
import table, db

class User():
    def __init__(self):
        self.user = tuple()
        self.username = StringVar()
        self.password = StringVar()
        self.role = ""

        self.username_field = Entry()
        self.password_field = Entry()

    def getRole(self):
        if len(self.user) > 0:
            return self.user[2]
        return "None"

    def checkLoginCredentials(self):
        if len(self.username.get()) > 0 and len(self.password.get()) > 0:
            database = db.Database()
            self.user = database.getUser(self.username.get(), self.password.get())
            if type(self.user) == tuple:
                if len(self.user) > 0:
                    return True
            else:
                self.user = tuple()

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

        # Database
        self.database = db.Database()

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

    def displayUsers(self, manage_form_frame, field_label, buttonA, buttonB):
        Label(manage_form_frame, text="Search by Username", bg="#DDDDDD", fg="#363636", font=field_label).place(relx=0.325, rely=0.200, anchor="center")
        Entry(manage_form_frame, textvariable=self.manage_username, bd=0).place(height=20, width=225, relx=.5, rely=0.250, anchor="center")

        Label(manage_form_frame, text="Search by Role", bg="#DDDDDD", fg="#363636", font=field_label).place(relx=.5, rely=0.325, anchor="center")
        self.manage_role_manager = Radiobutton(manage_form_frame, text="Manager", bg="#DDDDDD", variable=self.manage_role_int, value=1)
        self.manage_role_manager.place(relx=.30, rely=0.375, anchor="center")

        self.manage_role_clerk = Radiobutton(manage_form_frame, text="Inventory Clerk", bg="#DDDDDD", variable=self.manage_role_int, value=2)
        self.manage_role_clerk.place(relx=.65, rely=0.375, anchor="center")

        search_btn = Button(manage_form_frame, text="Search", width=13, command=lambda: self.filterTable(), bg="#DC5047", fg="#FFFFFF", bd=0, font=buttonA)
        search_btn.place(relx=.5, rely=0.475, anchor="center")

        clear_btn = Button(manage_form_frame, text="Clear Filter", width=13, command=lambda: self.filterTable(), bg="#404040", fg="#FFFFFF", bd=0, font=buttonB)
        clear_btn.place(relx=.5, rely=0.555, anchor="center")

    def displayTable(self, manage_table_frame):
        self.manage_canvas = Canvas(manage_table_frame, bg="#191919", width=605, height=500)
        manage_table_frame = manage_table_frame

        manage_filter = {"username": "", "role": ""}
        manage_measurements = {"cell_width": 150, "cell_height": 75, "rows": self.getContent(manage_filter), "columns": 4}
        self.manage_table = table.Table(manage_measurements, self.manage_canvas, self.manage_table_contents)
        self.manage_table.setScrollbars(manage_table_frame)
        self.manage_table.optionsTable(11, "radio")
        self.manage_canvas.configure(scrollregion=self.manage_canvas.bbox("all"))

    def getContent(self, filter_val):
        self.manage_table_contents = []
        manage_table_header = ["Modify", "Username", "Role", "Password"]
        curr_row = []
        for column in manage_table_header:
            curr_row.append(column)
        self.manage_table_contents.append(curr_row)

        users = self.database.viewTable(0, filter_val)
        if type(users) == list:
            for row in range(len(users)):
                curr_row = []
                for column in range(-1, len(users[row])):
                    if column == -1:
                        curr_row.append("")
                    else:
                        curr_row.append(users[row][column])
                self.manage_table_contents.append(curr_row)
            return len(users) + 1
        return 0

    def filterTable(self):
        self.manage_canvas.delete("all")

        if len(self.manage_username.get()) > 0 or self.manage_role_int.get() > 0:
            role = ""
            if self.manage_role_int.get() == 1:
                role = "manager"
            elif self.manage_role_int.get() == 2:
                role = "clerk"
            manage_filter = {"username": self.manage_username.get(), "role": role}
            self.manage_username.set("")
            self.manage_role_int.set(0)
        else:
            manage_filter = {"username": "", "role": ""}

        self.manage_table.rows = self.getContent(manage_filter)
        self.manage_table.contents = self.manage_table_contents
        self.manage_table.optionsTable(11, "radio")
        self.manage_canvas.configure(scrollregion=self.manage_canvas.bbox("all"))

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

            if self.database.createUser(self.create_username.get(), self.create_password.get(), self.create_user_role):
                return True

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

        operation_canvas = Canvas(operation_table_frame, bg="#191919", width=450, height=150)
        operation_measurements = {
            "cell_width": 150,
            "cell_height": 75,
            "rows": 2,
            "columns": 3
        }
        operation_table_header = ["Username", "Role", "Password"]

        operation_table_contents = []
        for row in range(2):
            curr_row = []
            for column in range(3):
                if row == 0:
                    curr_row.append(operation_table_header[column])
                else:
                    curr_row.append(self.manage_table_contents[self.selected_user + 1][column + 1])

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
                    if self.database.changePassword(self.manage_table_contents[self.selected_user + 1][1], self.confirm_password.get()):
                        return True
                    else:
                        self.change_error_label.config(text="Error Updating Password")
                        self.new_field.configure(highlightthickness=2, highlightbackground="#D64000", highlightcolor="#D64000")
                        self.confirm_field.configure(highlightthickness=2, highlightbackground="#D64000", highlightcolor="#D64000")
                else:
                    self.change_error_label.config(text="Password Must Be New")
                    self.new_field.configure(highlightthickness=2, highlightbackground="#D64000", highlightcolor="#D64000")
                    self.confirm_field.configure(highlightthickness=2, highlightbackground="#D64000", highlightcolor="#D64000")
            else:
                self.change_error_label.config(text="Passwords Do Not Match")
                self.new_field.configure(highlightthickness=2, highlightbackground="#D64000", highlightcolor="#D64000")
                self.confirm_field.configure(highlightthickness=2, highlightbackground="#D64000", highlightcolor="#D64000")

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
        return self.database.delUser(self.manage_table_contents[self.selected_user + 1][1])
