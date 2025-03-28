import json

df = "youtube.txt"


def load_data():
    try:
        with open(df, "r") as file:
            # test = json.load(file)
            # print(type(test))
            # return test
            return json.load(file)
    except FileNotFoundError:
        return []
    finally:
        pass


def save_data_helper(videos):
    with open(df, "w") as file:
        json.dump(videos, file)


def list_all_videos(videos):
    print("\n")
    print("-" * 70)
    for index, video in enumerate(videos, start=1):
        print(f"{index}. Video name: {video['name']}, Duration: {video['time']}")
        print("-" * 70)


def add_video(videos):
    name = input("Enter the video name: ")
    time = input("Enter the video time: ")
    videos.append({"name": name, "time": time})
    save_data_helper(videos)


def update_videos(videos):
    list_all_videos(videos)
    index = int(input("Enter the video number to update: "))

    if 1 <= index <= len(videos):
        name = input("Enter the video name: ")
        time = input("Enter the video time: ")
        videos[index - 1] = {"name": name, "time": time}
        save_data_helper(videos)
    else:
        print(f"Invalid index[{index}] selected!!!")


def delete_video(videos):
    list_all_videos(videos)
    index = int(input("Enter the video number to delete: "))

    if 1 <= index <= len(videos):
        del videos[index - 1]
        save_data_helper(videos)
    else:
        print(f"Invalid index[{index}] selected!!!")


def main():
    videos = load_data()
    while True:
        print("\n YouTube Manager | Choose an option")
        print("1. List all videos ")
        print("2. Add a video ")
        print("3. Update a video ")
        print("4. Delete a video ")
        print("5. Exit the app ")
        # print(videos)

        choice = input("Enter the choice: ")

        match choice:
            case "1":
                list_all_videos(videos)
            case "2":
                add_video(videos)
            case "3":
                update_videos(videos)
            case "4":
                delete_video(videos)
            case "5":
                break
            case _:
                print("Invalid choice!!!")


if __name__ == "__main__":
    main()
