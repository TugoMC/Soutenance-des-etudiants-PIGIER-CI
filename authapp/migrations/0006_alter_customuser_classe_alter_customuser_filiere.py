# Generated by Django 5.0.6 on 2024-06-21 23:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0005_customuser_classe_customuser_filiere'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='classe',
            field=models.CharField(blank=True, choices=[('classe1', 'Classe 1'), ('classe2', 'Classe 2'), ('classe3', 'Classe 3')], max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='filiere',
            field=models.CharField(blank=True, choices=[('informatique', 'Informatique'), ('mathematiques', 'Mathématiques'), ('physique', 'Physique')], max_length=50, null=True),
        ),
    ]
