# Generated by Django 4.2 on 2024-05-31 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('savepost', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posturls',
            name='views',
            field=models.IntegerField(default=0),
        ),
    ]
