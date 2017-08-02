import json


class LastfmCredentials:
    """LastFM API credentials.

    Args:
        session_key (str): Session key returned by the authentication endpoint.
    """

    def __init__(self, session_key):
        self.session_key = session_key

    def todict(self):
        return {'session_key': self.session_key}


class SpotifyCredentials:
    """Spotify credentials contains access and refresh tokens for requests to
    the Spotify API. It does not call the API.

    Args:
        access_token (str): The access token.
        token_type (str): OAuth2 token type, e.g. 'Bearer'
        refresh_token (str): Token used to retrieve a new access token.
        scope (str): Scope for all API calls. This should not change often.
    """

    def __init__(self, access_token, token_type, refresh_token, scope):
        self.access_token = access_token
        self.token_type = token_type
        self.refresh_token = refresh_token
        self.scope = scope

    def todict(self):
        return {'access_token': self.access_token,
                'token_type': self.token_type,
                'refresh_token': self.refresh_token,
                'scope': self.scope}

    def update(self, new_credentials):
        """Update the credentials after new tokens were retrieve with the
        refresh token.

        Args:
            new_credentials (dict): Parsed repsonse from Spotify's auth
            endpoint.
        """
        if 'access_token' in new_credentials:
            self.access_token = new_credentials['access_token']

        if 'refresh_token' in new_credentials:
            self.refresh_token = new_credentials['refresh_token']


class Credentials:

    def __init__(self, lastfm, spotify):
        self.lastfm = lastfm
        self.spotify = spotify

    def save(self, config_file_path):
        """Save credentials to file.

        Args:
            config_file_path (path-like object): Path to file containing
            credentials. The file os opened and closed by this method.
        """
        with open(config_file_path, 'w') as f:
            data = {}
            if self.lastfm is not None:
                data['lastfm'] = self.lastfm.todict()

            if self.spotify is not None:
                data['spotify'] = self.spotify.todict()

            json.dump(data, f)


def load(config_file_path):
    """Load credentials from file.

    Args:
        config_file_path (path-like object): Path were to save credentials.

    Returns:
        Credentials: object with LastFM and Spotify credentials.
    """
    with open(config_file_path, 'r') as f:
        data = json.load(f)

        lastfm = LastfmCredentials(data['lastfm']['session_key'])
        spotify = SpotifyCredentials(
            data['spotify']['access_token'],
            data['spotify']['token_type'],
            data['spotify']['refresh_token'],
            data['spotify']['scope']
        )

        return Credentials(lastfm, spotify)
