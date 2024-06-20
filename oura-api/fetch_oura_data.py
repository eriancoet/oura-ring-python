import json
import os
import requests
from datetime import date, timedelta
from oura import OuraClient
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve Oura API token from environment variables
oura_token = os.getenv('OURA_TOKEN')
if not oura_token:
    raise ValueError("No OURA_TOKEN found. Please set the OURA_TOKEN environment variable in your .env file.")

# Function to make a request and handle responses
def make_request(url, params, headers):
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed with status code {response.status_code}: {response.text}")
        return None

# Fetch heartrate data
heartrate_url = 'https://api.ouraring.com/v2/usercollection/heartrate'
heartrate_params = {
    'start_datetime': '2022-01-01T00:00:00-08:00',
    'end_datetime': '2022-01-31T00:00:00-08:00'
}
headers = {
    'Authorization': f'Bearer {oura_token}',
}
heartrate_data = make_request(heartrate_url, heartrate_params, headers)
if heartrate_data:
    print(json.dumps(heartrate_data, indent=4))

# Uncomment and use this section if you want to fetch workout data
# Fetch workout data
# workout_url = 'https://api.ouraring.com/v2/usercollection/workout'
# workout_params = {
#     'start_date': '2022-01-01',
#     'end_date': '2022-02-01'
# }
# workout_data = make_request(workout_url, workout_params, headers)
# if workout_data:
#     print(json.dumps(workout_data, indent=4))

# Use OuraClient to fetch user info and sleep summary
oura_client = OuraClient(personal_access_token=oura_token)

try:
    who_am_i = oura_client.user_info()
    print(json.dumps(who_am_i, indent=4))
except Exception as e:
    print(f"Error fetching user info: {e}")

try:
    week_past = str(date.today() - timedelta(days=7))
    sleep_summary = oura_client.sleep_summary(start=week_past)
    print(json.dumps(sleep_summary, indent=4))

    # Save sleep summary to a JSON file
    with open('result.json', 'w') as fp:
        json.dump(sleep_summary, fp, indent=4)
except Exception as e:
    print(f"Error fetching sleep summary: {e}")
