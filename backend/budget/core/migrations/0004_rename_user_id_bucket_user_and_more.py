# Generated by Django 5.1.4 on 2025-01-23 09:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_rename_user_bucket_user_id_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bucket',
            old_name='user_id',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='location',
            old_name='user_id',
            new_name='user',
        ),
    ]
