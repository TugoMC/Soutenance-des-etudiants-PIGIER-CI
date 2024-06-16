# dans soutenance_api/serializers.py

from rest_framework import serializers
from .models import Soutenance

class SoutenanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Soutenance
        fields = ['id', 'title', 'description', 'date', 'superviseur', 'etudiant']
