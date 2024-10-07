from time import sleep
from tkinter import StringVar

import customtkinter
import webbrowser
import requests
from localStoragePy import localStoragePy

from main.modules.api import load_api
from main.modules.progress import Load_API

# Step 1: Register your application and obtain client credentials
CLIENT_ID = '17593'
CLIENT_SECRET = '5FLMx3yxCAmHqjMCwkb2QTWKqZ2DFBqCOLZxM5iC'
REDIRECT_URI = 'https://ninestails.xyz/auth.html'

ls_settings = localStoragePy("Settings", "json")
ls = localStoragePy("Tanpopo Rewrite", "json")


# Step 2: Redirect user to AniList's authorization page
def get_authorization_code():
    auth_url = 'https://anilist.co/api/v2/oauth/authorize'
    params = {
        'client_id': CLIENT_ID,
        'redirect_uri': REDIRECT_URI,
        'response_type': 'code'  # Use 'code' for Authorization Code Grant flow
    }
    webbrowser.open_new(auth_url + '?' + '&'.join([f'{key}={value}' for key, value in params.items()]))


# Step 3: Exchange authorization code for access token
def exchange_code_for_token(authorization_code):
    token_url = 'https://anilist.co/api/v2/oauth/token'
    data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'redirect_uri': REDIRECT_URI,
        'grant_type': 'authorization_code',
        'code': authorization_code
    }
    response = requests.post(token_url, data=data)
    if response.status_code == 200:
        access_token = response.json().get('access_token')
        if access_token:
            user_info = get_user_info(access_token)
            if user_info:
                ls.setItem("access_token", access_token)
                ls.setItem("user_id", user_info['id'])
                ls.setItem("username", user_info['name'])
                ls.setItem("avatar_url", user_info['avatar']['large'])
                ls_settings.setItem("AniList/watching", True)
                ls_settings.setItem("AniList/planned", True)
                ls_settings.setItem("AniList/rewatched", False)
                ls_settings.setItem("AniList/completed", False)

                return ls.getItem("access_token")
            else:
                print("Failed to fetch user info.")
                return None
        else:
            print("Failed to exchange authorization code for access token.")
            return None
    else:
        print("Failed to exchange authorization code for access token.")
        return None


# Step 4: Fetch user information using access token
def get_user_info(access_token):
    user_info_url = 'https://graphql.anilist.co'
    query = '''
    query {
        Viewer {
            id
            name
            avatar {
                large
            }
        }
    }
    '''
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.post(user_info_url, json={'query': query}, headers=headers)
    if response.status_code == 200:
        return response.json()['data']['Viewer']
    else:
        print("Failed to fetch user info.")
        return None


class ToplevelWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #self.wm_iconbitmap("./favicon.ico")
        #self.after(201, lambda: self.iconbitmap('favicon.ico'))
        self.geometry("200x140")
        self.minsize(200, 140)
        # TODO: Somehow Fix the Window Focus, because window gets in background
        self.attributes('-topmost', True)

        #self.grab_set()

        # ---- Check Auth File and Open Browser
        get_authorization_code()

        # ---- Start Top Level Window
        self.title("Authorization Code")

        self.label = customtkinter.CTkLabel(self, text="Enter Authorization Code:")
        self.label.pack(padx=20, pady=5)

        self.wronglabel = customtkinter.CTkLabel(self, text="")
        self.wronglabel.pack()

        self.authkey = StringVar()
        self.entry = customtkinter.CTkEntry(self, textvariable=self.authkey)
        self.entry.pack()

        self.submit_button = customtkinter.CTkButton(self, text="Submit", command=self.submit_authorization_code)
        self.submit_button.pack(pady="10")

    def submit_authorization_code(self):
        print(self.authkey.get())
        authorization_code = self.authkey.get()
        if authorization_code:
            access_token = exchange_code_for_token(authorization_code.strip())
            if access_token:
                print("Access token:", access_token)
                print("Success")
                load_api()
                Load_API()
                self.destroy()
            else:
                print("Authorization failed.")
        else:
            self.wronglabel.configure(text="Paste Authentication Code", text_color="red")