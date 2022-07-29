import json
import pprint
import math
from operator import itemgetter

def change_dashes_to_null(obj):
    if isinstance(obj, dict):
        for key, value in obj.items():
            if isinstance(value, str) and len(value) != 0 and len(value.replace('-', '')) == 0:
                #print(f'Value changed: {value}')
                obj[key] = ''
            else:
                change_dashes_to_null(value)
    elif isinstance(obj, list):
        for index in reversed(range(0, len(obj))):
            value = obj[index]
            if isinstance(value, str) and len(value) != 0 and len(value.replace('-', '')) == 0:
                #print(f'Value changed: {value}')
                del obj[index]
            else:
                change_dashes_to_null(value)

def clean_json_file():
    allReplayData = []
    with open('fansite/other_scripts/replay_data.json', 'r') as dataFile:
        # Get Replay episode data
        allReplayData = json.load(dataFile)

        for replayData in allReplayData:
            # Convert any value with all '-' to empty string
            change_dashes_to_null(replayData)

            # Middle Segment
            # If middleSegment is blank but middleSegmentContent is NOT blank, add value for middleSegment
            # - Segment can be 'AD' OR 'RR' game OR 'Red Faction D&D Skit'
            # - Ads do not always have middleSegment blank. Could be labeled under 'Moments' middleSegment. 
            if 'middleSegment' in replayData:
                # If both middleSegment and middleSegmentContent have value
                if replayData['middleSegment'] and replayData['middleSegmentContent']:
                    # Check middleSegmentContent for 'Ad' when middleSegment is 'Moments'
                    if replayData['middleSegment'] == 'Moments' and replayData['middleSegmentContent'].endswith('Ad'):
                        replayData['middleSegment'] = 'AD'
                # Else if only middleSegment has value (ex. episode 346 'Life Advice with Ben Reeves')
                elif replayData['middleSegment']:
                    pass
                # Else if only middleSegmentContent has value (set middleSegment to 'AD', 'RR', or other)
                elif replayData['middleSegmentContent']:
                    # Blank middleSegment and non-blank middleSegmentContent that's not an AD
                    SEGMENT_CONTENT_EXCEPTIONS_NO_SEGMENT = (
                        ('Avatar: The Last Airbender - The Burning Earth', 'RR'), 
                        ('Final Fantasy 8 Buttz', None),
                        ('Game Informer\'s Extra Life 2015 - Ghost Pepper Highlight Reel', None),
                        ('Realm', 'RR'),
                        ('Red Faction D&D Skit', None),
                        ('Super Metroid Pamphlet', None),
                        ('The Tick', 'RR'),
                    )
                    # If middleSegmentContent ends with 'Ad', set middleSegment to 'AD'
                    if replayData['middleSegmentContent'].endswith('Ad'):
                        replayData['middleSegment'] = 'AD'
                    # Add 'RR' if middleSegmentContent matches list of contstants
                    for segment_exception in SEGMENT_CONTENT_EXCEPTIONS_NO_SEGMENT:
                        if replayData['middleSegmentContent'] == segment_exception[0] and segment_exception[1] is not None:
                            replayData['middleSegment'] = segment_exception[1]
                            break
                # Else both 'middleSegment' and 'middleSegmentContent' are blank, do nothing

                # If middleSegmentContent contains 'WiiU', replace with 'Wii U' to return accurate
                # results from IGDB
                if 'WiiU' in replayData['middleSegmentContent']:
                    replayData['middleSegmentContent'] = replayData['middleSegmentContent'].replace('WiiU', 'Wii U')

            if 'secondSegment' in replayData:
                # If both secondSegment AND secondSegmentGames have value
                if replayData['secondSegment'] and replayData['secondSegmentGames']:
                    pass
                # Else if only secondSegment has value
                elif replayData['secondSegment']:
                    pass
                # Else if only secondSegmentGames has value
                # 3 instances: 
                # - MGS3 Secret Theater
                # - Twisted Metal Head On: Extra Twisted Edition
                # - Mega Man: The\u00a0 Power Battle, Mega Man Soccer, Mega Man: Dr. Wily's Revenge
                elif replayData['secondSegmentGames']:
                    replayData['secondSegment'] = 'RR'
                # Else both 'secondSegment' and 'secondSegmentGames' are blank, do nothing

    with open('fansite/other_scripts/replay_data.json', 'w') as dataFile:
        json.dump(allReplayData, dataFile, indent=2)

def display_middle_segment_data():
    with open('fansite/other_scripts/replay_data.json', 'r') as outfile:
        # Get Replay episode data
        allReplayData = json.load(outfile)

        # (episode_number, middleSegment, middleSegmentContent)
        segment_data = []
        for replayData in allReplayData:
            if 'middleSegment' in replayData and (replayData['middleSegment'] or replayData['middleSegmentContent']):
                segment_data.append((replayData['episodeNumber'], replayData['middleSegment'], replayData['middleSegmentContent']))

        # Sort segments
        segment_data.sort(key=itemgetter(1,2,0))

        # Print sorted segment data
        pprint.pprint(segment_data)

def display_second_segment_data():
    with open('fansite/other_scripts/replay_data.json', 'r') as outfile:
        # Get Replay episode data
        allReplayData = json.load(outfile)

        # (secondSegment, secondSegmentGames array/list)
        segment_data = {}
        segment_type_set = set()
        for replayData in allReplayData:
            if 'secondSegment' in replayData and (replayData['secondSegment'] or replayData['secondSegmentGames']):
                if replayData['secondSegment'] in segment_type_set:
                    # Adds games to existing segment
                    segment_data[replayData['secondSegment']].append(replayData['secondSegmentGames'])
                else:
                    # Add new segment with games
                    segment_data[replayData['secondSegment']] = replayData['secondSegmentGames']
                    segment_type_set.add(replayData['secondSegment'])
            
        for key in sorted(segment_data.keys()):
            print(f'{key}: {len(segment_data[key])}')

def print_segment_types():
    with open('fansite/other_scripts/replay_data.json', 'r') as dataFile:

        # Get Replay episode data
        allReplayData = json.load(dataFile)

        segments = set()
        for replayData in allReplayData:
            # Middle Segment
            if 'middleSegment' in replayData and len(replayData['middleSegment'].replace('-', '')) != 0:
                segments.add(replayData['middleSegment'])
            # Second Segment
            if 'secondSegment' in replayData and len(replayData['secondSegment'].replace('-', '')) != 0:
                segments.add(replayData['secondSegment'])

        for segment in sorted(segments):
            print(segment)


def create_total_time_message(total_seconds):
    '''
    Creates time message given number of seconds (ex. 15 days, 18 hours, 45 minutes, 38 seconds)
    '''
    days = math.floor(total_seconds // 86400)
    hours = math.floor((total_seconds - days * 86400) // 3600)
    minutes = math.floor((total_seconds - days * 86400 - hours * 3600) // 60)
    seconds = total_seconds - days * 86400 - hours * 3600 - minutes * 60

    output_str = ''
    if days > 0:
        output_str += f'{days} days'
    if output_str or hours > 0:
        if output_str:
            output_str += ', '
        output_str += f'{hours} hours'
    if output_str or minutes > 0:
        if output_str:
            output_str += ', '
        output_str += f'{minutes} mins'
    if output_str or seconds > 0:
        if output_str:
            output_str += ', '
        output_str += f'{seconds} secs'

    return output_str

def get_blank_segment_type_replays():
    with open('utilities/replay_data.json', 'r') as outfile:
        all_replay_data = json.load(outfile)
        # pprint.pprint(all_replay_data[89], indent=2)

        blank_segment_type_replays = []
        for replay_data in all_replay_data:
            # Middle Segment
            if 'middleSegment' in replay_data and not replay_data['middleSegment'] and replay_data['middleSegmentContent']:
                blank_segment_type_replays.append(
                    (
                        replay_data['episodeNumber'],
                        replay_data['middleSegmentContent']
                    )
                )
            # Second Segment
            if 'secondSegment' in replay_data and not replay_data['secondSegment'] and replay_data['secondSegmentGames']:
                blank_segment_type_replays.append(
                    (
                        replay_data['episodeNumber'],
                        replay_data['secondSegmentGames']
                    )
                )
        print(blank_segment_type_replays)

def get_gi_shows():
    # ( (<tags>,), (<prioritized shows by key value>,) )
    # Tuple of tuples
    # Ex. 
    # 'replay': (('replay', 'replayshow'), ('super_replay'))
    # 'super_replay': (('super replay'),),
    # If video has both tags 'replay, super replay', show key 'super_replay'
    # will be chosen instead of show key 'replay'.
    GI_SHOWS = {
        'replay': (('replay', 'replayshow'), ('super_replay',)),
        'super_replay': (('super replay',),),
        'game_informer_show': (('gi show', 'game informer show', 'the game informer show'), ('spoiled',)),
        'test_chamber': (('test chamber',),),
        'review': (('review', 'game review'), ('game_informer_show', 'new_gameplay_today', 'test_chamber')),
        #'game_informer_podcast': (('game informer podcast',),),
        'new_gameplay_today': (('new gameplay today', 'new gameplay'), ('test_chamber',)),
        'chronicles': (('chronicles',), ('super_replay',)),
        'reiner_and_phil': (('Reiner and Phil',),),
        'spoiled': (('spoiled',),),
    }

    sorted_tags_obj = {}
    all_youtube_video_data = []
    with open('utilities/gi_youtube_video_data.json', 'r') as outfile:
        all_youtube_video_data = json.load(outfile)

        gi_shows = {
            'matches': {},
            'duplicates': [],
            'no_matches': [],
            'no_tags': [],
        }

        for youtube_video_data in all_youtube_video_data:
            if 'snippet' in youtube_video_data and 'tags' in youtube_video_data['snippet']:
                matching_shows = set()

                for tag in youtube_video_data['snippet']['tags']:
                    for show, tags_tuple in GI_SHOWS.items():
                        if tag in tags_tuple[0]:
                            matching_shows.add(show)

                # Handle duplicates shows with prioritization
                if len(matching_shows) > 1:
                    def handle_matching_show_filter(show):
                        if len(GI_SHOWS[show]) > 1:
                            for priority_show in GI_SHOWS[show][1]:
                                if priority_show in matching_shows:
                                    return False
                        return True
                    # Remove duplicates by checking for priorities
                    matching_shows = list(filter(handle_matching_show_filter, matching_shows))

                if len(matching_shows) > 1:
                    gi_shows['duplicates'].append(youtube_video_data)
                elif len(matching_shows) == 1:
                    matching_show = matching_shows.pop()
                    if matching_show in gi_shows['matches']:
                        gi_shows['matches'][matching_show].append(youtube_video_data)
                    else:
                        gi_shows['matches'][matching_show] = [youtube_video_data]

                else: # len(matching_shows) == 0
                    gi_shows['no_matches'].append(youtube_video_data)

            else:
                gi_shows['no_tags'].append(youtube_video_data)

        # Create obj with key as tag and value as count of tag for 'no_matches' videos
        tags_obj = {}
        for youtube_video_data in gi_shows['no_matches']:
            for tag in youtube_video_data['snippet']['tags']:
                # Increment or initialize tag count
                if tag in tags_obj:
                    tags_obj[tag] += 1
                else:
                    tags_obj[tag] = 1

        # Sort tags_obj by tag count
        sorted_tags_obj = dict(sorted(tags_obj.items(), key=lambda item: item[1], reverse=True))

    # Save sorted shows
    with open('utilities/gi_youtube_video_sorted_by_shows_data.json', 'w') as outfile:
        json.dump(gi_shows, outfile, indent=2)

    # Save sorted tags by count to file
    with open('utilities/gi_youtube_video_tags_data.json', 'w') as outfile:
        json.dump(sorted_tags_obj, outfile, indent=2)

    duplicates_count = len(gi_shows['duplicates'])
    no_matches_count = len(gi_shows['no_matches']) 
    no_tags_count = len(gi_shows['no_tags'])
    matches_count = len(all_youtube_video_data) - duplicates_count - no_matches_count - no_tags_count
    print(
        f"Matches: { matches_count }",
        f"Duplicates: { duplicates_count }",
        f"No Matches: { no_matches_count }",
        f"No Tags: { no_tags_count }",
        sep='\n'
    )

def main():
    get_gi_shows()
    #get_blank_segment_type_replays()
    
    #clean_json_file()
    #display_middle_segment_data()
    #display_second_segment_data()
    pass

if __name__ == '__main__':
    main()