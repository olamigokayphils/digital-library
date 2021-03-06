# Generated by Django 3.1.3 on 2020-12-12 13:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('catalog', '0003_auto_20201127_2219'),
    ]

    operations = [
        migrations.CreateModel(
            name='RentedBook',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('ru', 'Running'), ('re', 'Returned')], max_length=2)),
                ('book_instance', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='catalog.bookinstance')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
