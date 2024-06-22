# Generated by Django 5.0.6 on 2024-06-21 22:06

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('soutenance_api', '0005_soutenance_pdf_file'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='soutenance',
            name='etudiant',
            field=models.ForeignKey(blank=True, limit_choices_to={'role': 'etudiant'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='soutenances_etudiant', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='soutenance',
            name='superviseur',
            field=models.ForeignKey(blank=True, limit_choices_to={'role': 'superviseur'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='soutenances_superviseur', to=settings.AUTH_USER_MODEL),
        ),
    ]
