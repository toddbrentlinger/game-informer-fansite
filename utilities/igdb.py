import requests
import json
import time
import pprint
import re

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

    def get_platform_data(self, platform_name, fields = '*', exclude = None):
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

        if exclude is not None:
            data += f' exclude {exclude};'

        # Request game based on search
        response = requests.post(
            'https://api.igdb.com/v4/platforms', 
            data=data.encode('utf-8'),
            headers=IGDB.headers
        )

        # Sleep to account for limit of 4 requests per second
        time.sleep(0.25)

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
            #print(json.dumps(response_data, sort_keys=True, indent=4))
            pass
        else:
            #print('No search results!')
            pass
        return response_data

    def make_game_request(self, data):
        '''
        Makes request from IGDB game API using data parameter as attribute in request.

        Parameters:
            data (str): Used as data attribute in IGDB game request.

        Returns:
            (JSON|None): JSON response from IGDB request or None if request fails.
        '''
        # Request game based on search
        response = requests.post(
            'https://api.igdb.com/v4/games', 
            data=data.encode('utf-8'),
            headers=IGDB.headers
        )

        # Sleep to account for limit of 4 requests per second
        time.sleep(0.25)

        # Check status code from request
        if response.status_code != requests.codes.ok:
            print('Data Sent:')
            pprint.pprint(data, indent=2)
            print(f'Request to IGDB API failed with status code: {response.status_code}')
            return None

        # Set response from game request
        try:
            response_data = response.json()
        except requests.exceptions.JSONDecodeError:
            print('Converting IGDB API response to JSON failed!')
            return None

        if response_data:
            # print(json.dumps(response_data[0], sort_keys=True, indent=4))
            # print(f'No. of entries: {len(response_data)}')
            return response_data
        else:
            return None

    def get_game_data_by_id(self, id, fields = '*', exclude = None):
        ''''
        Requests data on video game using IGDB API using the IGDB game ID.

        Paramters:
            id (int): IGDB video game ID to search.
            fields (str): Fields used for IGDB API request to retrieve specific fields only.
            exclude (str): Fields used for IGDB API request to exclude specific fields.
        '''
        data = ' '.join((f'fields {fields};', f'where id={id};'))

        if exclude is not None:
            data += f' exclude {exclude};'

        return self.make_game_request(data)

    def get_game_data(self, name, platform = None, year_released = None, fields = '*', exclude = None):
        '''
        Requests data on video game using IGDB API.

        Parameters:
            name (str): Video game name to search.
            platform (str|number): Video game platform string OR IGDB ID for specific platform (optional).
            year_released (str|number): Year the video game was released (optional).
            fields (str): Fields used for IGDB API request to retrieve specific fields only.
            exclude (str): Fields used for IGDB API request to exclude specific fields.

        Returns:
            dict: 

        Notes:
        - Return None if IGDB request returns no search results with given arguments.
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

        if exclude is not None:
            data += f' exclude {exclude};'

        if platform is not None and year_released is not None:
            if type(year_released) == str:
                # Check if year_released is single or range of years
                if '-' in year_released:
                    year_range = re.split('-', year_released)
                    data += f' where release_dates.platform={platform} & release_dates.y>={year_range[0]} & release_dates.y<={year_range[1]};'
                else:
                    data += f' where release_dates.platform={platform} & release_dates.y={year_released};'
            elif type(year_released) == int:
                data += f' where release_dates.platform={platform} & release_dates.y={year_released};'
        elif platform is not None:
            data += f' where release_dates.platform={platform};'
        elif year_released is not None:
            # Check if year_released is single or range of years
            if '-' in year_released:
                year_range = re.split('-', year_released)
                data += f' where release_dates.y>={year_range[0]} & release_dates.y<={year_range[1]};'
            else:
                data += f' where release_dates.y={year_released};'
        # Else both platform and year_released have value None, do nothing

        return self.make_game_request(data)

def main():
    igdb = IGDB()
    fields = 'artworks.*,collection.*,cover.*,first_release_date,genres.*,franchise.*,franchises.*,id,involved_companies.*,involved_companies.company.*,involved_companies.company.logo.*,involved_companies.company.websites.*,keywords.*,name,platforms.*,platforms.platform_logo.*,platforms.websites.*,release_dates.*,release_dates.platform.*,release_dates.platform.platform_logo.*,release_dates.platform.websites.*,screenshots.*,slug,storyline,summary,themes.*,url,videos.*,websites.*'
    exclude = 'collection.games,franchise.games,franchises.games,involved_companies.company.published, involved_companies.company.developed'
    
    # data = 'fields {fields};', f'search "*"; where involved_companies'
    # response = requests.post(
    #     'https://api.igdb.com/v4/games', 
    #     data=data.encode('utf-8'),
    #     headers=igdb.headers
    # )
    # if response.status_code != requests.codes.ok:
    #     print(f'Request to IGDB API failed with status code: {response.status.code}')
    #     return None
    # response_data = response.json()
    # if response_data:
    #     print(json.dumps(response_data[0], sort_keys=True, indent=2))

    # platform_data = igdb.get_platform_data('SNES', '*,platform_logo.*')
    # platform_id = platform_data[0]['id'] if len(platform_data) > 0 else None
    
    # import re
    # pattern = r'(^NES,)|(,\sNES,)|(,\sNES$)|(^NES$)'
    # print(re.search(pattern, 'NES, SNES, Super Nintendo, NESitude'))
    # print(re.search(pattern, 'SNES, Super Nintendo, NES, NESitude'))
    # print(re.search(pattern, 'SNES, Super Nintendo, NESitude, NES'))
    # print(re.search(pattern, 'NES'))

    # import pprint
    # pprint.pprint(platform_data, indent=2)
    # pprint.pprint(igdb.get_game_data('Pokemon Snap', None, None, fields)[0], indent=2) # é \u00e9

    try:
        game_data = igdb.get_game_data(
            'Goldeneye 007',
            igdb.get_platform_data('Nintendo 64', '*,platform_logo.*')[0]['id'], #igdb.get_platform_data('PlayStation 2', '*,platform_logo.*')[0]['id'],
            None,
            fields=fields,
            exclude=exclude
        )[0]
        pprint.pprint(
            game_data['release_dates'], 
            indent=2
        )
    except TypeError:
        print('No game returned from IGDB!')

    return

    try:
        pprint.pprint(
            igdb.get_game_data_by_id(
                212,
                fields=fields,
                exclude=exclude
            )[0], 
            indent=2
        )
    except TypeError:
        print('No game returned from IGDB using ID!')

    pprint.pprint(
        igdb.get_platform_data('Game Boy Color', '*,platform_logo.*')[0]
    )

    pprint.pprint(
        igdb.get_game_data(
            'Rayman', 
            igdb.get_platform_data('PlayStation')[0]['id'],
            fields='*, involved_companies.*, involved_companies.company.*, platforms.*'
        )[0], 
        indent=2
    )

    platform_id = igdb.get_platform_data('Playstation 2', '*,platform_logo.*')[0]['id']
    pprint.pprint(igdb.get_game_data(
        'Metal Gear Solid 3: Snake Eater', 
        platform_id, 
        2004, 
        fields,
        exclude
    )[0], indent=2)
    pprint.pprint(igdb.get_platform_data('PS2'), indent=2)
    # igdb.get_game_data(
    #     'Metal Gear Solid 3: Snake Eater', 
    #     None, 
    #     None, 
    #     'cover.*,first_release_date,genres.*,id,involved_companies.*,name,platforms.*,platforms.platform_logo.*,release_dates.*,slug,summary'
    # )

if __name__ == '__main__':
    main()