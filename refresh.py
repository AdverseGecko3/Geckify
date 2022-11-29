from secrets import refresh_token, base_64
import requests

class Refresh:
    def __init__(self):
        self.refresh_token = refresh_token
        self.base_64 = base_64

    def refresh(self):
        query = "https://accounts.spotify.com/api/token"
        response = requests.post(query, 
                                 data={"grant_type": "refresh_token",
                                       "refresh_token": self.refresh_token},
        headers={"Authorization": "Basic {}".format(self.base_64)})

        return response.json()["access_token"]