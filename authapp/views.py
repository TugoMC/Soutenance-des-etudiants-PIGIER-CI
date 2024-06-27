
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.views import LoginView
from django.views import View
from .forms import SignUpForm, LoginForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
from .models import CustomUser
from .forms import EditProfileForm
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.http import HttpResponse
from .forms import UserSearchForm

User = get_user_model()

class SignUpView(View):
    form_class = SignUpForm
    template_name = 'authapp/register.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST, request=request)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  
            user.save()
            form.send_activation_email(user, request) 
            return redirect('register_done')
        return render(request, self.template_name, {'form': form})
    
    
class LoginView(View):
    form_class = LoginForm
    template_name = 'authapp/login.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
        return render(request, self.template_name, {'form': form})


@login_required
def index_view(request):
    return render(request, 'soutenance/index.html')

@login_required
def custom_logout_view(request):
    logout(request)
    return redirect('login')


class CustomLoginView(LoginView):
    template_name = 'authapp/login.html'
    form_class = LoginForm
    
    
@login_required
def profile_view(request):
    user = request.user  
    context = {
        'user': user 
    }
    return render(request, 'user/profile.html', context)


@login_required
def edit_profile(request):
    user = request.user

    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile') 
    else:
        form = EditProfileForm(instance=user)

    context = {
        'form': form,
        'is_etudiant': user.role == CustomUser.ETUDIANT
    }
    return render(request, 'user/profile.html', context)


def activate_account(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Votre compte a été activé avec succès ! Vous pouvez maintenant vous connecter.')
        return redirect('login') 
    else:
        messages.error(request, 'Le lien d\'activation est invalide ou a expiré.')
        return redirect('home')
    
    
def register_done_view(request):
    return render(request, 'authapp/register_done.html')


@require_http_methods(["GET"])
@login_required
def fetch_classe_choices(request):
    filiere = request.GET.get('filiere', None)
    user = request.user

    if filiere:
        if user.role == CustomUser.ETUDIANT: 
            classe_choices = user.get_classe_choices()
            return JsonResponse(classe_choices, safe=False)
        else:
            return JsonResponse({}, status=403)  
    else:
        return JsonResponse({}, status=400) 
    
    

@login_required
def select_classe(request):
    if request.method == 'POST':
        classe = request.POST.get('classe')
        if classe:
            request.user.classe = classe 
            request.user.save()           
            return redirect('profile')    

    return HttpResponse(status=405)



def user_search_view(request):
    form = UserSearchForm(request.GET)
    users = User.objects.all()

    if form.is_valid():
        nom = form.cleaned_data.get('nom')
        prenom = form.cleaned_data.get('prenom')
        filiere = form.cleaned_data.get('filiere')

        if nom:
            users = users.filter(last_name__icontains=nom)
        if prenom:
            users = users.filter(first_name__icontains=prenom)
        if filiere:
            users = users.filter(filiere__icontains=filiere)

    context = {
        'form': form,
        'users': users,
    }
    return render(request, 'user/user_list.html', context)