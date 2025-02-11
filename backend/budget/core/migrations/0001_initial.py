# Generated by Django 5.1.4 on 2025-02-11 13:31

import django.db.models.deletion
import django.db.models.manager
import model_utils.fields
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Bucket',
            fields=[
                ('is_removed', models.BooleanField(default=False)),
                ('id', model_utils.fields.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(help_text='Bucket name (e.g. Economy, Necessities, Education, Donation, etc.)', max_length=255, unique=True)),
                ('allocation_percentage', models.DecimalField(decimal_places=2, help_text='Percentage of income to allocate to this bucket', max_digits=5, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='buckets', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Bucket',
                'verbose_name_plural': 'Buckets',
                'ordering': ('name',),
            },
            managers=[
                ('available_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('is_removed', models.BooleanField(default=False)),
                ('id', model_utils.fields.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(help_text='Location name (e.g. Cash, Card, Revolut, ING, etc.)', max_length=255, unique=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='locations', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Location',
                'verbose_name_plural': 'Locations',
                'ordering': ('name',),
            },
            managers=[
                ('available_objects', django.db.models.manager.Manager()),
            ],
        ),
    ]
