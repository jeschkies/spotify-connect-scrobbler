#!/usr/bin/env python
import hashlib
import os
import requests
import secrets
import urllib

# LASTFM_API_KEY = os.environ['LASTFM_API_KEY']
# LASTFM_API_SECRET = os.environ['LASTFM_API_SECRET']

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
        'scope': 'user-read-recently-played',
        'state': request_secret
    }
    params = ("{}={}".format(param, value) for param, value in payload.items())
    auth_url = 'https://accounts.spotify.com/authorize?{}'.format(
            '&'.join(params))
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
    response = requests.post(
            'https://accounts.spotify.com/api/token', data=payload).json()
    print(response)


def recently_played_tracks():
    # Query Spotify for the recently played tracks of user.
    payload = {}
    headers = {'Authorization': '<ACCESS TOKEN>'}
    response = requests.get(
            'https://api.spotify.com/v1/me/player/recently-played',
            data=payload, headers=headers).json()
    for item in response['items']:
        track = item['track']['name']
        artists = [ a['name'] for a in item['track']['artists'] ]
        played_at = int(dateutil.parser.parse(item['played_at']).replace(tzinfo=tzutc()).timestamp())
        print("{} by {} at {} ".format(track, ', '.join(artists), played_at))


def lastfm_sign(parameters):
    sorted_params = ("{}{}".format(k, parameters[k])
                     for k
                     in sorted(parameters))

    md5 = hashlib.md5()

    string = "{}{}".format(''.join(sorted_params), LASTFM_API_SECRET)
    print(string)
    md5.update(string.encode('utf-8'))
    return md5.hexdigest()


def connect_lastfm():
    # Requests authorization
    payload = {
        'api_key': LASTFM_API_KEY,
        'cb': 'https://localhost:4000/steps/3',
    }
    params = ("{}={}".format(param, value) for param, value in payload.items())
    auth_url = 'http://www.last.fm/api/auth/?{}'.format('&'.join(params))
    print('Go to:')
    print(auth_url)

    # Simulate redirect
    redirect_url = input('Enter the redirect URL:')
    response = urllib.parse.urlparse(redirect_url)
    query = urllib.parse.parse_qs(response.query)

    # Get auth token
    payload = {
        'api_key': LASTFM_API_KEY,
        'method': 'auth.getSession',
        'token': query['token'][0]
    }
    payload['api_sig'] = lastfm_sign(payload)
    payload['format'] = 'json'
    print(payload)
    response = requests.post(
            'https://ws.audioscrobbler.com/2.0/', params=payload).json()
    print(response)


def main():
    # connect_spotify()
    # connect_lastfm()
    recently_played_tracks()


if __name__ == "__main__":
    main()
