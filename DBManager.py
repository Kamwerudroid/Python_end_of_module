import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId

class DBManager:
    """Manages connection to MongoDB and performs database operations."""
    def __init__(self, uri="mongodb+srv://mainakamweru_db_user:3RQ2CwPYcljoe0cB@cluster0.22s3qwq.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0", db_name="Library_management_system"):
        self.client = None
        self.db = None
        self.users_collection = None
        self.books_collection = None
        
        try:
            # Connect to MongoDB
            self.client = MongoClient(uri, serverSelectionTimeoutMS=5000) # Added timeout
            # The ismaster command is cheap and does not require auth.
            # It will throw an exception if the connection fails.
            self.client.admin.command('ping') 
            
            self.db = self.client[db_name]
            self.users_collection = self.db['users']
            self.books_collection = self.db['books']
            print("MongoDB connection successful.")
            
        except pymongo.errors.ConnectionError as e:
            print(f"Error connecting to MongoDB: {e}")
        except Exception as e:
            # Catch all other exceptions during connection/ping
            print(f"An unexpected error occurred during MongoDB setup: {e}")

    # --- R E A D / F E T C H  O P E R A T I O N S ---
            
    def get_user_by_username(self, username):
        """Fetches a user document by username for login."""
        # FIX: Check if the client/connection object is None instead of the database object
        if self.client is None: return None 
        
        # find_one returns a single dictionary matching the query
        return self.users_collection.find_one({"username": username}) 

    def get_all_books(self):
        """Fetches all book documents."""
        if self.client is None: return []
        # find returns a cursor, which we convert to a list
        return list(self.books_collection.find({}))
        
    # --- U P D A T E  O P E R A T I O N S ---

    def update_book_status(self, book_id: ObjectId, new_status: bool):
        """Updates the 'is_available' status of a book by its ObjectId."""
        if self.client is None: return False
        
        # Use $set to update specific fields
        result = self.books_collection.update_one(
            {"_id": book_id}, # Query filter by the unique ObjectId
            {"$set": {"is_available": new_status}}
        )
        # Check if exactly one document was modified
        return result.modified_count == 1
