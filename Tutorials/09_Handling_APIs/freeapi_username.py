import requests


def fetch_random_user_freeapi():
    url = "https://api.freeapi.app/api/v1/public/randomusers/user/random"

    try:
        response = requests.get(url)
        data = response.json()

        if data["success"] and data["data"]:
            user = data["data"]
            print(f"Name: {user['name']['first']} {user['name']['last']}")
            print(f"Email: {user['email']}")
            print(f"Phone: {user['phone']}")
            print(
                f"Location: {user['location']['city']}, {user['location']['country']}"
            )
            return user
        else:
            print("Failed to fetch user data")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None


def fetch_random_user():
    url = "https://randomuser.me/api/"

    try:
        response = requests.get(url)
        data = response.json()

        if data["results"]:
            user = data["results"][0]
            print(f"Name: {user['name']['first']} {user['name']['last']}")
            print(f"Email: {user['email']}")
            print(f"Phone: {user['phone']}")
            return user
        else:
            print("Failed to fetch user data")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None


def post_login():
    url = "https://api.freeapi.app/api/v1/auth/login"

    # These are example credentials - replace with actual credentials if needed
    credentials = {"email": "user@example.com", "password": "password123"}

    try:
        response = requests.post(url, json=credentials)
        data = response.json()

        if response.status_code == 200 and data.get("success"):
            print("Login successful!")
            print(f"Token: {data['data']['token']}")
            return data["data"]["token"]
        else:
            print(f"Login failed: {data.get('message', 'Unknown error')}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None


def main():
    print("1. Fetch Random User from FreeAPI")
    print("2. Fetch Random User from randomuser.me")
    print("3. Post Login")
    print("4. Exit")

    choice = input("Enter your choice (1-4): ")

    if choice == "1":
        fetch_random_user_freeapi()
    elif choice == "2":
        fetch_random_user()
    elif choice == "3":
        post_login()
    elif choice == "4":
        return
    else:
        print("Invalid choice. Please try again.")

    # Recursive call to keep the menu going
    main()


if __name__ == "__main__":
    main()
