# Generated by Django 3.2.8 on 2021-10-14 17:57

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bookHub_app', '0011_auto_20211014_1809'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogs',
            name='created_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 14, 23, 57, 48, 535308)),
        ),
        migrations.CreateModel(
            name='Subscribers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subscriber', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
