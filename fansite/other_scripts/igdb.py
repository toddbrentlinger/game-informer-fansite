import requests
import json

from decouple import config

class IGDB:
    '''This is a class to make requests to IGDB API.'''

    # Static Properties

    # IGDB access token
    access_token = ''

    # Headers for search request
    headers = {}

    def __init__(self):
        '''The constructor for IGDB class.'''
        # Set static variable for access token, if not already valid.
        IGDB.set_access_token()
        IGDB.headers = {
            'Accept': 'application/json',
            'Client-ID': config('IGDB_CLIENT_ID'),
            'Authorization': 'Bearer ' + IGDB.access_token
        }

    @staticmethod
    def set_access_token():
        # Request access token
        response = requests.post(
            'https://id.twitch.tv/oauth2/token',
            params={
                'client_id': config('IGDB_CLIENT_ID'),
                'client_secret': config('IGDB_CLIENT_SECRET'),
                'grant_type': 'client_credentials'
            }
        )

        if response.status_code != requests.codes.ok:
            print('Request failed!')
            return

        # Return access token
        try:
            IGDB.access_token = response.json()['access_token']
        except requests.exceptions.JSONDecodeError:
            print('JSONDecodeError on response from access token request!')
            return

    def get_platform_data(self, platform_name, fields = '*'):
        '''
        Summary line.

        Parameters:
            platform_name (str): Name of platform to search.
            fields (str): 

        Returns:
            dict|None: Dictionary converted from IGDB JSON response for the platform. 
        '''
        # Request details for IGDB
        #data = 'fields *;search "overblood";'
        # release_dates for matching platform OR first_release_date
        data = ' '.join((
            f'fields {fields};',
            f'search "{platform_name}";'
        ))
        # Request game based on search
        response = requests.post(
            'https://api.igdb.com/v4/platforms', 
            data=data,
            headers=IGDB.headers
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

    def get_game_data(self, name, platform = None, year_released = None, fields='*'):
        '''
        Requests data on video game using IGDB API.

        Parameters:
            name (str): Video game name to search.
            platform (str|number): Video game platform string OR IGDB ID for specific platform (optional).
            year_released (number): Year the video game was released (optional).
            fields (str): Fields used for IGDB API request to retrieve specific fields only.

        Returns:
            dict: 
        '''
        # If platform is number, assume it is the IGDB platform id. Do nothing.
        # If platform is string
        if type(platform) is str:
            # Try converting string to int
            try:
                platform = int(platform)
            # If not number, try to use API to get platform ID
            except ValueError:
                platform = self.get_platform_data(platform)[0]['id']
            except:
                platform = None

        # Request details for IGDB
        #data = 'fields *;search "overblood";'
        # release_dates for matching platform OR first_release_date
        data = ' '.join((f'fields {fields};', f'search "{name}";'))
        if platform is not None and year_released is not None:
            data += f' where release_dates.platform={platform} & release_dates.y={year_released};'
        elif platform is not None:
            data += f' where release_dates.platform={platform};'
        elif year_released is not None:
            data += f' where release_dates.y={year_released};'
        # Else both platform and year_released have value None, do nothing

        # Request game based on search
        response = requests.post(
            'https://api.igdb.com/v4/games', 
            data=data,
            headers=IGDB.headers
        )

        # Check status code from request
        if response.status_code != requests.codes.ok:
            print(f'Request to IGDB API failed with status code: {response.status.code}')
            return None

        # Set response from game request
        try:
            response_data = response.json()
        except requests.exceptions.JSONDecodeError:
            print('Converting IGDB API response to JSON failed!')
            return None

        if response_data:
            print(json.dumps(response_data[0], sort_keys=True, indent=4))
            # print(f'No. of entries: {len(response_data)}')
            return response_data
        else:
            print('No search results returned from IGDB API!')
            return None

def main():
    igdb = IGDB()
    # platform_id = igdb.get_platform_data('PC Windows', '*,platform_logo.*')[0]['id']
    # platform_id = igdb.get_platform_data('Playstation 2', '*,platform_logo.*')[0]['id']
    # igdb.get_game_data(
    #     'Metal Gear Solid 3: Snake Eater', 
    #     platform_id, 
    #     2004, 
    #     'cover.*,first_release_date,genres.*,id,involved_companies.*,name,platforms.*,platforms.platform_logo.*,release_dates.*,slug,summary'
    # )
    igdb.get_game_data(
        'Metal Gear Solid 3: Snake Eater', 
        None, 
        None, 
        'cover.*,first_release_date,genres.*,id,involved_companies.*,name,platforms.*,platforms.platform_logo.*,release_dates.*,slug,summary'
    )

if __name__ == '__main__':
    main()