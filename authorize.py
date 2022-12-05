from secret import client_id, client_secret
from requests_oauthlib import OAuth2Session


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
            "user-library-read"
        ]
        self.spotify = OAuth2Session()

    def begin_authorization(self):
        # Redirect user to Spotify for authorization
        self.spotify = OAuth2Session(
            client_id, scope=self.scopes, redirect_uri=self.redirect_uri)
        authorization_url = self.spotify.authorization_url(
            self.authorization_base_url)
        return authorization_url[0]

    def get_token(self, redirect_response):
        from requests.auth import HTTPBasicAuth

        # Fetch the access token
        auth = HTTPBasicAuth(client_id, client_secret)
        token = self.spotify.fetch_token(
            self.token_base_url, auth=auth, authorization_response=redirect_response)
        self.spotify.close()

        return token["access_token"]
