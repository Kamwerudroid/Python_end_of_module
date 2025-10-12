import pymongo
from pymongo import MongoClient

class DBManager:
    """Manages connection to MongoDB and performs database operations."""
    def __init__(self, uri="mongodb://localhost:27017/", db_name="LibraryDB"):
        try:
            # Replace with your actual MongoDB URI if it's remote
            self.client = MongoClient(uri)
            self.db = self.client[db_name]
            self.users_collection = self.db['users']
            self.books_collection = self.db['books']
            print("MongoDB connection successful.")
        except pymongo.errors.ConnectionError as e:
            print(f"Error connecting to MongoDB: {e}")
            self.client = None
            self.db = None

    def get_user_by_username(self, username):
        """Fetches a user document by username."""
        if not self.db: return None
        return self.users_collection.find_one({"username": username})

    def get_all_books(self):
        """Fetches all book documents."""
        if not self.db: return []
        return list(self.books_collection.find({}))

    def update_book_status(self, book_id, new_status):
        """Updates the 'is_available' status of a book."""
        if not self.db: return False
        result = self.books_collection.update_one(
            {"_id": book_id},
            {"$set": {"is_available": new_status}}
        )
        return result.modified_count > 0

# --- Add more methods for registering users, adding books, etc. ---