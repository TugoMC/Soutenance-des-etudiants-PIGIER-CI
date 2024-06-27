# Generated by Django 5.0.6 on 2024-06-27 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('soutenance_api', '0009_alter_soutenance_heure'),
    ]

    operations = [
        migrations.AlterField(
            model_name='soutenance',
            name='heure',
            field=models.CharField(choices=[('08:00', '08:00'), ('10:00', '10:00'), ('14:00', '14:00'), ('16:00', '16:00'), ('18:00', '18:00')], default='08:00', max_length=5),
        ),
    ]
