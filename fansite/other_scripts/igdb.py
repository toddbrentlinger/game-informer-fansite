import requests
import json

from decouple import config

def get_access_token():
    # Request access token
    response = requests.post(
        'https://id.twitch.tv/oauth2/token',
        params={
            'client_id': config('IGDB_CLIENT_ID'),
            'client_secret': config('IGDB_CLIENT_SECRET'),
            'grant_type': 'client_credentials'
        }
    )

    # Return access token
    try:
        return response.json()['access_token']
    except requests.exceptions.JSONDecodeError:
        return None

def get_igdb_data(access_token, fields, title, platform, year_released):
    # Headers for search request
    headers = {
        'Accept': 'application/json',
        'Client-ID': config('IGDB_CLIENT_ID'),
        'Authorization': 'Bearer ' + access_token
        }
    # Request details for IGDB
    #data = 'fields *;search "overblood";'
    # release_dates for matching platform OR first_release_date
    data = ' '.join((
        'fields cover.*,first_release_date,genres.*,id,involved_companies.*,name,platforms.*,platforms.platform_logo.*,release_dates.*,slug,summary;',
        f'search "{title}";'
    ))
    # Request game based on search
    response = requests.post(
        'https://api.igdb.com/v4/games', 
        data=data,
        headers=headers
    )
    # Set respone from game request
    response_data = response.json()
    
    if (response_data):
        print(json.dumps(response_data, sort_keys=True, indent=4))
    else:
        print('No search results!')
    return response_data

if __name__ == '__main__':
    access_token = get_access_token()
    if access_token is not None:
        request_data = 'fields cover.*,first_release_date,genres.*,id,involved_companies.*,name,platforms.*,platforms.platform_logo.*,release_dates.*,slug,summary;search "overblood";'
        get_igdb_data(access_token, request_data, 'Metal Gear Solid 3: Snake Eater', 'PlayStation 2', '2004')