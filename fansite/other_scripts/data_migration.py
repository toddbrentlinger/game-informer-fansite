import json
import datetime
from django.db.models import Q
from .igdb import IGDB #get_igdb_data, get_igdb_platform_data
#from ..models import Thumbnail, YouTubeVideo, Guest, StaffPosition, StaffPositionInstance, Staff, Article, SegmentType, Segment, ExternalLink, Heading, HeadingInstance, ReplaySeason, ReplayEpisode, SuperReplay, SuperReplayEpisode
#from ...game.models import *

SEGMENT_TYPES = {
    'RR': 'Replay Roulette',
    'SRS': 'Super Replay Showdown',
    'YDIW': 'You\'re Doing It Wrong',
    'ST': 'Stress Test',
    'RP': 'RePorted',
    'DP': 'Developer Pick',
    '2037': 'Replay 2037',
    'HF': 'Horror Fest',
    'RRL': 'Replay Real Life',
    'AD': 'Advertisement',
}

def createReplayEpisodeFromJSON(replayData, apps):
    # Cannot import models directly as it may be a newer version
    # than this migration expects. Use historical versions instead.
    Thumbnail = apps.get_model('fansite', 'Thumbnail')
    YouTubeVideo = apps.get_model('fansite', 'YouTubeVideo')
    Guest = apps.get_model('fansite', 'Guest')
    StaffPosition = apps.get_model('fansite', 'StaffPosition')
    StaffPositionInstance = apps.get_model('fansite', 'StaffPositionInstance')
    Staff = apps.get_model('fansite', 'Staff')
    Article = apps.get_model('fansite', 'Article')
    SegmentType = apps.get_model('fansite', 'SegmentType')
    Segment = apps.get_model('fansite', 'Segment')
    ExternalLink = apps.get_model('fansite', 'ExternalLink')
    Heading = apps.get_model('fansite', 'Heading')
    HeadingInstance = apps.get_model('fansite', 'HeadingInstance')
    ReplaySeason = apps.get_model('fansite', 'ReplaySeason')
    ReplayEpisode = apps.get_model('fansite', 'ReplayEpisode')
    SuperReplay = apps.get_model('fansite', 'SuperReplay')
    SuperReplayEpisode = apps.get_model('fansite', 'SuperReplayEpisode')

    Game = apps.get_model('game', 'Game')
    Platform = apps.get_model('game', 'Platform')

    # Instance initialization creates API access_token
    igdb = IGDB()

    # Create Replay episode object
    replay = ReplayEpisode()

    # ---------- Episode ----------

    # Title - replayData.episodeTitle
    replay.title = replayData['episodeTitle']

    # Runtime - replayData.details.runtime AND replayData.videoLength
    if 'details' in replayData and 'runtime' in replayData['details']:
        replay.runtime = replayData['details']['runtime']
    elif 'videoLength' in replayData and replayData['videoLength']:
        replay.runtime = replayData['videoLength']

    # Airdate - replayData.airDate AND replayData.details.airdate
    if 'airdate' in replayData and replayData['airDate']:
        replay.airdate = datetime.datetime.strptime(replayData['airDate'],'%m/%d/%y') # month/day/year
    elif 'details' in replayData and 'airdate' in replayData['details'] and replayData['details']['airdate']:
        replay.airdate = datetime.datetime.strptime(replayData['details']['airdate'], '%B %d, %Y') # month day, year

    # Host/Featuring/Guests inside 'details'
    if 'details' in replayData:

        # Host - replayData.details.host (ForeignKey)
        if 'host' in replayData['details'] and replayData['details']['host']:
            nameList = replayData['details']['host'][0].split()
            try:
                person = Staff.objects.get(first_name=nameList[0], last_name=nameList[1])
            except Staff.DoesNotExist:
                person = Staff.objects.create(first_name=nameList[0], last_name=nameList[1])
            replay.host = person

        # Featuring - replayData.details.featuring (ManyToMany)
        if 'featuring' in replayData['details'] and replayData['details']['featuring']:
            for personName in replayData['details']['featuring']:
                nameList = personName.split()
                try:
                    person = Staff.objects.get(first_name=nameList[0], last_name=nameList[1])
                except Staff.DoesNotExist:
                    person = Staff.objects.create(first_name=nameList[0], last_name=nameList[1])
                replay.featuring.add(person)

        # Guests - replayData.details.featuring (ManyToMany)

    # YouTube Video - replayData.youtube (OneToOne)
    if 'youtube' in replayData and replayData['youtube']:
        youtubeVideo = YouTubeVideo()

        # ID - replayData.details.external_links
        # Title
        if 'details' in replayData and 'external_links' in replayData['details'] and replayData['details']['external_links']:
            for link in replayData['details']['external_links']:
                # If link contains YouTube url, set ID, title, and break loop
                if ('youtube.com' in link['href']):
                    youtubeVideo.youtube_id = link['href'].split('watch?v=', 1)[1]
                    youtubeVideo.title = link['title']
                    break

        # Views
        youtubeVideo.views = replayData['youtube']['views']
        # Likes
        youtubeVideo.likes = replayData['youtube']['likes']
        # Dislikes
        youtubeVideo.dislikes = replayData['youtube']['dislikes']

        # Save YouTubeVideo before adding Thumbnails through Many-to-Many relationship
        youtubeVideo.save()

        # Thumbnails
        for key, value in replayData['youtube']['thumbnails'].items():
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

        # Add YouTubeVideo to ReplayEpisode
        replay.youtube_video = youtubeVideo

    # Thumbnails - replayData.youtube.thumbnails (ManyToMany)
    # Use YouTubeVideo.thumbnails instead or set to null

    # External Links and Other Headings inside 'details'
    if 'details' in replayData:

        # External Links - replayData.details.external_links (ManyToMany)
        if 'external_links' in replayData['details'] and replayData['details']['external_links']:
            for link in replayData['details']['external_links']:
                # Skip links containing 'youtube.com'
                if 'youtube.com' in link['href']:
                    continue
                externalLink = ExternalLink.objects.create(
                    url=link['href'],
                    title=link['title']
                )
                replay.external_links.add(externalLink)

        # Headings - replayData.details
        HEADINGS_TO_IGNORE = ('external_links', 'system', 'gamedate', 'airdate', 'runtime', 'host', 'featuring')
        headingsJSON = {}
        for key, value in replayData['details'].items():
            if key in HEADINGS_TO_IGNORE or not value:
                continue
            headingsJSON[key] = value
        replay.headings = headingsJSON

    # ---------- Replay Episode ----------
    
    # Number - replayData.episodeNumber
    if 'episodeNumber' in replayData and replayData['episodeNumber']:
        replay.number = replayData['episodeNumber']

        # Season - calculate using replayData.episodeNumber (ForeignKey)
        season = get_season(replay)[0]
        try:
            replay.season = ReplaySeason.objects.get(pk=season)
        except ReplaySeason.DoesNotExist:
            replay.season = ReplaySeason.objects.create(
                number=get_season(replay)[0]
            )
    
    # Main Segment Games - replayData.mainSegmentGamesAdv, replayData.details.system, replayData.details.gamedate (ManyToMany)
    if 'mainSegmentGamesAdv' in replayData:
        # Save ReplayEpisode before adding Games through Many-to-Many relationship
        replay.save()

        for game in replayData['mainSegmentGamesAdv']:
            # Game - Name
            game_name = game['title']

            # Game - Platform
            platform_name = game['system']
            platform = None
            try:
                platform = Platform.objects.get(
                    Q(abbreviation=platform_name) | Q(alternate_name__icontains=platform_name) | Q(name=platform_name)
                )
            except Platform.DoesNotExist:
                # Adjust name for 'PC' to 'PC Windows'
                if platform_name == 'PC':
                    platform_name += ' Windows'
                # Get data on game platform from IGDB API
                platform_data = igdb.get_platform_data(platform_name)[0]
                if platform_data is not None:
                    platform = Platform.objects.create(
                        id=platform_data['id'],
                        abbreviation=platform_data['abbreviation'],
                        alternate_name=platform_data['alternative_name'],
                        name=platform_data['name']
                    )

            # Game - Year Released
            game_year_released = game['yearReleased']
            
            # Get game data using IGDB API
            fields = 'cover.*,first_release_date,genres.*,id,involved_companies.*,name,platforms.*,platforms.platform_logo.*,release_dates.*,slug,summary;'
            game_data = igdb.get_game_data(game_name, platform.id, game_year_released, fields)[0]
            if game_data is not None:
                # Check if game ID already exists in database
                try:
                    game_inst = Game.objects.get(pk=game_data['id'])
                except Game.DoesNotExist:
                    game_inst = Game.objects.create(
                        igdb_id=game_data['id'],
                        name=game_data['name'],
                        slug=game_data['slug'],
                        summary=game_data['summary'],
                        platform=platform,
                        developer=None,
                        release_date=datetime.date.fromtimestamp(game_data['first_release_date'])
                    )
                    # Genre is ManyToManyField, use game.genre.add(newGenre)

                replay.main_segment_games.add(game_inst)
    
    # Other Segments - replayData.details (ManyToMany)

    # replayData.middleSegment, replayData.middleSegmentContent
    if 'middleSegment' in replayData:
        # - middleSegment could be blank while middleSegmentContent has value
        # - middleSegment is blank if middleSegmentContent is blank 
        # - middleSegment has value if middleSegmentContent has value
        # - both can be blank
        # - Could have games or description

        # If middleSegment is blank AND middleSegmentContent is NOT blank
        #     Segment is 'Ad'

        segmentContent = replayData['middleSegmentContent'] if replayData['middleSegmentContent'].replace('-', '') else ''
        if segmentContent:
            segment = Segment()
            segmentType = replayData['middleSegment'] if replayData['middleSegment'].replace('-', '') else 'AD'
            
            # Type
            
            # If type if all uppercase letters or match key in dictionary of known
            # abbreviations with title, then use dict values for segment.
            if segmentType in SEGMENT_TYPES:
                try:
                    segmentTypeInst = SegmentType.objects.get(abbreviation=segmentType)
                except SegmentType.DoesNotExist:
                    segmentTypeInst = SegmentType.objects.create(
                        title=SEGMENT_TYPES[segmentType],
                        abbreviation=segmentType
                    )
            # Else use value as segment title, leaving abbreviation blank.
            else:
                try:
                    segmentTypeInst = SegmentType.objects.get(title=segmentType)
                except SegmentType.DoesNotExist:
                    segmentTypeInst = SegmentType.objects.create(title=segmentType)

            segment.type = segmentTypeInst

            # Games
            # Description - If 'RRL' or 'AD'
            if segmentTypeInst.abbreviation in ('RRL', 'AD'):
                segment.description = segmentContent
            else:
                # Add to segment.games
                segment.description = segmentContent

            segment.save()
            replay.other_segments.add(segment)

    # replayData.secondSegment, replayData.secondSegmentGames
    if 'secondSegment' in replayData:
        segmentType = replayData['secondSegment'] if replayData['secondSegment'].replace('-', '') else ''
        segmentContent = replayData['secondSegmentGames']
        # - secondSegment could be blank while secondSegmentGames has value
        
        if replayData['secondSegmentGames']:

            segment = Segment()

            # Type
            if segmentType:
                # If type if all uppercase letters or match key in dictionary of known
                # abbreviations with title, then use dict values for segment.
                if segmentType in SEGMENT_TYPES:
                    try:
                        segmentTypeInst = SegmentType.objects.get(abbreviation=segmentType)
                    except SegmentType.DoesNotExist:
                        segmentTypeInst = SegmentType.objects.create(
                            title=SEGMENT_TYPES[segmentType],
                            abbreviation=segmentType
                        )
                # Else use value as segment title, leaving abbreviation blank.
                else:
                    try:
                        segmentTypeInst = SegmentType.objects.get(title=segmentType)
                    except SegmentType.DoesNotExist:
                        segmentTypeInst = SegmentType.objects.create(title=segmentType)
            else: # Else empty segment type
                try:
                    segmentTypeInst = SegmentType.objects.get(title='Other')
                except SegmentType.DoesNotExist:
                    segmentTypeInst = SegmentType.objects.create(title='Other')

            segment.type = segmentTypeInst

            # Games
            # Description - second segment has no description (always games)            
            segment.description = [
                game for game in filter(
                    lambda x: x.replace('-', ''), 
                    replayData['secondSegmentGames']
                )
            ]

            segment.save()
            replay.other_segments.add(segment)
    
    # Article - replayData.article  (OneToOne)
    if 'article' in replayData:
        article = Article()

        # Title - replayData.article.title
        article.title = replayData['article']['title']

        # Author - replayData.article.author
        nameList = replayData['article']['author'].split()
        try:
            person = Staff.objects.get(first_name=nameList[0], last_name__startswith=nameList[1])
        except Staff.DoesNotExist:
            # If name is NOT already in database, create new database entry (use 'create' to automatically save to database)
            person = Staff.objects.create(first_name=nameList[0], last_name=nameList[1])
        article.author = person

        # Datetime - replayData.article.date
        # " on Sep 26, 2015 at 03:00 AM"
        article.datetime = datetime.datetime.strptime(
            replayData['article']['date'],
            ' on %b %d, %Y at %I:%M %p'
        )

        # Content - replayData.article.content
        article.content = '\n'.join(replayData['article']['content'])

        # URL - replayData.details.external_links
        if 'details' in replayData and 'external_links' in replayData['details'] and replayData['details']['external_links']:
            for link in replayData['details']['external_links']:
                # If link contains GameInformer url, set ID, title, and break loop
                if 'gameinformer.com' in link['href']:
                    article.url = link['href']
                    break

        article.save()
        replay.article = article

    # Save Replay episode object to database
    replay.save()

def initialize_database(apps, schema_editor):
    with open('fansite/other_scripts/replay_data.json', 'r') as dataFile:

        # Get Replay episode data
        allReplayData = json.load(dataFile)

        # If there is Replay data
        # if (allReplayData):
        #     for replayData in allReplayData:
        #         createReplayEpisodeFromJSON(replayData)
        createReplayEpisodeFromJSON(allReplayData[0], apps)

    '''
    from django.db import migrations
    from fansite.other_scripts.data_migration import initialize_database

    class Migration(migrations.Migration):

        dependencies = [
            ('fansite', '0001_initial'),
            # added dependency to enable models from 'game' app to initialize_database method
            ('game', '0001_initial'),
        ]

        operations = [
            migrations.RunPython(initialize_database),
        ]
    '''

def get_season(replayEpisode):
        # Episode numbers less than 1 are special unofficial episodes
        replaySeasonStartEpisodes = [1, 107, 268, 385, 443, 499] # [S1, S2, S3, S4, S5, S6]

        # Season
        
        for index in range(len(replaySeasonStartEpisodes)):
            if (replayEpisode.number < replaySeasonStartEpisodes[index]):
                season = index
                break
            # If reached end of loop, assign last season
            if index == (len(replaySeasonStartEpisodes) - 1):
                season = len(replaySeasonStartEpisodes)

        # Season Episode

        seasonEpisode = replayEpisode.number - replaySeasonStartEpisodes[season - 1] + 1 if season > 1 else replayEpisode.number

        # Return tuple (season, seasonEpisode)
        return (season, seasonEpisode)