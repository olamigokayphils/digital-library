# Generated by Django 3.1.3 on 2020-12-18 21:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_rentedbook'),
    ]

    operations = [
        migrations.AddField(
            model_name='rentedbook',
            name='book',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='catalog.book'),
        ),
    ]
