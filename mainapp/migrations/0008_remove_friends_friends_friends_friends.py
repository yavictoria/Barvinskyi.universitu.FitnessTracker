# Generated by Django 5.0.3 on 2024-05-01 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0007_friends'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='friends',
            name='friends',
        ),
        migrations.AddField(
            model_name='friends',
            name='friends',
            field=models.IntegerField(default=1),
        ),
    ]
