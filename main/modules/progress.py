import os
import time
import json
import requests
from localStoragePy import localStoragePy
from main.modules.path import progressjson


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


# Function to print and write anime progress to progressjson
def process_anime_progress(media_list, progress_data):
    for media_list_section in media_list['lists']:
        for entry in media_list_section['entries']:
            anime_id = entry['media']['id']
            title_romaji = entry['media']['title']['romaji']
            episodes_watched = entry['progress']
            total_episodes = entry['media'].get('episodes')

            # Prepare the progress value
            if total_episodes:
                progress_value = f"{episodes_watched}/{total_episodes}"
            else:
                progress_value = f"{episodes_watched}/?"

            # Print the progress
            print(f"{anime_id}: {progress_value} ({title_romaji})")

            # Add data to progress_data dictionary
            progress_data[anime_id] = {
                'title': title_romaji,
                'progress': progress_value  # Just save the progress like "12/12"
            }


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

        progress_data = {}

        if current_shows:
            print("Current shows:")
            process_anime_progress(current_shows, progress_data)

        if rewatched_shows:
            print("\nRewatching shows:")
            process_anime_progress(rewatched_shows, progress_data)

        if completed_shows:
            print("\nCompleted shows:")
            process_anime_progress(completed_shows, progress_data)

        if plan_to_watch_shows:
            print("\nPlan to watch shows:")
            process_anime_progress(plan_to_watch_shows, progress_data)

        # Write the progress_data dictionary to progressjson file
        with open(progressjson, 'w', encoding='utf-8') as f:
            json.dump(progress_data, f, ensure_ascii=False, indent=4)

        print("AniList progress has been written to progressjson.")
    else:
        print("AniList access token or user ID not found.")
