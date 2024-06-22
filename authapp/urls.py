# authapp/urls.py

from django.urls import path
from .views import SignUpView, LoginView, activate_account, register_done_view
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', views.profile_view, name='profile'),
    path('edit-profile/', views.edit_profile, name='edit-profile'),
    path('activate/<str:uidb64>/<str:token>/', activate_account, name='activate'),
    path('signup/done/', register_done_view, name='register_done'),
    
    path('password_reset/', 
         auth_views.PasswordResetView.as_view(template_name='authapp/password_reset_form.html'), 
         name='password_reset'),
    
    # URL indiquant que l'e-mail de réinitialisation a été envoyé
    path('password_reset/done/', 
         auth_views.PasswordResetDoneView.as_view(template_name='authapp/password_reset_done.html'), 
         name='password_reset_done'),
    
    # URL pour le lien de réinitialisation envoyé par e-mail
    path('reset/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(template_name='authapp/password_reset_confirm.html'), 
         name='password_reset_confirm'),
    
    # URL de confirmation après la réinitialisation du mot de passe
    path('reset/done/', 
         auth_views.PasswordResetCompleteView.as_view(template_name='authapp/password_reset_complete.html'), 
         name='password_reset_complete'),
    
    path('fetch-classe-choices/', views.fetch_classe_choices, name='fetch_classe_choices'),
    path('select-classe/', views.select_classe, name='select-classe'),
]
