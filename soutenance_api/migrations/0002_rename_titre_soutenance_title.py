# Generated by Django 5.0.6 on 2024-06-14 01:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('soutenance_api', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='soutenance',
            old_name='titre',
            new_name='title',
        ),
    ]
