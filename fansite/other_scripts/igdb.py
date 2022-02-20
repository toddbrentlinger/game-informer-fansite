import requests
import json

from decouple import config

def main():
    # Request access token
    response = requests.post(
        'https://id.twitch.tv/oauth2/token',
        params={
            'client_id': config('IGDB_CLIENT_ID'),
            'client_secret': config('IGDB_CLIENT_SECRET'),
            'grant_type': 'client_credentials'
        }
    )
    # Set access token
    access_token = response.json()['access_token']

    # Headers for search request
    headers = {
        'Accept': 'application/json',
        'Client-ID': config('IGDB_CLIENT_ID'),
        'Authorization': 'Bearer ' + access_token
        }
    # Request details for IGDB
    #data = 'fields *;search "overblood";'
    data = 'fields id,name,platforms.*,release_dates.date,summary;search "uncharted";'
    # Request game based on search
    response = requests.post(
        'https://api.igdb.com/v4/games', 
        data=data,
        headers=headers
    )
    # Set respone from game request
    responseData = response.json()
    
    if (responseData):
        print(json.dumps(responseData, sort_keys=True, indent=4))
        
    else:
        print('No search results!')

if __name__ == '__main__':
    main()