import requests

def fetch_random_user_freeapi():
    url = "https://api.freeapi.app/api/v1/public/randomusers/user/random"
    response = requests.get(url)
    data = response.json()
    
    if data["success"] and "data" in data:
        user_data = data["data"]
        username = user_data["login"]["username"]
        return username
    else:
        raise Exception("Failed to fetch user data")
    
def fetch_random_user():
    url = "https://api.freeapi.app/api/v1/public/randomusers"
    response = requests.get(url)
    data = response.json()
    print(data["data"]["data"][0]["gender"])
    # print(response)
    
def post_login():
    url = "https://api.freeapi.app/api/v1/users/login"
    # response = requests.post(url)
    # data = response.json()
    # print(data)
    
    payload = {
        
        "username": "your_username",
        "password": "your_password"
    }
    
    headers = {
        "accept": "application/json",
        "content-Type": "application/json"
    }
    
    
    response = requests.post(url, json=payload, headers=headers)
    data = response.json()
    print(data)

def main():
    try:
        # username = fetch_random_user_freeapi()
        # print(f"username: {username}")
        # response = fetch_random_user()
        # print(f"Response: {response}")
        post_login()
    except Exception as e:
        print(str(e))

if __name__ == "__main__":
    main()