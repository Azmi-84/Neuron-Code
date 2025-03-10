import sqlite3

# Connect to the database (creates the file if it doesn't exist)
conn = sqlite3.connect('YouTube_Videos_List.db')
cursor = conn.cursor()

# Create the 'YouTube_Videos' table if it does not exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS YouTube_Videos(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    time TEXT NOT NULL    
)
''')

def list_videos():
    cursor.execute("SELECT * FROM YouTube_Videos")
    
    for row in cursor.fetchall():
        print(row) 

def add_videos():
    name = input("Enter the video name: ")
    time = input("Enter the video time: ")
    cursor.execute("INSERT INTO YouTube_Videos (name, time) VALUES (?, ?)", (name, time))
    conn.commit()

def update_videos():
    video_id = input("Enter the video ID: ")
    new_name = input("Enter the video name: ")
    new_time = input("Enter the video time: ")
    cursor.execute("UPDATE YouTube_Videos SET name = ?, time = ? WHERE id = ?", (new_name, new_time, video_id))
    conn.commit()

def delete_videos():
    video_id = input("Enter the video ID: ")
    cursor.execute("DELETE FROM YouTube_Videos WHERE id = ?", (video_id,))
    conn.commit()

def main():
    while True:
        print("\n")
        print("-" * 70)
        print("Youtube Manager with Sqlite3 DB")
        print('1. List all videos ')
        print('2. Add a video ')
        print('3. Update a video ')
        print('4. Delete a video ')
        print('5. Exit the app ')
        
        choice = input("Enter your choice: ")
        
        match choice:
            case '1':
                list_videos()
            case '2':
                add_videos()
            case '3':
                update_videos()
            case '4':
                delete_videos()
            case '5':
                break
            case _:
                print("Wrong input!!!")

    conn.close()
    
if __name__ == "__main__":
    main()
