# Generated by Django 5.1.4 on 2025-01-29 14:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0006_alter_category_bucket_alter_category_name'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Entry',
        ),
    ]
