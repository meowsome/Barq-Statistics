import requests
import json
from tqdm import tqdm
from time import sleep
from file_dealing import remove_dupes
from file_dealing import merge
from file_dealing import get_count_of_files
from datetime import datetime
import os

print(f"\n\nStarting brand new scrape {datetime.strftime(datetime.now(), '%m/%d/%Y %H:%M:%S')}")

locations = [{
    "location": "mississippi",
    "search": {
        "operationName": "ProfileOverview",
        "variables": {
            "offset": 0,
            "limit": 60,
            "search": {
                "isAd": False,
                "location": {
                    "latitude": 33.482068,
                    "longitude": -89.728137,
                    "placeId": "170595",
                    "type": "distance"
                }
            },
            "isAd": False
        },
        "query": "query ProfileOverview($isAd: Boolean, $search: ProfileSearchInput!, $offset: Int = 0, $limit: Int = 30) {\n  profiles(search: $search, offset: $offset, limit: $limit) {\n    uuid\n    displayName\n    relationType\n    profileImage(isAd: $isAd) {\n      image {\n        ...UploadedImage\n        __typename\n      }\n      __typename\n    }\n    location {\n      type\n      distance\n      searchDistance\n      place {\n        place\n        countryCode\n        __typename\n      }\n      __typename\n    }\n    roles\n    __typename\n  }\n}\n\nfragment UploadedImage on UploadedImage {\n  uuid\n  isExplicit\n  contentRating\n  __typename\n}\n"
    },
    "fullprofile": {
        "operationName": "ProfileDetail",
        "variables": {
            "uuid": "9b1dab7b-b5a6-4d56-af09-0cf97f3cfae3",
            "isAd": False,
            "location": {
                "longitude": -89.728137,
                "latitude": 33.482068
            }
        },
        "query": "query ProfileDetail($uuid: String!, $isAd: Boolean, $location: SearchLocationInput) {\n  profile(uuid: $uuid, location: $location) {\n    uuid\n    displayName\n    relationType\n    isAdOptIn\n    isBirthday\n    age\n    profileImage(isAd: $isAd) {\n      image {\n        ...UploadedImage\n        __typename\n      }\n      __typename\n    }\n    privacySettings {\n      ...PrivacyFragment\n      __typename\n    }\n    images {\n      id\n      image {\n        ...UploadedImage\n        __typename\n      }\n      isAd\n      likeCount\n      hasLiked\n      accessPermission\n      __typename\n    }\n    location {\n      type\n      distance\n      place {\n        place\n        region\n        countryCode\n        longitude\n        latitude\n        __typename\n      }\n      __typename\n    }\n    bio {\n      biography\n      genders\n      languages\n      relationshipStatus\n      sexualOrientation\n      interests\n      hobbies {\n        id\n        interest\n        __typename\n      }\n      socialAccounts {\n        ...SocialAccountsFragment\n        __typename\n      }\n      __typename\n    }\n    bioAd {\n      biography\n      sexPositions\n      behaviour\n      safeSex\n      canHost\n      __typename\n    }\n    sonas {\n      id\n      displayName\n      images {\n        id\n        __typename\n      }\n      description\n      hasFursuit\n      species {\n        id\n        displayName\n        __typename\n      }\n      __typename\n    }\n    kinks {\n      kink {\n        id\n        displayName\n        categoryName\n        isVerified\n        isSinglePlayer\n        __typename\n      }\n      pleasureReceive\n      pleasureGive\n      __typename\n    }\n    groups {\n      group {\n        uuid\n        displayName\n        isAd\n        contentRating\n        image {\n          ...UploadedImage\n          __typename\n        }\n        __typename\n      }\n      threadCount\n      replyCount\n      __typename\n    }\n    events {\n      event {\n        uuid\n        displayName\n        isAd\n        contentRating\n        eventBeginAt\n        eventEndAt\n        image {\n          ...UploadedImage\n          __typename\n        }\n        __typename\n      }\n      isWaitingList\n      __typename\n    }\n    roles\n    shareHash\n    __typename\n  }\n}\n\nfragment UploadedImage on UploadedImage {\n  uuid\n  isExplicit\n  contentRating\n  __typename\n}\n\nfragment PrivacyFragment on PrivacySettings {\n  startChat\n  viewAge\n  viewAd\n  viewKinks\n  viewProfile\n  blockAdults\n  blockMinors\n  __typename\n}\n\nfragment SocialAccountsFragment on ProfileSocialAccounts {\n  twitter {\n    value\n    accessPermission\n    __typename\n  }\n  twitterAd {\n    value\n    accessPermission\n    __typename\n  }\n  telegram {\n    value\n    accessPermission\n    __typename\n  }\n  instagram {\n    value\n    accessPermission\n    __typename\n  }\n  steam {\n    value\n    accessPermission\n    __typename\n  }\n  discord {\n    value\n    accessPermission\n    __typename\n  }\n  deviantArt {\n    value\n    accessPermission\n    __typename\n  }\n  furAffinity {\n    value\n    accessPermission\n    __typename\n  }\n  __typename\n}\n"
    }
}, {
    "location": "conneticut",
        "search": {
        "operationName": "ProfileOverview",
        "variables": {
            "offset": 0,
            "limit": 60,
            "search": {
                "isAd": False,
                "location": {
                    "placeId": "158385",
                    "latitude": 41.222222,
                    "longitude": -73.05706,
                    "type": "distance"
                }
            },
            "isAd": False
        },
        "query": "query ProfileOverview($isAd: Boolean, $search: ProfileSearchInput!, $offset: Int = 0, $limit: Int = 30) {\n  profiles(search: $search, offset: $offset, limit: $limit) {\n    uuid\n    displayName\n    relationType\n    profileImage(isAd: $isAd) {\n      image {\n        ...UploadedImage\n        __typename\n      }\n      __typename\n    }\n    location {\n      type\n      distance\n      searchDistance\n      place {\n        place\n        countryCode\n        __typename\n      }\n      __typename\n    }\n    roles\n    __typename\n  }\n}\n\nfragment UploadedImage on UploadedImage {\n  uuid\n  isExplicit\n  contentRating\n  __typename\n}\n"
    },
    "fullprofile": {
        "operationName": "ProfileDetail",
        "variables": {
            "uuid": "1414506f-bdeb-4cc6-bf5b-03291f1e14de",
            "isAd": False,
            "location": {
                "longitude": -73.05706,
                "latitude": 41.222222
            }
        },
        "query": "query ProfileDetail($uuid: String!, $isAd: Boolean, $location: SearchLocationInput) {\n  profile(uuid: $uuid, location: $location) {\n    uuid\n    displayName\n    relationType\n    isAdOptIn\n    isBirthday\n    age\n    profileImage(isAd: $isAd) {\n      image {\n        ...UploadedImage\n        __typename\n      }\n      __typename\n    }\n    privacySettings {\n      ...PrivacyFragment\n      __typename\n    }\n    images {\n      id\n      image {\n        ...UploadedImage\n        __typename\n      }\n      isAd\n      likeCount\n      hasLiked\n      accessPermission\n      __typename\n    }\n    location {\n      type\n      distance\n      place {\n        place\n        region\n        countryCode\n        longitude\n        latitude\n        __typename\n      }\n      __typename\n    }\n    bio {\n      biography\n      genders\n      languages\n      relationshipStatus\n      sexualOrientation\n      interests\n      hobbies {\n        id\n        interest\n        __typename\n      }\n      socialAccounts {\n        ...SocialAccountsFragment\n        __typename\n      }\n      __typename\n    }\n    bioAd {\n      biography\n      sexPositions\n      behaviour\n      safeSex\n      canHost\n      __typename\n    }\n    sonas {\n      id\n      displayName\n      images {\n        id\n        __typename\n      }\n      description\n      hasFursuit\n      species {\n        id\n        displayName\n        __typename\n      }\n      __typename\n    }\n    kinks {\n      kink {\n        id\n        displayName\n        categoryName\n        isVerified\n        isSinglePlayer\n        __typename\n      }\n      pleasureReceive\n      pleasureGive\n      __typename\n    }\n    groups {\n      group {\n        uuid\n        displayName\n        isAd\n        contentRating\n        image {\n          ...UploadedImage\n          __typename\n        }\n        __typename\n      }\n      threadCount\n      replyCount\n      __typename\n    }\n    events {\n      event {\n        uuid\n        displayName\n        isAd\n        contentRating\n        eventBeginAt\n        eventEndAt\n        image {\n          ...UploadedImage\n          __typename\n        }\n        __typename\n      }\n      isWaitingList\n      __typename\n    }\n    roles\n    shareHash\n    __typename\n  }\n}\n\nfragment UploadedImage on UploadedImage {\n  uuid\n  isExplicit\n  contentRating\n  __typename\n}\n\nfragment PrivacyFragment on PrivacySettings {\n  startChat\n  viewAge\n  viewAd\n  viewKinks\n  viewProfile\n  blockAdults\n  blockMinors\n  __typename\n}\n\nfragment SocialAccountsFragment on ProfileSocialAccounts {\n  twitter {\n    value\n    accessPermission\n    __typename\n  }\n  twitterAd {\n    value\n    accessPermission\n    __typename\n  }\n  telegram {\n    value\n    accessPermission\n    __typename\n  }\n  instagram {\n    value\n    accessPermission\n    __typename\n  }\n  steam {\n    value\n    accessPermission\n    __typename\n  }\n  discord {\n    value\n    accessPermission\n    __typename\n  }\n  deviantArt {\n    value\n    accessPermission\n    __typename\n  }\n  furAffinity {\n    value\n    accessPermission\n    __typename\n  }\n  __typename\n}\n"
    }
}, {
    "location": "south dakota",
    "search": {
        "operationName": "ProfileOverview",
        "variables": {
            "offset": 0,
            "limit": 60,
            "search": {
                "isAd": False,
                "location": {
                    "placeId": "154103",
                    "latitude": 44.086933,
                    "longitude": -103.227448,
                    "type": "distance"
                }
            },
            "isAd": False
        },
        "query": "query ProfileOverview($isAd: Boolean, $search: ProfileSearchInput!, $offset: Int = 0, $limit: Int = 30) {\n  profiles(search: $search, offset: $offset, limit: $limit) {\n    uuid\n    displayName\n    relationType\n    profileImage(isAd: $isAd) {\n      image {\n        ...UploadedImage\n        __typename\n      }\n      __typename\n    }\n    location {\n      type\n      distance\n      searchDistance\n      place {\n        place\n        countryCode\n        __typename\n      }\n      __typename\n    }\n    roles\n    __typename\n  }\n}\n\nfragment UploadedImage on UploadedImage {\n  uuid\n  isExplicit\n  contentRating\n  __typename\n}\n"
    },
    "fullprofile": {
        "operationName": "ProfileDetail",
        "variables": {
            "uuid": "7801b1ea-e284-403e-895d-d6fa3a6b3e11",
            "isAd": False,
            "location": {
                "longitude": -103.227448,
                "latitude": 44.086933
            }
        },
        "query": "query ProfileDetail($uuid: String!, $isAd: Boolean, $location: SearchLocationInput) {\n  profile(uuid: $uuid, location: $location) {\n    uuid\n    displayName\n    relationType\n    isAdOptIn\n    isBirthday\n    age\n    profileImage(isAd: $isAd) {\n      image {\n        ...UploadedImage\n        __typename\n      }\n      __typename\n    }\n    privacySettings {\n      ...PrivacyFragment\n      __typename\n    }\n    images {\n      id\n      image {\n        ...UploadedImage\n        __typename\n      }\n      isAd\n      likeCount\n      hasLiked\n      accessPermission\n      __typename\n    }\n    location {\n      type\n      distance\n      place {\n        place\n        region\n        countryCode\n        longitude\n        latitude\n        __typename\n      }\n      __typename\n    }\n    bio {\n      biography\n      genders\n      languages\n      relationshipStatus\n      sexualOrientation\n      interests\n      hobbies {\n        id\n        interest\n        __typename\n      }\n      socialAccounts {\n        ...SocialAccountsFragment\n        __typename\n      }\n      __typename\n    }\n    bioAd {\n      biography\n      sexPositions\n      behaviour\n      safeSex\n      canHost\n      __typename\n    }\n    sonas {\n      id\n      displayName\n      images {\n        id\n        __typename\n      }\n      description\n      hasFursuit\n      species {\n        id\n        displayName\n        __typename\n      }\n      __typename\n    }\n    kinks {\n      kink {\n        id\n        displayName\n        categoryName\n        isVerified\n        isSinglePlayer\n        __typename\n      }\n      pleasureReceive\n      pleasureGive\n      __typename\n    }\n    groups {\n      group {\n        uuid\n        displayName\n        isAd\n        contentRating\n        image {\n          ...UploadedImage\n          __typename\n        }\n        __typename\n      }\n      threadCount\n      replyCount\n      __typename\n    }\n    events {\n      event {\n        uuid\n        displayName\n        isAd\n        contentRating\n        eventBeginAt\n        eventEndAt\n        image {\n          ...UploadedImage\n          __typename\n        }\n        __typename\n      }\n      isWaitingList\n      __typename\n    }\n    roles\n    shareHash\n    __typename\n  }\n}\n\nfragment UploadedImage on UploadedImage {\n  uuid\n  isExplicit\n  contentRating\n  __typename\n}\n\nfragment PrivacyFragment on PrivacySettings {\n  startChat\n  viewAge\n  viewAd\n  viewKinks\n  viewProfile\n  blockAdults\n  blockMinors\n  __typename\n}\n\nfragment SocialAccountsFragment on ProfileSocialAccounts {\n  twitter {\n    value\n    accessPermission\n    __typename\n  }\n  twitterAd {\n    value\n    accessPermission\n    __typename\n  }\n  telegram {\n    value\n    accessPermission\n    __typename\n  }\n  instagram {\n    value\n    accessPermission\n    __typename\n  }\n  steam {\n    value\n    accessPermission\n    __typename\n  }\n  discord {\n    value\n    accessPermission\n    __typename\n  }\n  deviantArt {\n    value\n    accessPermission\n    __typename\n  }\n  furAffinity {\n    value\n    accessPermission\n    __typename\n  }\n  __typename\n}\n"
    }
}, {
    "location": "nyc",
    "search": {
        "operationName": "ProfileOverview",
        "variables": {
            "offset": 0,
            "limit": 60,
            "search": {
                "isAd": False,
                "location": {
                    "placeId": "832",
                    "latitude": 40.7306,
                    "longitude": -73.9866,
                    "type": "distance"
                }
            },
            "isAd": False
        },
        "query": "query ProfileOverview($isAd: Boolean, $search: ProfileSearchInput!, $offset: Int = 0, $limit: Int = 30) {\n  profiles(search: $search, offset: $offset, limit: $limit) {\n    uuid\n    displayName\n    relationType\n    profileImage(isAd: $isAd) {\n      image {\n        ...UploadedImage\n        __typename\n      }\n      __typename\n    }\n    location {\n      type\n      distance\n      searchDistance\n      place {\n        place\n        countryCode\n        __typename\n      }\n      __typename\n    }\n    roles\n    __typename\n  }\n}\n\nfragment UploadedImage on UploadedImage {\n  uuid\n  isExplicit\n  contentRating\n  __typename\n}\n"
    },
    "fullprofile": {
        "operationName": "ProfileDetail",
        "variables": {
            "uuid": "1fcd1e76-58ad-46cc-8fe0-d68ebd92c63c",
            "isAd": False,
            "location": {
                "longitude": -73.9866,
                "latitude": 40.7306
            }
        },
        "query": "query ProfileDetail($uuid: String!, $isAd: Boolean, $location: SearchLocationInput) {\n  profile(uuid: $uuid, location: $location) {\n    uuid\n    displayName\n    relationType\n    isAdOptIn\n    isBirthday\n    age\n    profileImage(isAd: $isAd) {\n      image {\n        ...UploadedImage\n        __typename\n      }\n      __typename\n    }\n    privacySettings {\n      ...PrivacyFragment\n      __typename\n    }\n    images {\n      id\n      image {\n        ...UploadedImage\n        __typename\n      }\n      isAd\n      likeCount\n      hasLiked\n      accessPermission\n      __typename\n    }\n    location {\n      type\n      distance\n      place {\n        place\n        region\n        countryCode\n        longitude\n        latitude\n        __typename\n      }\n      __typename\n    }\n    bio {\n      biography\n      genders\n      languages\n      relationshipStatus\n      sexualOrientation\n      interests\n      hobbies {\n        id\n        interest\n        __typename\n      }\n      socialAccounts {\n        ...SocialAccountsFragment\n        __typename\n      }\n      __typename\n    }\n    bioAd {\n      biography\n      sexPositions\n      behaviour\n      safeSex\n      canHost\n      __typename\n    }\n    sonas {\n      id\n      displayName\n      images {\n        id\n        __typename\n      }\n      description\n      hasFursuit\n      species {\n        id\n        displayName\n        __typename\n      }\n      __typename\n    }\n    kinks {\n      kink {\n        id\n        displayName\n        categoryName\n        isVerified\n        isSinglePlayer\n        __typename\n      }\n      pleasureReceive\n      pleasureGive\n      __typename\n    }\n    groups {\n      group {\n        uuid\n        displayName\n        isAd\n        contentRating\n        image {\n          ...UploadedImage\n          __typename\n        }\n        __typename\n      }\n      threadCount\n      replyCount\n      __typename\n    }\n    events {\n      event {\n        uuid\n        displayName\n        isAd\n        contentRating\n        eventBeginAt\n        eventEndAt\n        image {\n          ...UploadedImage\n          __typename\n        }\n        __typename\n      }\n      isWaitingList\n      __typename\n    }\n    roles\n    shareHash\n    __typename\n  }\n}\n\nfragment UploadedImage on UploadedImage {\n  uuid\n  isExplicit\n  contentRating\n  __typename\n}\n\nfragment PrivacyFragment on PrivacySettings {\n  startChat\n  viewAge\n  viewAd\n  viewKinks\n  viewProfile\n  blockAdults\n  blockMinors\n  __typename\n}\n\nfragment SocialAccountsFragment on ProfileSocialAccounts {\n  twitter {\n    value\n    accessPermission\n    __typename\n  }\n  twitterAd {\n    value\n    accessPermission\n    __typename\n  }\n  telegram {\n    value\n    accessPermission\n    __typename\n  }\n  instagram {\n    value\n    accessPermission\n    __typename\n  }\n  steam {\n    value\n    accessPermission\n    __typename\n  }\n  discord {\n    value\n    accessPermission\n    __typename\n  }\n  deviantArt {\n    value\n    accessPermission\n    __typename\n  }\n  furAffinity {\n    value\n    accessPermission\n    __typename\n  }\n  __typename\n}\n"
    }
}, {
    "location": "washington",
    "search": {
        "operationName": "ProfileOverview",
        "variables": {
            "offset": 0,
            "limit": 60,
            "search": {
                "isAd": False,
                "location": {
                    "placeId": "152504",
                    "latitude": 47.603832,
                    "longitude": -122.330062,
                    "type": "distance"
                }
            },
            "isAd": False
        },
        "query": "query ProfileOverview($isAd: Boolean, $search: ProfileSearchInput!, $offset: Int = 0, $limit: Int = 30) {\n  profiles(search: $search, offset: $offset, limit: $limit) {\n    uuid\n    displayName\n    relationType\n    profileImage(isAd: $isAd) {\n      image {\n        ...UploadedImage\n        __typename\n      }\n      __typename\n    }\n    location {\n      type\n      distance\n      searchDistance\n      place {\n        place\n        countryCode\n        __typename\n      }\n      __typename\n    }\n    roles\n    __typename\n  }\n}\n\nfragment UploadedImage on UploadedImage {\n  uuid\n  isExplicit\n  contentRating\n  __typename\n}\n"
    },
    "fullprofile": {
        "operationName": "ProfileDetail",
        "variables": {
            "uuid": "0292c608-d308-4348-ae86-0dcc31eae89e",
            "isAd": False,
            "location": {
                "longitude": -122.330062,
                "latitude": 47.603832
            }
        },
        "query": "query ProfileDetail($uuid: String!, $isAd: Boolean, $location: SearchLocationInput) {\n  profile(uuid: $uuid, location: $location) {\n    uuid\n    displayName\n    relationType\n    isAdOptIn\n    isBirthday\n    age\n    profileImage(isAd: $isAd) {\n      image {\n        ...UploadedImage\n        __typename\n      }\n      __typename\n    }\n    privacySettings {\n      ...PrivacyFragment\n      __typename\n    }\n    images {\n      id\n      image {\n        ...UploadedImage\n        __typename\n      }\n      isAd\n      likeCount\n      hasLiked\n      accessPermission\n      __typename\n    }\n    location {\n      type\n      distance\n      place {\n        place\n        region\n        countryCode\n        longitude\n        latitude\n        __typename\n      }\n      __typename\n    }\n    bio {\n      biography\n      genders\n      languages\n      relationshipStatus\n      sexualOrientation\n      interests\n      hobbies {\n        id\n        interest\n        __typename\n      }\n      socialAccounts {\n        ...SocialAccountsFragment\n        __typename\n      }\n      __typename\n    }\n    bioAd {\n      biography\n      sexPositions\n      behaviour\n      safeSex\n      canHost\n      __typename\n    }\n    sonas {\n      id\n      displayName\n      images {\n        id\n        __typename\n      }\n      description\n      hasFursuit\n      species {\n        id\n        displayName\n        __typename\n      }\n      __typename\n    }\n    kinks {\n      kink {\n        id\n        displayName\n        categoryName\n        isVerified\n        isSinglePlayer\n        __typename\n      }\n      pleasureReceive\n      pleasureGive\n      __typename\n    }\n    groups {\n      group {\n        uuid\n        displayName\n        isAd\n        contentRating\n        image {\n          ...UploadedImage\n          __typename\n        }\n        __typename\n      }\n      threadCount\n      replyCount\n      __typename\n    }\n    events {\n      event {\n        uuid\n        displayName\n        isAd\n        contentRating\n        eventBeginAt\n        eventEndAt\n        image {\n          ...UploadedImage\n          __typename\n        }\n        __typename\n      }\n      isWaitingList\n      __typename\n    }\n    roles\n    shareHash\n    __typename\n  }\n}\n\nfragment UploadedImage on UploadedImage {\n  uuid\n  isExplicit\n  contentRating\n  __typename\n}\n\nfragment PrivacyFragment on PrivacySettings {\n  startChat\n  viewAge\n  viewAd\n  viewKinks\n  viewProfile\n  blockAdults\n  blockMinors\n  __typename\n}\n\nfragment SocialAccountsFragment on ProfileSocialAccounts {\n  twitter {\n    value\n    accessPermission\n    __typename\n  }\n  twitterAd {\n    value\n    accessPermission\n    __typename\n  }\n  telegram {\n    value\n    accessPermission\n    __typename\n  }\n  instagram {\n    value\n    accessPermission\n    __typename\n  }\n  steam {\n    value\n    accessPermission\n    __typename\n  }\n  discord {\n    value\n    accessPermission\n    __typename\n  }\n  deviantArt {\n    value\n    accessPermission\n    __typename\n  }\n  furAffinity {\n    value\n    accessPermission\n    __typename\n  }\n  __typename\n}\n"
    }
}, {
    "location": "massachusetts",
    "search": {
        "operationName": "ProfileOverview",
        "variables": {
            "offset": 0,
            "limit": 60,
            "search": {
                "isAd": False,
                "location": {
                    "placeId": "152609",
                    "latitude": 42.360253,
                    "longitude": -71.058291,
                    "type": "distance"
                }
            },
            "isAd": False
        },
        "query": "query ProfileOverview($isAd: Boolean, $search: ProfileSearchInput!, $offset: Int = 0, $limit: Int = 30) {\n  profiles(search: $search, offset: $offset, limit: $limit) {\n    uuid\n    displayName\n    relationType\n    profileImage(isAd: $isAd) {\n      image {\n        ...UploadedImage\n        __typename\n      }\n      __typename\n    }\n    location {\n      type\n      distance\n      searchDistance\n      place {\n        place\n        countryCode\n        __typename\n      }\n      __typename\n    }\n    roles\n    __typename\n  }\n}\n\nfragment UploadedImage on UploadedImage {\n  uuid\n  isExplicit\n  contentRating\n  __typename\n}\n"
    },
    "fullprofile": {
        "operationName": "ProfileDetail",
        "variables": {
            "uuid": "f4a64cb3-c1b7-4fd7-8d94-f35565d21b15",
            "isAd": False,
            "location": {
                "longitude": -71.058291,
                "latitude": 42.360253
            }
        },
        "query": "query ProfileDetail($uuid: String!, $isAd: Boolean, $location: SearchLocationInput) {\n  profile(uuid: $uuid, location: $location) {\n    uuid\n    displayName\n    relationType\n    isAdOptIn\n    isBirthday\n    age\n    profileImage(isAd: $isAd) {\n      image {\n        ...UploadedImage\n        __typename\n      }\n      __typename\n    }\n    privacySettings {\n      ...PrivacyFragment\n      __typename\n    }\n    images {\n      id\n      image {\n        ...UploadedImage\n        __typename\n      }\n      isAd\n      likeCount\n      hasLiked\n      accessPermission\n      __typename\n    }\n    location {\n      type\n      distance\n      place {\n        place\n        region\n        countryCode\n        longitude\n        latitude\n        __typename\n      }\n      __typename\n    }\n    bio {\n      biography\n      genders\n      languages\n      relationshipStatus\n      sexualOrientation\n      interests\n      hobbies {\n        id\n        interest\n        __typename\n      }\n      socialAccounts {\n        ...SocialAccountsFragment\n        __typename\n      }\n      __typename\n    }\n    bioAd {\n      biography\n      sexPositions\n      behaviour\n      safeSex\n      canHost\n      __typename\n    }\n    sonas {\n      id\n      displayName\n      images {\n        id\n        __typename\n      }\n      description\n      hasFursuit\n      species {\n        id\n        displayName\n        __typename\n      }\n      __typename\n    }\n    kinks {\n      kink {\n        id\n        displayName\n        categoryName\n        isVerified\n        isSinglePlayer\n        __typename\n      }\n      pleasureReceive\n      pleasureGive\n      __typename\n    }\n    groups {\n      group {\n        uuid\n        displayName\n        isAd\n        contentRating\n        image {\n          ...UploadedImage\n          __typename\n        }\n        __typename\n      }\n      threadCount\n      replyCount\n      __typename\n    }\n    events {\n      event {\n        uuid\n        displayName\n        isAd\n        contentRating\n        eventBeginAt\n        eventEndAt\n        image {\n          ...UploadedImage\n          __typename\n        }\n        __typename\n      }\n      isWaitingList\n      __typename\n    }\n    roles\n    shareHash\n    __typename\n  }\n}\n\nfragment UploadedImage on UploadedImage {\n  uuid\n  isExplicit\n  contentRating\n  __typename\n}\n\nfragment PrivacyFragment on PrivacySettings {\n  startChat\n  viewAge\n  viewAd\n  viewKinks\n  viewProfile\n  blockAdults\n  blockMinors\n  __typename\n}\n\nfragment SocialAccountsFragment on ProfileSocialAccounts {\n  twitter {\n    value\n    accessPermission\n    __typename\n  }\n  twitterAd {\n    value\n    accessPermission\n    __typename\n  }\n  telegram {\n    value\n    accessPermission\n    __typename\n  }\n  instagram {\n    value\n    accessPermission\n    __typename\n  }\n  steam {\n    value\n    accessPermission\n    __typename\n  }\n  discord {\n    value\n    accessPermission\n    __typename\n  }\n  deviantArt {\n    value\n    accessPermission\n    __typename\n  }\n  furAffinity {\n    value\n    accessPermission\n    __typename\n  }\n  __typename\n}\n"
    }
}, {
    "location": "arkansas",
    "search": {
        "operationName": "ProfileOverview",
        "variables": {
            "offset": 0,
            "limit": 60,
            "search": {
                "isAd": False,
                "location": {
                    "placeId": "158519",
                    "latitude": 34.746481,
                    "longitude": -92.289595,
                    "type": "distance"
                }
            },
            "isAd": False
        },
        "query": "query ProfileOverview($isAd: Boolean, $search: ProfileSearchInput!, $offset: Int = 0, $limit: Int = 30) {\n  profiles(search: $search, offset: $offset, limit: $limit) {\n    uuid\n    displayName\n    relationType\n    profileImage(isAd: $isAd) {\n      image {\n        ...UploadedImage\n        __typename\n      }\n      __typename\n    }\n    location {\n      type\n      distance\n      searchDistance\n      place {\n        place\n        countryCode\n        __typename\n      }\n      __typename\n    }\n    roles\n    __typename\n  }\n}\n\nfragment UploadedImage on UploadedImage {\n  uuid\n  isExplicit\n  contentRating\n  __typename\n}\n"
    },
    "fullprofile": {
        "operationName": "ProfileDetail",
        "variables": {
            "uuid": "8ba7d4a2-35f9-4950-8042-164c4531f5b9",
            "isAd": False,
            "location": {
                "longitude": -92.289595,
                "latitude": 34.746481
            }
        },
        "query": "query ProfileDetail($uuid: String!, $isAd: Boolean, $location: SearchLocationInput) {\n  profile(uuid: $uuid, location: $location) {\n    uuid\n    displayName\n    relationType\n    isAdOptIn\n    isBirthday\n    age\n    profileImage(isAd: $isAd) {\n      image {\n        ...UploadedImage\n        __typename\n      }\n      __typename\n    }\n    privacySettings {\n      ...PrivacyFragment\n      __typename\n    }\n    images {\n      id\n      image {\n        ...UploadedImage\n        __typename\n      }\n      isAd\n      likeCount\n      hasLiked\n      accessPermission\n      __typename\n    }\n    location {\n      type\n      distance\n      place {\n        place\n        region\n        countryCode\n        longitude\n        latitude\n        __typename\n      }\n      __typename\n    }\n    bio {\n      biography\n      genders\n      languages\n      relationshipStatus\n      sexualOrientation\n      interests\n      hobbies {\n        id\n        interest\n        __typename\n      }\n      socialAccounts {\n        ...SocialAccountsFragment\n        __typename\n      }\n      __typename\n    }\n    bioAd {\n      biography\n      sexPositions\n      behaviour\n      safeSex\n      canHost\n      __typename\n    }\n    sonas {\n      id\n      displayName\n      images {\n        id\n        __typename\n      }\n      description\n      hasFursuit\n      species {\n        id\n        displayName\n        __typename\n      }\n      __typename\n    }\n    kinks {\n      kink {\n        id\n        displayName\n        categoryName\n        isVerified\n        isSinglePlayer\n        __typename\n      }\n      pleasureReceive\n      pleasureGive\n      __typename\n    }\n    groups {\n      group {\n        uuid\n        displayName\n        isAd\n        contentRating\n        image {\n          ...UploadedImage\n          __typename\n        }\n        __typename\n      }\n      threadCount\n      replyCount\n      __typename\n    }\n    events {\n      event {\n        uuid\n        displayName\n        isAd\n        contentRating\n        eventBeginAt\n        eventEndAt\n        image {\n          ...UploadedImage\n          __typename\n        }\n        __typename\n      }\n      isWaitingList\n      __typename\n    }\n    roles\n    shareHash\n    __typename\n  }\n}\n\nfragment UploadedImage on UploadedImage {\n  uuid\n  isExplicit\n  contentRating\n  __typename\n}\n\nfragment PrivacyFragment on PrivacySettings {\n  startChat\n  viewAge\n  viewAd\n  viewKinks\n  viewProfile\n  blockAdults\n  blockMinors\n  __typename\n}\n\nfragment SocialAccountsFragment on ProfileSocialAccounts {\n  twitter {\n    value\n    accessPermission\n    __typename\n  }\n  twitterAd {\n    value\n    accessPermission\n    __typename\n  }\n  telegram {\n    value\n    accessPermission\n    __typename\n  }\n  instagram {\n    value\n    accessPermission\n    __typename\n  }\n  steam {\n    value\n    accessPermission\n    __typename\n  }\n  discord {\n    value\n    accessPermission\n    __typename\n  }\n  deviantArt {\n    value\n    accessPermission\n    __typename\n  }\n  furAffinity {\n    value\n    accessPermission\n    __typename\n  }\n  __typename\n}\n"
    }
}]

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
print("Done")