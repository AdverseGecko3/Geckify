import requests
from base64 import b64encode
import os


class Refresh:
    def __init__(self):
        self.refresh_token = ""
        self.base_64 = self.base64code()

    # Encode client keys format base64
    def base64code(self):
        code = f"{os.getenv('client_id')}:{os.getenv('client_secret')}"
        code_bytes = code.encode("ascii")
        base_64_bytes = b64encode(code_bytes)
        base_64_message = base_64_bytes.decode("ascii")

        return base_64_message

    # Get the new access_token via the saved refresh_token given when the first authorization was done
    def refresh(self, refresh_token):
        query = "https://accounts.spotify.com/api/token"
        response = requests.post(query,
                                 data={"grant_type": "refresh_token",
                                       "refresh_token": refresh_token},
                                 headers={"Authorization": f"Basic {self.base_64}"})
        
        #print(response.json())

        return response.json()["access_token"]
