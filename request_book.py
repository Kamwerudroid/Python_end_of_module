import tkinter as tk
from tkinter import ttk, END
import sqlite3
import user_dashboard
from ttkbootstrap import Style
from tkinter.messagebox import showerror
import user_dashboard


class RequestBook(tk.Toplevel):
    def __init__(self,username):
        super().__init__()

        style = Style(theme='united')
        style.master = self
        style.configure('Medium.TButton', font=('inconsolata', 18))

        self.username = username

        self.connection = sqlite3.connect("library.db")
        self.cursor = self.connection.cursor()
        
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        width = 500
        height = 300
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2 - 200
        self.geometry(f"{width}x{height}+{x}+{y}")
        self.title("Request a book!")
        self.resizable(False, False)
        self.columnconfigure((0 ,1), weight= 1)
        self.rowconfigure((0,1,2,3,4), weight= 1)

        self.books = []
        self.getting_books()
        self.book_str = tk.StringVar(value = "Select from here!")
        self.email_str = tk.StringVar(value= "Please enter your e-mail here")
        self.creating_widgets()
        self.packing_widgets()
        self.email_entry.bind("<Button-1>", lambda event: self.entry_clicked())

        self.mainloop()

    def getting_books(self):
        is_taken = "False"
        self.cursor.execute("SELECT title FROM book_properties WHERE is_taken = ?", (is_taken,))
        rows = self.cursor.fetchall()
        self.books = [row[0] for row in rows]

    def creating_widgets(self):
        self.top_label = ttk.Label(self, text= f"Welcome {self.username}!", font="inconsolata 25")
        self.below_label = ttk.Label(self, text=f"Please select the book you want to request below!", font="inconsolata 15")
        self.book_selector = ttk.Combobox(self, textvariable= self.book_str)
        self.book_selector['values'] = self.books
        self.email_entry = ttk.Entry(self, textvariable= self.email_str)
        self.button1 = ttk.Button(self, text= "Request!", command= self.request, style= "Medium.TButton")
        self.previous_menu_button = ttk.Button(self, text= "Previous Menu", command= self.previous_menu, style= "Medium.TButton")

    def packing_widgets(self):
        self.top_label.grid(row = 0, column= 0, columnspan= 2)
        self.below_label.grid(row = 1, column=0, columnspan= 2)
        self.book_selector.grid(row = 2, column= 0, sticky= "we", pady= (0,20), padx= 10, columnspan= 2)
        self.email_entry.grid(row = 3, column= 0, sticky= "we",  padx= 10, columnspan= 2)
        self.button1.grid(row = 4, column= 0)
        self.previous_menu_button.grid(row = 4, column= 1)

    def request(self):
        if self.book_str.get() == "Select from here!":
            showerror(message= "Please choose a book!")
        elif self.email_str.get() in ["Please enter your e-mail here", "", " "]:
            showerror(message= "Please enter your e-mail accordingly!")
        else:
            self.cursor.execute("UPDATE book_properties SET is_taken = ?, who_took = ?, email = ? WHERE title = ?", ("True", self.username, self.email_str.get(), self.book_str.get(),))
            self.connection.commit()
            showerror(message= "Your Request has been accepted! \n \n You can request only one book per session!")
            self.button1.config(state= "disabled")
            self.email_entry.delete(0, END)

    def entry_clicked(self):
        self.email_entry.delete(0, END)

    def previous_menu(self):
        self.withdraw() 
        add_book_window = user_dashboard.userDashboard(self.username)
        add_book_window.wait_window()
        self.deiconify()