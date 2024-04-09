import requests
from selenium_driver import driversetup
import codeforces
import codechef
import leetcode
import getUser

driver = driversetup()


def get_submissions(username, platform):
    print(f"Getting submissions for {platform}...")
    if platform == 'codeforces':
        return codeforces.get_problems_solved(username)
    elif platform == 'codechef':
        return codechef.get_problems_solved(driver, username)
    elif platform == 'leetcode':
        return leetcode.get_problems_solved(username)


def get_rating(username, platform):
    print(f"Getting rating for {platform}...")
    if platform == 'codeforces':
        return codeforces.get_rating(username)
    elif platform == 'codechef':
        return codechef.get_rating(driver, username)
    elif platform == 'leetcode':
        return leetcode.get_rating(username)


def push_to_api(endpoint, data, method='POST'):
    api_endpoint = "http://ec2-13-48-96-215.eu-north-1.compute.amazonaws.com/api/"
    api_url = api_endpoint + endpoint
    headers = {
        'Authorization': 'Bearer C6efvByQWTLM8DTlyImyv_tL7aPVAVLvISzI_1ssvJo',
        'Content-Type': 'application/json'
    }
    try:
        if method.upper() == 'POST':
            response = requests.post(api_url, json=data, headers=headers)
        elif method.upper() == 'PATCH':
            response = requests.patch(api_url, json=data, headers=headers)
        response.raise_for_status()
        print("Data pushed successfully.")
    except requests.exceptions.RequestException as e:
        print(f"Failed to push data. Error: {e}")


def run_tasks(users):
    for user in users:
        print(f"Running tasks for {user['username']}...")
        username = user['username']
        codechef_id = user['codechef_id']
        codeforces_id = user['codeforces_id']
        leetcode_id = user['leetcode_id']
        rating_data = {
            'email': user['email'],
            'first_name': user['first_name'],
            'last_name': user['last_name'],
        }
        cfrating = int(get_rating(codeforces_id, 'codeforces'))
        ccrating = int(get_rating(codechef_id, 'codechef'))
        lcrating = int(get_rating(leetcode_id, 'leetcode'))
        if (cfrating != -1):
            rating_data['codeforces_rating'] = cfrating
        if (ccrating != -1):
            rating_data['codechef_rating'] = ccrating
        if (lcrating != -1):
            rating_data['leetcode_rating'] = lcrating
        push_to_api(f'user/{username}/update', rating_data, method='PATCH')

        submissions = []
        for platform in ['leetcode', 'codeforces', 'codechef']:
            submissions.extend(get_submissions(user[platform+'_id'], platform))

        push_to_api(f'user/{username}/updatesubmissions', submissions)


def main():
    users = getUser.get_user()
    run_tasks(users)


if __name__ == "__main__":
    main()
