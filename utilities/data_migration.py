import json
import datetime
import time
import pprint # Used to debug
import math
import re
from django.db.models import Q
from django.utils import timezone
from utilities.igdb import IGDB # Make requests from IGDB API
from utilities.data_migration_constants import SEGMENT_TYPES, STAFF, GAME_NAME_ALTERNATIVES # Separate file to hold constants
from utilities.misc import create_total_time_message # misc utility functions
from django.template.defaultfilters import slugify

class Models:
    def __init__(self, apps):
        # Cannot import models directly as it may be a newer version
        # than this migration expects. Use historical versions instead.
        
        # Fansite app
        # self.SuperReplay = apps.get_model('fansite', 'SuperReplay')
        # self.SuperReplayEpisode = apps.get_model('fansite', 'SuperReplayEpisode')

        # People app
        self.Person = apps.get_model('people', 'Person')
        # self.Guest = apps.get_model('people', 'Guest')
        # self.StaffPosition = apps.get_model('people', 'StaffPosition')
        # self.StaffPositionInstance = apps.get_model('people', 'StaffPositionInstance')
        self.Staff = apps.get_model('people', 'Staff')

        # Game app
        self.Artwork = apps.get_model('games', 'Artwork')
        self.Collection = apps.get_model('games', 'Collection')
        self.Developer = apps.get_model('games', 'Developer')
        self.Franchise = apps.get_model('games', 'Franchise')
        self.Game = apps.get_model('games', 'Game')
        self.GameVideo = apps.get_model('games', 'GameVideo')
        self.Genre = apps.get_model('games', 'Genre')
        self.ImageIGDB = apps.get_model('games', 'ImageIGDB')
        self.Keyword = apps.get_model('games', 'Keyword')
        self.Platform = apps.get_model('games', 'Platform')
        self.Screenshot = apps.get_model('games', 'Screenshot')
        self.Theme = apps.get_model('games', 'Theme')
        self.Website = apps.get_model('games', 'Website')

        # Replay app
        self.Article = apps.get_model('replay', 'Article')
        self.ExternalLink = apps.get_model('replay', 'ExternalLink')
        # self.Heading = apps.get_model('replay', 'Heading')
        # self.HeadingInstance = apps.get_model('replay', 'HeadingInstance')
        self.ReplayEpisode = apps.get_model('replay', 'ReplayEpisode')
        self.ReplaySeason = apps.get_model('replay', 'ReplaySeason')
        self.Segment = apps.get_model('replay', 'Segment')
        self.SegmentType = apps.get_model('replay', 'SegmentType')
        self.Thumbnail = apps.get_model('replay', 'Thumbnail')
        self.YouTubeVideo = apps.get_model('replay', 'YouTubeVideo')

def is_franchise_in_list(franchise, franchise_list):
    '''
    Returns True if franchise object already exists in list, else returns False.

    Parameter:
        franchise (dict): JSON object of franchise data returned by IGDB request
        franchise_list (list): List/array of JSON objects of franchise data returned by IGDB request

    Returns:
        Boolean: True if franchise object already exists in list, else False
    '''
    for franchise_list_item in franchise_list:
        if franchise['id'] == franchise_list_item['id']:
            return True
    return False

def create_game_model(models, igdb, name, platform_inst = None, year_released = None, fields = '*', exclude = None):
    '''
    Returns Game model instance from database if it already exists OR needs to be created.

    Parameters:
        models (Models): 
        igdb (): 
        name (str|int): Title of video game if string OR IGDB ID if integer.
        platform_inst (Platform): Platform model instance for the video game (NOTE: Will be saved to database if game search succeeds)
        year_released (str|int): Year the video game was released
        fields (str): Search fields passed to IGDB API request
        exclude (str): Fields to exclude from response to IGDB API request

    Returns:
        Game|None: Game model instance OR None if could not be found in database and could not be created using IGDB API
    '''
    # Get game data from IGDB API
    if isinstance(name, int):
        game_data = igdb.get_game_data_by_id(name, fields, exclude)
    else:
        game_data = igdb.get_game_data(name, platform_inst.id if platform_inst is not None else None, year_released, fields, exclude)
    
    # If game search succeeds with given platform AND NOT empty
    if game_data is not None and len(game_data) > 0:
        # Check if game ID already exists in database
        try:
            game_inst = models.Game.objects.get(id=game_data[0]['id'])
        except models.Game.DoesNotExist:
            # TODO: Is this responsible for final value not being correct
            # Make release date (Unix Timestamp) timezone aware
            if 'first_release_date' in game_data[0]:
                # release_date = timezone.make_aware(
                #     datetime.datetime.utcfromtimestamp(game_data[0]['first_release_date']),
                #     timezone=timezone.utc
                # )
                release_date = datetime.datetime.fromtimestamp(
                    game_data[0]['first_release_date'], 
                    timezone.utc
                )
            else:
                release_date = None

            # Platform
            platform_final_inst = None
            if platform_inst is not None:
                for platform in game_data[0]['platforms']:
                    # If platform id from IGDB response matches parameter platform id model
                    if platform_inst.id == platform['id']:
                        platform_final_inst = platform_inst
                        break

                # Save or remove model instances if platform_inst was successful
                if platform_final_inst is None:
                    # Do NOT save platform_inst
                    # Delete ImageIGDB instance in 'logo' field
                    platform_inst.logo.delete()
                else: # Else platform_final_inst is not None
                    # Save platform in case it was created for this game and not yet inside database.
                    # Did NOT save new instance to database until now to confirm game name and platform search succeeded.
                    platform_inst.save()
            
            # If platform_final_inst is still None when reaching this point, use one from the IGDB response
            if platform_final_inst is None and 'release_dates' in game_data[0]:
                # Filter release_dates by region code North America or Worldwide
                region_codes = (2,8)
                filtered_release_dates = [
                    release_date for release_date in game_data[0]['release_dates'] if release_date['region'] in region_codes
                ]

                # If filter leaves empty list, use original unfiltered release dates list
                if not filtered_release_dates:
                    filtered_release_dates = game_data[0]['release_dates']

                # Use platform with release date closest to the 'gamedate' JSON attribute or just year_released parameter
                if (year_released is not None) and (len(filtered_release_dates) > 1):
                    if (type(year_released) == str and '-' not in year_released) or type(year_released) == int:
                        filtered_release_dates.sort(key=lambda release_date: abs(release_date['y'] - int(year_released)))

                # Use first platform from top filtered_release_dates
                if filtered_release_dates:
                    platform = filtered_release_dates[0]['platform']
                    try:
                        platform_final_inst = models.Platform.objects.get(pk=platform['id'])
                    except models.Platform.DoesNotExist:
                        image_igdb_inst = None
                        if 'platform_logo' in platform:
                            try:
                                image_igdb_inst = models.ImageIGDB.objects.get(pk=platform['platform_logo']['id'])
                            except models.ImageIGDB.DoesNotExist:
                                image_igdb_inst = models.ImageIGDB.objects.create(
                                    id=platform['platform_logo']['id'],
                                    image_id=platform['platform_logo']['image_id'],
                                    width=platform['platform_logo']['width'] if 'width' in platform['platform_logo'] else None,
                                    height=platform['platform_logo']['height'] if 'height' in platform['platform_logo'] else None
                                )

                        platform_final_inst = models.Platform.objects.create(
                            id=platform['id'],
                            name=platform['name'],
                            abbreviation=platform['abbreviation'] if 'abbreviation' in platform else '',
                            alternative_name=platform['alternative_name'] if 'alternative_name' in platform else '',
                            logo=image_igdb_inst,
                            slug=platform['slug'],
                            summary=platform['summary'] if 'summary' in platform else '',
                            url=platform['url']
                        )

            # Developer
            developer_inst = None
            if 'involved_companies' in game_data[0]:
                for involved_company in game_data[0]['involved_companies']:
                    if involved_company['developer']:
                        developer = involved_company['company']
                        try:
                            developer_inst = models.Developer.objects.get(pk=developer['id'])
                        except models.Developer.DoesNotExist:
                            try:
                                image_igdb_inst = models.ImageIGDB.objects.get(pk=developer['logo']['id'])
                            except models.ImageIGDB.DoesNotExist:
                                image_igdb_inst = models.ImageIGDB.objects.create(
                                    id=developer['logo']['id'],
                                    image_id=developer['logo']['image_id'],
                                    width=developer['logo']['width'] if 'width' in developer['logo'] else None,
                                    height=developer['logo']['height'] if 'height' in developer['logo'] else None
                                )
                            except KeyError:
                                image_igdb_inst = None

                            developer_inst = models.Developer.objects.create(
                                id=developer['id'],
                                name=developer['name'],
                                country=developer['country'] if 'country' in developer else None,
                                description=developer['description'] if 'description' in developer else '',
                                logo=image_igdb_inst,
                                slug=developer['slug'],
                                url=developer['url']
                            )
                        break

            # Images - Cover
            image_igdb_inst = None
            if 'cover' in game_data[0]:
                cover = game_data[0]['cover']
                try:
                    image_igdb_inst = models.ImageIGDB.objects.get(pk=cover['id'])
                except:
                    image_igdb_inst = models.ImageIGDB.objects.create(
                        id=cover['id'],
                        image_id=cover['image_id'],
                        width=cover['width'] if 'width' in cover else None,
                        height=cover['height'] if 'height' in cover else None
                    )

            game_inst = models.Game.objects.create(
                id=game_data[0]['id'],
                name=game_data[0]['name'],
                slug=game_data[0]['slug'],
                summary=game_data[0]['summary'] if 'summary' in game_data[0] else '',
                storyline=game_data[0]['storyline'] if 'storyline' in game_data[0] else '',
                platform=platform_final_inst,
                developer=developer_inst,
                release_date=release_date,
                cover=image_igdb_inst,
                url=game_data[0]['url'] if 'url' in game_data[0] else None
            )

            # Images - Screenshots
            if 'screenshots' in game_data[0]:
                for screenshot in game_data[0]['screenshots']:
                    # Get or create ImageIGDB inst
                    try:
                        image_igdb_inst = models.ImageIGDB.objects.get(pk=screenshot['id'])
                    except models.ImageIGDB.DoesNotExist:
                        image_igdb_inst = models.ImageIGDB.objects.create(
                            id=screenshot['id'],
                            image_id=screenshot['image_id'],
                            width=screenshot['width'] if 'width' in screenshot else None,
                            height=screenshot['height'] if 'height' in screenshot else None
                        )
                    
                    # Create screenshot inst with ImageIGDB and Game from above
                    models.Screenshot.objects.create(
                        image=image_igdb_inst,
                        game=game_inst
                    )

            # Images - Artworks
            if 'artworks' in game_data[0]:
                for artwork in game_data[0]['artworks']:
                    # Get or create ImageIGDB inst
                    try:
                        image_igdb_inst = models.ImageIGDB.objects.get(pk=artwork['id'])
                    except models.ImageIGDB.DoesNotExist:
                        image_igdb_inst = models.ImageIGDB.objects.create(
                            id=artwork['id'],
                            image_id=artwork['image_id'],
                            width=artwork['width'] if 'width' in artwork else None,
                            height=artwork['height'] if 'height' in artwork else None
                        )

                    # Create artwork inst with ImageIGDB and Game from above
                    models.Artwork.objects.create(
                        image=image_igdb_inst,
                        game=game_inst
                    )

            # Videos
            if 'videos' in game_data[0]:
                for video in game_data[0]['videos']:
                    # Get or create GameVideo inst
                    try:
                        game_video_inst = models.GameVideo.objects.get(pk=video['id'])
                    except models.GameVideo.DoesNotExist:
                        game_video_inst = models.GameVideo.objects.create(
                            id=video['id'],
                            name=video['name'] if 'name' in video else '',
                            video_id=video['video_id'],
                            game=game_inst
                        )

            # Collections/Series
            if 'collection' in game_data[0]:
                collection = game_data[0]['collection']
                # Get or create Collection inst
                try: 
                    collection_inst = models.Collection.objects.get(pk=collection['id'])
                except models.Collection.DoesNotExist:
                    collection_inst = models.Collection(
                        id=collection['id'],
                        name=collection['name'],
                        slug=collection['slug'],
                        url=collection['url'],
                    )

                # Save Collection model in case it was just created
                collection_inst.save()

                # Add game to Collection ManyToManyField
                collection_inst.games.add(game_inst)

            # Franchises
            franchises_all = []
            if 'franchises' in game_data[0]:
                franchises_all = game_data[0]['franchises']
            if 'franchise' in game_data[0]:
                # Check that 'franchise' id NOT already in 'franchises' list
                if not is_franchise_in_list(game_data[0]['franchise'], franchises_all):
                    franchises_all.append(game_data[0]['franchise'])

            for franchise in franchises_all:
                # Get or create Franchise inst
                try: 
                    franchise_inst = models.Franchise.objects.get(pk=franchise['id'])
                except models.Franchise.DoesNotExist:
                    franchise_inst = models.Franchise(
                        id=franchise['id'],
                        name=franchise['name'],
                        slug=franchise['slug'],
                        url=franchise['url'],
                    )

                # Save Franchise model in case it was just created
                franchise_inst.save()

                # Add game to Franchise ManyToManyField
                franchise_inst.games.add(game_inst)

            # Genre is ManyToManyField, use game.genres.add(new_genre)
            if 'genres' in game_data[0]:
                for genre in game_data[0]['genres']:
                    genre_inst = None
                    try:
                        genre_inst = models.Genre.objects.get(pk=genre['id'])
                    except models.Genre.DoesNotExist:
                        genre_inst = models.Genre.objects.create(
                            id=genre['id'],
                            name=genre['name'],
                            slug=genre['slug'],
                            url=genre['url'] if 'url' in genre else None
                        )
                    if genre_inst is not None:
                        game_inst.genres.add(genre_inst)
            
            # Keyword is ManyToManyField, use game.keywords.add(new_keyword)
            if 'keywords' in game_data[0]:
                for keyword in game_data[0]['keywords']:
                    keyword_inst = None
                    try:
                        keyword_inst = models.Keyword.objects.get(pk=keyword['id'])
                    except models.Keyword.DoesNotExist:
                        keyword_inst = models.Keyword.objects.create(
                            id=keyword['id'],
                            name=keyword['name'],
                            slug=keyword['slug'],
                            url=keyword['url'] if 'url' in keyword else None
                        )
                    if keyword_inst is not None:
                        game_inst.keywords.add(keyword_inst)

            # Theme is ManyToManyField, use game.keywords.add(new_keyword)
            if 'themes' in game_data[0]:
                for theme in game_data[0]['themes']:
                    theme_inst = None
                    try:
                        theme_inst = models.Theme.objects.get(pk=theme['id'])
                    except models.Theme.DoesNotExist:
                        theme_inst = models.Theme.objects.create(
                            id=theme['id'],
                            name=theme['name'],
                            slug=theme['slug'],
                            url=theme['url'] if 'url' in theme else None
                        )
                    if theme_inst is not None:
                        game_inst.themes.add(theme_inst)

            # Websites is ManyToManyField
            if 'websites' in game_data[0]:
                for website in game_data[0]['websites']:
                    website_inst = None
                    try:
                        website_inst = models.Website.objects.get(url=website['url'])
                    except models.Website.DoesNotExist:
                        website_inst = models.Website.objects.create(
                            category=website['category'],
                            trusted=website['trusted'],
                            url=website['url']
                        )
                    if website_inst is not None:
                        game_inst.websites.add(website_inst)
        return game_inst
    return None

def get_platform_inst(models, igdb, platform_name):
    '''
    Returns specific instance of Platform model.

    Parameters:
        models (Models): 
        igdb (): 
        platform_name (str|int): String name or IGDB ID of video game platform

    Returns:
        Platform|None: Platform instance matching platform_name or None if not found
    '''
    # Assign platform using platform_name parameter (initialized to None)
    platform = None
    # If platform_name has value
    if platform_name:
        # Check if platform is already in database by string OR number
        if type(platform_name) is str:
            # If platform_name already exists in database as different name fields, assign Platform instance to platform
            try:
                # Regex Pattern using 'NES': r'(^NES,)|(,\sNES,)|(,\sNES$)|(^NES$)'
                platform_alt_name_regex = r'(^' + platform_name + r',)|(,\s' + platform_name + r',)|(,\s' + platform_name + r'$)|(^' + platform_name + r'$)'
                platform = models.Platform.objects.get(
                    Q(abbreviation=platform_name) | Q(alternative_name__regex=platform_alt_name_regex) | Q(name=platform_name)
                )
            # Else platform_name does NOT exist in database
            except models.Platform.DoesNotExist:
                # Adjust name for 'PC' to 'PC Windows' before using IGDB API
                # TODO: Move this to function that cleans JSON file
                if platform_name == 'PC':
                    platform_name += ' Windows'

        elif type(platform_name) is int:
            # If platform_name already exists in database as ID, assign Platform instance to platform
            try:
                platform = models.Platform.objects.get(pk=platform_name)
            # Else platform_name does NOT exist in database
            except models.Platform.DoesNotExist:
                # Leaving platform value as None
                pass

        # If could not find existing platform in database (platform has value of None)
        if platform is None:
            # Use IGDB API to search for platform data
            platform_data = igdb.get_platform_data(platform_name, '*,platform_logo.*')
            
            # If search succeeds AND not empty
            if platform_data is not None and len(platform_data) > 0:
                # If platform id already exists in database, assign Platform instance to platform
                try:
                    platform = models.Platform.objects.get(pk=platform_data[0]['id'])
                # Else create new platform model instance using IGDB platform data and assign it to platform.
                # IMPORTANT: Do NOT save new instance to database until confirm game name and platform search succeeds
                # inside create_game_model()
                except models.Platform.DoesNotExist:
                    image_igdb_inst = None
                    if 'platform_logo' in platform_data[0]:
                        try:
                            image_igdb_inst = models.ImageIGDB.objects.get(pk=platform_data[0]['platform_logo']['id'])
                        except models.ImageIGDB.DoesNotExist:
                            image_igdb_inst = models.ImageIGDB.objects.create(
                                id=platform_data[0]['platform_logo']['id'],
                                image_id=platform_data[0]['platform_logo']['image_id'],
                                width=platform_data[0]['platform_logo']['width'] if 'width' in platform_data[0]['platform_logo'] else None,
                                height=platform_data[0]['platform_logo']['height'] if 'height' in platform_data[0]['platform_logo'] else None
                            )

                    platform = models.Platform()
                    platform.id = platform_data[0]['id']
                    platform.name = platform_data[0]['name']
                    if 'abbreviation' in platform_data[0]:
                        platform.abbreviation = platform_data[0]['abbreviation']
                    if 'alternative_name' in platform_data[0]:
                        platform.alternative_name = platform_data[0]['alternative_name']
                    platform.logo = image_igdb_inst
                    platform.slug = platform_data[0]['slug']
                    if 'summary' in platform_data[0]:
                        platform.summary = platform_data[0]['summary']
                    platform.url = platform_data[0]['url']
            # Else search fails or is empty
                # Must search for game using only name
                # Leave platform value as None so it's not used to search for game using IGDB
    return platform

def get_game_inst(models, igdb, name, platform_name = None, year_released = None):
    ''' 
    Returns specific instance of Game model.

    Parameters:
        models (Models): 
        igdb (IGDB): Reference to IGDB instance to use IGDB API
        name (str): Name of video game
        platform (str|int): Name of platform as string type OR IGDB platform ID as number type (optional)
        year_released (str|int): Year the game was released (optional)

    Returns:
        Game: Existing or created instance of Game model
    '''

    '''
    Pseudo-Code

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
    platform = get_platform_inst(models, igdb, platform_name) if platform_name else None

    # Search IGDB for game based on title AND platform ID
    fields = 'artworks.*,collection.*,cover.*,first_release_date,genres.*,franchise.*,franchises.*,id,involved_companies.*,involved_companies.company.*,involved_companies.company.logo.*,keywords.*,name,platforms.*,platforms.platform_logo.*,release_dates.*,release_dates.platform.*,release_dates.platform.platform_logo.*,screenshots.*,slug,storyline,summary,themes.*,url,videos.*,websites.*'
    exclude = 'collection.games,franchise.games,franchises.games,involved_companies.company.published, involved_companies.company.developed'
    
    # Check alternative names in constant variable GAME_NAME_ALTERNATIVES
    if name in GAME_NAME_ALTERNATIVES:
        name = GAME_NAME_ALTERNATIVES[name]

    # Search for game with name+platform+year_released
    game_inst = create_game_model(models, igdb, name, platform, year_released, fields, exclude)
    # If game search succeeds with name+platform, return the game model instance
    if game_inst is not None:
        return game_inst

    # If no game found, search with name+platform
    if year_released is not None:
        game_inst = create_game_model(models, igdb, name, platform, None, fields, exclude)
        # If game search succeeds with name+platform, return the game model instance
        if game_inst is not None:
            return game_inst

    # If no game found, search with only name
    if platform is not None:
        game_inst = create_game_model(models, igdb, name, None, None, fields, exclude)
        # If game search succeeds with name only, return the game model instance
        if game_inst is not None:
            return game_inst

    # If no game found with only name, check if system in parentheses at end of name
    match = re.fullmatch(r'(.+) \((\w+)\)', name)
    if match:
        # Name: match.group(1)
        # Platform: match.group(2)
        # Note: exclude 'demo' in parentheses since 'demo' platform search would return PS2
        platform = get_platform_inst(models, igdb, match.group(2)) if match.group(2) not in ('demo','JPN', 'The High Road level') else None
        game_inst = create_game_model(models, igdb, match.group(1), platform, None, fields, exclude)
        # If game search succeeds with name+platform, return the game model instance
        if game_inst is not None:
            return game_inst

    # No game found if reach this point
    print(f'Get Game Inst: Could not find game!: Name: {name} - Platform: {platform_name} - Year: {year_released}')
    return None

    # # If platform has value, search for game with both name+platform+year_released
    # if platform is not None:
    #     game_inst = create_game_model(models, igdb, name, platform, year_released, fields, exclude)
    #     # If game search succeeds with name+platform, return the game model instance
    #     if game_inst is not None:
    #         return game_inst
    #     print(f'Game Game Inst: Could not find game with 3 args!: Name: {name} - Platform: {platform_name} - Year: {year_released}')

    # # If platform has value but reaches this point, could not find game with name+platform.
    # # Attempt search with just the name of the video game
    # game_inst = create_game_model(models, igdb, name, None, year_released, fields, exclude)
    # # If game search succeeds with no platform, return the game model instance
    # if game_inst is not None:
    #     return game_inst
    # # Else game search fails with no platform
    # print(f'Get Game Inst: Could not find game with 2 args!: Name: {name} - Year: {year_released}')

    # # Reach here when neither name+platform nor just name has successful game search.    
    # # If reach here, could not find game
    # return None

def get_person_inst(models, person_data):
    '''
    Get existing Person model from database or add a new model instance if not in database.

    Parameters:
        models (Models): 
        person_data (dict): Dictionary of data about specific person
        person_data.name (str): Name of person

    Returns:
        (Person): Matching Person model already existing in database or created and added to the database
    '''
    '''
    info_box_details
        company
        position
        years
        twitter
        website
        ...
    '''
    try:
        return models.Person.objects.get(full_name=person_data['name'])
    except models.Person.DoesNotExist:
        try:
            thumbnail_inst = models.Thumbnail.objects.get(url=person_data['image']['srcset'][0])
        except KeyError:
            thumbnail_inst = None
        except models.Thumbnail.DoesNotExist:
            thumbnail_inst = models.Thumbnail.objects.create(
                url=person_data['image']['srcset'][0],
                width=int(person_data['image']['width']),
                height=int(person_data['image']['height'])
            )

        person = models.Person.objects.create(
            full_name=person_data['name'],
            slug=slugify(person_data['name']),
            thumbnail=thumbnail_inst,
            description='\n\n'.join(person_data['description']) if 'description' in person_data else '',
            headings=person_data['headings'] if 'headings' in person_data else None,
            infobox_details=person_data['info_box_details'] if 'info_box_details' in person_data else None
        )
        # TODO: If person is part of staff, create Staff model as well.
        if person_data['name'] in STAFF:
            models.Staff.objects.create(person=person)
        return person

def get_segment_inst(models, platform, igdb, segmentType, segmentContent):
    '''
    Creates instance of Segment model, saves to database, and returns.

    Parameter:
        segmentType (str): Name or abbreviation of segment type.
        segmentContent ([str]): List of game names or segment description.

    Returns:
        Segment
    '''
    segment = models.Segment()
    segment_manytomany_instances_dict = {
        'games': []
    }

    segmentTypeInst = None
    for segmentTitle, segment_abbreviation, gameTextID, segment_content_dict in SEGMENT_TYPES:
        if segmentType in (segment_abbreviation, segmentTitle):
            try:
                segmentTypeInst = models.SegmentType.objects.get(
                    Q(abbreviation=segmentType) | Q(title=segmentType)
                )
            except models.SegmentType.DoesNotExist:
                segmentTypeInst = models.SegmentType.objects.create(
                    title=segmentTitle,
                    abbreviation=segment_abbreviation if segment_abbreviation is not None else '',
                    slug=slugify(segmentTitle),
                    description='\n\n'.join(segment_content_dict['description']) if 'description' in segment_content_dict else ''
                )

            # Game/Text ID: 0-game 1-text 2-game/text

            if gameTextID == 0: # game
                for game in segmentContent:
                    # Add content to 'games', leaving 'description' empty
                    # Account for advertisements
                    game_title = game.rpartition(' Ad')[0] if game.endswith('Ad') else game
                    # Get game using title and platform from main_segment_games
                    game_inst = get_game_inst(
                        models=models,
                        igdb=igdb, 
                        name=game_title, 
                        platform_name=platform, 
                        year_released=None
                    )
                    if game_inst is not None:
                        segment_manytomany_instances_dict['games'].append(game_inst)
                    else:
                        print(f'Get Segment Inst: Could not find game in segment type 0!: Name: {game_title} - Platform: {platform}')

            elif gameTextID == 1: # text
                # Add content to 'description' leaving 'games' empty
                segment.description = ', '.join(segmentContent)

            elif gameTextID == 2: # game/text
                # Special Cases: Moments and Developer Spotlight
                if segmentType == 'Moments':
                    if segmentContent[0] == 'Syphone Filter\'s Cutscenes':
                        # Add game
                        # Get game using title and platform from main_segment_games
                        game_inst = get_game_inst(
                            models=models,
                            igdb=igdb, 
                            name='Syphone Filter',
                            platform_name=platform, 
                            year_released=None
                        )
                        if game_inst is not None:
                            #segment.games.add(game_inst)
                            segment_manytomany_instances_dict['games'].append(game_inst)
                        else:
                            print(f'Get Segment Inst: Could not find game in segment type 2!: Name: Syphone Filter - Platform: {platform}')
                        # Add description
                        segment.description = segmentContent[0]
                elif segmentType == 'Developer Spotlight':
                    for index, game in enumerate(segmentContent):
                        if index == 0:
                            # First index of game list example: Rare Games: Slalom
                            title_split = game.split(': ', 1)
                            # Get game using title_split[1] and platform from main_segment_games
                            game_inst = get_game_inst(
                                models=models,
                                igdb=igdb, 
                                name=title_split[1], 
                                platform_name=platform, 
                                year_released=None
                            )
                            if game_inst is not None:
                                #segment.games.add(game_inst)
                                segment_manytomany_instances_dict['games'].append(game_inst)
                            else:
                                print(f'Get Segment Inst: Could not find game in segment type 2!: Name: {title_split[1]} - Platform: {platform}')
                            # Add description from title_split[0]
                            segment.description = title_split[0]
                        else:
                            # Add game
                            # Get game using title and platform from main_segment_games
                            game_inst = get_game_inst(
                                models=models,
                                igdb=igdb, 
                                name=game, 
                                platform_name=platform, 
                                year_released=None
                            )
                            if game_inst is not None:
                                #segment.games.add(game_inst)
                                segment_manytomany_instances_dict['games'].append(game_inst)
                            else:
                                print(f'Get Segment Inst: Could not find game in segment type 2!: Name: {game} - Platform: {platform}')
            # Break loop to find matching segment type in SEGMENT_TYPES
            break
    # If segmentTypeInst is still none, unknown segment type.
    # Use value as segment title, leaving abbreviation blank.
    if segmentTypeInst is None:
        # If segmentType is empty string, assign to 'Other'
        if segmentType == '':
            segmentType = 'Other'
        try:
            segmentTypeInst = models.SegmentType.objects.get(title=segmentType)
        except models.SegmentType.DoesNotExist:
            segmentTypeInst = models.SegmentType.objects.create(title=segmentType, slug=slugify(segmentType))

        # Add description
        segment.description = ', '.join(segmentContent)

    # Set type field in segment model instance
    segment.type = segmentTypeInst

    # Save to database
    segment.save()

    # Now that segment is saved to database, add ManyToManyFields
    for game in segment_manytomany_instances_dict['games']:
        game.save()
        segment.games.add(game)

    return segment

def add_model_inst_list_to_field(m2m_field, model_inst_list):
    '''
    Adds list of model instances to ManyToManyField.

    Parameters:
        m2m_field (ManyToManyField):
        model_inst_list (Model[]):
    '''
    for model_inst in model_inst_list:
        model_inst.save()
        m2m_field.add(model_inst)

def createReplayEpisodeFromJSON(replayData, models):
    '''
    Converts dictionary of key/value pairs into defined models inside database for data migration.

    Parameters:
        replayData (dict):
        models (Models):
    '''

    # IGDB instance initialization creates API access_token
    igdb = IGDB()

    # Create Replay episode object
    replay = models.ReplayEpisode()

    # Dictionary to hold model instances for ManyToManyFields.
    # Key is field name and value is list of model instances.
    # After other fields in Replay instance are set and it's saved to database,
    # can then add to the actual ManyToManyFields.
    replay_manytomany_instances_dict = {
        'featuring': [],
        'external_links': [],
        'main_segment_games': [],
        'other_segments': [],
    }

    # ---------- Episode ----------

    # Title - replayData.episodeTitle
    replay.title = replayData['episodeTitle']

    # Slug - convert 'title' field
    replay.slug = slugify(re.sub(r'Replay:\s?', '', replay.title, 1, re.IGNORECASE))
    
    # Runtime - replayData.details.runtime AND replayData.videoLength
    if 'details' in replayData and 'runtime' in replayData['details']:
        replay.runtime = replayData['details']['runtime']
    elif 'videoLength' in replayData and replayData['videoLength']:
        replay.runtime = replayData['videoLength']

    # Airdate - replayData.airDate AND replayData.details.airdate
    if 'airdate' in replayData and replayData['airDate']:
        replay.airdate = timezone.make_aware(
            datetime.datetime.strptime(replayData['airDate'],'%m/%d/%y'), # month/day/year
            timezone=timezone.get_current_timezone()
        )
    elif 'details' in replayData and 'airdate' in replayData['details'] and replayData['details']['airdate']:
        replay.airdate = timezone.make_aware(
            datetime.datetime.strptime(replayData['details']['airdate'], '%B %d, %Y'), # month day, year
            timezone=timezone.get_current_timezone()
        )

    # Host/Featuring/Guests inside 'details'
    if 'details' in replayData:
        # Host - replayData.details.host (ForeignKey)
        if 'host' in replayData['details'] and replayData['details']['host']:
            replay.host = get_person_inst(models, {'name': replayData['details']['host'][0]})

        # Featuring - replayData.details.featuring (ManyToMany)
        if 'featuring' in replayData['details'] and replayData['details']['featuring']:
            for personName in replayData['details']['featuring']:
                person = get_person_inst(models, {'name': personName})
                replay_manytomany_instances_dict['featuring'].append(person)

    # YouTube Video - replayData.youtube (OneToOne)
    if 'youtube' in replayData and 'views' in replayData['youtube']:
        youtubeVideo = models.YouTubeVideo()

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
                thumbnail = models.Thumbnail.objects.get(url=value['url'])
            except models.Thumbnail.DoesNotExist:
                thumbnail = models.Thumbnail.objects.create(
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
                # if 'youtube.com' in link['href']:
                #     continue
                externalLink = models.ExternalLink.objects.create(
                    url=link['href'],
                    title=link['title']
                )
                replay_manytomany_instances_dict['external_links'].append(externalLink)
            
            # Fandom Link - replayData.fandomWikiURL (ManyToMany)
            if 'fandomWikiURL' in replayData and replayData['fandomWikiURL']:
                externalLink = models.ExternalLink.objects.create(
                    url=f'https://replay.fandom.com{replayData["fandomWikiURL"]}',
                    title=replay.title
                )
                replay_manytomany_instances_dict['external_links'].append(externalLink)

        # Headings - replayData.details
        HEADINGS_TO_IGNORE = ('external_links', 'system', 'gamedate', 'airdate', 'runtime', 'host', 'featuring', 'image')
        headingsJSON = {}
        for key, value in replayData['details'].items():
            if key in HEADINGS_TO_IGNORE or not value:
                continue
            headingsJSON[key] = value
        replay.headings = headingsJSON

    # ---------- Replay Episode ----------
    
    # Number - replayData.episodeNumber
    if 'episodeNumber' in replayData and replayData['episodeNumber']:
        # Check for unofficial episodes (number is str and between 0 exclusive to 1 exclusive)
        # 0.01 to 0.14 converted to -1 to -14
        episode_number = replayData['episodeNumber']
        if type(episode_number) is str:
            episode_number = -int(float(episode_number) * 100)
        replay.number = episode_number

        # Season - calculate using replayData.episodeNumber (ForeignKey)
        season = get_season(replay)[0]
        try:
            replay.season = models.ReplaySeason.objects.get(pk=season)
        except models.ReplaySeason.DoesNotExist:
            replay.season = models.ReplaySeason.objects.create(
                number=get_season(replay)[0]
            )
    
    # Main Segment Games - replayData.mainSegmentGamesAdv, replayData.details.system, replayData.details.gamedate (ManyToMany)
    if 'mainSegmentGamesAdv' in replayData:
        # Save ReplayEpisode before adding Games through Many-to-Many relationship
        #replay.save()

        for game in replayData['mainSegmentGamesAdv']:
            # Game - Name
            game_name = game['title']

            # Game - Year Released
            game_year_released = game['yearReleased']

            # Game - Platform
            platform_name = game['system']

            game_inst = get_game_inst(
                models,
                igdb=igdb, 
                name=game_name, 
                platform_name=platform_name, 
                year_released=game_year_released
            )
            if game_inst is not None:
                #replay.main_segment_games.add(game_inst)
                replay_manytomany_instances_dict['main_segment_games'].append(game_inst)
    
    # Use most played platform from main_segment_games field to search for games in other segments
    # TODO: Why not search all platforms?
    platform = None # Platform string OR number of IGDB platform code
    if replay_manytomany_instances_dict['main_segment_games']:
        platform_count = {} # key: IGDB platform ID, value: number of games with this platform in main_segment_games
        for game in replay_manytomany_instances_dict['main_segment_games']:
            if game.platform is None:
                continue
            if game.platform.id in platform_count:
                platform_count[game.platform.id] += 1
            else:
                platform_count[game.platform.id] = 1
        # Use platform id with highest count
        max_count = 0
        for id, count in platform_count.items():
            if count > max_count:
                max_count = count
                platform = int(id)
    # try:
    #     platform = Platform.objects.get(pk=platform_key)
    # except Platform.DoesNotExist:
    #     platform = None

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
            replay_manytomany_instances_dict['other_segments'].append(
                get_segment_inst(
                    models,
                    platform, 
                    igdb, 
                    segmentType, 
                    [segmentContent] # Add content to list
                )
            )

    # replayData.secondSegment, replayData.secondSegmentGames
    if 'secondSegment' in replayData:
        segmentType = replayData['secondSegment']
        segmentContent = replayData['secondSegmentGames']

        if segmentContent:
            replay_manytomany_instances_dict['other_segments'].append(
                get_segment_inst(
                    models,
                    platform, 
                    igdb, 
                    segmentType, 
                    segmentContent # Assuming content is list
                )
            )
    
    # Article - replayData.article  (OneToOne)
    if 'article' in replayData:
        article = models.Article()

        # Title - replayData.article.title
        article.title = replayData['article']['title']

        # Author - replayData.article.author
        # TODO: Add Staff to author field
        article.author = get_person_inst(models, {'name': replayData['article']['author']})

        # Datetime - replayData.article.date
        # " on Sep 26, 2015 at 03:00 AM"
        article.datetime = timezone.make_aware(
            datetime.datetime.strptime(replayData['article']['date'], ' on %b %d, %Y at %I:%M %p'),
            timezone=timezone.get_current_timezone()
        )

        # Content - replayData.article.content
        article.content = '\n\n'.join(replayData['article']['content'])

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

    # Now that Replay is saved to database, add ManyToManyFields
    add_model_inst_list_to_field(replay.featuring, replay_manytomany_instances_dict['featuring'])
    add_model_inst_list_to_field(replay.external_links, replay_manytomany_instances_dict['external_links'])
    add_model_inst_list_to_field(replay.main_segment_games, replay_manytomany_instances_dict['main_segment_games'])
    add_model_inst_list_to_field(replay.other_segments, replay_manytomany_instances_dict['other_segments'])

def database_init(apps):
    '''
    Initializes database with known data.

    Parameters:
        apps (): 
    '''
    # Create Segment models
    SegmentType = apps.get_model('replay', 'SegmentType')
    for title, abbreviation, gameTextID, segment_content_dict in SEGMENT_TYPES.items():
        SegmentType.objects.create(
            title=title, 
            abbreviation=abbreviation if abbreviation is not None else '', 
            slug=slugify(title),
            description=segment_content_dict['description'] if 'description' in segment_content_dict else ''
        )

    # Create Person and Staff models

def create_person_from_json(person_data, models):
    '''
    Converts dictionary of key/value pairs of Game Informer staff/guest into defined models inside database for data migration.

    Parameters:
        person_data (dict):
        models (Models):
    '''

    get_person_inst(models, person_data)

def initialize_people_database(models):
    '''
    Adds models to database for Game Informer staff/guests from JSON file.

    Parameters:
        models (Models): Models instance holding historic versions of each model

    '''
    with open('utilities/gi_people.json', 'r', encoding='utf-8') as data_file:

        # Get all people data
        people_data = json.load(data_file)

        # Return if no data
        if not people_data: return

        total_count = len(people_data)
        curr_count = 0
        start_time = time.time()

        for person_data in reversed(people_data):
            create_person_from_json(person_data, models)

            curr_count += 1

            avg_seconds_per_item = (time.time() - start_time) / curr_count
            est_seconds_remaining = math.floor(avg_seconds_per_item * (total_count - curr_count))

            print(f'Person: {person_data["name"]} - {curr_count}/{total_count} Completed! - Est. Time Remaining: {create_total_time_message(est_seconds_remaining)}')

def initialize_database(apps, schema_editor):
    models = Models(apps)

    initialize_people_database(models)

    with open('utilities/replay_data.json', 'r', encoding='utf-8') as dataFile:

        # Get Replay episode data
        allReplayData = json.load(dataFile)

        # If there is Replay data
        if (allReplayData):
            total_replay_count = len(allReplayData)
            curr_replay_count = 0
            start_time = time.time()
            for replayData in reversed(allReplayData):
                createReplayEpisodeFromJSON(replayData, models)

                curr_replay_count += 1
                avg_seconds_per_replay = (time.time() - start_time) / curr_replay_count
                est_seconds_remaining = math.floor(avg_seconds_per_replay * (total_replay_count - curr_replay_count))

                print(f'Replay #{replayData["episodeNumber"]} - {curr_replay_count}/{total_replay_count} Completed! - Est. Time Remaining: {create_total_time_message(est_seconds_remaining)}')

            # Use YouTube Data API to update all YouTubeVideo models.
            # Can batch video IDs into single request rather than doing them 
            # individually when YouTubeVideo model is first created.

        #createReplayEpisodeFromJSON(allReplayData[0], apps)

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

def main():
    print(f'SEGMENT_TYPES length: {len(SEGMENT_TYPES)}')
    igdb_inst = IGDB()
    #igdb_inst.get_platform_data('PlayStation 2', '*,platform_logo.*')
    igdb_inst.get_game_data('Metal Gear Solid 2', platform = 'PS2', year_released = None, fields='cover.*,first_release_date,genres.*,id,involved_companies.*,involved_companies.company.*,involved_companies.company.logo.*,name,platforms.*,platforms.platform_logo.*,release_dates.*,screenshots,slug,storyline,summary,url;')

if __name__ == '__main__':
    main()

'''
from django.db import migrations
from utilities.data_migration import initialize_database

class Migration(migrations.Migration):

    dependencies = [
        ('fansite', '0001_initial'),
        # added dependencies to enable models from other apps to be available initialize_database method
        ('games', '0001_initial'),
        ('people', '0001_initial'),
        ('replay', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(initialize_database),
    ]

# Create PostgreSQL extensions using migration

from django.db import migrations
from django.contrib.postgres.operations import TrigramExtension, UnaccentExtension

class Migration(migrations.Migration):

    dependencies = [
        ('fansite', '0001_initial'),
        ('games', '0001_initial'),
        ('people', '0001_initial'),
        ('replay', '0001_initial'),
    ]

    operations = [
        TrigramExtension(),
        UnaccentExtension(),
    ]
'''