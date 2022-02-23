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

def get_igdb_platform_data(access_token, platform_name, fields = '*'):
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
        'fields ' + fields + ';',
        f'search "{platform_name}";'
    ))
    # Request game based on search
    response = requests.post(
        'https://api.igdb.com/v4/platforms', 
        data=data,
        headers=headers
    )

    if response.status_code != requests.codes.ok:
        print('Request failed!')
        return None

    # Set respone from game request
    try:
        response_data = response.json()
    except requests.exceptions.JSONDecodeError:
        print('Converting response to JSON failed!')
        return None

    if response_data:
        print(json.dumps(response_data, sort_keys=True, indent=4))
    else:
        print('No search results!')
    return response_data

def get_igdb_game_data(access_token, fields, name, platform, year_released):
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
        fields,
        f'search "{name}";'
    ))
    # Request game based on search
    response = requests.post(
        'https://api.igdb.com/v4/games', 
        data=data,
        headers=headers
    )
    if response.status_code != requests.codes.ok:
        print('Request failed!')
        return None

    # Set response from game request
    try:
        response_data = response.json()
    except requests.exceptions.JSONDecodeError:
        print('Converting response to JSON failed!')
        return None

    if response_data:
        print(json.dumps(response_data, sort_keys=True, indent=4))
        return response_data
    else:
        print('No search results!')
        return None

if __name__ == '__main__':
    access_token = get_access_token()
    if access_token is not None:
        get_igdb_platform_data(access_token, 'Playstation 2')
        # request_data = 'fields cover.*,first_release_date,genres.*,id,involved_companies.*,name,platforms.*,platforms.platform_logo.*,release_dates.*,slug,summary;search "overblood";'
        # get_igdb_game_data(access_token, request_data, 'Metal Gear Solid 3: Snake Eater', 'PlayStation 2', '2004')