import json
import datetime
from django.db.models import Q
from .igdb import IGDB #get_igdb_data, get_igdb_platform_data
from data_migration_constants import *
#from ..models import Thumbnail, YouTubeVideo, Guest, StaffPosition, StaffPositionInstance, Staff, Article, SegmentType, Segment, ExternalLink, Heading, HeadingInstance, ReplaySeason, ReplayEpisode, SuperReplay, SuperReplayEpisode
#from ...game.models import *

def databaseInit(apps):
    # Create Segment Types
    SegmentType = apps.get_model('fansite', 'SegmentType')
    for title, abbreviation, gameTextID in SEGMENT_TYPES.items():
        SegmentType.objects.create(title=title, abbreviation=abbreviation)

def get_game_inst(game_model, platform_model, igdb, name, platform_name = None, year_released = None):
    ''' 
    Returns specific instance of Game model.

    Parameters:
    game_model (Game): Reference to historic version of Game model
    platform_model (Platform): Reference to historic version of Platform model
    igdb (IGDB): Reference to IGDB instance to use IGDB API
    name (str): Name of video game
    platform (str|number): Name of platform as string type OR IGDB platform ID as number type

    Returns:
    Game: Existing or created instance of Game model
    '''

    # If platform is string
        # If platform already exists in database, assign id to platform
        # Else platform does NOT exist in database
            # Use IGDB API to search for platform data
            # If search succeeds
                # If platform id already exists in database, assign id to platform
                # Else add new platform model using IGDB platform data and assign id to platform
            # Else search fails
                # Must search for game using only title
                # Set platform to None so it's not used to search for game using IGDB

    # Search IGDB for game based on title AND platform ID
    # If search succeeds
        # Use first game from response AND platform ID
    # Else search fails
        # Attempt another search with just the title
        # If search succeeds
            # Use first game from response
            # If game has single platform, assign that platform
        # Else search failed
            # Raise error OR create Game model using only game name but required id is pk

    # If platform is None
    # Else platform is pk of Platform model instance (IGDB platform id)

    # ISSUE: If name+platform fails search but just name succeeds, platform would already have been added to database
    # even though it will NOT be assigned to field in Game model instance.

    '''
    define platform and platform_id default initialized or initialized to None
    if platform_name is not None:
        if platform_name is str
            if platform_name already exists in database
                set platform to Platform instance
                set platform_id
            else platform_name does NOT exist in database
                request platform data using IGDB and platform_name
                if platform response is successful AND NOT empty
                    if IGDB platform id already exists in database (name may not have matched but unique ID would match for duplicated in database)
                        set platform to Platform model instance
                        set platform_id
                    else IGDB platform id does NOT already exist in database
                        NOTE: Do not save Platform model to database since the platform and name may not return any game results on IGDB
                        but name alone might be successful. Save to database later ONLY if it matches with the game name.
                        set platform to new instance of Platform model (do NOT save to database yet)
                        set platform_id
                else platform response failed OR is empty
                    leave platform and platform_id as None
    '''
    # Assign platform using platform_name parameter (initialized to None)
    platform = None
    # If platform_name has value
    if platform_name:
        if type(platform_name) is str:
            # If platform_name already exists in database as different name fields, assign Platform instance to platform
            try:
                platform = platform_model.objects.get(
                    Q(abbreviation=platform_name) | Q(alternate_name__icontains=platform_name) | Q(name=platform_name)
                )
            # Else platform_name does NOT exist in database
            except platform_model.DoesNotExist:
                # Adjust name for 'PC' to 'PC Windows' before using IGDB API
                # TODO: Move this to misc module inside function to clean JSON file
                if platform_name == 'PC':
                    platform_name += ' Windows'

        elif type(platform_name) is int:
            # If platform_name already exists in database as ID, assign Platform instance to platform
            try:
                platform = platform_model.objects.get(pk=platform_name)
            # Else platform_name does NOT exist in database
            except platform_model.DoesNotExist:
                pass

        # If could not find existing platform in database
        if platform is None:
            # Use IGDB API to search for platform data
            platform_data = igdb.get_platform_data(platform_name)
            
            # If search succeeds AND not empty
            if platform_data is not None and len(platform_data) > 0:
                # If platform id already exists in database, assign Platform instance to platform
                try:
                    platform = platform_model.objects.get(pk=platform_data[0]['id'])
                # Else create new platform model instance using IGDB platform data and assign it to platform.
                # Do NOT save new instance to database until confirm game name and platform search succeeds.
                except platform_model.DoesNotExist:
                    platform = platform_model()
                    platform.id = platform_data[0]['id']
                    platform.abbreviation = platform_data[0]['abbreviation']
                    platform.alternate_name = platform_data[0]['alternative_name']
                    platform.name = platform_data[0]['name']
            # Else search fails or is empty
                # Must search for game using only name
                # Set platform to None so it's not used to search for game using IGDB

    # Inner function to get or create a Game model instance with optional platform paramter
    def create_game_model(name, platform = None):
        game_data = igdb.get_game_data(name, platform.id if platform is not None else None, year_released, fields)
        # If game search succeeds with given platform AND NOT empty
        if game_data is not None and len(game_data) > 0:
            # Check if game ID already exists in database
            try:
                game_inst = game_model.objects.get(pk=game_data[0]['id'])
            except game_model.DoesNotExist:
                # Save platform in case it was created for this game and not yet inside database
                if platform is not None:
                    platform.save()
                
                game_inst = game_model.objects.create(
                    igdb_id=game_data[0]['id'],
                    name=game_data[0]['name'],
                    slug=game_data[0]['slug'],
                    summary=game_data[0]['summary'],
                    platform=platform,
                    developer=None,
                    release_date=datetime.date.fromtimestamp(game_data[0]['first_release_date'])
                )
                # Genre is ManyToManyField, use game.genre.add(newGenre)
            finally:
                return game_inst
        return None

    # Search IGDB for game based on title AND platform ID
    fields = 'cover.*,first_release_date,genres.*,id,involved_companies.*,name,platforms.*,platforms.platform_logo.*,release_dates.*,slug,summary;'
    
    # If platform has value, search for game with both name+platform
    if platform is not None:
        game_inst = create_game_model(name, platform, year_released, fields)
        # If game search succeeds with name+platform, return the game model instance
        if game_inst is not None:
            return game_inst

    # If platform has value but reaches this point, could not find game with name+platform.
    # Attempt search with just the name of the video game
    game_inst = create_game_model(name, None, year_released, fields)
    # If game search succeeds with no platform, return the game model instance
    if game_inst is not None:
        return game_inst
    # Else game search fails with no platform
        # Reach here when neither name+platform nor just name has successful game search
        
    # If reach here, could not find game
    print(f'Could not find game using:\nName: {name}\nP: {platform_name}\nYear: {year_released}')
    return None

def createReplayEpisodeFromJSON(replayData, apps):
    '''
    Converts dictionary of key/value pairs into defined models inside database for data migration.

    Parameters:
        replayData (dict):
        app ():
    '''
    # Cannot import models directly as it may be a newer version
    # than this migration expects. Use historical versions instead.
    Thumbnail = apps.get_model('fansite', 'Thumbnail')
    YouTubeVideo = apps.get_model('fansite', 'YouTubeVideo')
    Person = apps.get_model('fansite', 'Person')
    #Guest = apps.get_model('fansite', 'Guest')
    #StaffPosition = apps.get_model('fansite', 'StaffPosition')
    #StaffPositionInstance = apps.get_model('fansite', 'StaffPositionInstance')
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
            name = replayData['details']['host'][0]
            try:
                person = Person.objects.get(full_name=name)
            except Person.DoesNotExist:
                person = Person.objects.create(full_name=name)
            replay.host = person

        # Featuring - replayData.details.featuring (ManyToMany)
        if 'featuring' in replayData['details'] and replayData['details']['featuring']:
            for personName in replayData['details']['featuring']:
                name = personName
                try:
                    person = Person.objects.get(full_name=name)
                except Person.DoesNotExist:
                    person = Person.objects.create(full_name=name)
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

            # Game - Year Released
            game_year_released = game['yearReleased']

            # Game - Platform
            platform_name = game['system']

            game_inst = get_game_inst(Game, Platform, igdb, game_name, platform_name, game_year_released)
            if game_inst is not None:
                replay.main_segment_games.add(game_inst)
    
    # Use platform from main_segment_games field to search for games in other segments
    platform = None
    if replay.main_segment_games.exists():
        platform_count = {} # key: IGDB platform ID, value: number of games with this platform in main_segment_games
        for game in replay.main_segment_games.all():
            if game.platform__id in platform_count:
                platform_count[game.platform__id] += 1
            else:
                platform_count[game.platform__id] = 1
        # Use platform id with highest count
        max_count = 0
        for key, value in platform_count.items():
            if value > max_count:
                max_count = value
                platform = key

    def create_segment_inst(segmentType, segmentContent):
        '''
        Creates instance of Segment model, saves to database, and returns.

        Parameter:
            segmentType (str): Name or abbreviation of segment type.
            segmentContent ([str]): List of game names or segment description.

        Returns:
            Segment
        '''
        segment = Segment()

        segmentTypeInst = None
        for segmentTitle, abbreviation, gameTextID in SEGMENT_TYPES.items():
            if segmentType in (abbreviation, segmentTitle):
                try:
                    segmentTypeInst = SegmentType.objects.get(abbreviation=segmentType)
                except SegmentType.DoesNotExist:
                    segmentTypeInst = SegmentType.objects.create(
                        title=SEGMENT_TYPES[segmentType] ,
                        abbreviation=segmentType
                    )

                # Game/Text ID: 0-game 1-text 2-game/text

                if gameTextID == 0: # game
                    for game in segmentContent:
                        # Add content to 'games', leaving 'description' empty
                        game_title = game.rpartition(' Ad')[0] if game.endswith('Ad') else game
                        # Get game using title and platform from main_segment_games
                        game_inst = get_game_inst(Game, Platform, igdb, game_title, platform, None)
                        if game_inst is not None:
                            segment.games.add(game_inst)

                elif gameTextID == 1: # text
                    # Add content to 'description' leaving 'games' empty
                    segment.description = ', '.join(segmentContent)

                elif gameTextID == 2: # game/text
                    # Special Cases: Moments and Developer Spotlight
                    if segmentType == 'Moments':
                        if segmentContent[0] == 'Syphone Filter\'s Cutscenes':
                            # Add game
                            # Get game using title and platform from main_segment_games
                            game_inst = get_game_inst(Game, Platform, igdb, segmentContent, platform, None)
                            if game_inst is not None:
                                segment.games.add(game_inst)
                            # Add description
                            segment.description = segmentContent[0]
                    elif segmentType == 'Developer Spotlight':
                        for index, game in enumerate(segmentContent):
                            if index == 0:
                                # First index of game list example: Rare Games: Slalom
                                title_split = game.split(': ', 1)
                                # Get game using title_split[1] and platform from main_segment_games
                                game_inst = get_game_inst(Game, Platform, igdb, title_split[1], platform, None)
                                if game_inst is not None:
                                    segment.games.add(game_inst)
                                # Add description from title_split[0]
                                segment.description = title_split[0]
                            else:
                                # Add game
                                # Get game using title and platform from main_segment_games
                                game_inst = get_game_inst(Game, Platform, igdb, game, platform, None)
                                if game_inst is not None:
                                    segment.games.add(game_inst)

                break
        # If segmentTypeInst is still none, unknown segment type.
        # Use value as segment title, leaving abbreviation blank.
        if segmentTypeInst is None:
            try:
                segmentTypeInst = SegmentType.objects.get(title=segmentType)
            except SegmentType.DoesNotExist:
                segmentTypeInst = SegmentType.objects.create(title=segmentType)

            # Add description
            segment.description = ', '.join(segmentContent)

        # Set type field in segment model instance
        segment.type = segmentTypeInst

        segment.save()
        return segment

    # Other Segments - replayData.details (ManyToMany)
    # replayData.middleSegment, replayData.middleSegmentContent
    # If middleSegment or middleSegmentContent are NOT blank
    if 'middleSegment' in replayData and (replayData['middleSegment'] or replayData['middleSegmentContent']):
        # - middleSegment could be blank while middleSegmentContent has value
        # - middleSegment is blank if middleSegmentContent is blank
        # - both can be blank
        # - Could have games or description

        # If middleSegment is blank AND middleSegmentContent is NOT blank
        #     Segment is 'Ad' OR RR game OR Red Faction D&D Skit

        # Ads do not always have middleSegment blank. Could be labeled under 'Moments'.
        # Should instead add Ads to Moments segment rather then Advertisement
        # OR add single Moments advertisement to Advertisement segment.

        segmentType = replayData['middleSegment']
        segmentContent = replayData['middleSegmentContent']
        
        if segmentContent:
            replay.other_segments.add(create_segment_inst(segmentType, segmentContent))
            # segment = Segment()

            # segmentTypeInst = None
            # for segmentTitle, abbreviation, gameTextID in SEGMENT_TYPES.items():
            #     if segmentType in (abbreviation, segmentTitle):
            #         try:
            #             segmentTypeInst = SegmentType.objects.get(abbreviation=segmentType)
            #         except SegmentType.DoesNotExist:
            #             segmentTypeInst = SegmentType.objects.create(
            #                 title=SEGMENT_TYPES[segmentType] ,
            #                 abbreviation=segmentType
            #             )
            #         # Game/Text ID: 0-game 1-text 2-game/text
            #         if gameTextID == 0: # game
            #             # Add content to 'games', leaving 'description' empty
            #             game_title = segmentContent.rpartition(' Ad')[0] if segmentContent.endswith('Ad') else segmentContent
            #             # Get game using title and platform from main_segment_games
            #             game_inst = get_game_inst(Game, Platform, igdb, game_title, platform, None)
            #             if game_inst is not None:
            #                 segment.games.add(game_inst)

            #         elif gameTextID == 1: # text
            #             # Add content to 'description' leaving 'games' empty
            #             segment.description = segmentContent

            #         elif gameTextID == 2: # game/text
            #             # Special Cases: Moments and Developer Spotlight
            #             if segmentType == 'Moments':
            #                 if segmentContent == 'Syphone Filter\'s Cutscenes':
            #                     # Add game
            #                     # Get game using title and platform from main_segment_games
            #                     game_inst = get_game_inst(Game, Platform, igdb, segmentContent, platform, None)
            #                     if game_inst is not None:
            #                         segment.games.add(game_inst)
            #                     # Add description
            #                     segment.description = segmentContent
            #             elif segmentType == 'Developer Spotlight':
            #                 for index, game in enumerate(segmentContent):
            #                     if index == 0:
            #                         # First index of game list example: Rare Games: Slalom
            #                         title_split = segmentContent.split(': ', 1)
            #                         # Get game using title_split[1] and platform from main_segment_games
            #                         game_inst = get_game_inst(Game, Platform, igdb, title_split[1], platform, None)
            #                         if game_inst is not None:
            #                             segment.games.add(game_inst)
            #                         # Add description from title_split[0]
            #                         segment.description = title_split[0]
            #                     else:
            #                         # Add game
            #                         # Get game using title and platform from main_segment_games
            #                         game_inst = get_game_inst(Game, Platform, igdb, game, platform, None)
            #                         if game_inst is not None:
            #                             segment.games.add(game_inst)

            #         break
            # # If segmentTypeInst is still none, unknown segment type.
            # # Use value as segment title, leaving abbreviation blank.
            # if segmentTypeInst is None:
            #     try:
            #         segmentTypeInst = SegmentType.objects.get(title=segmentType)
            #     except SegmentType.DoesNotExist:
            #         segmentTypeInst = SegmentType.objects.create(title=segmentType)

            #     # Add description
            #     segment.description = segmentContent

            # # Set type field in segment model instance
            # segment.type = segmentTypeInst

            # # Save segment instance before adding it to ManyToManyField in replay instance
            # segment.save()
            # replay.other_segments.add(segment)

    # replayData.secondSegment, replayData.secondSegmentGames
    if 'secondSegment' in replayData:
        segmentType = replayData['secondSegment']
        segmentContent = replayData['secondSegmentGames']

        if segmentContent:
            replay.other_segments.add(create_segment_inst(segmentType, segmentContent))
            # segment = Segment()

            # segmentTypeInst = None
            # for segmentTitle, abbreviation, gameTextID in SEGMENT_TYPES.items():
            #     if segmentType in (abbreviation, segmentTitle):
            #         try:
            #             segmentTypeInst = SegmentType.objects.get(abbreviation=segmentType)
            #         except SegmentType.DoesNotExist:
            #             segmentTypeInst = SegmentType.objects.create(
            #                 title=SEGMENT_TYPES[segmentType] ,
            #                 abbreviation=segmentType
            #             )

            #         # Game/Text ID: 0-game 1-text 2-game/text

            #         if gameTextID == 0: # game
            #             for game in segmentContent:
            #                 # Add content to 'games', leaving 'description' empty
            #                 game_title = game.rpartition(' Ad')[0] if game.endswith('Ad') else game
            #                 # Get game using title and platform from main_segment_games
            #                 game_inst = get_game_inst(Game, Platform, igdb, game_title, platform, None)
            #                 if game_inst is not None:
            #                     segment.games.add(game_inst)

            #         elif gameTextID == 1: # text
            #             # Add content to 'description' leaving 'games' empty
            #             segment.description = ', '.join(segmentContent)

            #         elif gameTextID == 2: # game/text
            #             # Special Cases: Moments and Developer Spotlight
            #             if segmentType == 'Moments':
            #                 if segmentContent[0] == 'Syphone Filter\'s Cutscenes':
            #                     # Add game
            #                     # Get game using title and platform from main_segment_games
            #                     game_inst = get_game_inst(Game, Platform, igdb, segmentContent, platform, None)
            #                     if game_inst is not None:
            #                         segment.games.add(game_inst)
            #                     # Add description
            #                     segment.description = segmentContent
            #             elif segmentType == 'Developer Spotlight':
            #                 for index, game in enumerate(segmentContent):
            #                     if index == 0:
            #                         # First index of game list example: Rare Games: Slalom
            #                         title_split = game.split(': ', 1)
            #                         # Get game using title_split[1] and platform from main_segment_games
            #                         game_inst = get_game_inst(Game, Platform, igdb, title_split[1], platform, None)
            #                         if game_inst is not None:
            #                             segment.games.add(game_inst)
            #                         # Add description from title_split[0]
            #                         segment.description = title_split[0]
            #                     else:
            #                         # Add game
            #                         # Get game using title and platform from main_segment_games
            #                         game_inst = get_game_inst(Game, Platform, igdb, game, platform, None)
            #                         if game_inst is not None:
            #                             segment.games.add(game_inst)

            #         break
            # # If segmentTypeInst is still none, unknown segment type.
            # # Use value as segment title, leaving abbreviation blank.
            # if segmentTypeInst is None:
            #     try:
            #         segmentTypeInst = SegmentType.objects.get(title=segmentType)
            #     except SegmentType.DoesNotExist:
            #         segmentTypeInst = SegmentType.objects.create(title=segmentType)

            #     # Add description
            #     segment.description = segmentContent

            # # Set type field in segment model instance
            # segment.type = segmentTypeInst

            # segment.save()
            # replay.other_segments.add(segment)
    
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
        if (allReplayData):
            for replayData in allReplayData:
                createReplayEpisodeFromJSON(replayData, apps)

            # Use YouTube Data API to update all YouTubeVideo models.
            # Can batch video IDs into single request rather than doing them 
            # individually when YouTubeVideo model is first created.
        #createReplayEpisodeFromJSON(allReplayData[0], apps)

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