import requests
from refresh import Refresh
import constant


class Geckify:
    def __init__(self):
        self.spotify_token = ""
        self.user_id = ""
        self.artists_dict = dict()

    def refresh_spotify_token(self):
        refresh_class = Refresh()
        self.spotify_token = refresh_class.refresh()

    def get_user_profile(self):
        query = "https://api.spotify.com/v1/me"
        response = requests.get(query,
                                headers={"Content-Type": constant.TYPE_JSON,
                                         "Authorization": constant.BEARER.format(self.spotify_token)})
        response_json = response.json()

        self.user_id = response_json["id"]

    def get_user_playlists(self):
        query = "https://api.spotify.com/v1/users/{}/playlists".format(
            self.user_id)
        params = {"limit": 50}
        response = requests.get(query,
                                headers={"Content-Type": constant.TYPE_JSON,
                                         "Authorization": constant.BEARER.format(self.spotify_token)},
                                params=params)
        response_json = response.json()

        print("\nUser playlists\n")
        for i in response_json["items"]:
            print("{} with {} tracks".format(i["name"], i["tracks"]["total"]))

    def get_artists_on_user_tracks(self):
        query = "https://api.spotify.com/v1/me/tracks"
        params = {"limit": 50}
        index = 1

        while True:
            response = requests.get(query,
                                    headers={"Content-Type": constant.TYPE_JSON,
                                             "Authorization": constant.BEARER.format(self.spotify_token)},
                                    params=params)
            response_json = response.json()

            if (index == 1):
                print("\nUser tracks has {} songs\n".format(
                    response_json["total"]))

            for i in response_json["items"]:
                print("Checking song {} of {}".format(
                    index, response_json["total"]))

                current_artist = (i["track"]["album"]["artists"][0]
                                  ["name"], i["track"]["album"]["artists"][0]["id"])
                if (current_artist in self.artists_dict):
                    self.artists_dict.update(
                        {current_artist: (self.artists_dict.get(current_artist) + 1)})
                else:
                    self.artists_dict[current_artist] = 1

                index += 1

            if (response_json["next"] != None):
                query = response_json["next"]
            else:
                self.order_artists_on_user_tracks()
                break
    
    def order_artists_on_user_tracks(self):
        following_artists = self.following_people()

        print("\nDATA\n")
        self.artists_dict = dict(
            sorted(self.artists_dict.items(), key=lambda item: item[1]))

        following_text = ""
        for artist, saved in self.artists_dict.items():
            if artist[1] in following_artists:
                following_text = "Following"
            else:
                following_text = "Not following"

            print("{} saved from {} ({})".format(
                saved, artist[0], following_text))
        print("\n")

    def following_people(self):
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
                print("\nFollowing {} people\n".format(
                    response_json["artists"]["total"]))

            for i in response_json["artists"]["items"]:
                print("Checking follower {} of {}".format(
                    index, response_json["artists"]["total"]))
                following_artists[i["id"]] = i["name"]
                index += 1

            if (response_json["artists"]["next"] != None):
                query = response_json["artists"]["next"]
            else:
                break
        return following_artists

def main():
    geckify = Geckify()
    geckify.refresh_spotify_token()
    geckify.get_user_profile()
    while True:
        print("GECKIFY")
        print("MENU")
        print("0. Exit")
        print("1. Print my playlists")
        print("2. Check artists from my Liked Songs")
        try:
            option = int(input("Please choose an option:"))
            match option:
                case 0:
                    print("See ya!")
                    return
                case 1:
                    geckify.get_user_playlists()
                    return
                case 2:
                    geckify.get_artists_on_user_tracks()
                    return
                case _:
                    print("Oops, I didn't hear you!")
        except ValueError:
            print("Wrong input")

if __name__ == "__main__":
    main()
