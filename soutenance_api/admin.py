
from django.contrib import admin
from .models import Soutenance
from .forms import SoutenanceForm

class SoutenanceAdmin(admin.ModelAdmin):
    form = SoutenanceForm
    list_display = ('title', 'date', 'superviseur', 'etudiant')
    list_filter = ('date', 'superviseur', 'etudiant')
    search_fields = ('title', 'description', 'superviseur__username', 'etudiant__username')
    ordering = ('date',)

admin.site.register(Soutenance, SoutenanceAdmin)
