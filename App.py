import tkinter as tk
from tkinter import messagebox
from Library import LibrarySystem 

class LibraryApp(tk.Tk):
    """The main application window and frame manager."""
    def __init__(self):
        super().__init__()
        self.title("Library Management System")
        self.geometry("600x400")
        
        self.library_system = LibrarySystem()
        
        # Container frame for stacking pages
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (LoginPage, UserPage, AdminPage): # <-- Add AdminPage
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("LoginPage")

    def show_frame(self, page_name):
        """Raises the desired frame to the front."""
        frame = self.frames[page_name]
        frame.tkraise()

    def login_success(self):
        """Called after successful login to switch to the appropriate page."""
        user = self.library_system.current_user
        if user.is_admin:
            messagebox.showinfo("Success", "Admin login successful!")
            # self.frames["AdminPage"].load_admin_data() # (Optional) load data for admin
            self.show_frame("AdminPage") # <-- Navigate to Admin Page
        else:
            messagebox.showinfo("Success", "User login successful!")
            self.frames["UserPage"].load_user_data()
            self.show_frame("UserPage")
        
    def logout(self):
        """Clears current user and switches back to LoginPage."""
        self.library_system.current_user = None
        self.show_frame("LoginPage")

class LoginPage(tk.Frame):
    """The sign-in page."""
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        tk.Label(self, text="Library Sign In", font=('Arial', 18, 'bold')).pack(pady=10)

        # Username
        tk.Label(self, text="Username:").pack(pady=5)
        self.username_entry = tk.Entry(self)
        self.username_entry.pack(padx=20, fill='x')

        # Password
        tk.Label(self, text="Password:").pack(pady=5)
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack(padx=20, fill='x')

        # Login Button
        tk.Button(self, text="Login", command=self._login_command).pack(pady=15)

    def _login_command(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if self.controller.library_system.verify_login(username, password):
            messagebox.showinfo("Success", "Login successful!")
            self.controller.login_success()
        else:
            messagebox.showerror("Error", "Invalid username or password.")

class AdminPage(tk.Frame):
    """The administrative page for managing the library."""
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        # Admin Header
        tk.Label(self, text="Admin Dashboard", font=('Arial', 24, 'bold')).pack(pady=20)
        
        # User Info
        user = self.controller.library_system.current_user
        if user:
            tk.Label(self, text=f"Logged in as: {user.name}", font=('Arial', 14)).pack(pady=5)
        
        # Admin Tasks (PLACEHOLDERS)
        tk.Button(self, text="Add New Book", width=25).pack(pady=10)
        tk.Button(self, text="Manage Users", width=25).pack(pady=10)
        tk.Button(self, text="View All Transactions", width=25).pack(pady=10)

        # Logout Button
        tk.Button(self, text="Logout", command=self.controller.logout).pack(pady=30)            
            
class UserPage(tk.Frame):
    """The main user page showing available books and user info."""
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        # User Info Header
        self.user_label = tk.Label(self, text="", font=('Arial', 14, 'italic'))
        self.user_label.pack(pady=10)

        tk.Label(self, text="Available Books", font=('Arial', 16, 'bold')).pack(pady=5)
        
        # Book List Box
        self.books_listbox = tk.Listbox(self, width=80, height=10)
        self.books_listbox.pack(padx=20, pady=10, fill='x')

        # Checkout Button
        tk.Button(self, text="Checkout Selected Book", command=self._checkout_command).pack(pady=10)

        # Logout Button
        tk.Button(self, text="Logout", command=self.controller.logout).pack(pady=10)

    def load_user_data(self):
        """Updates the page with current user info and available books."""
        user = self.controller.library_system.current_user
        if user:
            self.user_label.config(text=f"Welcome, {user.name} ({user.username})")
        
        self.books_listbox.delete(0, tk.END)
        books = self.controller.library_system.get_available_books()
        
        for book in books:
            # Store the book ID (or a unique identifier) as part of the listbox item 
            # for easy retrieval when checking out.
            display_text = f"{book.title} by {book.author} (ISBN: {book.isbn}) | ID: {book._id}"
            self.books_listbox.insert(tk.END, display_text)

    def _checkout_command(self):
        try:
            selected_index = self.books_listbox.curselection()[0]
            selected_text = self.books_listbox.get(selected_index)
            
            # Simple way to extract the book ID from the displayed text
            # This is brittle and should be improved in a production app 
            # (e.g., storing the ID in a dictionary linked to the listbox index)
            book_id_str = selected_text.split(" | ID: ")[-1]
            
            # Assuming MongoDB's ObjectId might be stored as a string
            from bson.objectid import ObjectId
            book_id = ObjectId(book_id_str)

            result_msg = self.controller.library_system.checkout_book(book_id)
            messagebox.showinfo("Checkout Status", result_msg)
            
            # Refresh the book list after successful checkout
            if "successfully" in result_msg:
                self.load_user_data() 
                
        except IndexError:
            messagebox.showerror("Selection Error", "Please select a book to checkout.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")


if __name__ == "__main__":
    # Ensure you have the `pymongo` package installed: pip install pymongo
    # And a MongoDB instance running on localhost:27017
    
    # --- For initial setup, you might need to insert test data manually ---
    # Example MongoDB inserts for testing:
    """
    db.users.insert_one({"username": "alice", "password": "password123", "name": "Alice Smith"})
    db.books.insert_many([
        {"title": "The Great Novel", "author": "J. Doe", "isbn": "12345", "is_available": True},
        {"title": "Python Programming", "author": "G. Code", "isbn": "67890", "is_available": True}
    ])
    """
    
    app = LibraryApp()
    app.mainloop()