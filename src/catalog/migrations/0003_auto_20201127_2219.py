# Generated by Django 3.1.3 on 2020-11-27 21:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_book_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='bio',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='author',
            name='image',
            field=models.URLField(null=True),
        ),
    ]
