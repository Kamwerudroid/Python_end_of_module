import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId

class DBManager:
    """Manages connection to MongoDB and performs database operations."""
    def __init__(self, uri="mongodb+srv://mainakamweru_db_user:3RQ2CwPYcljoe0cB@cluster0.22s3qwq.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"):
        
        # NOTE: Verify this database name EXACTLY matches the one in your Atlas setup.
        db_name = "Library_management_system" 

        self.client = None
        self.db = None
        self.users_collection = None
        self.books_collection = None
        
        print("\n--- MongoDB Connection Status ---")

        try:
            # FIX from previous step: Bypass strict SSL certificate validation
            connect_uri = f"{uri}&tlsAllowInvalidCertificates=true"
            
            self.client = MongoClient(connect_uri, serverSelectionTimeoutMS=5000)
            self.client.admin.command('ping') 
            
            # DIAGNOSTIC 1: Confirm the client can see databases
            available_dbs = self.client.list_database_names()
            print(f"Connection OK. Available DBs: {available_dbs}")
            
            if db_name not in available_dbs and self.client[db_name].list_collection_names():
                 # This warning only shows if the DB is missing, but has collections (rare, usually means no data)
                 print(f"WARNING: Target DB '{db_name}' not explicitly listed, but connection is live.")

            self.db = self.client[db_name]
            self.users_collection = self.db['users']
            self.books_collection = self.db['books']
            
            # DIAGNOSTIC 2: Confirm the 'users' collection exists and has data
            collection_names = self.db.list_collection_names()
            print(f"Target DB collections: {collection_names}")
            if 'users' not in collection_names:
                print("FATAL ERROR: 'users' collection is missing. Please create it in MongoDB Atlas.")
            
            user_count = self.users_collection.count_documents({})
            print(f"Found {user_count} documents in the 'users' collection.")


            print(f"MongoDB connection successful to {db_name}.")
            
        except pymongo.errors.ConnectionError as e:
            print(f"Error connecting to MongoDB: {e}")
            self.client = None 
        except Exception as e:
            print(f"An unexpected error occurred during MongoDB setup: {e}")
            self.client = None 
            
        print("-----------------------------------")


    def get_user_by_username(self, username):
        """
        Fetches a user document by username for login.
        FIX: Uses a case-insensitive query to resolve "admin not found" issues
        due to potential case mismatches in the database or user input.
        """
        if self.users_collection is None: 
            print("Error: Database connection failed during initialization.")
            return None 
        
        
        
        query = {"username": {"$regex": f"^{username.strip()}$", "$options": "i"}}
        
        print(f"Querying users collection with case-insensitive query: {query}") 

        # find_one returns a single dictionary matching the query
        return self.users_collection.find_one(query) 

    def get_all_books(self):
        """Fetches all book documents."""
        if self.client is None: return []
        
        return list(self.books_collection.find({}))
        
    def update_book_status(self, book_id: ObjectId, new_status: bool):
        """Updates the 'is_available' status of a book by its ObjectId."""
        if self.client is None: return False
        
        result = self.books_collection.update_one(
            {"_id": book_id}, 
            {"$set": {"is_available": new_status}}
        )
        return result.modified_count == 1
