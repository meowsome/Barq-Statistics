import json
import os
from dotenv import load_dotenv
from database import add_row
load_dotenv()

print(f"\n\nTesting posting data to database")

with open('test_profile.json') as test_json:
    test_profile = json.load(test_json)

api_url = "https://api.barq.social/graphql"
authorization = os.getenv("barq_authorization")
headers = {
    "Authorization": "Bearer " + authorization,
    'Content-type': 'application/json'
}

if 'data' in test_profile:
    detailed_profile = test_profile['data']['profile']

    print(f"Saving {detailed_profile['displayName']}")
    add_row(detailed_profile) # Save to database
else:
    print("Invalid json error")

print("Done")