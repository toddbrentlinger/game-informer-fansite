import json
import datetime
import time
import math
import re

from django.template.defaultfilters import slugify
from django.utils import timezone

from utilities.data_migration_constants import SHOWS, STAFF
from utilities.replay_data_migration import Models, create_total_time_message, add_model_inst_list_to_field, get_person_inst
from utilities.igdb import IGDB # Make requests to IGDB API
from utilities.youtube import YouTube # Make requests to YouTube Data API

# TODO:
# - Search tags to find different Show instances to add to 'shows' field
# - Move imports from replay_data_migration into this file instead

def slugify_unique(model, title):
    slug_title = slugify(title)

    while model.objects.filter(slug=slug_title).count():
        # Add incremented number after two dashes to end
        slug_title_match = re.fullmatch(r'(.+)--(\d)$', slug_title, re.IGNORECASE)

        # If matching slug title increment number already present
        if slug_title_match:
            slug_title = f'{slug_title_match.group(1)}--{int(slug_title_match.group(2)) + 1}'
        else: # Else NO matching slug title increment number already present
            slug_title += '--1'

    return slug_title

def create_episode(models, episode_data):
    '''
    Converts dictionary of key/value pairs into defined models inside database for data migration.

    Parameters:
        models (Models): 
        episode_data (dict):
    '''
    # Check if Episode already exists with matching YouTubeVideo ID.
    try:
        youtube_id = episode_data['id']
        episode = models.Episode.objects.get(
            youtube_video__youtube_id=youtube_id
        )
    except models.Episode.DoesNotExist:
        # Create Episode object
        episode = models.Episode()

        # Dictionary to hold model instances for ManyToManyFields.
        # Key is field name and value is list of model instances.
        # After other fields in Episode instance are set and it's saved to database,
        # can then add to the actual ManyToManyFields.
        manytomany_instances_dict = {
            'featuring': [],
            'external_links': [],
        }

        # Title - snippet.title
        episode.title = episode_data['snippet']['title']

        # Slug
        episode.slug = slugify_unique(models.Episode, episode.title)

        # YouTube Video
        try:
            youtube_video_inst = models.YouTubeVideo.objects.get(youtube_id=episode_data['id'])
        except models.YouTubeVideo.DoesNotExist:
            youtube_video_inst = models.YouTubeVideo()

            # YouTube ID
            youtube_video_inst.youtube_id = youtube_id

            if 'contentDetails' in episode_data:
                # Duration - episode_data['contentDetails']['duration']
                if 'duration' in episode_data['contentDetails']:
                    youtube_video_inst.duration = episode_data['contentDetails']['duration']

            if 'statistics' in episode_data:
                # Views - episode_data['statistics']['viewCount']
                if 'viewCount' in episode_data['statistics']:
                    youtube_video_inst.views = int(episode_data['statistics']['viewCount'])

                # Likes - episode_data['statistics']['likeCount]
                if 'likeCount' in episode_data['statistics']:
                    youtube_video_inst.likes = int(episode_data['statistics']['likeCount'])

            if 'snippet' in episode_data:
                # Title - episode_data['snippet']['title']
                if 'title' in episode_data['snippet']:
                    youtube_video_inst.title = episode_data['snippet']['title']

                # Description - episode_data['snippet']['description']
                if 'description' in episode_data['snippet']:
                    youtube_video_inst.description = episode_data['snippet']['description']

                # Tags - episode_data['snippet']['tags']
                if 'tags' in episode_data['snippet']:
                    youtube_video_inst.tags = episode_data['snippet']['tags']

                # Published At - episode_data['snippet']['publishedAt']
                # Example Format: 2015-08-08T16:03:03Z
                if 'publishedAt' in episode_data['snippet']:
                    youtube_video_inst.published_at = timezone.make_aware(
                        datetime.datetime.strptime(episode_data['snippet']['publishedAt'], '%Y-%m-%dT%H:%M:%SZ'),
                        timezone=timezone.get_current_timezone()
                    )

            # Save YouTubeVideo before adding Thumbnails through Many-to-Many relationship
            youtube_video_inst.save()

            # Thumbnails - episode_data['snippet']['thumbnails']
            if 'snippet' in episode_data and 'thumbnails' in episode_data['snippet']:
                for key, value in episode_data['snippet']['thumbnails'].items():
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

        # Add YouTubeVideo instance to Episode instance
        episode.youtube_video = youtube_video_inst

        # Runtime
        episode.runtime = youtube_video_inst.duration

        # Airdate
        episode.airdate = youtube_video_inst.published_at

        # Host
        # Featuring - snippet.tags
        if youtube_video_inst.tags:
            for name in STAFF:
                if name.lower() in youtube_video_inst.tags:
                    person = get_person_inst(models, {'name': name})
                    manytomany_instances_dict['featuring'].append(person)

        # External Links
        # Headings

        # Save Episode instance to database
        episode.save()

        # Now that SuperReplayEpisode is saved to database, add ManyToManyFields
        add_model_inst_list_to_field(episode.featuring, manytomany_instances_dict['featuring'])
        add_model_inst_list_to_field(episode.external_links, manytomany_instances_dict['external_links'])

        # Create Show Episodes using base Episode
        create_show_episodes_from_episode(models, episode)

    # Return Episode instance
    return episode

def create_show_episode_slug(models, episode, show_tags):
    # Initialize title with base episode title
    show_episode_title = episode.title

    # Sort tags by length from max to min so don't match a shortened version and leave a portion of the longer version.
    # Ex. 'New Gameplay Today | Last of Us 2'
    # tags: 'new gameplay', 'new gameplay today'
    # If 'new gameplay' is matched first, title would be 'Today | Last of Us 2'
    # Should first match 'new gameplay today' and title would be '| Last of Us 2'
    sorted_tags = sorted(show_tags, key=lambda s: len(s), reverse=True)

    # Check beginning of title for show name
    for tag in sorted_tags:
        pattern = r'(?:^' + tag + ')(.*)'
        match = re.match(pattern, show_episode_title, flags=re.IGNORECASE)
        if match is not None:
            show_episode_title = match.group(1)
            break

    # Check end of title for show name
    for tag in sorted_tags:
        pattern = r'(.*)(?:' + tag + '$)'
        match = re.match(pattern, show_episode_title, flags=re.IGNORECASE)
        if match is not None:
            show_episode_title = match.group(1)
            break

    return slugify_unique(models.ShowEpisode, show_episode_title)

def create_show_episodes_from_episode(models, episode):
    # Use YouTube video tags, title, and/or description to determine Show types
    shows = set()

    # YouTube tags
    if episode.youtube_video:
        youtube_tags_lowercase = map(lambda tag: tag.lower(), episode.youtube_video.tags) if episode.youtube_video.tags else []
        for show_key, show_dict in SHOWS.items():
            for show_tag in show_dict['tags']:
                # YouTubeVideo tags
                if show_tag.lower() in youtube_tags_lowercase:
                    # Add show to list
                    shows.add(show_key)
                    break
                # YouTubeVideo title
                if show_tag.lower() in episode.youtube_video.title.lower():
                    # Add show to list
                    shows.add(show_key)
                    break

    # Episode Title
    # TODO

    # Remove any shows by prioritization
    if len(shows) > 1:
        def handle_matching_show_filter(show):
            for priority_show in SHOWS[show]['higher_priority_shows']:
                if priority_show in shows:
                    return False
            return True
        # Remove duplicates by checking for priorities
        shows = list(filter(handle_matching_show_filter, shows))

    # Create ShowEpisode for every matching Show
    for show_key in shows:
        models.ShowEpisode.objects.create(
            show=get_or_create_show(models, SHOWS[show_key]),
            episode=episode,
            slug=create_show_episode_slug(models, episode, SHOWS[show_key]['tags'])
        )

# TODO: Remove after using as reference to write other methods
def create_episode_old(models, episode_data, show_inst, igdb, youtube):
    '''
    Converts dictionary of key/value pairs into defined models inside database for data migration.

    Parameters:
        models (Models): 
        episode_data (dict):
        show_inst (Show): 
        igdb (IGDB): 
        youtube (YouTube): 
    '''
    # Check if Episode already exists with matching YouTubeVideo ID.
    # YouTubeVideo can have multiple Episodes BUT each Episode should 
    # be a unique Show field.
    # TODO: Since Episode has OneToOneField for YouTubeVideo, query Episode with just
    # The YouTube ID AND then check if need to just add Show inst to 'shows' M2M field.
    try:
        youtube_id = episode_data['id']
        episode = models.Episode.objects.get(
            youtube_video__youtube_id=youtube_id
        )
        # If reach here, Episode already exists
        # Add Show inst if it does NOT already exist in 'shows' field
        if show_inst and not show_inst.episode_set.filter(pk=show_inst.pk).exists():
            add_model_inst_list_to_field(episode.shows, [ show_inst ])
            
    except models.Episode.DoesNotExist:
        # Create Episode object
        episode = models.Episode()

        # Dictionary to hold model instances for ManyToManyFields.
        # Key is field name and value is list of model instances.
        # After other fields in Episode instance are set and it's saved to database,
        # can then add to the actual ManyToManyFields.
        manytomany_instances_dict = {
            'shows': [],
            'featuring': [],
            'external_links': [],
        }

        # Add Show instance
        # episode.show = show_inst
        if show_inst:
            manytomany_instances_dict['shows'].append(show_inst)

        # Title - snippet.title
        episode.title = episode_data['snippet']['title']

        # Slug
        episode.slug = slugify_unique(models.Episode, episode.title)

        # YouTube Video
        try:
            youtube_video_inst = models.YouTubeVideo.objects.get(youtube_id=episode_data['id'])
        except models.YouTubeVideo.DoesNotExist:
            youtube_video_inst = models.YouTubeVideo()

            # YouTube ID
            youtube_video_inst.youtube_id = youtube_id

            if 'contentDetails' in episode_data:
                # Duration - episode_data['contentDetails']['duration']
                if 'duration' in episode_data['contentDetails']:
                    youtube_video_inst.duration = episode_data['contentDetails']['duration']

            if 'statistics' in episode_data:
                # Views - episode_data['statistics']['viewCount']
                if 'viewCount' in episode_data['statistics']:
                    youtube_video_inst.views = int(episode_data['statistics']['viewCount'])

                # Likes - episode_data['statistics']['likeCount]
                if 'likeCount' in episode_data['statistics']:
                    youtube_video_inst.likes = int(episode_data['statistics']['likeCount'])

            if 'snippet' in episode_data:
                # Title - episode_data['snippet']['title']
                if 'title' in episode_data['snippet']:
                    youtube_video_inst.title = episode_data['snippet']['title']

                # Description - episode_data['snippet']['description']
                if 'description' in episode_data['snippet']:
                    youtube_video_inst.description = episode_data['snippet']['description']

                # Tags - episode_data['snippet']['tags']
                if 'tags' in episode_data['snippet']:
                    youtube_video_inst.tags = episode_data['snippet']['tags']

                # Published At - episode_data['snippet']['publishedAt']
                # Example Format: 2015-08-08T16:03:03Z
                if 'publishedAt' in episode_data['snippet']:
                    youtube_video_inst.published_at = timezone.make_aware(
                        datetime.datetime.strptime(episode_data['snippet']['publishedAt'], '%Y-%m-%dT%H:%M:%SZ'),
                        timezone=timezone.get_current_timezone()
                    )

            # Save YouTubeVideo before adding Thumbnails through Many-to-Many relationship
            youtube_video_inst.save()

            # Thumbnails - episode_data['snippet']['thumbnails']
            if 'snippet' in episode_data and 'thumbnails' in episode_data['snippet']:
                for key, value in episode_data['snippet']['thumbnails'].items():
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

        # Add YouTubeVideo instance to Episode instance
        episode.youtube_video = youtube_video_inst

        # Runtime
        episode.runtime = youtube_video_inst.duration

        # Airdate
        episode.airdate = youtube_video_inst.published_at

        # Host
        # Featuring - snippet.tags
        if youtube_video_inst.tags:
            for name in STAFF:
                if name.lower() in youtube_video_inst.tags:
                    person = get_person_inst(models, {'name': name})
                    manytomany_instances_dict['featuring'].append(person)

        # External Links
        # Headings

        # Save Episode instance to database
        episode.save()

        # Now that SuperReplayEpisode is saved to database, add ManyToManyFields
        add_model_inst_list_to_field(episode.shows, manytomany_instances_dict['shows'])
        add_model_inst_list_to_field(episode.featuring, manytomany_instances_dict['featuring'])
        add_model_inst_list_to_field(episode.external_links, manytomany_instances_dict['external_links'])

    # Return Episode instance
    return episode

def get_or_create_show(models, show_dict):
    try:
        return models.Show.objects.get(name=show_dict['name'])
    except models.Show.DoesNotExist:
        return models.Show.objects.create(
            name=show_dict['name'],
            description=show_dict['description'],
            slug=show_dict['slug']
        )

def initialize_database(apps, schema_editor):
    models = Models(apps)

    # Add known shows from SHOWS constant
    for show in SHOWS:
        get_or_create_show(models, show)

    with open('utilities/gi_youtube_video_data.json', 'r', encoding='utf-8') as outfile:

        # Get episode data
        all_episode_data = json.load(outfile)

        # If there is episode data
        if (all_episode_data):
            # IGDB instance initialization creates API access_token
            # igdb = IGDB()

            # YouTube Data API instance
            # youtube = YouTube()

            total_count = len(all_episode_data)
            curr_count = 0
            start_time = time.time()

            for episode_data in all_episode_data:
                episode_inst = create_episode(models, episode_data)

                curr_count += 1
                avg_seconds_per_item = (time.time() - start_time) / curr_count
                est_seconds_remaining = math.floor(avg_seconds_per_item * (total_count - curr_count))

                print(
                    f'Episode {curr_count}/{total_count} Completed! - {episode_inst.title} - Est. Time Remaining: {create_total_time_message(est_seconds_remaining)}',
                )

def main():
    pass

if __name__ == '__main__':
    main()
