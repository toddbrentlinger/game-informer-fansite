from googleapiclient.discovery import build
from decouple import config
import pprint
import json

class YouTube:
    '''Class to make requests using YouTube Data API.'''

    # Static property for YouTube Resource Object used to make requests
    youtube_object = None

    def __init__(self):
        '''Constructor for YouTube class.'''
        if YouTube.youtube_object is not None:
            return

        # Arguments that need to passed to the build function 
        DEVELOPER_KEY = config('YOUTUBE_DEVELOPER_KEY')
        YOUTUBE_API_SERVICE_NAME = 'youtube'
        YOUTUBE_API_VERSION = 'v3'
    
        # Create Youtube Resource Object 
        YouTube.youtube_object = build(
            YOUTUBE_API_SERVICE_NAME, 
            YOUTUBE_API_VERSION,
            developerKey = DEVELOPER_KEY
        )
    
    def get_youtube_video_data(self, video_id, param = 'contentDetails,id,snippet,statistics'):
        '''
        Returns data on video from YouTube Data API.

        Param:
            video_id (str): YouTube video ID
            param (str): Parameters returned from YouTube Data API request

        Return:
            list|None: Response from YouTube Data API request
        '''
        request = YouTube.youtube_object.videos().list(
            part=param,
            id=video_id
        )
        response = request.execute()

        if response['items']:
            return response['items']
        else:
            print(f'Could NOT get data from YouTube video ID: {video_id}')
            return None

    def request_video_data_from_playlist(self, playlist_id, param = 'contentDetails,id,snippet', max_results = 50, next_page_token = None):
        '''
        Returns data from single request of playlist using YouTube Data API.

        Parameter:
            playlist_id (str): YouTube playlist ID
            param (str): Parameters returned from YouTube Data API request
            max_results (number): Max results returned per page of request
            next_page_token (str): YouTube Data API token for next page of request

        Returns:
            dict|None: Response from the request to the YouTube Data API playlistItems list method 
        '''
        request = YouTube.youtube_object.playlistItems().list(
            part=param,
            playlistId=playlist_id,
            maxResults=max_results,
            pageToken=next_page_token
        )
        response = request.execute()

        if response:
            return response
        else:
            print(f'Could NOT get data from YouTube playlist ID: {playlist_id}')
            return None

    def get_all_video_data_from_playlist(self, playlist_id, param = 'contentDetails,id,snippet'):
        '''
        Returns data from all videos in playlist using YouTube Data API.

        Parameters:
            playlist_id (str): YouTube playlist ID
            param (str): Parameters returned from YouTube Data API request

        Returns:
            list: List of data for each video in playlist
        '''
        playlist_items = []
        next_page_token = None

        while True:
            # Make request
            playlist_items_response = self.request_video_data_from_playlist(playlist_id, param, 50, next_page_token)

            # Add items to list if response is valid
            if (playlist_items_response and 'items' in playlist_items_response and len(playlist_items_response['items']) > 0):
                playlist_items += playlist_items_response['items']

            # Break out of while loop if no more results (no 'nextPageToken' key in response dict)
            if 'nextPageToken' not in playlist_items_response:
                break

            # Assign new next_page_token for next loop
            next_page_token = playlist_items_response['nextPageToken']

        return playlist_items

    def get_video_data_from_video_id_list(self, video_id_list, param = 'contentDetails,id,snippet,statistics'):
        '''
        Returns data for each video ID using YouTube Data API.

        Parameters:
            video_id_list (str[]): List of YouTube video IDs
            param (str): Parameters returned from YouTube Data API request

        Returns:
            list: response data from API for each video ID
        '''
        video_data_list = []
        index = 0
        list_length = len(video_id_list)
        while index < list_length:
            video_ids_string = ','.join(video_id_list[index:(index + 50)])
            video_data_response = self.get_youtube_video_data(video_ids_string)
            if len(video_data_response) > 0:
                video_data_list += video_data_response
            # Increment index by 50 for next loop
            index += 50
        return video_data_list

def main():
    youtube_inst = YouTube()

    # Game Informer Uploads Playlist ID: UUK-65DO2oOxxMwphl2tYtcw
    playlist_video_data = youtube_inst.get_all_video_data_from_playlist('UUK-65DO2oOxxMwphl2tYtcw', param='contentDetails')

    video_id_list = list(map(lambda playlist_item: playlist_item['contentDetails']['videoId'], playlist_video_data))
    video_data = youtube_inst.get_video_data_from_video_id_list(video_id_list)

    with open('utilities/gi_youtube_video_data.json', 'w') as outfile:
            json.dump(video_data, outfile, indent=2)

if __name__ == "__main__":
    main()