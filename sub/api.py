import requests
import re
from localStoragePy import localStoragePy

watching_db = localStoragePy('watching', 'json')
ls = localStoragePy('Tanpopo Rewrite', 'json')


def get_currently_watching_anime(user_id):
    # AniList API endpoint
    url = 'https://graphql.anilist.co'

    # GraphQL query to fetch currently watching anime
    query = '''
    query ($userId: Int) {
      MediaListCollection(userId: $userId, type: ANIME, status: CURRENT) {
        lists {
          name
          entries {
            media {
              id
              title {
                romaji
                english
              }
              episodes
              coverImage {
                large
              }
            }
            progress
          }
        }
      }
    }
    '''

    # Variables for the query
    variables = {
        'userId': user_id
    }

    # Making the HTTP request to the AniList API
    response = requests.post(url, json={'query': query, 'variables': variables})

    # Raise an exception if the request was unsuccessful
    response.raise_for_status()

    # Parse the JSON response
    data = response.json()

    # Extract and return the list of currently watching anime
    currently_watching = data['data']['MediaListCollection']['lists'][0]['entries']

    return currently_watching


def filter_description(description):
    # Remove <br> tags and other HTML markup
    filtered_description = re.sub(r'<.*?>', '', description)
    return filtered_description


# Function to rearrange data alphabetically by anime title (Romaji)
def sort_data_alphabetically(data):
    sorted_data = sorted(data, key=lambda x: x['Titles']['Romaji'])
    return sorted_data


def format_anime_info(media_info):
    return {
        "ID": media_info["id"],
        "Titles": {
            "Romaji": media_info["title"]["romaji"],
            "English": media_info["title"]["english"],
            "Native": media_info["title"]["native"]
        },
        "CoverImage": media_info.get("coverImage", {}).get("extraLarge", "N/A"),
        "Description": filter_description(media_info.get("description", "No description available"))
    }


def get_anime_list_data(access_token, user_id, list_type):
    # GraphQL query to fetch anime list based on list_type
    query = '''
    query ($userName: String) {
      MediaListCollection(userName: $userName, type: ANIME, status: CURRENT) {
        lists {
          name
          entries {
            media {
              id
              title {
                romaji
                english
              }
              episodes
              coverImage {
                large
              }
            }
            progress
          }
        }
      }
    }
    '''

    # Variables for the GraphQL query
    variables = {
        'userId': user_id,
    }

    # API endpoint
    url = 'https://graphql.anilist.co'

    # Headers including the access token
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }

    # Send POST request to AniList API
    response = requests.post(url, json={'query': query, 'variables': variables}, headers=headers)

    if response.status_code == 200:
        data = response.json()
        anime_list = data['data']['MediaListCollection']['lists'][0]['entries']  # Assuming one list is fetched
        return anime_list
    else:
        print(f"Error fetching anime list: {response.status_code} - {response.text}")
        return None


# Example usage:
def get_anime_list():
    user_id = ls.getItem("user_id")

    anime_list = get_currently_watching_anime(user_id)
    format = format_anime_info(anime_list)
    sort = sort_data_alphabetically(format)

    if anime_list:
        watching_db.setItem("watching", sort)

    else:
        print("Failed to fetch anime list.")
