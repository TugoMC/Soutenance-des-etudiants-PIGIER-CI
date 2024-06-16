# dans soutenance_api/models.py

from django.db import models
from authapp.models import CustomUser

class Soutenance(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField()
    superviseur = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='soutenances_superviseur', limit_choices_to={'role': CustomUser.SUPERVISOR})
    etudiant = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='soutenances_etudiant', limit_choices_to={'role': CustomUser.STUDENT})
    pdf_file = models.FileField(upload_to='pdfs/', null=True, blank=True)  # Champ pour le fichier PDF

    def __str__(self):
        return self.title
