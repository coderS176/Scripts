import requests
import json
from datetime import datetime, timedelta


def getCodeforcesContests():
    response = requests.get("https://codeforces.com/api/contest.list")
    codeforcesContests = []
    if response.status_code == 200:
        jsonResponse = json.loads(response.text)
        contests = jsonResponse["result"]
        for contest in contests:
            if contest["phase"] == "BEFORE":
                codeforcesContest = {}
                codeforcesContest["platform"] = "Codeforces"
                codeforcesContest["title"] = contest["name"]
                codeforcesContest["url"] = "https://codeforces.com/contests/" + str(
                    contest["id"])
                codeforcesContest["start_time"] = datetime.strftime(datetime.fromtimestamp(
                    contest["startTimeSeconds"]), '%Y-%m-%dT%H:%M:%S') + '+0530'
                codeforcesContest["duration"] = "PT" + str(contest["durationSeconds"] // 3600).zfill(
                    2) + "H" + str((contest["durationSeconds"] % 3600) // 60).zfill(2) + "M"

                codeforcesContests.append(codeforcesContest)
    return codeforcesContests


def getCodechefContests():
    contest_details = []
    start_date = datetime(2024, 4, 18)
    start_num = 130
    today = datetime.now()
    contest_since_start = (today - start_date).days // 7
    current_num = start_num + contest_since_start+1
    current_date = today + timedelta(days=(2 - today.weekday() + 7) % 7)

    # Find the next Wednesday
    for i in range(5):
        # Generate the contest name
        contest_name = f"Starters {i + current_num}"
        # Generate the contest URL
        contest_url = f"https://www.codechef.com/START{i + current_num}"
        # Calculate the start time (assuming 2:30 PM)
        start_time = current_date.replace(hour=20, minute=0, second=0)
        # Add 2 hours to the start time for the duration
        end_time = start_time + timedelta(hours=2)
        # Format start time and duration as ISO 8601 strings
        start_time_iso = start_time.strftime('%Y-%m-%dT%H:%M:%S')
        duration_iso = "PT2H"  # Duration is 2 hours
        # Define the total number of questions
        total_questions = 8
        # Create contest details dictionary
        contest_info = {
            "title": contest_name,
            "url": contest_url,
            "platform": "Codechef",
            "start_time": start_time_iso,
            "duration": duration_iso,
            "total_questions": total_questions
        }
        # Append contest details to the list
        contest_details.append(contest_info)
        # Move to the next Wednesday for the next iteration
        current_date += timedelta(weeks=1)  # Increment by 1 week

    return contest_details


def generate_leetcode_contests(contest_type, num_days, start_date, contest_num):
    contest_details = []
    current_date = start_date
    for _ in range(num_days):
        # Generate the contest name and URL based on contest type
        if contest_type == "weekly":
            contest_name = f"Weekly Contest {contest_num + _}"
            contest_url = f"https://leetcode.com/contest/weekly-contest-{contest_num + _}/"

        elif contest_type == "biweekly":
            contest_name = f"Biweekly Contest {_+ contest_num}"
            contest_url = f"https://leetcode.com/contest/biweekly-contest-{_+contest_num}/"
        else:
            raise ValueError(
                "Invalid contest type. Must be 'weekly' or 'biweekly'.")

        # Calculate the start time (assuming 8:00 AM in Indian timezone)
        start_time = current_date.replace(hour=8, minute=0, second=0)
        # Add 1.5 hours to the start time for the duration
        end_time = start_time + timedelta(hours=1, minutes=30)
        # Format start time and duration as ISO 8601 strings
        start_time_iso = start_time.strftime('%Y-%m-%dT%H:%M:%S')
        duration_iso = "PT1H30M"  # Duration is 1.5 hours
        # Define the total number of questions
        total_questions = 4
        # Create contest details dictionary
        contest_info = {
            "title": contest_name,
            "url": contest_url,
            "platform": "Leetcode",
            "start_time": start_time_iso,
            "duration": duration_iso,
            "total_questions": total_questions
        }
        # Append contest details to the list
        contest_details.append(contest_info)
        # Move to the next contest date for the next iteration
        current_date += timedelta(
            weeks=2) if contest_type == "biweekly" else timedelta(weeks=1)

    return contest_details


def getLeetcodecontests():
    biweekly_start_date = datetime(2024, 3, 16)
    weekly_start_date = datetime(2024, 3, 3)
    start_weekly_contest_num = 387
    start_biweekly_contest_num = 126
    current_date = datetime.now()

    weekly_contests_since_start = (current_date - weekly_start_date).days / 7
    # print(weekly_contests_since_start)
    biweekly_contests_since_start = (
        current_date - biweekly_start_date).days / 14

    current_weekly_contest_num = start_weekly_contest_num + weekly_contests_since_start+1
    current_biweekly_contest_num = start_biweekly_contest_num + \
        biweekly_contests_since_start+1

    next_weekly_start = current_date + \
        timedelta(days=(7-(current_date - weekly_start_date).days % 7))
    next_biweekly_start = current_date + \
        timedelta(days=(14-(current_date - biweekly_start_date).days % 14))

    weekly_contests = generate_leetcode_contests(
        "weekly", 5, next_weekly_start, int(current_weekly_contest_num))
    biweekly_contests = generate_leetcode_contests(
        "biweekly", 5, next_biweekly_start, int(current_biweekly_contest_num))

    return weekly_contests + biweekly_contests

print(getLeetcodecontests())