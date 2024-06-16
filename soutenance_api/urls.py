from django.urls import path
from . import views
from .views import soutenance_update, soutenance_delete

urlpatterns = [
    path('soutenances/', views.soutenance_list, name='soutenance-list'),
    path('soutenances/<int:id>/', views.soutenance_detail, name='soutenance-detail'),
    path('soutenances/update/<int:id>/', soutenance_update, name='soutenance-update'),
    path('soutenances/delete/<int:id>/', soutenance_delete, name='soutenance-delete'),
    path('list/', views.user_list, name='user-list'),
    path('soutenances/user', views.soutenances_utilisateur, name='soutenances-utilisateur'),
    path('upload_pdf/<int:soutenance_id>/', views.upload_pdf, name='upload_pdf'),
    path('download_pdf/<int:soutenance_id>/', views.download_pdf, name='download_pdf'),
]

