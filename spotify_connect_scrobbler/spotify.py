#!/usr/bin/env python
import base64
import requests
import secrets
import sys

from .credentials import SpotifyCredentials


class SpotifyClient:
    """ A simple client for the Spotify Web API."""

    def __init__(self, client_id, client_secret):
        """Create Spotify client.

        Args:
            client_id (str): Identifies the client and the app.
            client_secret (str): API secret.
        """
        self.__client_id = client_id
        self.__client_secret = client_secret

    def _make_authorization_headers(self):
        auth = "{}:{}".format(self.__client_id, self.__client_secret)
        auth_base64 = base64.b64encode(auth.encode('utf-8')).decode('utf-8')
        return {'Authorization': "Basic {}".format(auth_base64)}

    def request_authorization(self, redirect_uri):
        """Returns an URL the user has to follow to authorize this app.

        Args:
            redirect_uri (str): Spotify redirects to this URL.
        """

        # Requests authorization
        request_secret = secrets.token_hex()
        payload = {
            'client_id': self.__client_id,
            'response_type': 'code',
            'redirect_uri': redirect_uri,
            'scope': 'user-read-recently-played',
            'state': request_secret
        }
        params = ("{}={}".format(param, value)
                  for param, value
                  in payload.items())
        auth_url = 'https://accounts.spotify.com/authorize?{}'.format(
                '&'.join(params))
        return auth_url

    def request_access_token(self, code, redirect_uri):
        """ Returns the access token for Spotify Web API.

        Args:
            code (string): The code passed by the authorization redirect.
            redirect_uri (str): Spotify redirected to this URL.

        Returns:
            dict: The response from Spotify.
        """

        # Get auth token
        payload = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': redirect_uri,
            'client_id': self.__client_id,
            'client_secret': self.__client_secret
        }
        response = requests.post(
                'https://accounts.spotify.com/api/token', data=payload).json()

        return SpotifyCredentials(
                response['access_token'],
                response['token_type'],
                response['refresh_token'],
                response['scope'])

    def refresh_access_token(self, refresh_token):
        """ Returns the access token for Spotify Web API using a refresh token.

        Args:
            refresh_token (string): The token has been returned by the access
            token request.

        Returns:
            SpotifyCredentials: The parsed response from Spotify.
        """
        # Get new auth token
        payload = {
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token
        }
        headers = self._make_authorization_headers()
        return requests.post(
            'https://accounts.spotify.com/api/token',
            data=payload,
            headers=headers
        ).json()

    def recently_played_tracks(self, auth):
        """Query Spotify for the recently played tracks of user.

        Args:
            auth (SpotifyCredentials): The authentication credentials returned
                by Spotify.

        Returns:
            dict: A dictionary including tracks and metadata.
        """
        payload = {}
        token = "{} {}".format(auth.token_type, auth.access_token)
        headers = {'Authorization': token}
        response = requests.get(
            'https://api.spotify.com/v1/me/player/recently-played?limit=50',
            data=payload,
            headers=headers
        )
        if response.ok:
            return response.json()
        elif response.status_code == 401:
            print("Spotify access token expired")
            auth.update(self.refresh_access_token(auth.refresh_token))
            # Retry
            return self.recently_played_tracks(auth)
        else:
            print(response.text)
            sys.exit(1)
