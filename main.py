#!/usr/bin/env python
import os
import requests
import secrets
import urllib

SPOTIFY_CLIENT_ID = os.environ['SPOTIFY_CLIENT_ID']
SPOTIFY_CLIENT_SECRET = os.environ['SPOTIFY_CLIENT_SECRET']

def connect_spotify():
    print("Connect Spotify")

    # Requests authorization
    request_secret = secrets.token_hex()
    payload = {
        'client_id': SPOTIFY_CLIENT_ID,
        'response_type': 'code',
        'redirect_uri': 'https://localhost:4000/steps/2',
        'state': request_secret
    }
    params = ("{}={}".format(param, value) for param, value in payload.items())
    auth_url = 'https://accounts.spotify.com/authorize?{}'.format('&'.join(params))
    print('Go to:')
    print(auth_url)

    # Simulate redirect
    redirect_url = input('Enter the redirect URL:')
    response = urllib.parse.urlparse(redirect_url)
    query = urllib.parse.parse_qs(response.query)

    # Get auth token
    payload = {
        'grant_type': 'authorization_code',
        'code': query['code'],
        'redirect_uri': 'https://localhost:4000/steps/2',
        'client_id': SPOTIFY_CLIENT_ID,
        'client_secret': SPOTIFY_CLIENT_SECRET
    }
    response = requests.post('https://accounts.spotify.com/api/token', data=payload).json()
    print(response)

def main():
    connect_spotify()


if __name__ == "__main__":
    main()
