import time
import json
from authwindow import *
from localStoragePy import localStoragePy

ls = localStoragePy('Tanpopo Rewrite', 'json')


# Function to clear the JSON file
def clear_json_file(file_path):
    with open(file_path, 'w') as file:
        json.dump({}, file)


# Function to fetch anime information from AniList
def fetch_anime_info(anime_ids):
    base_url = "https://graphql.anilist.co"
    headers = {"Content-Type": "application/json"}

    anime_info = []

    for anime_id in anime_ids:
        query = '''
        query ($id: Int) {
          Media(id: $id, type: ANIME) {
            id
            title {
              romaji
              english
              native
            }
            status
            averageScore
            genres
            description(asHtml: false)
            coverImage {
              extraLarge
            }
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
        time.sleep(2)

    return anime_info


# Function to filter out unwanted text from anime description
def filter_description(description):
    # Remove <br> tags and other HTML markup
    filtered_description = re.sub(r'<.*?>', '', description)
    return filtered_description


# Function to rearrange data alphabetically by anime title (Romaji)
def sort_data_alphabetically(data):
    sorted_data = sorted(data, key=lambda x: x['Titles']['Romaji'])
    return sorted_data


# Function to format anime information
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


# Function to store anime information in a JSON file
def store_anime_info(formatted_info, filename):
    data = {}

    # Read existing data from the JSON file if it exists
    if os.path.exists(filename):
        with open(filename, "r") as file:
            try:
                data = json.load(file)
            except json.decoder.JSONDecodeError:
                # Handle the case where the file is empty or malformed
                pass

    for section, anime_list in formatted_info.items():
        if section not in data:
            data[section] = []

        for anime_info in anime_list:
            # Check if the entry already exists in the data
            entry_exists = any(entry["ID"] == anime_info["ID"] for entry in data[section])

            # If the entry doesn't exist, append it to the data
            if not entry_exists:
                data[section].append(anime_info)

        # Sort data alphabetically within each section
        data[section] = sort_data_alphabetically(data[section])

    # Write the updated data back to the JSON file
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)

    print("Formatted information stored successfully.")


# Function to retrieve media list collection from AniList
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
                }
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
    time.sleep(2)
    rewatched_shows = fetch_media_list('REPEATING')
    time.sleep(2)
    completed_shows = fetch_media_list('COMPLETED')
    time.sleep(2)
    plan_to_watch_shows = fetch_media_list('PLANNING')
    time.sleep(2)

    return current_shows, rewatched_shows, completed_shows, plan_to_watch_shows


def Load_API():
    # Fetch the AniList access token and user ID from account.json
    try:
        access_token = ls.getItem('access_token')
        user_id = ls.getItem('user_id')
    except FileNotFoundError:
        ToplevelWindow()
        access_token = None
        user_id = None

    if access_token and user_id:
        current_shows, rewatched_shows, completed_shows, plan_to_watch_shows = get_media_list_collection(access_token,
                                                                                                         user_id)
        if current_shows or rewatched_shows or completed_shows or plan_to_watch_shows:
            # Clear the JSON file before refreshing it
            clear_json_file("media_info.json")

            # Proceed with fetching anime information and storing it in the JSON file
            current_anime_ids = set(entry['media']['id'] for media_list in current_shows['lists'] for entry in
                                    media_list.get('entries', [])) if current_shows else set()
            rewatching_anime_ids = set(entry['media']['id'] for media_list in rewatched_shows['lists'] for entry in
                                       media_list.get('entries', [])) if rewatched_shows else set()
            completed_anime_ids = set(entry['media']['id'] for media_list in completed_shows['lists'] for entry in
                                      media_list.get('entries', [])) if completed_shows else set()
            plan_to_watch_anime_ids = set(
                entry['media']['id'] for media_list in plan_to_watch_shows['lists'] for entry in
                media_list.get('entries', [])) if plan_to_watch_shows else set()

            # Fetch anime info for the collected IDs
            current_anime_info = fetch_anime_info(current_anime_ids)
            rewatching_anime_info = fetch_anime_info(rewatching_anime_ids)
            completed_anime_info = fetch_anime_info(completed_anime_ids)
            plan_to_watch_anime_info = fetch_anime_info(plan_to_watch_anime_ids)

            formatted_info = {
                "Currently Watching": [format_anime_info(info) for info in current_anime_info],
                "Rewatching": [format_anime_info(info) for info in rewatching_anime_info],
                "Completed": [format_anime_info(info) for info in completed_anime_info],
                "Plan to Watch": [format_anime_info(info) for info in plan_to_watch_anime_info]
            }

            # Store anime info in JSON file
            store_anime_info(formatted_info, "media_info.json")

            print("AniList refresh successful.")
        else:
            print("No data retrieved for any of the lists.")
    else:
        print("AniList access token or user ID not found in account.json.")
