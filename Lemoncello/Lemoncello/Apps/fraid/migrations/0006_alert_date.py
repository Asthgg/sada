# Generated by Django 2.0.7 on 2019-11-20 03:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fraid', '0005_auto_20191119_1753'),
    ]

    operations = [
        migrations.AddField(
            model_name='alert',
            name='date',
            field=models.DateTimeField(default=datetime.date.today),
        ),
    ]
