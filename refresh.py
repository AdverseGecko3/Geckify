import requests
from base64 import b64encode
import os


class Refresh:
    def __init__(self):
        self.refresh_token = ""
        self.base_64 = self.base64code()
        self.get_refresh_token()
    
    def get_refresh_token(self):
        from data_store import DataStore
        data = DataStore().load_data()


    def base64code(self):
        code = f"{os.getenv('client_id')}:{os.getenv('client_secret')}"
        code_bytes = code.encode("ascii")
        base_64_bytes = b64encode(code_bytes)
        base_64_message = base_64_bytes.decode("ascii")

        return base_64_message

    def refresh(self):
        query = "https://accounts.spotify.com/api/token"
        response = requests.post(query,
                                 data={"grant_type": "refresh_token",
                                       "refresh_token": self.refresh_token},
                                 headers={"Authorization": f"Basic {self.base_64}"})

        return response.json()["access_token"]
