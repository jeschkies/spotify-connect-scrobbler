#!/usr/bin/env python
import hashlib
import os
import requests
import urllib

LASTFM_API_KEY = os.environ['LASTFM_API_KEY']
LASTFM_API_SECRET = os.environ['LASTFM_API_SECRET']

class LastfmClient:
    """ A simple client for the Last.fm API."""

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

        string = "{}{}".format(''.join(sorted_params), LASTFM_API_SECRET)
        md5.update(string.encode('utf-8'))
        return md5.hexdigest()


    def request_authorization(self):
        """ Returns authorization URL."""
        payload = {
            'api_key': LASTFM_API_KEY,
            'cb': 'https://localhost:4000/steps/3',
        }
        params = ("{}={}".format(param, value) for param, value in payload.items())
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
            'api_key': LASTFM_API_KEY,
            'method': 'auth.getSession',
            'token': token
        }
        payload['api_sig'] = self.sign(payload)
        payload['format'] = 'json'
        return requests.post(
            'https://ws.audioscrobbler.com/2.0/', params=payload).json()


if __name__ == "__main__":
    client = LastfmClient()
    auth_url = client.request_authorization()
    print('Go to:')
    print(auth_url)

    # Simulate redirect
    redirect_url = input('Enter the redirect URL:')
    response = urllib.parse.urlparse(redirect_url)
    query = urllib.parse.parse_qs(response.query)

    access_token = client.request_access_token(query['token'][0])
    print(access_token)
