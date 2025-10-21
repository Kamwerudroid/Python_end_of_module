import tkinter as tk
from tkinter import ttk, END
from ttkbootstrap import Style
import sqlite3
from tkinter.messagebox import showerror, showinfo
from datetime import datetime
import add_book
import all_books
import login_screen
import request_book_back

class adminDashboard(tk.Toplevel):
    def __init__(self, username):
        super().__init__()

        style = Style(theme='united')
        style.master = self
        style.configure('Medium.TButton', font=('inconsolata', 18))

        today = datetime.now()
        self.formatted_date = today.strftime("%B %-d, %Y.")

        self.username = username

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        width = 500
        height = 300
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2 - 200
        self.geometry(f"{width}x{height}+{x}+{y}")
        self.resizable(False, False)
        self.title("Admin Dashboard")

        self.columnconfigure(0, weight=1)
        self.rowconfigure((0, 1, 2, 3, 4, 5), weight=1)

        self.creating_widgets()
        self.packing_widgets()

        self.mainloop()

    def creating_widgets(self):
        self.top_label = ttk.Label(self, text=f"Welcome {self.username}!", font="inconsolata 25")
        self.below_label = ttk.Label(self, text=f"It is currently: {self.formatted_date}", font="inconsolata 14")

        self.add_book_button = ttk.Button(self, text="Add Book to Library", style="Medium.TButton", command= self.add_book)
        self.request_book_button = ttk.Button(self, text="Request A Book Back", style="Medium.TButton", command= self.request_book)
        self.all_book_button = ttk.Button(self, text="All Books in the Library", style="Medium.TButton", command= self.all_books)
        self.go_back_button = ttk.Button(self, text= "Log Out!", style="Medium.TButton", command= self.previous_menu)


    def packing_widgets(self):
        self.top_label.grid(row=0, column=0)
        self.below_label.grid(row=1, column=0)
        self.add_book_button.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)
        self.request_book_button.grid(row=3, column=0, sticky="nsew", padx=10, pady=10)
        self.all_book_button.grid(row=4, column=0, sticky="nsew", padx=10, pady=10)
        self.go_back_button.grid(row=5, column=0, sticky="nsew", padx=10, pady=10)


    def add_book(self):
        self.withdraw() 
        add_book_window = add_book.addBook(self.username)
        add_book_window.wait_window()
        self.deiconify()

    def request_book(self):
        self.withdraw() 
        add_book_window = request_book_back.RequestBookBack(self.username)
        add_book_window.wait_window()
        self.deiconify()

    def all_books(self):
        self.withdraw() 
        add_book_window = all_books.AllBooks("admin", self.username)
        add_book_window.wait_window()
        self.deiconify()

    def previous_menu(self):
        self.withdraw() 
        add_book_window = login_screen.LoginScreen()
        add_book_window.wait_window()
        self.deiconify()