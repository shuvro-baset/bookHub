# Generated by Django 3.2.8 on 2021-10-13 04:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookHub_app', '0002_auto_20211013_0737'),
    ]

    operations = [
        migrations.AlterField(
            model_name='books',
            name='book_thumbnail',
            field=models.ImageField(null=True, upload_to='pdf/thumbnails'),
        ),
    ]
