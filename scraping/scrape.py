import requests
import json
from tqdm import tqdm
from time import sleep
from datetime import datetime
import os
from dotenv import load_dotenv
from database import add_row, is_uuid_already_scraped
load_dotenv()

print(f"\n\nStarting brand new scrape {datetime.strftime(datetime.now(), '%m/%d/%Y %H:%M:%S')}")

with open('locations.json') as location_json:
    locations = json.load(location_json)

with open('bodies.json') as bodies_json:
    bodies = json.load(bodies_json)
    
api_url = "https://api.barq.app/graphql"
authorization = os.getenv("BARQ_AUTHORIZATION")
headers = {
    "Authorization": "Bearer " + authorization,
    'Content-type': 'application/json',
    "host": "api.barq.app",
    "user-agent": "BARQ/2.10.0+265",
    "accept-encoding": "gzip",
    "accept": "*/*"
}

def save_profile(detailed_profile):         
    add_row(detailed_profile) # Save to database

    if detailed_profile['location']['distance'] is not None:
        too_far_away = detailed_profile['location']['distance'] > 500
        return too_far_away
    else:
        print("Profile missing distance")
        print(detailed_profile)
        return False

for location in locations:
    print(f"Scraping location {location['city']}")
    offset = 0
    increment = 30
    too_far_away = False
    zero_results = False
    count_in_location = 0

    body = bodies['profile_overview']
    body['variables']['filters']['location']['latitude'] = location['lat']
    body['variables']['filters']['location']['longitude'] = location['lon']
    body['variables']['cursor'] = str(offset)

    body_profile_detail = bodies['profile_detail']
    body_profile_detail['variables']['location']['latitude'] = location['lat']
    body_profile_detail['variables']['location']['longitude'] = location['lon']

    # Scrape 30 furs at a time
    while not too_far_away and not zero_results:
        res = requests.post(api_url, data=json.dumps(body), headers=headers)
        try:
            raw_json = json.loads(res.text)
        except ValueError:
            print("Json decode err")
        else:
            if 'data' in raw_json:
                offset += increment
                body['variables']['cursor'] = str(offset)

                profiles = raw_json['data']['profiles']

                if len(profiles) == 0:
                    print("Zero profiles found, continuing")
                    print(raw_json)
                    zero_results = True
                    continue

                # Get details for each individual profile found
                print(f"Scraping batch of {len(profiles)} profiles")
                for profile in tqdm(profiles):
                    if not is_uuid_already_scraped(profile['uuid']):
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
                                    too_far_away = save_profile(detailed_profile)
                                    count_in_location += 1
                                elif 'extensions' in raw_json and raw_json['extensions']['code'] == "RATE_LIMIT_EXCEEDED":
                                    print("Rate limit exceeded, waiting...")
                                    sleep(60)
                                    print("Trying again...")

                                    too_far_away = save_profile(detailed_profile)
                                    count_in_location += 1
                                else:
                                    print("Profile data empty")
                                    print(raw_json)
                            else:
                                print("Invalid json error")
                            
                        sleep(5)
                     
            else:
                print("Invalid json error")

            sleep(10)

    print(f"Done scraping {count_in_location} furs in location {location['city']}")
    count_in_location = 0

print("Done")