from secret import refresh_token, client_id, client_secret
import requests
from base64 import b64encode


class Refresh:
    def __init__(self):
        self.refresh_token = refresh_token
        self.base_64 = self.base64code()

    def base64code(self):
        code = f"{client_id}:{client_secret}"
        code_bytes = code.encode("ascii")
        base_64_bytes = b64encode(code_bytes)
        base_64_message = base_64_bytes.decode("ascii")

        return base_64_message

    def refresh(self):
        query = "https://accounts.spotify.com/api/token"
        response = requests.post(query,
                                 data={"grant_type": "refresh_token",
                                       "refresh_token": self.refresh_token},
                                 headers={"Authorization": "Basic {}".format(self.base_64)})

        return response.json()["access_token"]
