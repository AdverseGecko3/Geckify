# Credentials you get from registering a new application
client_id = "6f39e7e8761d40039b898cb37f056cb2"
client_secret = "ed0e306963ee4aec86bd0c39a2c50c43"
redirect_uri = 'https://adversegecko3.github.io/'
# OAuth endpoints given in the Spotify API documentation
# https://developer.spotify.com/documentation/general/guides/authorization/code-flow/
authorization_base_url = "https://accounts.spotify.com/authorize"
token_url = "https://accounts.spotify.com/api/token"
# https://developer.spotify.com/documentation/general/guides/authorization/scopes/
scope = [
    "playlist-read-private",
    "playlist-read-collaborative",
    "user-follow-read",
    "user-top-read",
    "user-library-read"
]
from requests_oauthlib import OAuth2Session
spotify = OAuth2Session(client_id, scope=scope, redirect_uri=redirect_uri)
# Redirect user to Spotify for authorization
authorization_url, state = spotify.authorization_url(authorization_base_url)
print('Please go here and authorize: ', authorization_url)
# Get the authorization verifier code from the callback url
redirect_response = input('\n\nPaste the full redirect URL here: ')
from requests.auth import HTTPBasicAuth
auth = HTTPBasicAuth(client_id, client_secret)
# Fetch the access token
token = spotify.fetch_token(token_url, auth=auth,
        authorization_response=redirect_response)
print(token)
# Fetch a protected resource, i.e. user profile
r = spotify.get('https://api.spotify.com/v1/me')
print(r.content)