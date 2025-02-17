# Generated by Django 5.1.4 on 2025-02-17 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='amount',
            field=models.DecimalField(decimal_places=2, help_text='Transaction amount', max_digits=10),
        ),
    ]
