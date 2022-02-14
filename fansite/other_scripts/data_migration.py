import json
import datetime
from ..models import Thumbnail, YouTubeVideo, Game, Guest, StaffPosition, StaffPositionInstance, Staff, Article, SegmentType, Segment, ExternalLink, Heading, HeadingInstance, ReplaySeason, ReplayEpisode, SuperReplay, SuperReplayEpisode

def createReplayEpisodeFromJSON(replayData):
    # Create Replay episode object
    replay = ReplayEpisode()

    # ---------- Episode ----------

    # Title - replayData.episodeTitle
    replay.title = replayData.episodeTitle

    # Runtime - replayData.details.runtime AND replayData.videoLength
    replay.runtime = replayData.details.runtime if replayData.details.runtime else (
        replayData.videoLength if replayData.videoLength else ""
    )

    # Airdate - replayData.airDate AND replayData.details.airdate
    if (replayData.airDate):
        replay.airdate = datetime.strptime(replayData.airDate,'%m/%d/%y') # month/day/year
    elif (replayData.details.airdate):
        replay.airdate = datetime.strptime(replayData.details.airdate, '%B %d, %Y') # month day, year

    # Host - replayData.details.host (ForeignKey)
    if replayData.details.host:
        nameList = replayData.details.host.split()
        try:
            person = Staff.objects.get(first_name=nameList[0], last_name__startswith=nameList[1])
        except Staff.DoesNotExist:
            # If name is NOT already in database, create new database entry (use 'create' to automatically save to database)
            person = Staff.objects.create(first_name=nameList[0], last_name=nameList[1])
        replay.host = person

    # Featuring - replayData.details.featuring (ManyToMany)
    if replayData.details.featuring:
        for personName in replayData.details.featuring:
            nameList = personName.split()
            try:
                person = Staff.objects.get(first_name=nameList[0], last_name__startswith=nameList[1])
            except Staff.DoesNotExist:
                person = Staff.objects.create(first_name=nameList[0], last_name=nameList[1])
            replay.featuring.add(person)

    # Guests - replayData.details.featuring (ManyToMany)

    # YouTube Video - replayData.youtube (OneToOne)
    if replayData.youtube:
        youtubeVideo = YouTubeVideo()

        # ID - replayData.details.external_links
        # Title
        if replayData.details.external_links:
            for link in replayData.details.external_links:
                # If link contains YouTube url, set ID, title, and break loop
                if ('youtube.com' in link['href']):
                    youtubeVideo.youtube_id = link['href'].split('watch?v=', 1)[1]
                    youtubeVideo.title = link['title']
                    break

        # Views
        youtubeVideo.views = replayData.youtube.views
        # Likes
        youtubeVideo.likes = replayData.youtube.likes
        # Dislikes
        youtubeVideo.dislikes = replayData.youtube.dislikes

        # Thumbnails
        for key, value in replayData.youtube.thumbnails:
            try:
                thumbnail = Thumbnail.objects.get(url=value['url'])
            except Thumbnail.DoesNotExist:
                thumbnail = Thumbnail.objects.create(
                    quality=key.upper(),
                    url=value['url'],
                    width=value['width'],
                    height=value['height']
                )
            youtubeVideo.thumbnails.add(thumbnail)

        youtubeVideo.save()
        replay.youtube_video = youtubeVideo

    # Thumbnails - replayData.youtube.thumbnails (ManyToMany)
    # Use YouTubeVideo.thumbnails instead or set to null

    # External Links - replayData.details.external_links (ManyToMany)
    # Headings - replayData.details

    # ---------- Replay Episode ----------

    # Season - calculate using replayData.episodeNumber (ForeignKey)
    
    # Number - replayData.episodeNumber
    
    # Main Segment Games - replayData.mainSegmentGamesAdv, replayData.details.system, replayData.details.gamedate (ManyToMany)
    
    # Other Segments - replayData.details (ManyToMany)
    
    # Article - replayData.article  (OneToOne)

    # Save Replay episode object to database
    replay.save()

def initialize_database(apps, schema_editor):
    # Open JSON data file
    dataFile = open('replay_data.json')

    # Get Replay episode data
    allReplayData = json.load(dataFile)

    # If there is Replay data
    # if (allReplayData):
    #     for replayData in allReplayData:
    #         createReplayEpisodeFromJSON(replayData)
    createReplayEpisodeFromJSON(allReplayData[0])

    # Close JSON data file
    dataFile.close()