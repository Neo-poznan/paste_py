# Generated by Django 4.2 on 2024-05-31 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PostUrls',
            fields=[
                ('key', models.CharField(max_length=13, primary_key=True, serialize=False)),
                ('file_url', models.URLField()),
                ('views', models.IntegerField()),
                ('del_date', models.DateField()),
            ],
        ),
    ]
