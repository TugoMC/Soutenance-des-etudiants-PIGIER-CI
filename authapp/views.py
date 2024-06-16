from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import SignUpForm, LoginForm
from django.contrib.auth.decorators import login_required


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirection vers la page d'accueil après l'inscription
    else:
        form = SignUpForm()
    return render(request, 'authapp/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirection vers la page d'accueil
            else:
                form.add_error(None, 'Nom d’utilisateur ou mot de passe incorrect.')
    else:
        form = LoginForm()
    return render(request, 'authapp/login.html', {'form': form})


@login_required
def index_view(request):
    return render(request, 'soutenance/index.html')


def custom_logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def profile_view(request):
    user = request.user  # Récupère l'utilisateur connecté
    context = {
        'user': user  # Passe l'utilisateur au contexte du template
    }
    return render(request, 'user/profile.html', context)


