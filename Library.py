import hashlib
from bson.objectid import ObjectId
from DBManager import DBManager 

class Book:
    """Represents a book in the library."""
    def __init__(self, title, author, isbn, book_id=None, is_available=True):
        self.title = title
        self.author = author
        self.isbn = isbn
        self._id = book_id # MongoDB uses _id
        self.is_available = is_available

class User:
    """Represents a library user or administrator."""
    def __init__(self, username, name, user_id=None, is_admin=False):
        self.username = username
        self.name = name
        self._id = user_id
        self.is_admin = is_admin 

class LibrarySystem:
    """Manages the overall library operations and interacts with the database."""
    def __init__(self):
        self.db_manager = DBManager()
        self.current_user = None

    def verify_login(self, username, password):
        """
        Checks credentials against the database.
        Includes logging for debugging.
        """
        # Clean inputs to prevent whitespace issues
        clean_username = username.strip()
        clean_password = password.strip()
        
        print(f"\n--- Login Attempt ---")
        print(f"Attempting login for user: {clean_username}")

        user_data = self.db_manager.get_user_by_username(clean_username)

        if user_data:
            print(f"User data fetched successfully.")
            # Retrieve the password from the database document
            db_password = user_data.get("password")
            is_admin_user = user_data.get('is_admin', False) 
            
            print(f"DB Record Username: {user_data.get('username')}, Admin: {is_admin_user}")
            print(f"DB Password (from DB): '{db_password}'")
            print(f"Input Password (from Tkinter): '{clean_password}'")
            
            # 1. Check if the password field exists and is not None
            if db_password is None:
                 print("Failure: 'password' field missing or None in DB record. Check your MongoDB schema!")
                 return False

            # 2. Compare the input password with the stored password (case-sensitive)
            if db_password == clean_password: 
                print("Success: Password matched.")
                # MAPPING: Create a User object from the MongoDB dictionary
                self.current_user = User(
                    username=user_data['username'], 
                    name=user_data.get('name', 'N/A'),
                    user_id=user_data['_id'],
                    is_admin=is_admin_user
                )
                return True
            else:
                print("Failure: Password mismatch.")
                return False
        else:
            print(f"Failure: User '{clean_username}' not found in database.")
            return False

    def get_available_books(self):
        """Returns a list of Book objects."""
        book_list = self.db_manager.get_all_books()
        # MAPPING: Create a list of Book objects from the MongoDB documents
        return [
            Book(
                title=b['title'], 
                author=b['author'], 
                isbn=b['isbn'], 
                book_id=b['_id'], 
                is_available=b.get('is_available', True)
            ) 
            for b in book_list if b.get('is_available', True)
        ]

    def checkout_book(self, book_id):
        """Marks a book as unavailable using its MongoDB ObjectId."""
        if not self.current_user:
            return "Error: Must be logged in to checkout a book."
        
        # Use the DBManager method to perform the database update
        if self.db_manager.update_book_status(book_id, False):
            # Success
            return f"Book checked out successfully by {self.current_user.username}."
        else:
            # Failure (e.g., book not found or already checked out)
            return "Error: Could not checkout book (already unavailable or not found)."
