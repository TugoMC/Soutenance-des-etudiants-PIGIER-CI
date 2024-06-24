from django.db import models
from authapp.models import CustomUser

class Soutenance(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField()
    
    HEURE_CHOICES = (
        ('08:00', '08:00'),
        ('10:00', '10:00'),
        ('14:00', '14:00'),
        ('16:00', '16:00'),
        ('18:00', '18:00'),
    )
    heure = models.CharField(max_length=5, choices=HEURE_CHOICES, default='08:00')
    
    superviseur = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='soutenances_superviseur',
        limit_choices_to={'role': CustomUser.SUPERVISEUR}
    )
    
    etudiant = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='soutenances_etudiant',
        limit_choices_to={'role': CustomUser.ETUDIANT}
    )
    
    membres_jury = models.ManyToManyField(
        CustomUser,
        related_name='soutenances_membre_jury',
        limit_choices_to={'role': CustomUser.MEMBRE_JURY},
        blank=True
    )
    
    pdf_file = models.FileField(upload_to='pdfs/', null=True, blank=True)

    def __str__(self):
        return self.title
