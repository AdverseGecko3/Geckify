from requests_oauthlib import OAuth2Session
import os


class Authorize:
    def __init__(self):
        self.redirect_uri = 'https://adversegecko3.github.io/'
        self.authorization_base_url = "https://accounts.spotify.com/authorize"
        self.token_base_url = "https://accounts.spotify.com/api/token"
        self.scopes = [
            "playlist-read-private",
            "playlist-read-collaborative",
            "user-follow-read",
            "user-top-read",
            "user-read-recently-played",
            "user-library-read"
        ]
        self.spotify = OAuth2Session()

    # Start authorization via OAuth2Session, and return the created authorization URL
    def begin_authorization(self):
        # Redirect user to Spotify for authorization
        self.spotify = OAuth2Session(
            client_id=os.getenv("client_id"), scope=self.scopes, redirect_uri=self.redirect_uri)
        authorization_url, state = self.spotify.authorization_url(
            self.authorization_base_url)
        return authorization_url

    # Treat the returned new URL and get the access_token and the refresh_token
    def get_token(self, redirect_response):
        from requests.auth import HTTPBasicAuth

        # Fetch the access token
        try:
            auth = HTTPBasicAuth(os.getenv("client_id"),
                                 os.getenv("client_secret"))
            token = self.spotify.fetch_token(
                self.token_base_url, auth=auth, authorization_response=redirect_response)
            self.spotify.close()
            return token["access_token"], token["refresh_token"]
        except Exception as e:
            print(f"Ooops, and error occurred!\nError: {e}\n")
            return 0
