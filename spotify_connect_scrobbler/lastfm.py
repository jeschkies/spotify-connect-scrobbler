#!/usr/bin/env python
import hashlib
import requests

from .credentials import LastfmCredentials


class LastfmClient:
    """ A simple client for the Last.fm API."""

    def __init__(self, key, secret):
        """Creates a Last.fm client.

        Args:
            key (str): Web API key.
            secret (str): Web API secret.
        """
        self.__key = key
        self.__secret = secret

    def sign(self, parameters):
        """ Generates the signature for autheorized API calls.

        Args:
            parameters (dict): Name and value of parameters for API call.

        Returns:
            string: Signature according to http://www.last.fm/api/webauth#6.
        """
        sorted_params = ("{}{}".format(k, parameters[k])
                         for k
                         in sorted(parameters))

        md5 = hashlib.md5()

        string = "{}{}".format(''.join(sorted_params), self.__secret)
        md5.update(string.encode('utf-8'))
        return md5.hexdigest()

    def request_authorization(self, redirect_uri):
        """ Returns authorization URL.

        Args:
            redirect_uri (str): Last.fm redirects to this URL.
        """
        payload = {
            'api_key': self.__key,
            'cb': redirect_uri,
        }
        params = ("{}={}".format(param, value)
                  for param, value
                  in payload.items())
        auth_url = 'http://www.last.fm/api/auth/?{}'.format('&'.join(params))
        return auth_url

    def request_access_token(self, token):
        """ Request access token from Last.fm.

        Args:
            token (string): Token from redirect.

        Return:
            dict: Response from get session call.
        """
        payload = {
            'api_key': self.__key,
            'method': 'auth.getSession',
            'token': token
        }
        payload['api_sig'] = self.sign(payload)
        payload['format'] = 'json'
        response = requests.post(
            'https://ws.audioscrobbler.com/2.0/', params=payload).json()

        return LastfmCredentials(response['session']['key'])

    def scrobble(self, tracks, credentials):
        """ Scrobble tracks.

        Args:
            tracks (list(dict)): List over {name, artists, played_at}
            credentials (LastfmCredentials): LastFM API credentials object.
        """
        print(credentials.session_key)
        payload = {
            'api_key': self.__key,
            'method': 'track.scrobble',
            'sk': credentials.session_key
        }

        for i, track in enumerate(tracks):
            payload["track[{}]".format(i)] = track['name']
            payload["artist[{}]".format(i)] = track['artists'][0]
            payload["timestamp[{}]".format(i)] = track['played_at']

        payload['api_sig'] = self.sign(payload)
        payload['format'] = 'json'
        return requests.post(
            'https://ws.audioscrobbler.com/2.0/', params=payload).json()
