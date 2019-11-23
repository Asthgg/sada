# Generated by Django 2.0.7 on 2019-11-19 02:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fraid', '0002_auto_20191118_1303'),
    ]

    operations = [
        migrations.CreateModel(
            name='Alert',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alertMessage', models.CharField(max_length=1000)),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='length',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
