# Generated by Django 2.0.7 on 2019-11-23 22:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fraid', '0011_auto_20191120_2332'),
    ]

    operations = [
        migrations.AddField(
            model_name='alert',
            name='color',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='event',
            name='color',
            field=models.CharField(default='', max_length=200),
        ),
    ]
