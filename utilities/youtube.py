from googleapiclient.discovery import build
from decouple import config

# convert url to videoID => url.split("watch?v=",1)[1]
def getYouTubeData(videoID, param = 'snippet,statistics'):
    # Arguments that need to passed to the build function 
    DEVELOPER_KEY = config('YOUTUBE_DEVELOPER_KEY')
    YOUTUBE_API_SERVICE_NAME = 'youtube'
    YOUTUBE_API_VERSION = 'v3'
   
    # creating Youtube Resource Object 
    youtube_object = build(
        YOUTUBE_API_SERVICE_NAME, 
        YOUTUBE_API_VERSION,
        developerKey = DEVELOPER_KEY
    )

    request = youtube_object.videos().list(
        part=param,
        id=videoID
    )
    response = request.execute()

    if response['items']:
        return response['items'][0]
    else:
        print(f'Could NOT get data from YouTube video ID: {videoID}')
        return None

def main():
    print(getYouTubeData('nSFdetbQ18M')) # Revolution X Replay

if __name__ == "__main__":
    main()