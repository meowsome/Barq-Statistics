import requests
import json
from tqdm import tqdm
from time import sleep
from datetime import datetime
import os
from dotenv import load_dotenv
from database import add_row
load_dotenv()

print(f"\n\nStarting brand new scrape {datetime.strftime(datetime.now(), '%m/%d/%Y %H:%M:%S')}")

with open('locations.json') as location_json:
    locations = json.load(location_json)

with open('bodies.json') as bodies_json:
    bodies = json.load(bodies_json)
    
api_url = "https://api.barq.social/graphql"
authorization = os.getenv("barq_authorization")
headers = {
    "Authorization": "Bearer " + authorization,
    'Content-type': 'application/json'
}

for location in locations:
    print(f"Scraping location {location['location']}")
    offset = 0
    increment = 60
    too_far_away = False
    count_in_location = 0

    body = location['search']
    body_profile_detail = bodies['profile_detail']
    body_profile_detail['variables']['location']['latitude'] = body['variables']['search']['location']['latitude']
    body_profile_detail['variables']['location']['longitude'] = body['variables']['search']['location']['longitude']



    # Scrape 60 furs at a time
    while not too_far_away:
        res = requests.post(api_url, data=json.dumps(body), headers=headers)
        try:
            raw_json = json.loads(res.text)
        except ValueError:
            print("Json decode err")
        else:
            if 'data' in raw_json:
                offset += increment
                body['variables']['offset'] = offset

                profiles = raw_json['data']['profiles']

                # Get details for each individual profile found
                print(f"Scraping batch of {len(profiles)} profiles")
                for profile in tqdm(profiles):
                    body_profile_detail['variables']['uuid'] = profile['uuid'] # Specify uuid to get details of

                    res = requests.post(api_url, data=json.dumps(body_profile_detail), headers=headers) # Send request
                    try:
                        raw_json = json.loads(res.text)
                    except (ValueError, requests.exceptions.SSLError):
                        print("Json decode err")
                    else:
                        if 'data' in raw_json:
                            detailed_profile = raw_json['data']['profile']

                            if detailed_profile:
                                print(f"Saving {detailed_profile['displayName']}")
                                add_row(detailed_profile) # Save to database

                                if detailed_profile['location']['distance'] > 500:
                                    too_far_away = True
                            elif 'extensions' in raw_json and raw_json['extensions']['code'] == "RATE_LIMIT_EXCEEDED":
                                print("Rate limit exceeded, waiting...")
                                sleep(60)
                                print("Trying again...")
                                
                                print(f"Saving {detailed_profile['displayName']}")
                                add_row(detailed_profile) # Save to database

                                if detailed_profile['location']['distance'] > 500:
                                    too_far_away = True
                            else:
                                print("Profile data empty")
                                print(raw_json)
                        else:
                            print("Invalid json error")
                        
                    sleep(5)
                count_in_location += len(profiles)
                     
            else:
                print("Invalid json error")

            sleep(10)

    print(f"Done scraping {count_in_location} furs in location {location['location']}")
    count_in_location = 0

print("Done")