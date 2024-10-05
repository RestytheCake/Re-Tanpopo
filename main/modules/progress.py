import os
import time
import json
import requests
from localStoragePy import localStoragePy

# Function to fetch anime information from AniList, including total episodes and progress
def fetch_anime_info_with_progress(anime_ids, access_token):
    base_url = "https://graphql.anilist.co"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    anime_info = []

    for anime_id in anime_ids:
        query = '''
        query ($id: Int) {
          Media(id: $id, type: ANIME) {
            id
            title {
              romaji
              english
            }
            episodes
            status
          }
        }
        '''

        variables = {
            "id": anime_id
        }

        response = requests.post(base_url, headers=headers, json={"query": query, "variables": variables})
        data = response.json()

        if "errors" in data:
            print(f"Error fetching data for anime with ID {anime_id}: {data['errors'][0]['message']}")
        else:
            anime_info.append(data['data']['Media'])

        # Adding delay to avoid hitting rate limit
        time.sleep(0.5)

    return anime_info


# Function to fetch the user's anime progress from AniList
def get_media_list_collection(access_token, user_id):
    def fetch_media_list(status):
        query = '''
        query ($userId: Int, $type: MediaType, $status: MediaListStatus) {
          MediaListCollection (userId: $userId, type: $type, status: $status) {
            lists {
              entries {
                media {
                  id
                  title {
                    romaji
                  }
                  episodes
                }
                progress
                status
              }
            }
          }
        }
        '''

        variables = {
            'userId': user_id,
            'type': 'ANIME',
            'status': status
        }

        response = requests.post('https://graphql.anilist.co', json={'query': query, 'variables': variables},
                                 headers=headers)

        if response.status_code == 200:
            data = response.json()
            if 'errors' in data:
                print("Error occurred:")
                for error in data['errors']:
                    print(error['message'])
            else:
                return data['data']['MediaListCollection']
        else:
            print(f"Request failed with status code {response.status_code}")
            print(f"Response content: {response.content.decode('utf-8')}")
            return None

    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    current_shows = fetch_media_list('CURRENT')
    time.sleep(1)
    rewatched_shows = fetch_media_list('REPEATING')
    time.sleep(1)
    completed_shows = fetch_media_list('COMPLETED')
    time.sleep(1)
    plan_to_watch_shows = fetch_media_list('PLANNING')
    time.sleep(1)

    return current_shows, rewatched_shows, completed_shows, plan_to_watch_shows


# Function to print progress and total episodes for each anime
def print_anime_progress(media_list):
    for media_list_section in media_list['lists']:
        for entry in media_list_section['entries']:
            anime_id = entry['media']['id']
            title_romaji = entry['media']['title']['romaji']
            episodes_watched = entry['progress']
            total_episodes = entry['media'].get('episodes')

            # Check if the show has a total episode count
            if total_episodes:
                print(f"{anime_id}: {episodes_watched}/{total_episodes} ({title_romaji})")
            else:
                # If ongoing with unknown total episodes, print progress/?
                print(f"{anime_id}: {episodes_watched}/? ({title_romaji})")


def Load_API():
    ls = localStoragePy('Tanpopo Rewrite', 'json')
    # Fetch the AniList access token and user ID from account.json
    try:
        access_token = ls.getItem('access_token')
        user_id = ls.getItem('user_id')
    except FileNotFoundError:
        access_token = None
        user_id = None

    if access_token and user_id:
        current_shows, rewatched_shows, completed_shows, plan_to_watch_shows = get_media_list_collection(access_token, user_id)
        
        if current_shows:
            print("Current shows:")
            print_anime_progress(current_shows)
        
        if rewatched_shows:
            print("\nRewatching shows:")
            print_anime_progress(rewatched_shows)
        
        if completed_shows:
            print("\nCompleted shows:")
            print_anime_progress(completed_shows)
        
        if plan_to_watch_shows:
            print("\nPlan to watch shows:")
            print_anime_progress(plan_to_watch_shows)

        print("AniList progress display complete.")
    else:
        print("AniList access token or user ID not found.")


# Call Load_API to start the process
Load_API()
