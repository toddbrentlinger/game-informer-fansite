import json
import pprint
from youtube import YouTube

MINN_MAX_SHOW_TITLES = (
    'MinnMax Show',
)

def main():
    youtube_inst = YouTube()

    # response = youtube_inst.get_youtube_video_data('nSFdetbQ18M') # Revolution X Replay
    # pprint.pprint(response, indent=2)

    # YouTube Channel ID: UCiUhKqsBH-Is2VeC2sykEfg
    # Uploads Playlist ID: UUiUhKqsBH-Is2VeC2sykEfg
    # playlist_items = youtube_inst.get_all_video_data_from_playlist('UUiUhKqsBH-Is2VeC2sykEfg')
    # print(f'Videos In List: {len(playlist_items)}')
    # with open('utilities/minn_max_video_data.json', 'w+') as outfile:
    #     json.dump(playlist_items, outfile, indent=2)

    # new_videos_data = []
    # with open('utilities/minn_max_video_data.json', 'r') as outfile:
    #     all_videos_data = json.load(outfile)
    #     # Create list of video ID's
    #     video_id_list = []
    #     for video_data in all_videos_data:
    #         video_id_list.append(video_data['contentDetails']['videoId'])
    #     # Get video data for each video ID
    #     new_videos_data = youtube_inst.get_video_data_from_video_id_list(video_id_list)
    # # Write new data to json file
    # with open('utilities/minn_max_video_data.json', 'w') as outfile:
    #     json.dump(new_videos_data, outfile, indent=2)

    with open('utilities/minn_max_video_data.json', 'r') as outfile:
        all_videos_data = json.load(outfile)
        matches = []
        for video_data in all_videos_data:
            if 'MinnMax Show'.upper() in video_data['snippet']['title'].upper() or 'MinnMax Show'.upper() in video_data['snippet']['description'].upper():
                matches.append(video_data['snippet']['title'])
        pprint.pprint(matches, indent=2)

if __name__ == '__main__':
    main()