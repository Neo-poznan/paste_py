# Generated by Django 4.2 on 2024-08-14 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('savepost', '0002_posturls_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='posturls',
            name='last_query',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='posturls',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
