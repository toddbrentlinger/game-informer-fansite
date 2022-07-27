import json
import datetime
import time
import pprint # Used to debug
import math
import re
from django.db.models import Q
from django.utils import timezone
from utilities.igdb import IGDB # Make requests from IGDB API
from utilities.data_migration import Models
from utilities.misc import create_total_time_message # misc utility functions
from utilities.data_migration import get_game_inst, get_person_inst, add_model_inst_list_to_field

def createSuperReplayEpisodeFromJSON(superReplayEpisodeData, superReplayInst, episode_num, models, igdb):
    '''
    Converts dictionary of key/value pairs into defined models inside database for data migration.

    Parameters:
        superReplayEpisodeData (dict):
        superReplayInst (SuperReplay): 
        episode_num (int): 
        models (Models): 
        igdb (IGDB): 
    '''
    # Create Super Replay Episode object
    superreplayepisode = models.SuperReplayEpisode()

    # Dictionary to hold model instances for ManyToManyFields.
    # Key is field name and value is list of model instances.
    # After other fields in Super Replay Episode instance are set and it's saved to database,
    # can then add to the actual ManyToManyFields.
    manytomany_instances_dict = {
        'featuring': [],
        'external_links': [],
    }

    # Super Replay
    superreplayepisode.super_replay = superReplayInst

    # Number
    superreplayepisode.episode_number = episode_num

    # Airdate

    # Runtime

    # Host

    # Featuring

    # External Links

    # Headlines/Description

    # YouTube Video 

def createSuperReplayFromJSON(superReplayData, models, igdb):
    '''
    Converts dictionary of key/value pairs into defined models inside database for data migration.

    Parameters:
        superReplayData (dict):
        models (Models):
        igdb (IGDB): 
    '''

    # Create Super Replay object
    superreplay = models.SuperReplay()

    # Dictionary to hold model instances for ManyToManyFields.
    # Key is field name and value is list of model instances.
    # After other fields in Super Replay instance are set and it's saved to database,
    # can then add to the actual ManyToManyFields.
    superreplay_manytomany_instances_dict = {
        'external_links': [],
    }

    # Title
    superreplay.title = superReplayData['title']

    # Number
    superreplay.number = superReplayData['number']

    # Content - Description
    # Content - External Links
    if 'content' in superReplayData:
        # External Links - superReplayData.content.external_links (ManyToMany)
        if 'external_links' in superReplayData['content'] and superReplayData['content']['external_links']:
            for link in superReplayData['content']['external_links']:
                external_link = models.ExternalLink.objects.create(
                    url=link['href'],
                    title=link['title']
                )
                superreplay_manytomany_instances_dict['external_links'].append(external_link)

        # Headings - replayData.details
        HEADINGS_TO_IGNORE = ('external_links',)
        headingsJSON = {}
        for key, value in superReplayData['content'].items():
            if key in HEADINGS_TO_IGNORE or not value:
                continue
            headingsJSON[key] = value
        superreplay.headings = headingsJSON

    # Article
    if 'gameInformerArticle' in superReplayData:
        article = models.Article()
        article_data = superReplayData['gameInformerArticle']

        # URL
        article.url = f"https://www.gameinformer.com{article_data['url']}"

        # Title
        article.title = article_data['title']

        # Author
        article.author = get_person_inst(models, { 'name': article_data['author']})

        # Date
        article.datetime = timezone.make_aware(
            datetime.datetime.strptime(article['date'], ' on %b %d, %Y at %I:%M %p'),
            timezone=timezone.get_current_timezone()
        )

        # Content HTML
        article.content = article['contentHTML']

    # Image
    # Thumbnails

    # Save SuperReplay instance before using to as a field for other models
    superreplay.save()

    # Now that Super Replay is saved to database, add ManyToManyFields
    add_model_inst_list_to_field(superreplay.external_links, superreplay_manytomany_instances_dict['external_links'])

    # Episode List
    if 'episodeList' in superReplayData:
        for num, super_replay_episode_data in enumerate(superReplayData['episodeList'], start=1):
            createSuperReplayEpisodeFromJSON(super_replay_episode_data, superreplay, num, models, igdb)

    # Games
    for game in superReplayData['games']:

        # Game Year Released
        year_released_match = re.fullmatch(r'.+,\s(\d+)', game['releaseDate'])
        if year_released_match:
            year_released = year_released_match.group(1)
        else:
            year_released = None

        game_inst = get_game_inst(
            models,
            igdb=igdb,
            name=game['title'],
            platform_name=game['system'],
            year_released=year_released,
        )

        if game_inst is not None:
            # Create SuperReplayGame instance
            super_replay_game_inst = models.SuperReplayGame.objects.create(
                game=game_inst,
                super_replay=superreplay
            )

def initialize_database(apps, schema_editor):
    models = Models(apps)

    with open('utilities/super_replay_data.json', 'r', encoding='utf-8') as outfile:

        # Get Replay episode data
        allSuperReplayData = json.load(outfile)

        # If there is Replay data
        if (allSuperReplayData):
            total_count = len(allSuperReplayData)
            curr_count = 0
            start_time = time.time()

            # IGDB instance initialization creates API access_token
            igdb = IGDB()

            for superReplayData in reversed(allSuperReplayData):
                createSuperReplayFromJSON(superReplayData, models, igdb)

                curr_count += 1
                avg_seconds_per_replay = (time.time() - start_time) / curr_count
                est_seconds_remaining = math.floor(avg_seconds_per_replay * (total_count - curr_count))

                print(f'Super Replay #{superReplayData["number"]} - {curr_count}/{total_count} Completed! - Est. Time Remaining: {create_total_time_message(est_seconds_remaining)}')

def main():
    pass

if __name__ == '__main__':
    main()