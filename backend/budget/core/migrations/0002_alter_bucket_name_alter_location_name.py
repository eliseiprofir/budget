# Generated by Django 5.1.4 on 2025-02-11 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bucket',
            name='name',
            field=models.CharField(help_text='Bucket name (e.g. Economy, Necessities, Education, Donation, etc.)', max_length=255),
        ),
        migrations.AlterField(
            model_name='location',
            name='name',
            field=models.CharField(help_text='Location name (e.g. Cash, Card, Revolut, ING, etc.)', max_length=255),
        ),
    ]
