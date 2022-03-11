import json
from textwrap import indent

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
                if replayData['middleSegment'] and replayData['middleSegmentContent']:
                    pass
                elif replayData['middleSegment']:
                    pass
                elif replayData['middleSegmentContent']:
                    pass
                # Else both 'middleSegment' and 'middleSegmentContent' are blank

    with open('fansite/other_scripts/replay_data.json', 'w') as dataFile:
        json.dump(allReplayData, dataFile, indent=4)

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

if __name__ == '__main__':
    main()