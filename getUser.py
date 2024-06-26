import requests
import os
from dotenv import load_dotenv
load_dotenv()

def get_user():
    bearer_token = os.getenv('BEARER_TOKEN')
    api_url = 'https://72zlh1l27i.execute-api.ap-south-1.amazonaws.com/dev/api/users'
    headers = {
        'Authorization': f'Bearer {bearer_token}',
        'Content-Type': 'application/json'
    }
    try:
        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            print("User data fetched successfully:")
            # for user in data:
            #     print(user)
            return data
        else:
            print(f"Failed to fetch user data. Status code: {response.status_code}, Error: {response.text}")
    except Exception as e:
        print("An error occurred:", e)
