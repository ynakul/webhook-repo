from pymongo import MongoClient

def test_mongodb_connection():
    try:
        # Connect to the MongoDB server
        client = MongoClient('mongodb://localhost:27017/')
        # Access the 'admin' database
        admin_db = client.admin
        # Run the 'ping' command to check connectivity
        admin_db.command('ping')
        print("MongoDB connection successful!")
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    test_mongodb_connection()
