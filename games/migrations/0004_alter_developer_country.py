# Generated by Django 4.0.1 on 2022-06-27 22:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0003_remove_platform_alternate_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='developer',
            name='country',
            field=models.PositiveSmallIntegerField(blank=True, help_text='Enter the ISO 3166-1 country code.', null=True),
        ),
    ]