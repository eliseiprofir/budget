# Generated by Django 5.1.4 on 2025-02-21 12:45

import django.db.models.deletion
import django.db.models.manager
import django.utils.timezone
import model_utils.fields
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('is_removed', models.BooleanField(default=False)),
                ('id', model_utils.fields.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(help_text='Category name (e.g. (1) for Income: Salary, Bonuses, etc.; (2) for Expense: Utilities, Necessities/Utilities, Books, Education/Books, etc.', max_length=255)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categories', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
                'ordering': ('name',),
            },
            managers=[
                ('available_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', model_utils.fields.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('description', models.CharField(help_text='Transaction description', max_length=255)),
                ('date', models.DateTimeField(default=django.utils.timezone.now, help_text='Transaction date')),
                ('amount', models.DecimalField(decimal_places=2, help_text='Transaction amount', max_digits=10)),
                ('split_income', models.BooleanField(default=False, help_text='Whether to split income into multiple buckets or not (only for positive transactions).')),
                ('bucket', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='transactions', to='core.bucket')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='transactions', to='transactions.category')),
                ('location', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='transactions', to='core.location')),
                ('parent_transaction', models.ForeignKey(blank=True, help_text='Parent transaction for a split positive transaction.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='split_transactions', to='transactions.transaction')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Transaction',
                'verbose_name_plural': 'Transactions',
                'ordering': ('-date',),
            },
        ),
        migrations.CreateModel(
            name='TransactionType',
            fields=[
                ('is_removed', models.BooleanField(default=False)),
                ('id', model_utils.fields.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(help_text='Transaction type name (e.g. Income, Expense, Transfer, etc.)', max_length=255)),
                ('sign', models.CharField(choices=[('POSITIVE', 'POSITIVE'), ('NEGATIVE', 'NEGATIVE'), ('NEUTRAL', 'NEUTRAL')], default='NEUTRAL', help_text='Specifies the nature of the transactions. POSITIVE: money coming in, NEGATIVE: money going out, or NEUTRAL: moving between locations/buckets.', max_length=20)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transaction_types', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Transaction Type',
                'verbose_name_plural': 'Transaction Types',
                'ordering': ('name',),
            },
            managers=[
                ('available_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AddField(
            model_name='category',
            name='transaction_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='transactions.transactiontype'),
        ),
    ]
