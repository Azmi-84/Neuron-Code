from pymongo import MongoClient, errors
from bson import ObjectId

def mongoDB_connection():
    try:
        client = MongoClient("mongodb://localhost:27017/")
        db = client["YouTube_Manager"]
        return db.videos
    except errors.ConnectionFailure:
        print("Failed to connect to MongoDB.")
        return None

def main():
    videos_collection = mongoDB_connection()
    
    if not videos_collection:
        return
    
    while True:
        print("\nYouTube Manager with MongoDB")
        print("1. List all videos")
        print("2. Add a video")
        print("3. Update a video")
        print("4. Delete a video")
        print("5. Search videos")
        print("6. Exit")
        
        choice = input("Enter your choice (1-6): ")
        
        if choice == '1':
            videos = videos_collection.find()
            if videos.count() == 0:
                print("No videos found!")
            else:
                for video in videos:
                    print(f"ID: {video['_id']}, Title: {video['title']}, Time: {video['time']}")
        
        elif choice == '2':
            title = input("Enter video title: ")
            time = input("Enter video time (MM:SS): ")
            videos_collection.insert_one({
                "title": title,
                "time": time
            })
            print("Video added successfully!")
        
        elif choice == '3':
            video_id = input("Enter video ID to update: ")
            title = input("Enter new title: ")
            time = input("Enter new time (MM:SS): ")
            try:
                videos_collection.update_one(
                    {"_id": ObjectId(video_id)},
                    {"$set": {"title": title, "time": time}}
                )
                print("Video updated successfully!")
            except:
                print("Error updating video. Check the ID.")
        
        elif choice == '4':
            video_id = input("Enter video ID to delete: ")
            try:
                videos_collection.delete_one({"_id": ObjectId(video_id)})
                print("Video deleted successfully!")
            except:
                print("Error deleting video. Check the ID.")
        
        elif choice == '5':
            search_term = input("Enter search term: ")
            videos = videos_collection.find({"title": {"$regex": search_term, "$options": "i"}})
            if videos.count() == 0:
                print("No matching videos found!")
            else:
                for video in videos:
                    print(f"ID: {video['_id']}, Title: {video['title']}, Time: {video['time']}")
        
        elif choice == '6':
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()