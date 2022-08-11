import json
import datetime
import time
import pprint # Used to debug
import math
import re
from django.db.models import Q
from django.utils import timezone
from django.template.defaultfilters import slugify
from utilities.igdb import IGDB # Make requests to IGDB API
from utilities.youtube import YouTube # Make requests to YouTube Data API
from utilities.misc import create_total_time_message # misc utility functions
from utilities.replay_data_migration import Models, get_or_create_youtube_video, get_game_inst, get_person_inst, add_model_inst_list_to_field

def createSuperReplayEpisodeFromJSON(models, superReplayEpisodeData, superReplayInst, episode_num, show_inst, igdb, youtube):
    '''
    Converts dictionary of key/value pairs into defined models inside database for data migration.

    Parameters:
        models (Models): 
        superReplayEpisodeData (dict):
        superReplayInst (SuperReplay): 
        episode_num (int): 
        show_inst (Show): 
        igdb (IGDB): 
        youtube (YouTube): 
    '''
    # Create Super Replay Episode object
    superreplayepisode = models.SuperReplayEpisode()

    # Dictionary to hold model instances for ManyToManyFields.
    # Key is field name and value is list of model instances.
    # After other fields in Super Replay Episode instance are set and it's saved to database,
    # can then add to the actual ManyToManyFields.
    manytomany_instances_dict = {
        'shows': [],
        'featuring': [],
        'external_links': [],
    }

    # Add Show instance
    # superreplayepisode.show = show_inst
    manytomany_instances_dict['shows'].append(show_inst)

    # Super Replay
    superreplayepisode.super_replay = superReplayInst

    # Number
    superreplayepisode.episode_number = episode_num

    # Airdate
    if 'airdate' in superReplayEpisodeData and superReplayEpisodeData['airdate']:
        if '/' in superReplayEpisodeData['airdate']:
            airdate = datetime.datetime.strptime(superReplayEpisodeData['airdate'],'%m/%d/%y') # month/day/year
        else:
            airdate = datetime.datetime.strptime(superReplayEpisodeData['airdate'],'%B %d, %Y') # month day, year
        
        superreplayepisode.airdate = timezone.make_aware(
            airdate,
            timezone=timezone.get_current_timezone()
        )

    # Runtime
    if 'runtime' in superReplayEpisodeData and superReplayEpisodeData['runtime']:
        superreplayepisode.runtime = superReplayEpisodeData['runtime']

    # Host (ForeignKey)
    if 'host' in superReplayEpisodeData and superReplayEpisodeData['host']:
        superreplayepisode.host = get_person_inst(models, {'name': superReplayEpisodeData['host'][0]})

    # Featuring (ManyToMany)
    if 'featuring' in superReplayEpisodeData and superReplayEpisodeData['featuring']:
        for personName in superReplayEpisodeData['featuring']:
            person = get_person_inst(models, {'name': personName})
            manytomany_instances_dict['featuring'].append(person)

    # External Links
    if 'external_links' in superReplayEpisodeData and superReplayEpisodeData['externalLinks']:
        for link in superReplayEpisodeData['externalLinks']:
            external_link = models.ExternalLink.objects.create(
                url=link['href'],
                title=link['title']
            )
            manytomany_instances_dict['external_links'].append(external_link)

    # Headlines/Description
    headings = {}
    if 'description' in superReplayEpisodeData and superReplayEpisodeData['description']:
        headings['description'] = superReplayEpisodeData['description']
    if 'headlines' in superReplayEpisodeData:
        for key, value in superReplayEpisodeData['headlines'].items():
            headings[key] = value
    superreplayepisode.headings = headings

    # YouTube Video
    if 'youtubeVideo' in superReplayEpisodeData:
        youtube_video_data = superReplayEpisodeData['youtubeVideo']

        youtube_video_inst = get_or_create_youtube_video(models, youtube_video_data['id'], youtube)

        if youtube_video_inst is None:
            # Create YouTubeVideo instance
            youtube_video_inst = models.YouTubeVideo()

            # YouTube Video ID
            youtube_video_inst.youtube_id = youtube_video_data['id']

            # Title
            youtube_video_inst.title = youtube_video_data['title']

            # Views
            youtube_video_inst.views = youtube_video_data['views']

            # Likes
            youtube_video_inst.likes = youtube_video_data['likes']

            # Dislikes
            youtube_video_inst.dislikes = youtube_video_data['dislikes']

            # Description
            youtube_video_inst.description = youtube_video_data['description']

            # Duration
            youtube_video_inst.duration = youtube_video_data['runtime']

            # Published At
            youtube_video_inst.published_at = timezone.make_aware(
                datetime.datetime.strptime(youtube_video_data['airdate'],'%B %d, %Y'), # month day, year
                timezone=timezone.get_current_timezone()
            )

            # Tags
            if 'tags' in youtube_video_data and youtube_video_data['tags']:
                youtube_video_inst.tags = youtube_video_data['tags']

            # Save YouTubeVideo instance before adding ManyToManyFields
            youtube_video_inst.save()

            # Thumbnails
            for key, value in youtube_video_data['thumbnails'].items():
                try:
                    thumbnail = models.Thumbnail.objects.get(url=value['url'])
                except models.Thumbnail.DoesNotExist:
                    thumbnail = models.Thumbnail.objects.create(
                        quality=key.upper(),
                        url=value['url'],
                        width=value['width'],
                        height=value['height']
                    )
                youtube_video_inst.thumbnails.add(thumbnail)

        # Add YouTubeVideo to SuperReplayEpisode
        superreplayepisode.youtube_video = youtube_video_inst

        # Save SuperReplayEpisode instance to database
        superreplayepisode.save()

        # Now that SuperReplayEpisode is saved to database, add ManyToManyFields
        add_model_inst_list_to_field(superreplayepisode.shows, manytomany_instances_dict['shows'])
        add_model_inst_list_to_field(superreplayepisode.featuring, manytomany_instances_dict['featuring'])
        add_model_inst_list_to_field(superreplayepisode.external_links, manytomany_instances_dict['external_links'])

def createSuperReplayFromJSON(models, superReplayData, show_inst, igdb, youtube):
    '''
    Converts dictionary of key/value pairs into defined models inside database for data migration.

    Parameters:
        models (Models):
        superReplayData (dict):
        show_inst (Show): 
        igdb (IGDB): 
        youtube (YouTube): 
    '''

    # Create Super Replay object
    superreplay = models.SuperReplay()

    # Dictionary to hold model instances for ManyToManyFields.
    # Key is field name and value is list of model instances.
    # After other fields in Super Replay instance are set and it's saved to database,
    # can then add to the actual ManyToManyFields.
    manytomany_instances_dict = {
        'external_links': [],
    }

    # Title
    superreplay.title = superReplayData['title']

    # Slug - convert 'title' field
    superreplay.slug = slugify(re.sub(r'Super Replay:\s?', '', superreplay.title, 1, re.IGNORECASE))

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
                manytomany_instances_dict['external_links'].append(external_link)

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
            datetime.datetime.strptime(article_data['date'], ' on %b %d, %Y at %I:%M %p'),
            timezone=timezone.get_current_timezone()
        )

        # Content HTML
        article.content = article_data['contentHTML']

    # Image
    # Thumbnails

    # Save SuperReplay instance before using to as a field for other models
    superreplay.save()

    # Now that Super Replay is saved to database, add ManyToManyFields
    add_model_inst_list_to_field(superreplay.external_links, manytomany_instances_dict['external_links'])

    # Episode List
    if 'episodeList' in superReplayData:
        for num, super_replay_episode_data in enumerate(superReplayData['episodeList'], start=1):
            createSuperReplayEpisodeFromJSON(models, super_replay_episode_data, superreplay, num, show_inst, igdb, youtube)

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

            # YouTube Data API instance
            youtube = YouTube()

            # Super Replay Show instance
            try:
                show_inst = models.Show.objects.get(name='Super Replay')
            except models.Show.DoesNotExist:
                show_inst = models.Show.objects.create(
                    name='Super Replay',
                    slug='super-replay'
                )

            for superReplayData in reversed(allSuperReplayData):
                createSuperReplayFromJSON(models, superReplayData, show_inst, igdb, youtube)

                curr_count += 1
                avg_seconds_per_replay = (time.time() - start_time) / curr_count
                est_seconds_remaining = math.floor(avg_seconds_per_replay * (total_count - curr_count))

                print(f'Super Replay #{superReplayData["number"]} - {curr_count}/{total_count} Completed! - Est. Time Remaining: {create_total_time_message(est_seconds_remaining)}')

def main():
    pass

if __name__ == '__main__':
    main()