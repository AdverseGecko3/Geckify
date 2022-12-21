import requests
from refresh import Refresh
import constant


class Geckify:
    def __init__(self):
        self.spotify_token = ""
        self.spotify_user_id = ""

    def refresh_spotify_token(self):
        refresh_class = Refresh()
        self.spotify_token = refresh_class.refresh()
        print(self.spotify_token)

    def get_user_profile(self, spotify_token=None):
        query = "https://api.spotify.com/v1/me"
        response = requests.get(query,
                                headers={"Content-Type": constant.TYPE_JSON,
                                         "Authorization": constant.BEARER.format(spotify_token if spotify_token != None else self.spotify_token)})

        print(response.json())

        if response.status_code != 200:
            return 0

        response_json = response.json()

        return response_json

    def set_spotify_token(self, token):
        self.spotify_token = token

    def get_spotify_token(self):
        return self.spotify_token

    def set_user_id(self, user_id):
        self.spotify_user_id = user_id

    def get_user_playlists(self):
        query = f"https://api.spotify.com/v1/users/{self.spotify_user_id}/playlists"
        params = {"limit": 50}
        response = requests.get(query,
                                headers={"Content-Type": constant.TYPE_JSON,
                                         "Authorization": constant.BEARER.format(self.spotify_token)},
                                params=params)
        response_json = response.json()

        user_playlists_dict = dict()
        for i in response_json["items"]:
            user_playlists_dict[i["name"]] = i["tracks"]["total"]

        return user_playlists_dict

    def get_artists_on_user_tracks(self):
        query = "https://api.spotify.com/v1/me/tracks"
        params = {"limit": 50}
        index = 1
        artists_dict = dict()

        while True:
            response = requests.get(query,
                                    headers={"Content-Type": constant.TYPE_JSON,
                                             "Authorization": constant.BEARER.format(self.spotify_token)},
                                    params=params)
            response_json = response.json()

            if (index == 1):
                print(
                    f"User tracks has {response_json['total']} saved songs\n")

            for i in response_json["items"]:
                print(
                    f"Checking saved song {index} of {response_json['total']}")

                current_artist = (i["track"]["album"]["artists"][0]
                                  ["name"], i["track"]["album"]["artists"][0]["id"])
                if (current_artist in artists_dict):
                    artists_dict.update(
                        {current_artist: (artists_dict.get(current_artist) + 1)})
                else:
                    artists_dict[current_artist] = 1

                index += 1

            if (response_json["next"] != None):
                query = response_json["next"]
            else:
                return artists_dict

    def following_people(self, type: str):
        query = "https://api.spotify.com/v1/me/following"
        params = {"type": "artist", "limit": 50}
        index = 1
        following_artists = dict()

        while True:
            response = requests.get(query,
                                    headers={"Content-Type": constant.TYPE_JSON,
                                             "Authorization": constant.BEARER.format(self.spotify_token)},
                                    params=params)
            response_json = response.json()

            if (index == 1):
                print(
                    f"Following {response_json['artists']['total']} people\n")

            for i in response_json["artists"]["items"]:
                print(
                    f"Checking follower {index} of {response_json['artists']['total']}")
                if (type == "id-name"):
                    following_artists[i["id"]] = i["name"]
                else:
                    following_artists[i["name"]] = i["followers"]["total"]
                index += 1

            if (response_json["artists"]["next"] != None):
                query = response_json["artists"]["next"]
            else:
                return following_artists

    def get_top_user(self, type: str, time_range: str):
        query = f"https://api.spotify.com/v1/me/top/{type}"
        params = {"limit": 50, "time_range": time_range}
        index = 1
        list_top = list()

        while True:
            response = requests.get(query,
                                    headers={"Content-Type": constant.TYPE_JSON,
                                             "Authorization": constant.BEARER.format(self.spotify_token)},
                                    params=params)
            response_json = response.json()

            for i in response_json["items"]:
                print(
                    f"Checking {type[:-1]} {index} of {response_json['total']}")
                if (type == "artists"):
                    list_top.append(i["name"])
                else:
                    list_top.append(
                        f"{i['name']} from {i['artists'][0]['name']}")
                index += 1

            if (response_json["next"] != None):
                query = response_json["next"]
            else:
                list_top.append(type)
                return list_top
