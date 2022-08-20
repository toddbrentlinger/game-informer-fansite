# Generated by Django 4.0.1 on 2022-08-19 02:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Show',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Enter name of the show.', max_length=100)),
                ('description', models.TextField(blank=True, help_text='Enter description of the show.')),
                ('slug', models.SlugField(help_text='Enter a url-safe, unique, lower-case version of the show.', max_length=100, unique=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
    ]
