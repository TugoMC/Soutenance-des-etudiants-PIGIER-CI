# authapp/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm

class CustomUserAdmin(BaseUserAdmin):
    form = CustomUserChangeForm  # Formulaire utilisé pour la modification des utilisateurs
    add_form = CustomUserCreationForm  # Formulaire utilisé pour la création des utilisateurs

    list_display = ('username', 'email', 'role', 'is_staff', 'is_superuser')  # Colonnes affichées dans la liste des utilisateurs
    list_filter = ('is_staff', 'is_superuser', 'role')  # Filtres disponibles
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Informations personnelles', {'fields': ('first_name', 'last_name', 'role')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser')}),
        ('Dates importantes', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'role', 'password1', 'password2'),
        }),
    )
    search_fields = ('username', 'email', 'role')
    ordering = ('email',)
    filter_horizontal = ()

# Enregistrement du modèle CustomUser avec la classe CustomUserAdmin
admin.site.register(CustomUser, CustomUserAdmin)
