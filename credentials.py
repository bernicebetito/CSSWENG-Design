from tkinter import *
import tkinter.font as tkfont

class User():
    def __init__(self):
        self.username = StringVar()
        self.password = StringVar()

        self.username_field = Entry()
        self.password_field = Entry()

        self.curr_password = StringVar()
        self.new_password = StringVar()
        self.confirm_password = StringVar()

        self.current_field = Entry()
        self.new_field = Entry()
        self.confirm_field = Entry()

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
        Label(login_bg, text="LOGIN", bg="#DDDDDD", fg="#3E3E3E", font=login_label).place(relx=.5, rely=0.375, anchor="c")

        Label(login_bg, text="Username", bg="#DDDDDD", fg="#363636", font=field_label).place(relx=.5, rely=0.45, anchor="c")
        self.username_field = Entry(login_bg, textvariable=self.username, bd=0)
        self.username_field.focus()
        self.username_field.place(height=20, width=225, relx=.5, rely=0.5, anchor="c")

        Label(login_bg, text="Password", bg="#DDDDDD", fg="#363636", font=field_label).place(relx=.5, rely=0.6, anchor="c")
        self.password_field = Entry(login_bg, textvariable=self.password, show="*", width=35, bd=0)
        self.password_field.place(height=20, width=225, relx=.5, rely=0.65, anchor="c")

        self.login_error_label = Label(login_bg, text="Invalid Username and / or Password", bg="#DDDDDD", fg="#DDDDDD", font=field_label)
        self.login_error_label.place(relx=.5, rely=0.725, anchor="c")

    def checkChangePassword(self):
        self.change_error_label.config(text="")
        self.current_field.configure(highlightthickness=0, highlightbackground="#D64000", highlightcolor="#D64000")
        self.new_field.configure(highlightthickness=0, highlightbackground="#D64000", highlightcolor="#D64000")
        self.confirm_field.configure(highlightthickness=0, highlightbackground="#D64000", highlightcolor="#D64000")

        if len(self.curr_password.get()) > 0 and len(self.new_password.get()) > 0 and len(self.confirm_password.get()) > 0:
            if self.curr_password.get() == self.password.get():
                if self.curr_password.get() != self.new_password.get() and self.curr_password.get() != self.confirm_password.get():
                    if self.new_password.get() == self.confirm_password.get():
                        self.password = self.new_password
                        return True
                    else:
                        self.change_error_label.config(text="Passwords Do Not Match")
                        self.new_field.configure(highlightthickness=2, highlightbackground="#D64000", highlightcolor="#D64000")
                        self.confirm_field.configure(highlightthickness=2, highlightbackground="#D64000", highlightcolor="#D64000")
                else:
                    self.change_error_label.config(text="Password Must Be New")
                    self.new_field.configure(highlightthickness=2, highlightbackground="#D64000", highlightcolor="#D64000")
                    self.confirm_field.configure(highlightthickness=2, highlightbackground="#D64000", highlightcolor="#D64000")
            else:
                self.change_error_label.config(text="Invalid Current Password")
                self.current_field.configure(highlightthickness=2, highlightbackground="#D64000", highlightcolor="#D64000")

        return False

    def setChangePassword(self, change_pass_bg, field_label):
        change_pass_label = tkfont.Font(family='Oswald', weight="bold", size=15)
        Label(change_pass_bg, text="CHANGE PASSWORD", bg="#DDDDDD", fg="#3E3E3E", font=change_pass_label).place(relx=.5, rely=0.275, anchor="c")

        Label(change_pass_bg, text="Current Password", bg="#DDDDDD", fg="#363636", font=field_label).place(relx=.5, rely=0.375, anchor="c")
        self.current_field = Entry(change_pass_bg, textvariable=self.curr_password, show="*", width=35, bd=0)
        self.current_field.place(height=20, width=225, relx=.5, rely=0.425, anchor="c")

        Label(change_pass_bg, text="New Password", bg="#DDDDDD", fg="#363636", font=field_label).place(relx=.5, rely=0.500, anchor="c")
        self.new_field = Entry(change_pass_bg, textvariable=self.new_password, show="*", width=35, bd=0)
        self.new_field.place(height=20, width=225, relx=.5, rely=0.550, anchor="c")

        Label(change_pass_bg, text="Confirm Password", bg="#DDDDDD", fg="#363636", font=field_label).place(relx=.5, rely=0.625, anchor="c")
        self.confirm_field = Entry(change_pass_bg, textvariable=self.confirm_password, show="*", width=35, bd=0)
        self.confirm_field.place(height=20, width=225, relx=.5, rely=0.675, anchor="c")

        self.change_error_label = Label(change_pass_bg, bg="#DDDDDD", fg="#D64000", font=field_label)
        self.change_error_label.place(relx=.5, rely=0.725, anchor="c")


class createNewUser():
    def __init__(self):
        self.create_username = StringVar()
        self.create_password = StringVar()
        self.create_user_role = "clerk"
        self.create_role_int = IntVar()

        self.create_username_field = Entry()
        self.create_password_field = Entry()
        self.create_role_label = Label()
        self.create_role_manager = Radiobutton()
        self.create_role_clerk = Radiobutton()

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
        Label(create_user_bg, text="CREATE A USER", bg="#DDDDDD", fg="#3E3E3E", font=change_pass_label).place(relx=.5, rely=0.275, anchor="c")

        Label(create_user_bg, text="Username", bg="#DDDDDD", fg="#363636", font=field_label).place(relx=.5, rely=0.375, anchor="c")
        self.create_username_field = Entry(create_user_bg, textvariable=self.create_username, width=35, bd=0)
        self.create_username_field.place(height=20, width=225, relx=.5, rely=0.425, anchor="c")

        Label(create_user_bg, text="Password", bg="#DDDDDD", fg="#363636", font=field_label).place(relx=.5, rely=0.500, anchor="c")
        self.create_password_field = Entry(create_user_bg, textvariable=self.create_password, show="*", width=35, bd=0)
        self.create_password_field.place(height=20, width=225, relx=.5, rely=0.550, anchor="c")

        self.create_role_label = Label(create_user_bg, text="User Role", bg="#DDDDDD", fg="#363636", font=field_label)
        self.create_role_label.place(relx=.5, rely=0.625, anchor="c")
        self.create_role_manager = Radiobutton(create_user_bg, text="Manager", bg="#DDDDDD", variable=self.create_role_int, value=1)
        self.create_role_manager.place(relx=.35, rely=0.675, anchor="c")

        self.create_role_clerk = Radiobutton(create_user_bg, text="Clerk", bg="#DDDDDD", variable=self.create_role_int, value=2)
        self.create_role_clerk.place(relx=.65, rely=0.675, anchor="c")

        self.user_error_label = Label(create_user_bg, bg="#DDDDDD", fg="#D64000", font=field_label)
        self.user_error_label.place(relx=.5, rely=0.725, anchor="c")