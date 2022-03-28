# Generated by Django 4.0.1 on 2022-03-21 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0004_alter_platform_alternate_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='platform',
            name='abbreviation',
            field=models.CharField(blank=True, help_text='Enter shortened abbreviation for this system/platform.', max_length=20),
        ),
    ]