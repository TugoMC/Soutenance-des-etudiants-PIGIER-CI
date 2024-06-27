from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # Choix pour le rôle
    ETUDIANT = 'etudiant'
    SUPERVISEUR = 'superviseur'
    MEMBRE_JURY = 'membre_jury'

    ROLE_CHOICES = [
        (ETUDIANT, 'Étudiant'),
        (SUPERVISEUR, 'Superviseur'),
        (MEMBRE_JURY, 'Membre du jury'),
    ]

    # Choix pour les filières
    CF = 'cf'
    GRH = 'grh'
    AD = 'ad'
    CDM = 'cdm'
    GE = 'ge'
    MA = 'ma'
    RGL = 'rgl'

    FILIERE_CHOICES = [
        (CF, 'CF'),
        (GRH, 'GRH'),
        (AD, 'AD'),
        (CDM, 'CDM'),
        (GE, 'GE'),
        (MA, 'MA'),
        (RGL, 'RGL'),
    ]

    # Choix pour les classes par filière
    CLASSE_CF_CHOICES = [
        ('3A', '3A'),
        ('3B', '3B'),
        ('3C', '3C'),
    ]

    CLASSE_GRH_CHOICES = [
        ('3A', '3A'),
    ]

    CLASSE_AD_CHOICES = [
        ('3A', '3A'),
    ]

    CLASSE_CDM_CHOICES = [
        ('3A', '3A'),
    ]

    CLASSE_GE_CHOICES = [
        ('3A', '3A'),
    ]

    CLASSE_MA_CHOICES = [
        ('3A', '3A'),
    ]

    CLASSE_RGL_CHOICES = [
        ('3A', '3A'),
    ]

    CLASSE_CHOICES = [
        ('3A', 'Classe 3A'),
        ('3B', 'Classe 3B'),
        ('3C', 'Classe 3C'),
    ]

    role = models.CharField(max_length=15, choices=ROLE_CHOICES, default=ETUDIANT)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=False)
    filiere = models.CharField(max_length=50, choices=FILIERE_CHOICES, null=True, blank=True)
    classe = models.CharField(max_length=50, choices=CLASSE_CHOICES, null=True, blank=True)

    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

    def __str__(self):
        return self.username

    def get_classe_choices(self):
        if self.filiere == self.CF:
            return self.CLASSE_CF_CHOICES
        elif self.filiere == self.GRH:
            return self.CLASSE_GRH_CHOICES
        elif self.filiere == self.AD:
            return self.CLASSE_AD_CHOICES
        elif self.filiere == self.CDM:
            return self.CLASSE_CDM_CHOICES
        elif self.filiere == self.GE:
            return self.CLASSE_GE_CHOICES
        elif self.filiere == self.MA:
            return self.CLASSE_MA_CHOICES
        elif self.filiere == self.RGL:
            return self.CLASSE_RGL_CHOICES
        else:
            return []  



