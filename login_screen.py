import tkinter as tk
from tkinter import ttk, END
from ttkbootstrap import Style
import sqlite3
from tkinter.messagebox import showerror, showinfo

import admin_dashboard
import user_dashboard

class LoginScreen(tk.Toplevel):
    def __init__(self):
        super().__init__()

        self.radio_button_var = tk.IntVar(value=0)
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()

        style = Style(theme='united')
        style.master = self

        # SQLite3:
        self.con = sqlite3.connect('library.db')
        self.cur = self.con.cursor()

        self.cur.execute("SELECT name FROM userdatabase")
        self.member_names = [row[0] for row in self.cur.fetchall()]

        self.cur.execute("SELECT id FROM userdatabase")
        self.id_numbers = [row[0] for row in self.cur.fetchall()]
        if self.id_numbers:
            self.last_id = self.id_numbers[-1]
        else:
            self.last_id = 0

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        width = 420
        height = 200
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2 - 200
        self.geometry(f"{width}x{height}+{x}+{y}")
        self.title("Welcome to Kamweru Library!")
        self.resizable(False, False)
        
        self.columnconfigure((0, 1), weight=1)
        self.rowconfigure((0, 1, 3, 4), weight=1)

        style.configure('Medium.TButton', font=('inconsolata', 15))
        style.configure('Custom.TRadiobutton', font=('inconsolata', 13))

        self.creating_widgets()
        self.packing_widgets()

        self.mainloop()

    def creating_widgets(self):
        self.welcome_text = ttk.Label(self, text="Welcome! Please enter your user details.", font="inconsolata 18")
        self.username_text = ttk.Label(self, text="Please enter your username:", font="inconsolata 14")
        self.username_entry = ttk.Entry(self, textvariable=self.username_var)
        self.password_text = ttk.Label(self, text="Please enter your password:", font="inconsolata 14")
        self.password_entry = ttk.Entry(self, textvariable=self.password_var, show='*')
        self.user_select = ttk.Radiobutton(self, text="USER", value=0, variable=self.radio_button_var, command=self.for_radio_buttons, style="Custom.TRadiobutton")
        self.admin_select = ttk.Radiobutton(self, text="ADMIN", value=1, variable=self.radio_button_var, command=self.for_radio_buttons, style="Custom.TRadiobutton")
        self.login_button = ttk.Button(self, text="Log In!", command=self.login, style="Medium.TButton")
        self.signup_button = ttk.Button(self, text="Sign Up!", command=self.signup, style="Medium.TButton")
        
    def packing_widgets(self):
        self.welcome_text.grid(row=0, column=0, columnspan=2)
        self.username_text.grid(row=1, column=0, padx=4)
        self.username_entry.grid(row=1, column=1, padx=10)
        self.password_text.grid(row=2, column=0, padx=4)
        self.password_entry.grid(row=2, column=1, padx=10)
        self.user_select.grid(row=3, column=0)
        self.admin_select.grid(row=3, column=1)
        self.login_button.grid(row=4, column=0)
        self.signup_button.grid(row=4, column=1)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        isAdmin = self.radio_button_var.get()

        if username and password:
            if " " in username:
                showerror(message="Your username can not contain space!")
                self.password_entry.delete(0, END)
            elif any(char.isupper() for char in username):
                showerror(message="Your username can not contain uppercase letter!")
                self.password_entry.delete(0, END)
            else:
                if username in self.member_names:
                    self.cur.execute("SELECT password FROM userdatabase WHERE name = ?", (username,))
                    saved_password = self.cur.fetchall()[0][0]
                    self.cur.execute("SELECT isadmin FROM userdatabase WHERE name = ?", (username,))
                    adminValue = self.cur.fetchall()[0][0]
                    if saved_password != password:
                        showerror(message="Your password is incorrect!")
                        self.password_entry.delete(0, END)
                    elif adminValue == 0 and isAdmin == 1:
                        showerror(message="You are not admin!")
                        self.radio_button_var.set(0)
                        self.signup_button.config(state= "enabled")
                    else:
                        if isAdmin == 1:
                            self.withdraw() 
                            add_book_window = admin_dashboard.adminDashboard(username)
                            add_book_window.wait_window()
                            self.deiconify()
                        else:
                            self.withdraw() 
                            add_book_window = user_dashboard.userDashboard(username)
                            add_book_window.wait_window()
                            self.deiconify()
                            
                else:
                    showerror(message="There is no user with this username!")
                    self.username_entry.delete(0, END)
                    self.password_entry.delete(0, END)
        else:
            showerror(message="Please fill both username and password box!")
            self.password_entry.delete(0, END)

    def signup(self):
        username = self.username_var.get()
        password = self.password_var.get()
        id = self.last_id + 1

        if username and password:
            if " " in username:
                showerror(message="Your username can not contain space!")
                self.password_entry.delete(0, END)
            elif any(char.isupper() for char in username):
                showerror(message="Your username can not contain uppercase letter!")
                self.password_entry.delete(0, END)
            else:
                if username not in self.member_names:
                    self.cur.execute('INSERT INTO userdatabase (id, name, password, isadmin) VALUES (?, ?, ?, ?)', (id, username, password, self.radio_button_var.get()))
                    self.con.commit()
                    showinfo(message=f"Your account has been created! \n \n Your Username: {username} \n \n Your ID: {id}")
                    self.password_entry.delete(0, END)
                    self.cur.execute("SELECT name FROM userdatabase")
                    self.member_names = [row[0] for row in self.cur.fetchall()]
                else:
                    showerror(message="This username is already in the system!")
                    self.username_entry.delete(0, END)
                    self.password_entry.delete(0, END)
        else:
            showerror(message="Please fill both username and password box!")
            self.password_entry.delete(0, END)

    def for_radio_buttons(self):
        if self.radio_button_var.get() == 1:
            self.signup_button.config(state="disabled")
        else:
            self.signup_button.config(state="enabled")