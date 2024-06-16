from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('home/', views.index_view, name='home'),
    path('profile/', views.profile_view, name='profile'),
    
]