import hashlib
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
        """Checks credentials against the database and sets user type."""
        user_data = self.db_manager.get_user_by_username(username)
        if user_data:
            # Check password (simplified)
            if user_data.get("password") == password: 
                # MAPPING: Create a User object with the admin status
                is_admin_user = user_data.get('is_admin', False) # Default to False if field is missing
                
                self.current_user = User(
                    username=user_data['username'], 
                    name=user_data.get('name', 'N/A'),
                    user_id=user_data['_id'],
                    is_admin=is_admin_user # Store the status
                )
                return True
        return False

    def get_available_books(self):
        """Returns a list of Book objects."""
        book_list = self.db_manager.get_all_books()
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
        """Marks a book as unavailable."""
        if not self.current_user:
            return "Error: Must be logged in to checkout a book."
        
        if self.db_manager.update_book_status(book_id, False):
            return f"Book ID {book_id} checked out successfully by {self.current_user.username}."
        else:
            return "Error: Could not checkout book."

    # --- Add methods for return_book, register_user, add_book, etc. ---