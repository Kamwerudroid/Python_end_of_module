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
    """Represents a library user."""
    def __init__(self, username, name, user_id=None):
        self.username = username
        self.name = name
        self._id = user_id

class LibrarySystem:
    """Manages the overall library operations and interacts with the database."""
    def __init__(self):
        self.db_manager = DBManager()
        self.current_user = None

    def verify_login(self, username, password):
        """Checks credentials against the database."""
        user_data = self.db_manager.get_user_by_username(username)
        if user_data:
            # Note: In a real app, you would securely hash the password 
            # and compare the hash, not the plaintext.
            # Example: hash = hashlib.sha256(password.encode()).hexdigest()
            # if user_data.get("password_hash") == hash:
            
            # For this example, we'll use a placeholder check:
            if user_data.get("password") == password: 
                self.current_user = User(
                    username=user_data['username'], 
                    name=user_data.get('name', 'N/A'),
                    user_id=user_data['_id']
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