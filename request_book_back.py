import tkinter as tk
from tkinter import ttk
import sqlite3
import admin_dashboard
from ttkbootstrap import Style
from tkinter.messagebox import showerror


class RequestBookBack(tk.Toplevel):
    def __init__(self, username):
        super().__init__()

        style = Style(theme= "united")
        style.master = self
        style.configure('Medium.TButton', font = ('inconsolata, 18'))

        self.username = username

        self.connection = sqlite3.connect('library.db')
        self.cursor = self.connection.cursor()

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        width = 500
        height = 300
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2 - 200
        self.geometry(f"{width}x{height}+{x}+{y}")
        self.title("Request a book back!")
        self.resizable(False, False)
        self.columnconfigure((0,1), weight= 1)
        self.rowconfigure((0,1,2,3), weight= 1)

        self.books = []
        self.book_str = tk.StringVar(value = "Select from here!")

        self.getting_books()
        self.creating_widgets()
        self.packing_widgets()

        self.mainloop()

    def getting_books(self):
        is_taken = "True"
        self.cursor.execute("SELECT title FROM book_properties WHERE is_taken = ?", (is_taken, ))
        rows = self.cursor.fetchall()
        self.books = [row[0] for row in rows]

    def creating_widgets(self):
        self.top_label = ttk.Label(self, text= f"Welcome {self.username}!", font="inconsolata 25")
        self.below_label = ttk.Label(self, text= f"Please select the book you want to request back below", font="inconsolata 15")
        self.book_selector = ttk.Combobox(self, textvariable= self.book_str)
        self.book_selector['values'] = self.books
        self.button1 = ttk.Button(self, text= "Send E-Mail!", command= self.request_back, style= "Medium.TButton")
        self.previous_menu_button = ttk.Button(self, text= "Previous Menu", command= self.previous_menu, style= "Medium.TButton")

    def packing_widgets(self):
        self.top_label.grid(row = 0, column= 0, columnspan= 2)
        self.below_label.grid(row = 1, column= 0, columnspan= 2)
        self.book_selector.grid(row = 2, column= 0, sticky= "we", pady= (0,20), padx= 10, columnspan= 2)
        self.button1.grid(row = 3, column= 0)
        self.previous_menu_button.grid(row = 3, column= 1)

    def request_back(self):
        self.cursor.execute("SELECT email FROM book_properties WHERE title = ?", (self.book_str.get(),))
        e_mail = (self.cursor.fetchall()[0][0])
        showerror(message= f"E-Mail has been sent to: \n \n {e_mail}")

        # There should be a sending e-mail prompt here, but I do not want to risking to expose my gmail app password here :)

    def previous_menu(self):
        self.withdraw() 
        add_book_window = admin_dashboard.adminDashboard(self.username)
        add_book_window.wait_window()
        self.deiconify()
