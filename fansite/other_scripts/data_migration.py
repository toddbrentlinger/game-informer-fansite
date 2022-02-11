import json
from venv import create
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

    # Host - replayData.details.host
    # Featuring - replayData.details.featuring
    # Guests - replayData.details.featuring

    # YouTube Video - replayData.youtube
    # Thumbnails - replayData.youtube.thumbnails

    # External Links - replayData.details.external_links
    # Headings - replayData.details

    # ---------- Replay Episode ----------

    # Season - calculate using replayData.episodeNumber
    
    # Number - replayData.episodeNumber
    
    # Main Segment Games - replayData.mainSegmentGamesAdv, replayData.details.system, replayData.details.gamedate
    
    # Other Segments - replayData.details
    
    # Article - replayData.article

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