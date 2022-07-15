import json
import pprint
import re
import datetime
from youtube import YouTube

# (<show_title(str)>, <regex_pattern(raw_str)> <check_description(bool)>)
MINN_MAX_SHOW_TITLES = (
    ('A Fire Inside Out', None, False),
    ('BetterQuest', None, False),
    ('Bonus Podcast', None, False),
    ('Deepest Dive', None, False),
    ('Everything We Know', r'^Everything\s.+Know', False),
    ('Extra Life', None, False),
    ('Game Case Trivia', None, False),
    ('Great GOTY Hunt', None, False),
    ('Hitman 3 Challenge', r"^Hitman\s3's.+Challenge", False),
    ('House Hunter Rise', None, False),
    ('Kyle Hilliard\'s Top 10 Games', None, False),
    ('Leo Plays', None, False),
    ('Live Reaction', None, False),
    ('Nintendo OnWine', None, False),
    ('Max Spoilers', None, False),
    ('MinnMax Interview', None, False),
    ('MinnMax Plays', None, False),
    ('MinnMax Show', None, True),
    ('MinnSnax', None, False),
    ('Photomode Snap', None, False),
    ('Sarah The Horse Girl', None, False),
    ('Steam\'s Secret Stash', None, False),
    ('Trivia Tower', None, False),
    ('Twilight Highlight Zone', None, False),
)

def write_playlist_items_to_json(youtube_inst):
    # YouTube Channel ID: UCiUhKqsBH-Is2VeC2sykEfg
    # Uploads Playlist ID: UUiUhKqsBH-Is2VeC2sykEfg
    playlist_items = youtube_inst.get_all_video_data_from_playlist('UUiUhKqsBH-Is2VeC2sykEfg')
    print(f'Videos In List: {len(playlist_items)}')
    with open('utilities/minn_max_video_data.json', 'w+') as outfile:
        json.dump(playlist_items, outfile, indent=2)

def convert_playlist_items_json_to_video_data_json(youtube_inst):
    new_videos_data = []
    with open('utilities/minn_max_video_data.json', 'r') as outfile:
        all_videos_data = json.load(outfile)
        # Create list of video ID's
        video_id_list = []
        for video_data in all_videos_data:
            video_id_list.append(video_data['contentDetails']['videoId'])
        # Get video data for each video ID
        new_videos_data = youtube_inst.get_video_data_from_video_id_list(video_id_list)
    # Write new data to json file
    with open('utilities/minn_max_video_data.json', 'w') as outfile:
        json.dump(new_videos_data, outfile, indent=2)

def main():
    youtube_inst = YouTube()

    # response = youtube_inst.get_youtube_video_data('nSFdetbQ18M') # Revolution X Replay
    # pprint.pprint(response, indent=2)

    matches = {'Other': []}
    for show_title in MINN_MAX_SHOW_TITLES:
            matches[show_title[0]] = []

    with open('utilities/minn_max_video_data.json', 'r') as outfile:
        all_videos_data = json.load(outfile)
        for video_data in all_videos_data:
            title_to_search = video_data['snippet']['title']
            description_to_search = video_data['snippet']['description']
            found_match = False
            for show_title, regex_pattern, do_check_description in MINN_MAX_SHOW_TITLES:
                # If regex_patters is NOT None, search using regex pattern
                if regex_pattern is not None:
                    if re.search(regex_pattern, title_to_search):
                        found_match = True
                        break
                    if do_check_description and re.search(regex_pattern, description_to_search):
                        found_match = True
                        break
                # Else search using show_title
                elif show_title.upper() in title_to_search.upper():
                    found_match = True
                    break
                elif do_check_description and show_title.upper() in description_to_search:
                    found_match = True
                    break
            dict_to_add = {
                'title': title_to_search, 
                'description': description_to_search, 
                'published_at': datetime.datetime.strptime(video_data['snippet']['publishedAt'], '%Y-%m-%dT%H:%M:%SZ').timestamp(),
            }
            # If found_match is still False, append to 'Other'
            if not found_match:
                matches['Other'].append(dict_to_add)
            else:
                matches[show_title].append(dict_to_add)

        # for val in matches.values():
        #     val.sort()

        pprint.pprint(matches['Other'], indent=2)

    with open('utilities/minn_max_shows_data.json', 'w+') as outfile:
        json.dump(matches, outfile, indent=2)

if __name__ == '__main__':
    main()