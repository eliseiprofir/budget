# Generated by Django 5.1.4 on 2025-01-22 22:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_rename_user_id_location_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bucket',
            old_name='user',
            new_name='user_id',
        ),
        migrations.RenameField(
            model_name='location',
            old_name='user',
            new_name='user_id',
        ),
    ]
