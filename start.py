import login_screen
import tkinter as tk
from tkinter import ttk, END
from ttkbootstrap import Style

class start_menu(tk.Tk):
    def __init__(self):
        super().__init__()

        self.withdraw() 
        add_book_window = login_screen.LoginScreen()
        add_book_window.wait_window()
        self.deiconify()


start_menu()