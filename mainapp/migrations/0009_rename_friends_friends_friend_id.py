# Generated by Django 5.0.3 on 2024-05-01 08:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0008_remove_friends_friends_friends_friends'),
    ]

    operations = [
        migrations.RenameField(
            model_name='friends',
            old_name='friends',
            new_name='friend_id',
        ),
    ]