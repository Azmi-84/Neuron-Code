from pymongo import MongoClient

def mongoDB_connection():
    """
    Establishes a connection to the MongoDB server and selects the YouTube_Manager database.
    """
    client = MongoClient("mongodb://localhost:27017/")
    db = client["YouTube_Manager"]
    
    print(client.list_database_names())

def main():
    mongoDB_connection()
    
if __name__ == "__main__":
    main()