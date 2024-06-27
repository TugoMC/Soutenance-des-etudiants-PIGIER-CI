# authapp/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.utils.html import strip_tags

class SignUpForm(UserCreationForm):
    role = forms.ChoiceField(choices=CustomUser.ROLE_CHOICES, required=True)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'role', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_active = False  # Le compte n'est pas encore activé
        user.role = self.cleaned_data['role']
        if commit:
            user.save()
            self.send_activation_email(user, self.request)  # Passer request à la méthode d'envoi d'e-mail
        return user

    def send_activation_email(self, user, request):
        # Générer le lien d'activation
        activation_link = self.activation_link(user, request)

        # Sujet et contenu de l'e-mail
        subject = '[Soutenance PIGIER] Activation de compte'
        html_message = render_to_string('authapp/activation_email.html', {'activation_link': activation_link})
        plain_message = strip_tags(html_message)
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = user.email

        # Envoi de l'e-mail
        send_mail(subject, plain_message, from_email, [to_email], html_message=html_message)

    def activation_link(self, user, request):
        from django.contrib.sites.shortcuts import get_current_site
        from django.urls import reverse

        current_site = get_current_site(request)
        domain = current_site.domain
        # Créer le lien d'activation en utilisant la vue d'activation (à définir)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        activation_url = reverse('activate', kwargs={'uidb64': uid, 'token': token})
        return f'http://{domain}{activation_url}'
    
    
# Ajout de la classe LoginForm pour gérer le formulaire de connexion
class LoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=254,
        required=True,
        widget=forms.TextInput(attrs={'autofocus': True})
    )
    password = forms.CharField(
        label="Mot de passe",
        strip=False,
        widget=forms.PasswordInput
    )


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'filiere', 'classe']

    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        
        # Charger les choix dynamiquement, si besoin
        self.fields['filiere'].choices = [(filiere[0], filiere[1]) for filiere in CustomUser.FILIERE_CHOICES]
        self.fields['classe'].choices = [(classe[0], classe[1]) for classe in CustomUser.CLASSE_CHOICES]
        
        # Désactiver les champs 'filiere' et 'classe' si l'utilisateur n'est pas un étudiant
        if self.instance.role != CustomUser.ETUDIANT:
            self.fields['filiere'].disabled = True
            self.fields['classe'].disabled = True

    def clean(self):
        cleaned_data = super().clean()
        
        # Valider les champs 'filiere' et 'classe' si l'utilisateur est un étudiant
        if self.instance.role == CustomUser.ETUDIANT:
            filiere = cleaned_data.get('filiere')
            classe = cleaned_data.get('classe')
            
            if not filiere:
                self.add_error('filiere', "Ce champ est obligatoire.")
            if not classe:
                self.add_error('classe', "Ce champ est obligatoire.")
        
        return cleaned_data



class UserSearchForm(forms.Form):
    nom = forms.CharField(label='Nom', required=False)
    prenom = forms.CharField(label='Prénom', required=False)
    filiere = forms.CharField(label='Filière', required=False)