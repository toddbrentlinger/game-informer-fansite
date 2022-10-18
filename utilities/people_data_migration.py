import json
import time
import math

from django.template.defaultfilters import slugify

from utilities.data_migration_utilities import Models
from utilities.data_migration_constants import STAFF
from utilities.misc import create_total_time_message # misc utility functions

def update_or_create_person_inst(models, person_data):
    '''
    Update existing Person model from database or create a new model instance if not in database.

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
        person = models.Person.objects.get(full_name=person_data['name'])
    except models.Person.DoesNotExist:
        person = models.Person()

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
    person.thumbnail = thumbnail_inst

    person.full_name = person_data['name']
    person.slug = slugify(person_data['name'])
    person.description = '\n\n'.join(person_data['description']) if 'description' in person_data else ''
    person.headings = person_data['headings'] if 'headings' in person_data else None
    person.infobox_details = person_data['info_box_details'] if 'info_box_details' in person_data else None
    
    # Save person instance in case it was just created
    person.save()

    # TODO: If person is part of staff, create Staff model as well.
    if person_data['name'] in STAFF and not models.Staff.objects.filter(person=person).exists():
        models.Staff.objects.create(person=person)
    
    return person

def initialize_database(apps, scheme_editor):
    '''
    Adds models to database for Game Informer staff/guests from JSON file.
    '''
    with open('utilities/gi_people.json', 'r', encoding='utf-8') as data_file:
        models = Models(apps)

        # Get all people data
        people_data = json.load(data_file)

        # Return if no data
        if not people_data: return

        total_count = len(people_data)
        curr_count = 0
        start_time = time.time()

        for person_data in people_data:
            update_or_create_person_inst(models, person_data)

            curr_count += 1

            avg_seconds_per_item = (time.time() - start_time) / curr_count
            est_seconds_remaining = math.floor(avg_seconds_per_item * (total_count - curr_count))

            print(f'Person: {person_data["name"]} - {curr_count}/{total_count} Completed! - Est. Time Remaining: {create_total_time_message(est_seconds_remaining)}')
