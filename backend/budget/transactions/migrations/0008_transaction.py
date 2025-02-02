# Generated by Django 5.1.4 on 2025-02-03 19:48

import datetime
import django.db.models.deletion
import model_utils.fields
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_alter_bucket_managers_alter_location_managers'),
        ('transactions', '0007_delete_entry'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', model_utils.fields.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('description', models.CharField(help_text='Transaction description', max_length=255)),
                ('transaction_type', models.CharField(choices=[('Expense', 'Expense'), ('Income', 'Income'), ('Transfer', 'Transfer'), ('Temporary', 'Temporary')], default='Expense', help_text='Transaction type', max_length=100)),
                ('date', models.DateField(default=datetime.datetime.today, help_text='Transaction date')),
                ('amount', models.DecimalField(decimal_places=2, help_text='Transaction amount', max_digits=1000)),
                ('bucket', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='transactions', to='core.bucket')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='transactions', to='transactions.category')),
                ('location', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='transactions', to='core.location')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Transaction',
                'verbose_name_plural': 'Transactions',
                'ordering': ('-date',),
            },
        ),
    ]
