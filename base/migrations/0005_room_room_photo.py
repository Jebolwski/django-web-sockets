# Generated by Django 4.0 on 2022-09-16 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_profile_profile_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='room_photo',
            field=models.ImageField(default='room_pics/default_room_pic.png', upload_to='room_pics'),
        ),
    ]
