# Generated by Django 3.2.7 on 2021-10-14 05:19

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookHub_app', '0007_alter_blogs_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogs',
            name='created_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 14, 11, 19, 47, 896090)),
        ),
    ]
