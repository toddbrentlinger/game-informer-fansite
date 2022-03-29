import json
import pprint
import math
from operator import itemgetter
from venv import create

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

def main():
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

    #clean_json_file()
    #display_middle_segment_data()
    #display_second_segment_data()

if __name__ == '__main__':
    main()