# Generated by Django 5.0.6 on 2024-06-22 14:21

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('soutenance_api', '0006_alter_soutenance_etudiant_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='soutenance',
            name='membres_jury',
            field=models.ManyToManyField(blank=True, limit_choices_to={'role': 'membre_jury'}, related_name='soutenances_membre_jury', to=settings.AUTH_USER_MODEL),
        ),
    ]
