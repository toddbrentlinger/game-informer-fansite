import json
import pprint
from operator import itemgetter

def change_dashes_to_null(obj):
    if isinstance(obj, dict):
        for key, value in obj.items():
            if isinstance(value, str) and len(value) != 0 and len(value.replace('-', '')) == 0:
                print(f'Value changed: {value}')
                obj[key] = ''
            else:
                change_dashes_to_null(value)
    elif isinstance(obj, list):
        for index, value in enumerate(obj):
            if isinstance(value, str) and len(value) != 0 and len(value.replace('-', '')) == 0:
                print(f'Value changed: {value}')
                obj[index] = ''
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

    with open('fansite/other_scripts/replay_data.json', 'w') as dataFile:
        json.dump(allReplayData, dataFile, indent=4)

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

def print_segment_types():
    with open('fansite/other_scripts/replay_data.json', 'r') as dataFile:

        # Get Replay episode data
        try:
            allReplayData = json.load(dataFile)
        except json.JSONDecodeError:
            return

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

def main():
    clean_json_file()
    display_middle_segment_data()

if __name__ == '__main__':
    main()