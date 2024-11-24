import mysql.connector
import os
from dotenv import load_dotenv
load_dotenv()

mysql_db = mysql.connector.connect(
    host=os.getenv("mysql_host"),
    user=os.getenv("mysql_user"),
    password=os.getenv("mysql_pass"),
    database=os.getenv("mysql_db")
)

def add_row(user_data):
    cur = mysql_db.cursor()
    uuid = user_data['uuid']
    
    if user_data['bioAd']:
        canHost = user_data['bioAd']['canHost']
        safeSex = user_data['bioAd']['safeSex']
    else:
        canHost = None
        safeSex = None

    main_sql = "INSERT IGNORE INTO users (id, uuid, displayName, username, age, bio, relationshipStatus, sexualOrientation, canHost, safeSex) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    main_val = (user_data['id'], uuid, user_data['displayName'], user_data['username'], user_data['age'], user_data['bio']['biography'], user_data['bio']['relationshipStatus'], user_data['bio']['sexualOrientation'], canHost, safeSex)
    cur.execute(main_sql, main_val)

    if user_data['bioAd'] and user_data['bioAd']['behaviour']:
        for behavior in user_data['bioAd']['behaviour']:
            sexualBehavior_sql = "INSERT IGNORE INTO sexualBehavior (uuid, behavior) VALUES (%s, %s)"
            sexualBehavior_val = (uuid, behavior)

    if user_data['socialAccounts']:
        for social in user_data['socialAccounts']:
            social_sql = "INSERT IGNORE INTO social (uuid, socialNetwork, displayName, value) VALUES (%s, %s, %s, %s)"
            social_val = (uuid, social['socialNetwork'], social['displayName'], social['value'])
            cur.execute(social_sql, social_val)

    location_sql = "INSERT IGNORE INTO locations (uuid, place_id, place, region, country, countryCode, lon, lat) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    location_val = (uuid, user_data['location']['place']['id'], user_data['location']['place']['place'], user_data['location']['place']['region'], user_data['location']['place']['country'], user_data['location']['place']['countryCode'], user_data['location']['place']['longitude'], user_data['location']['place']['latitude'])
    cur.execute(location_sql, location_val)
    
    if user_data['location']['homePlace']:
        homeplace_sql = "INSERT IGNORE INTO homeplaces (uuid, place_id, place, region, country, countryCode, lon, lat) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        homeplace_val = (uuid, user_data['location']['homePlace']['id'], user_data['location']['homePlace']['place'], user_data['location']['homePlace']['region'], user_data['location']['homePlace']['country'], user_data['location']['homePlace']['countryCode'], user_data['location']['homePlace']['longitude'], user_data['location']['homePlace']['latitude'])
        cur.execute(homeplace_sql, homeplace_val)

    if user_data['sonas']:
        for sona in user_data['sonas']:
            sonas_sql = "INSERT IGNORE INTO sonas (uuid, sona_id, displayName, description, hasFursuit, speciesId, speciesDisplayName) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            sonas_val = (uuid, sona['id'], sona['displayName'], sona['description'], sona['hasFursuit'], sona['species']['id'], sona['species']['displayName'])
            cur.execute(sonas_sql, sonas_val)

    if user_data['kinks']:
        for kink in user_data['kinks']:
            kinks_sql = "INSERT IGNORE INTO kinks (uuid, kink_id, displayName, categoryName, receive, give) VALUES (%s, %s, %s, %s, %s, %s)"
            kinks_val = (uuid, kink['kink']['id'], kink['kink']['displayName'], kink['kink']['categoryName'], kink['pleasureReceive'], kink['pleasureGive'])
            cur.execute(kinks_sql, kinks_val)

    if user_data['groups']:
        for group in user_data['groups']:
            groups_sql = "INSERT IGNORE INTO user_groups (uuid, group_id, displayName, contentRating) VALUES (%s, %s, %s, %s)"
            groups_val = (uuid, group['group']['id'], group['group']['displayName'], group['group']['contentRating'])
            cur.execute(groups_sql, groups_val)

    if user_data['bio']['genders']:
        for gender in user_data['bio']['genders']:
            genders_sql = "INSERT IGNORE INTO genders (uuid, gender) VALUES (%s, %s)"
            genders_val = (uuid, gender)
            cur.execute(genders_sql, genders_val)

    if user_data['bio']['languages']:
        for language in user_data['bio']['languages']:
            languages_sql = "INSERT IGNORE INTO languages (uuid, language) VALUES (%s, %s)"
            languages_val = (uuid, language)
            cur.execute(languages_sql, languages_val)

    if user_data['bio']['hobbies']:
        for hobby in user_data['bio']['hobbies']:
            hobbies_sql = "INSERT IGNORE INTO hobbies (uuid, hobby_id, interest) VALUES (%s, %s, %s)"
            hobbies_val = (uuid, hobby['id'], hobby['interest'])
            cur.execute(hobbies_sql, hobbies_val)

    mysql_db.commit()
    cur.close()