import json

def main():
    with open('fansite/other_scripts/replay_data.json', 'r') as dataFile:

        # Get Replay episode data
        try:
            allReplayData = json.load(dataFile)
        except json.JSONDecodeError:
            allReplayData = None

        if (allReplayData):
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

if __name__ == '__main__':
    main()