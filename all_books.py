import tkinter as tk
from tkinter import ttk
import sqlite3
import user_dashboard
import admin_dashboard
from ttkbootstrap import Style


class AllBooks(tk.Toplevel):
    def __init__(self, location, username):
        super().__init__()
 
        self.books = []
        self.location = location
        self.username = username
        
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        width = 1300
        height = 500
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2 - 100
        self.geometry(f"{width}x{height}+{x}+{y}")
        self.title("All Books in the Kamweru Library!")
        self.resizable(False, False)

        self.rowconfigure(0, weight=9)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        self.table_frame = ttk.Frame(self)
        self.table_frame.grid(row=0, column=0, sticky="nsew")

        self.getting_books()
        self.creating_table()
        self.packing_table()

    def creating_table(self):
        self.table = ttk.Treeview(
            self.table_frame,
            columns=("Title", "Author", "Genre", "Language", "Page Count", "Is Taken?", "Who Took?", "E-Mail"),
            show="headings"
        )
        self.table.heading("Title", text="Title")
        self.table.heading("Author", text="Author")
        self.table.heading("Genre", text="Genre")
        self.table.heading("Language", text="Language")
        self.table.heading("Page Count", text="Page Count")
        self.table.heading("Is Taken?", text="Is Taken?")
        self.table.heading("Who Took?", text="Who Took?")
        self.table.heading("E-Mail", text="E-Mail")

        self.table.column("Title", width=350, anchor="center")
        self.table.column("Author", width=120, anchor="center")
        self.table.column("Genre", width=100, anchor="center")
        self.table.column("Language", width=100, anchor="center")
        self.table.column("Page Count", width=80, anchor="center")
        self.table.column("Is Taken?", width=70, anchor="center")
        self.table.column("Who Took?", width=150, anchor="center")
        self.table.column("E-Mail", width=300, anchor="center")

        self.table.pack(expand=True, fill='both')

        self.previous_menu_button = ttk.Button(self, text="Go back to previous menu!", command=self.go_back)

    def packing_table(self):
        self.previous_menu_button.grid(row=1, column=0, sticky="ew")

        for book in self.books:
            self.table.insert('', 'end', values=(
                book[1], book[2], book[3], book[4], 
                book[5], book[6], book[7], book[8]
            ))

    def getting_books(self):
        connection = sqlite3.connect("library.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM book_properties")
        rows = cursor.fetchall()
        connection.close()

        self.books.extend(rows)

    def go_back(self):
        if self.location == "user":
            self.withdraw() 
            add_book_window = user_dashboard.userDashboard(self.username)
            add_book_window.wait_window()
            self.deiconify()
        elif self.location == "admin":
            self.withdraw() 
            add_book_window = admin_dashboard.adminDashboard(self.username)
            add_book_window.wait_window()
            self.deiconify()