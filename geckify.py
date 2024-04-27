import requests
from refresh import Refresh
import constant


class Geckify:
    def __init__(self):
        self.access_token = ""
        self.user_id = ""
        self.display_name = ""

    # Initialize Refresh, get the refresh_token and return it
    def refresh_spotify_token(self, refresh_token):
        refresh_class = Refresh()
        self.access_token = refresh_class.refresh(refresh_token)
        return self.get_spotify_token()

    # Get the user profile
    def get_user_profile(self, spotify_token=None):
        query = "https://api.spotify.com/v1/me"
        response = requests.get(query,
                                headers={"Content-Type": constant.TYPE_JSON,
                                         "Authorization": constant.BEARER.format(spotify_token if spotify_token != None else self.access_token)})
        
        response_json = response.json()

        #print(response_json)
        #print(type(response_json))

        # If status code is not 200 (401, 403, or others) return a custom string with 0 and the error message
        if response.status_code != 200:
            return f"0{response_json['error']['message']}"

        return response_json

    def get_spotify_token(self):
        return self.access_token

    def set_spotify_token(self, spotify_token):
        self.access_token = spotify_token

    def get_user_id(self):
        return self.user_id

    def set_user_id(self, user_id):
        self.user_id = user_id

    def get_display_name(self):
        return self.display_name

    def set_display_name(self, display_name):
        self.display_name = display_name

    # Get all the user playlists
    def get_user_playlists(self):
        query = f"https://api.spotify.com/v1/users/{self.user_id}/playlists"
        params = {"limit": 50}
        response = requests.get(query,
                                headers={"Content-Type": constant.TYPE_JSON,
                                         "Authorization": constant.BEARER.format(self.access_token)},
                                params=params)
        response_json = response.json()

        # Save in a dict the name as key and the number of tracks it has as value
        user_playlists_dict = dict()
        for i in response_json["items"]:
            user_playlists_dict[i["name"]] = i["tracks"]["total"]

        return user_playlists_dict

    # Get how many songs of each artists the user has on the Liked Songs
    def get_artists_on_user_tracks(self):
        query = "https://api.spotify.com/v1/me/tracks"
        params = {"limit": 50}
        index = 1
        artists_dict = dict()

        while True:
            response = requests.get(query,
                                    headers={"Content-Type": constant.TYPE_JSON,
                                             "Authorization": constant.BEARER.format(self.access_token)},
                                    params=params)
            response_json = response.json()
            print(response_json)

            if index == 1:
                print(
                    f"User tracks has {response_json['total']} saved songs\n")

            for i in response_json["items"]:
                print(
                    f"Checking saved song {index} of {response_json['total']}")
                
                # Save in a dict each artist (name and id) as key and the number of songs saved as value
                # If the artists is not on the dict, add it with 1 as value
                # If the user is in the dict, get the value and add 1
                current_artist = (i["track"]["album"]["artists"][0]
                                  ["name"], i["track"]["album"]["artists"][0]["id"])
                if current_artist in artists_dict:
                    artists_dict.update(
                        {current_artist: (artists_dict.get(current_artist) + 1)})
                else:
                    artists_dict[current_artist] = 1

                index += 1

            if response_json["next"] != None:
                query = response_json["next"]
            else:
                return artists_dict

    # Get the following people
    def following_people(self, type: str):
        query = "https://api.spotify.com/v1/me/following"
        params = {"type": "artist", "limit": 50}
        index = 1
        following_artists = dict()

        while True:
            response = requests.get(query,
                                    headers={"Content-Type": constant.TYPE_JSON,
                                             "Authorization": constant.BEARER.format(self.access_token)},
                                    params=params)
            response_json = response.json()

            if index == 1:
                print(
                    f"Following {response_json['artists']['total']} people\n")

            for i in response_json["artists"]["items"]:
                print(
                    f"Checking follower {index} of {response_json['artists']['total']}")
                
                # Depending on the type passed as a parameter, save in a dict the Id - Name, or the Name - Quantity of followers
                if type == "id-name":
                    following_artists[i["id"]] = i["name"]
                else:
                    following_artists[i["name"]] = i["followers"]["total"]
                index += 1

            if response_json["artists"]["next"] != None:
                query = response_json["artists"]["next"]
            else:
                return following_artists

    # Get the top listened songs / artists
    def get_top_user(self, type: str, time_range: str):
        # This api call has the time_range parameter, with 3 possible values:
        # 1. short_term
        # 2. medium_term
        # 3. long_term
        query = f"https://api.spotify.com/v1/me/top/{type}"
        params = {"limit": 50, "time_range": time_range}
        index = 1
        list_top = list()

        while True:
            response = requests.get(query,
                                    headers={"Content-Type": constant.TYPE_JSON,
                                             "Authorization": constant.BEARER.format(self.access_token)},
                                    params=params)
            response_json = response.json()

            for i in response_json["items"]:
                print(
                    f"Checking {type[:-1]} {index} of {response_json['total']}")
                
                # Add to a list the top artists or songs (Depending the type parameter)
                if type == "artists":
                    list_top.append(i["name"])
                else:
                    # Check if the current song has multiple artists, and concat them
                    artists = ""
                    for j in i["artists"]:
                        artists += f"{j['name']}, "
                    artists = artists[:-2]
                    list_top.append(
                        f"{i['name']} from {artists}")
                index += 1

            if response_json["next"] != None:
                query = response_json["next"]
            else:
                list_top.append(type)
                return list_top
    
    # Get the recently played songs
    def get_recently_played(self):
        #import time
        #time_after = time.time() - 604800000
        query = f"https://api.spotify.com/v1/me/player/recently-played"
        #params = {"after": time_after}
        index = 1
        list_recently_played = list()

        while True:
            response = requests.get(query,
                                    headers={"Content-Type": constant.TYPE_JSON,
                                             "Authorization": constant.BEARER.format(self.access_token)})
            response_json = response.json()

            # As before, check if the song has multiple artists, and concat them
            for i in response_json["items"]:
                artists = ""
                for j in i["track"]["album"]["artists"]:
                    artists += f"{j['name']}, "
                artists = artists[:-2]

                list_recently_played.append(
                    f"{i['track']['album']['name']} from {artists}")
                
                index += 1
            
            return list_recently_played
