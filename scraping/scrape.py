import requests
import json
from tqdm import tqdm
from time import sleep
from file_dealing import remove_dupes
from file_dealing import merge
from file_dealing import get_count_of_files
from file_dealing import remove_overall_dupes
from datetime import datetime
import os
import json
from dotenv import load_dotenv
load_dotenv()

print(f"\n\nStarting brand new scrape {datetime.strftime(datetime.now(), '%m/%d/%Y %H:%M:%S')}")

with open('locations.json') as location_json:
    locations = json.load(location_json)

api_url = "https://api.barq.social/graphql"
authorization = os.getenv("barq_authorization")
headers = {
    "Authorization": "Bearer " + authorization,
    'Content-type': 'application/json'
}

# # Clear file
# open('./data/all_profiles.json', 'w', encoding='utf-8').close()

# for location in locations:
#     print(f"scraping {location['location']}")
#     # Get users
#     # all_profiles = []
#     offset = 0
#     increment = 60

#     body = location['search']

#     for i in tqdm(list(range(1000))): # scrape 20k people (20 at at time) or maybe 30?
#         res = requests.post(api_url, data=json.dumps(body), headers=headers)
#         try:
#             raw_json = json.loads(res.text)
#         except ValueError:
#             print("JSON DECODE ERROR")
#         else:
#             if 'data' in raw_json:
#                 offset += increment
#                 body['variables']['offset'] = offset

#                 profiles = raw_json['data']['profiles']
#                 # all_profiles += profiles

#                 with open('./data/all_profiles.json', 'a', encoding='utf-8') as file:
#                     # file.seek(0)
#                     # file.truncate()
#                     json.dump(profiles, file)
#                     file.close()
#             else:
#                 stopped = True
                
#             sleep(0.5)

        
# remove_dupes() # Creates all_profiles_not_found_yet.json


        

with open('./data/all_profiles_not_found_yet.json', 'r') as file:
    response = file.read()
    all_profiles = json.loads(response)

    body = {
        "operationName": "ProfileDetail",
        "variables": {
            "uuid": "0e74a75d-2a71-4a81-86bb-1e5657346cd9",
            "isAd": False,
            "location": {
                "longitude": -149.894852,
                "latitude": 61.216313
            }
        },
        "query": "query ProfileDetail($uuid: String!, $isAd: Boolean, $location: SearchLocationInput) {\n  profile(uuid: $uuid, location: $location) {\n    uuid\n    displayName\n    relationType\n    isAdOptIn\n    isBirthday\n    age\n    profileImage(isAd: $isAd) {\n      image {\n        ...UploadedImage\n        __typename\n      }\n      __typename\n    }\n    privacySettings {\n      ...PrivacyFragment\n      __typename\n    }\n    images {\n      id\n      image {\n        ...UploadedImage\n        __typename\n      }\n      isAd\n      likeCount\n      hasLiked\n      accessPermission\n      __typename\n    }\n    location {\n      type\n      distance\n      place {\n        place\n        region\n        countryCode\n        longitude\n        latitude\n        __typename\n      }\n      __typename\n    }\n    bio {\n      biography\n      genders\n      languages\n      relationshipStatus\n      sexualOrientation\n      interests\n      hobbies {\n        id\n        interest\n        __typename\n      }\n      socialAccounts {\n        ...SocialAccountsFragment\n        __typename\n      }\n      __typename\n    }\n    bioAd {\n      biography\n      sexPositions\n      behaviour\n      safeSex\n      canHost\n      __typename\n    }\n    sonas {\n      id\n      displayName\n      images {\n        id\n        __typename\n      }\n      description\n      hasFursuit\n      species {\n        id\n        displayName\n        __typename\n      }\n      __typename\n    }\n    kinks {\n      kink {\n        id\n        displayName\n        categoryName\n        isVerified\n        isSinglePlayer\n        __typename\n      }\n      pleasureReceive\n      pleasureGive\n      __typename\n    }\n    groups {\n      group {\n        uuid\n        displayName\n        isAd\n        contentRating\n        image {\n          ...UploadedImage\n          __typename\n        }\n        __typename\n      }\n      threadCount\n      replyCount\n      __typename\n    }\n    events {\n      event {\n        uuid\n        displayName\n        isAd\n        contentRating\n        eventBeginAt\n        eventEndAt\n        image {\n          ...UploadedImage\n          __typename\n        }\n        __typename\n      }\n      isWaitingList\n      __typename\n    }\n    roles\n    shareHash\n    __typename\n  }\n}\n\nfragment UploadedImage on UploadedImage {\n  uuid\n  isExplicit\n  contentRating\n  __typename\n}\n\nfragment PrivacyFragment on PrivacySettings {\n  startChat\n  viewAge\n  viewAd\n  viewKinks\n  viewProfile\n  blockAdults\n  blockMinors\n  __typename\n}\n\nfragment SocialAccountsFragment on ProfileSocialAccounts {\n  twitter {\n    value\n    accessPermission\n    __typename\n  }\n  twitterAd {\n    value\n    accessPermission\n    __typename\n  }\n  telegram {\n    value\n    accessPermission\n    __typename\n  }\n  instagram {\n    value\n    accessPermission\n    __typename\n  }\n  steam {\n    value\n    accessPermission\n    __typename\n  }\n  discord {\n    value\n    accessPermission\n    __typename\n  }\n  deviantArt {\n    value\n    accessPermission\n    __typename\n  }\n  furAffinity {\n    value\n    accessPermission\n    __typename\n  }\n  __typename\n}\n"
    }

    stopped = False

    num = get_count_of_files()
    print(f"Writing to file {num}")

    filename = f'./data/all_detailed_profiles{num}.json'

    
    # Clear file
    open(filename, 'w+', encoding='utf-8').close()

    for profile in tqdm(all_profiles):
        body['variables']['uuid'] = profile['uuid']
        res = requests.post(api_url, data=json.dumps(body), headers=headers)
        try:
            raw_json = json.loads(res.text)
        except (ValueError, requests.exceptions.SSLError):
            print("Json decode err")
        else:

            detailed_profile = raw_json['data']['profile']

            with open(filename, 'a', encoding='utf-8') as file:
                json.dump(detailed_profile, file)
                file.close()

            sleep(0.5)



# merge()

# Remove dupes, again
remove_overall_dupes()

print("Done")