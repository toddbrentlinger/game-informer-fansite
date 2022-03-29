# (<Segment Title>, <Segment Abbreviation>, <Game/Text ID>)
# Game/Text ID: 0-game 1-text 2-game/text
SEGMENT_TYPES = [
    ('Advertisement', 'AD', 0), # game (remove 'Ad' from end when searching IGDB for game title)
    ('A Poor Retelling of Gaming History', None, 1), # text
    ('Developer Pick', 'DP', 0), # game
    ('Developer Spotlight', 'DS', 2), # game/text
    ('Embarassing Moments', 'EM', 1), # text
    ('GI Versus', 'GIV', 0), # game
    ('Horror Fest', 'HF', 0), # game
    ('Life Advice with Ben Reeves', None, 1), # text (empty content)
    ('Moments', None, 2), # game/text
    ('NES Games With User-Generated Content', None, 0), # game
    ('Reevesplay', None, 0), # game
    ('Reflections', None, 1), # text
    ('Replay 2037', '2037', 0), # game
    ('Replay Civil War', None, 1), # text (empty content)
    ('Replay Real Life', 'RRL', 1), # text
    ('Replay Roulette', 'RR', 0), # game
    ('RePorted', 'RP', 0), # game
    ('Secret Access', 'SA', 0), # game
    ('Stress Test', 'ST', 0), # game
    ('Suite Nostalgia', 'SN', 0), # game
    ('Super Replay Showdown', 'SRS', 0), # game (except 'Editor's Picks' and blank values)
    ('The Commodore 64 Spectacular: Part 3', None, 0), # game
    ('The Wiebeatdown', None, 0), # game ('Super Smash Bros. for WiiU' should be 'Super Smash Bros. for Wii U' when searching IGDB)
    ('You\'re Doing It Wrong', 'YDIW', 0), # game
]

STAFF = [
    'Adam Biessener',
    'Alex Stadnik',
    'Andrew Reiner',
    'Andy McNamara',
    'Annette Gonzalez',
    'Ben Hanson',
    'Ben Reeves',
    'Blake Hester',
    'Brian Shea',
    'Bryan Vore',
    'Cathy Preston',
    'Curtis Fung',
    'Dan Ryckert',
    'Dan Tack',
    'Elise Favis',
    'Imran Khan',
    'Jason Guisao',
    'Jason Oestreicher',
    'Javy Gwaltney',
    'Jeff Akervik',
    'Jeff Cork',
    'Jeff Marchiafava',
    'Jen Vinson',
    'Jim Reilly',
    'Joe Juba',
    'Kimberley Wallace',
    'Kristin Williams',
    'Kyle Hilliard',
    'Laleh Tobin',
    'Leo Vader',
    'Liana Ruppert',
    'Marcus Stewart',
    'Margaret Andrews',
    'Matt Bertz',
    'Matt Helgeson',
    'Matt Miller',
    'Matthew Kato',
    'Meagan Marie',
    'Nick Ahrens',
    'Phil Kollar',
    'Samm Langer',
    'Suriel Vasquez',
    'Tim Turi',
    'Wade Wojcik',
]