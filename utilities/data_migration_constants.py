# (<Segment Title>, <Segment Abbreviation>, <Game/Text ID>)
# Game/Text ID: 0-game 1-text 2-game/text
SEGMENT_TYPES = [
    ('Advertisement', 'AD', 0, {}), # game (remove 'Ad' from end when searching IGDB for game title)
    ('A Poor Retelling of Gaming History', None, 1, {
        'description': ['A Poor Retelling of Gaming History is a segment introduced in the third season of Replay, that airs between the main game and the second segment.']
    }), # text
    ('Developer Pick', 'DP', 0, {
        'description': [
            'Developer Pick is one of the new segments in the second season of Replay, which occasionally appears in the second segment of an episode (which was originally occupied exclusively by Roulette).',
            'As the name implies, Developer Pick lets game developers choose which game the crew plays for the second segment. The debut of Developer Pick was on the 50 Cent: Bulletproof episode featuring Haydn Dalton, lead designer of Darksiders II (who also worked on 50 Cent: Bulletproof). He chose Venom/Spider-Man: Separation Anxiety for Developer Pick, another game he worked on.',
            'Given the nature of this segment, Developer Pick will probably only appear in episodes of Replay which feature guest appearances by game developers. However, one could speculate that almost every episode that features a game developer as a guest will probably feature an episode of Developer Pick. The existence of Developer Pick may also indicate an increased ability (or desire) to have game designers appear on episodes of Replay.'
        ]
    }), # game
    ('Developer Spotlight', 'DS', 2, {
        'description': ['Developer Pick is a second segment on Replay, wherein a special guest that does not work at GI chooses a game from the vault.']
    }), # game/text
    ('Embarassing Moments', 'EM', 1, {}), # text
    ('GI Versus', 'GIV', 0, {
        'description': ['GI Versus is a second segment introduced in the third season of Replay.']
    }), # game
    ('Horror Fest', 'HF', 0, {
        'description': ['Horror Fest is a special segment in honor of Friday the 13th (the day, not the game) and may or may not reoccur on other Friday the 13th\'s or Halloween. The introduction of this segment seemed impromptu since the original Roulette they were going to play on the Friday the 13th episode was Ocarina of Time. Reiner said, "Just throw that away, Jason. Everybody knows what that game is, let\'s continue our horror fest."']
    }), # game
    ('Life Advice with Ben Reeves', None, 1, {}), # text (empty content)
    ('Moments', None, 2, {
        'description': ['Moments is a segment introduced in the third season of Replay, that airs between the main game and the second segment.']
    }), # game/text
    ('NES Games With User-Generated Content', None, 0, {}), # game
    ('Reevesplay', None, 0, {}), # game
    ('Reflections', None, 1, {
        'description': ['Reflections is a segment introduced in the third season of Replay, that airs between the main Game and the second segment.']
    }), # text
    ('Replay 2037', '2037', 0, {
        'description': [
            'Replay 2037 is a feature new to Replay , debuting in the first episode of the second season. Replay 2037 opens in a Megaman 2 style intro, panning up a building to a pixelated version of the editors, visibly aged. This segment replays games that are current-gen today (obviously last-gen in 2037).',
            'The editors pretend to be older, or different, versions of themselves. Tim Turi is an overweight middle-aged man, Andrew Reiner is slightly delirious and seems only to hold on to his hatred of Dan Ryckert (who is dead), Ben Reeves travelled off the planet leaving Reeverbot in his place, and Rowdy Ricky Ryckert (Dan\'s fart baby son) now works (against his will?) at Game Informer and is Reiner\'s indentured servant.',
            'This segment proved to be highly controversial, because of its large change from the regular Replay Roulette. Many fans were not pleased by the strange concept, while many others thought it was funny. Being a very love/hate type of show, it would be difficult to make more episodes of this show. Dan is the only editor who, seemingly, wants to make another episode. Reiner, though, is firmly against returning to this concept.'
        ]
    }), # game
    ('Replay Civil War', None, 1, {}), # text (empty content)
    ('Replay Real Life', 'RRL', 1, {}), # text
    ('Replay Roulette', 'RR', 0, {
        'description': [
            'Replay Roulette (often shortened to Roulette) is a recurring segment on Replay in which the editors play an additional game after the title game.',
            'Originally, the game was picked from the Vault at random, but this approach was quickly abandoned. Replay Roulette debuted with Replay: Bushido Blade and continues to be a frequent final segment to this day, returning to Season 2 with Replay: Alex Kidd in the Enchanted Castle and to Season 3 with Replay: Tomb Raider II.'
        ],
        'openings': [
            'The original opening strangely featured a slot machine with a multitude of games passing by before lining up three of the same game and displaying the title.',
            'A new intro inaugurated in Season 2 of Replay showed a roulette wheel spinning around with the letters "roulette" along the edges before breaking off and arriving at their final resting place next to "Replay".',
            'The intro was updated again in Season 3, after a number of Roulettes, in Replay: Super Mario RPG: Legend of the Seven Stars. This intro features a casino roulette spinning and landing on a Mario "?" block, which then animates, lights up, and darkens the background as "replay toulette" fades in gently.'
        ]
    }), # game
    ('RePorted', 'RP', 0, {
        'description': ['RePorted is a Replay segment that debuted on the second episode of Season 2 of Replay. The intro plays a plane flying sound while the word "Imported" collides with the word "Replay" to make "RePorted." There is a slight pause then Dan\'s "Fwumpf" sound as a bunch of rubber stamp images are added in the background. In this segment the editors play a game that didn\'t make the hop to North America (or maybe just the USA?).']
    }), # game
    ('Secret Access', 'SA', 0, {
        'description': ['Secret Access is a recurring middle segment for Replay in which the Game Informer cast shows the watcher how to access cheats within various (usually outdated and forgotten) games.']
    }), # game
    ('Stress Test', 'ST', 0, {}), # game
    ('Suite Nostalgia', 'SN', 0, {
        'description': ['Suite Nostalgia is a segment introduced in the third season of Replay, that airs between the main Game and the second segment. The segment covers the music of video games.']
    }), # game
    ('Super Replay Showdown', 'SRS', 0, {}), # game (except 'Editor's Picks' and blank values)
    ('The Commodore 64 Spectacular: Part 3', None, 0, {}), # game
    ('The Wiebeatdown', None, 0, {}), # game ('Super Smash Bros. for WiiU' should be 'Super Smash Bros. for Wii U' when searching IGDB)
    ('You\'re Doing It Wrong', 'YDIW', 0, {
        'description': [
            'You\'re Doing It Wrong is a Replay segment that debuted on the Mischief Makers Replay.',
            'The title sequence has Tim going through the vault, picking out Super Metroid, blowing in the cartridge and then putting it in the SNES upside down, while music from Bionic Commando plays.'
        ]
    }), # game
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

GAME_NAME_ALTERNATIVES = {
    "Alone in the Dark: One-Eyed Jack's Revenge": "Alone in the Dark 2",
    "Beetlejuice": 7778,
    "Beyond the Beyond": 20303,
    "Big Motha Truckers 2: Truck Me Harder": "Big Mutha Truckers 2",
    "Bioshock Infinite Part 2": "Bioshock Infinite",
    "Brütal Legend": 212,
    "Cat Mario Impossible": "Syobon Action",
    "Caveman Ughlympics": "Caveman Games",
    "Cliffhanger": 5370,
    "Crash Bandicoot (The High Road level)": "Crash Bandicoot",
    "Dragon Ball Z: Chou Saiya Densetsu": "Dragon Ball Z: Super Saiya Densetsu",
    "Einhander": 1360,
    "Gargoyle's Quest II: The Demon Darkness": "Gargoyle's Quest II",
    "Golden Nugget for PlayStation": "Golden Nugget",
    "GoldenEye 007": 1638,
    "Halo: Reach Co-Op": "Halo: Reach",
    "James Cameron's Dark Angel": "Dark Angel",
    "Jurassic Park: Trespasser": "Trespasser",
    "MGS3 Secret Theater": "Metal Gear Solid 3: Subsistence",
    "Minerva: Metastasis": "MINERVA",
    "Murder House Finale": "Murder House",
    "Murder House Part 2": "Murder House",
    "Pac-Man Cereal": 2750,
    "Portable Donkey Kong Arcade": 1086,
    "Resident Evil 3 Demo": "Resident Evil 3",
    "Rygar": 28841,
    "Shock Wave: Invasion Earth: 2019": "Shock Wave",
    "Silent Hill: Downpour Part 2": "Silent Hill: Downpour",
    "Star Trek: The Next Generation: Future's Past": "Star Trek: The Next Generation - Echoes from the Past",
    "Star Wars for Atari": "Star Wars: The Arcade Game",
    "Star Wars: Masters of Teräs Käsi": 18044,
    "The Elder Scrolls V: Skyrim Part 2": "The Elder Scrolls V: Skyrim",
    "The Fantastic Adventures of Dizzy": "Fantastic Dizzy",
    "The Walking Dead S1E5: No Time Left": "The Walking Dead: Episode 5 - No Time Left",
    "Tweety's Hearty Party (トゥイーティーのハーティーパーティー)": "Tweety's High-Flying Adventure"
}

SHOWS = [
    {
        "name": "Chronicles",
        "description": "",
        "slug": "chronicles",
    },
    {
        "name": "Game Informer Show",
        "description": "",
        "slug": "game-informer-show",
    },
    {
        "name": "New Gameplay Today",
        "description": "New Gameplay Today is a GI video series, hosted by Jeff Cork and Leo Vader, showing off gameplay from upcoming games and new releases. It replaces Test Chamber, which had a similar premise. The first episode aired on October 16, 2017.",
        "slug": "new-gameplay-today",
    },
    {
        "name": "Reiner and Phil",
        "description": "",
        "slug": "reiner-and-phil",
    },
    {
        "name": "Replay",
        "description": "Replay is a weekly web video series produced by Game Informer in which the publication's editors play bits of older video games while providing commentary. The series premiered on January 27, 2010 with Replay: Twisted Metal 1–4 and has more than one hundred episodes. A spin-off series in which they play through an entire game, Super Replay, debuted in May 2010.",
        "slug": "replay",
    },
    {
        "name": "Review",
        "description": "",
        "slug": "review",
    },
    {
        "name": "Spoiled",
        "description": "",
        "slug": "spoiled",
    },
    {
        "name": "Super Replay",
        "description": "Super Replay is a web video series from Game Informer in which the publication's editors play through the entirety of a video game from a previous console generation while providing commentary. Each entry in the series is broken up into episodes, which are usually about one hour in length. The series' premiere game is The Legend of Zelda: A Link to the Past, which aired its first episode on May 24, 2010. Super Replay is a spin-off of Replay.",
        "slug": "super-replay",
    },
    {
        "name": "Test Chamber",
        "description": "",
        "slug": "test-chamber",
    },
]
