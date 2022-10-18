import re

from django.template.defaultfilters import slugify

class Models:
    def __init__(self, apps):
        # Cannot import models directly as it may be a newer version
        # than this migration expects. Use historical versions instead.
        
        # Fansite app

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
        self.ReplayEpisode = apps.get_model('replay', 'ReplayEpisode')
        self.ReplaySeason = apps.get_model('replay', 'ReplaySeason')
        self.Segment = apps.get_model('replay', 'Segment')
        self.SegmentType = apps.get_model('replay', 'SegmentType')

        # Episodes app
        self.Episode = apps.get_model('episodes', 'Episode')
        self.ExternalLink = apps.get_model('episodes', 'ExternalLink')
        self.Thumbnail = apps.get_model('episodes', 'Thumbnail')
        self.YouTubeVideo = apps.get_model('episodes', 'YouTubeVideo')

        # Shows app
        self.Show = apps.get_model('shows', 'Show')
        self.ShowEpisode = apps.get_model('shows', 'ShowEpisode')

        # Super Replay app
        self.SuperReplay = apps.get_model('superreplay', 'SuperReplay')
        self.SuperReplayEpisode = apps.get_model('superreplay', 'SuperReplayEpisode')
        self.SuperReplayGame = apps.get_model('superreplay', 'SuperReplayGame')

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