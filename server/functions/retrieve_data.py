import pandas as pd
import json

def import_df():
    with open('data/all_detailed_profiles.json', 'r') as file:
        response = file.read()
        all_detailed_users = json.loads(response)

        all_detailed_users = list(filter(None, all_detailed_users))

        # print(all_detailed_users)
        
        return pd.DataFrame(all_detailed_users)

def generic_update(df, column1, column2, column3):
    return df[column1].dropna().apply(lambda items: [item[column2][column3] for item in items])

def update_location(df):
    location = df['location'].apply(pd.Series)
    place = location['place'].apply(pd.Series)
    location.drop('place',axis=1,inplace=True)
    location[place.columns] = place
    df[location.columns] = location
    df.drop('location',axis=1,inplace=True)
    return df

def update_kinks(df):
    print("Update kinks")
    df['kinks'] = df['kinks'].apply(lambda kinks: [kink['kink']['displayName'] for kink in kinks if kink['pleasureReceive'] == 1 or kink['pleasureGive'] == 1] if kinks else [])
    return df

def update_privacy(df):
    print("Update privacy")
    privacySettings = df['privacySettings'].apply(pd.Series)
    df[privacySettings.columns] = privacySettings
    df.drop('privacySettings',axis=1,inplace=True)
    return df

def update_bio(df):
    print("Update bio")
    bio = df['bio'].dropna().apply(pd.Series)
    bio['hobbies'] = bio['hobbies'].apply(lambda hobbies: [hobby['interest'] for hobby in hobbies])
    df[bio.columns] = bio
    df.drop('bio',axis=1,inplace=True)

    df['socialAccounts'] = df['socialAccounts'].dropna().apply(lambda socialAccounts: [acct for acct in socialAccounts.keys() if socialAccounts[acct] and acct != "__typename"] if socialAccounts else None)

    return df

def update_events(df):
    print("Update events")
    df['events'] = generic_update(df, 'events', 'event', 'displayName')
    return df

def update_sonas(df):
    print("Update sonas")
    df['sonas'] = generic_update(df, 'sonas', 'species', 'displayName')
    return df

def update_groups(df):
    print("Update groups")
    df['groups'] = generic_update(df, 'groups', 'group', 'displayName')
    return df

def update_genders(df):
    print("Update genders")
    df['genders'] = df['genders'].astype(str).apply(lambda gender: "Nonbinary" if "non" in gender.lower() and "binary" in gender.lower() else gender)
    df['genders'] = df['genders'].astype(str).apply(lambda gender: "Genderfluid" if "gender" in gender.lower() and "fluid" in gender.lower() else gender)
    return df

def drop_irrelevant_cols(df):
    print("Update irrelevant cols")
    df.drop(['images', 'profileImage', '__typename'], inplace=True, axis=1)
    return df

def apply_settings():
    pd.set_option('display.max_columns', None)

def filter_by_country(df, countryCode='US'):
    return df[df['countryCode'] == countryCode]



# TODO use pipeline instead?? 
# TODO combine non-binary variants in genders
def get_altered_df():
    print("Starting altering df")
    df = import_df()
    apply_settings()
    print(df)
    df = update_location(df)
    df = update_kinks(df)
    df = update_privacy(df)
    df = update_bio(df)
    df = update_events(df)
    df = update_sonas(df)
    df = update_groups(df)
    df = update_genders(df)
    df = drop_irrelevant_cols(df)
    print("done altering df")

    return df