# Generated by Django 5.1.4 on 2025-01-28 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0003_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='name',
            field=models.CharField(choices=[('Expense', 'Expense'), ('Income', 'Income'), ('Transfer', 'Transfer')], default='Expense', help_text='Transaction type', max_length=100, unique=True),
        ),
    ]
