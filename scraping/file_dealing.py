import json
import os
import re
from tqdm import tqdm

def merge():
    print("Merge start")
    # Merge all json files thus far

    merged_profiles = []

    print("Getting all user profiles in ram")
    nums = get_count_of_files()
    for num in tqdm(list(range(nums))):
        with open(f'data/all_detailed_profiles{num}.json', 'r') as file:
            response = file.read()
            profiles = json.loads(response)

            profiles = list(filter(None, profiles))
            merged_profiles += profiles

    print("Merging files")
    with open('data/all_detailed_profiles.json', 'w') as file:
        json.dump(merged_profiles, file)

def remove_dupes():
    print("Removing dupes function start")

    all_profiles = []
    with open('data/all_profiles.json', 'r') as file:
        response = file.read()
        all_profiles = json.loads(response)

        all_profiles = list(filter(None, all_profiles))

    # Get all_profiles_not_found_yet
    with open('data/all_detailed_profiles.json', 'r') as file:
        response = file.read()
        all_detailed_users = json.loads(response)

        all_detailed_users = list(filter(None, all_detailed_users))

        print("Removing dupes")
        found_uuids = [p['uuid'] for p in all_detailed_users]
        all_profiles_not_found_yet = [p for p in tqdm(all_profiles) if p['uuid'] not in found_uuids]

        print("Dumping to all_profiles_not_found_yet.json")
        with open('data/all_profiles_not_found_yet.json', 'w') as file:
            json.dump(all_profiles_not_found_yet, file)


def get_count_of_files():
    return len([item for item in os.listdir("./data") if re.match(r"all_detailed_profiles[\d]+\.json", item)])

def remove_overall_dupes():
    print('remove dupes again')

    new_detailed_users = []
    uuids = []

    with open('data/all_detailed_profiles.json', 'r') as file:
        response = file.read()
        all_detailed_users = json.loads(response)

        all_detailed_users = list(filter(None, all_detailed_users))

    # Keep first occurance of each uuid
    for user in tqdm(all_detailed_users):
        if user['uuid'] not in uuids:
            new_detailed_users.append(user)
            uuids.append(user['uuid'])

    with open('data/all_detailed_profiles.json', 'w') as write:
        json.dump(new_detailed_users, write)