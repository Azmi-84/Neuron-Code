import sqlite3


def list_videos():
    conn = sqlite3.connect("youtube_videos.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM videos")
    videos = cursor.fetchall()

    if not videos:
        print("No videos found!")
    else:
        for video in videos:
            print(f"ID: {video[0]}, Title: {video[1]}, Time: {video[2]}")

    conn.close()


def add_videos():
    title = input("Enter video title: ")
    time = input("Enter video time (MM:SS): ")

    conn = sqlite3.connect("youtube_videos.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO videos (title, time) VALUES (?, ?)", (title, time))
    conn.commit()
    print("Video added successfully!")
    conn.close()


def update_videos():
    video_id = input("Enter video ID to update: ")
    title = input("Enter new title: ")
    time = input("Enter new time (MM:SS): ")

    conn = sqlite3.connect("youtube_videos.db")
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE videos SET title = ?, time = ? WHERE id = ?", (title, time, video_id)
    )
    conn.commit()
    print("Video updated successfully!")
    conn.close()


def delete_videos():
    video_id = input("Enter video ID to delete: ")

    conn = sqlite3.connect("youtube_videos.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM videos WHERE id = ?", (video_id,))
    conn.commit()
    print("Video deleted successfully!")
    conn.close()


def main():
    conn = sqlite3.connect("youtube_videos.db")
    cursor = conn.cursor()
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS videos (
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        time TEXT NOT NULL
    )
    """
    )
    conn.commit()
    conn.close()

    while True:
        print("\nYouTube Manager")
        print("1. List all videos")
        print("2. Add a video")
        print("3. Update a video")
        print("4. Delete a video")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ")

        if choice == "1":
            list_videos()
        elif choice == "2":
            add_videos()
        elif choice == "3":
            update_videos()
        elif choice == "4":
            delete_videos()
        elif choice == "5":
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
