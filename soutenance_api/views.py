from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Soutenance
from django.forms.models import model_to_dict
from .serializers import SoutenanceSerializer
from authapp.models import CustomUser  # Import du modèle CustomUser
from django.contrib.auth.decorators import login_required
from .forms import SoutenanceForm
from django.contrib import messages
from django.http import HttpResponse


@login_required
def soutenance_list(request):
    if request.method == 'POST':
        data = request.POST.copy()
        data['superviseur'] = data.get('superviseur') or None  # Assurez-vous de gérer le cas où aucun superviseur n'est sélectionné
        data['etudiant'] = data.get('etudiant') or None  # Gestion du champ étudiant
        serializer = SoutenanceSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return redirect('soutenance-list')
        else:
            return JsonResponse(serializer.errors, status=400)
    else:
        soutenances = Soutenance.objects.all()
        superviseurs = CustomUser.objects.filter(role=CustomUser.SUPERVISOR)  # Filtrer les superviseurs
        etudiants = CustomUser.objects.filter(role=CustomUser.STUDENT)  # Filtrer les étudiants

        return render(request, 'soutenance_api/soutenances_list.html', {
            'soutenances': soutenances,
            'superviseurs': superviseurs,
            'etudiants': etudiants  # Passer la liste des étudiants au template
        })

@login_required
def soutenance_detail(request, id):
    soutenance = Soutenance.objects.get(id=id)
    
    if request.headers.get('accept') == 'application/json':
        # Si l'accept header est 'application/json', retourner les données en JSON
        soutenance_json = model_to_dict(soutenance)
        return JsonResponse(soutenance_json)
    else:
        # Sinon, retourner le rendu du template HTML
        return render(request, 'soutenance_api/soutenances_detail.html', {'soutenance': soutenance})


@login_required
def soutenance_update(request, id):
    soutenance = get_object_or_404(Soutenance, id=id)
    if request.method == 'POST':
        data = request.POST.copy()
        data['superviseur'] = data.get('superviseur') or None
        data['etudiant'] = data.get('etudiant') or None
        serializer = SoutenanceSerializer(soutenance, data=data)
        if serializer.is_valid():
            serializer.save()
            return redirect('soutenance-list')
        else:
            return JsonResponse(serializer.errors, status=400)
        
        
@login_required
def soutenance_delete(request, id):
    soutenance = get_object_or_404(Soutenance, id=id)
    if request.method == 'POST':
        soutenance.delete()
        return redirect('soutenance-list')
    
@login_required
def user_list(request):
    users = CustomUser.objects.all()
    return render(request, 'user/user_list.html', {'users': users})

@login_required
def soutenances_utilisateur(request):
    user = request.user  # Récupère l'utilisateur connecté
    if user.role == 'student':
        soutenances = Soutenance.objects.filter(etudiant=user)
    elif user.role == 'supervisor':
        soutenances = Soutenance.objects.filter(superviseur=user)
    else:
        soutenances = None  # Gérer le cas où l'utilisateur n'a pas de soutenances associées
    
    if request.method == 'POST':
        form = SoutenanceForm(request.POST, request.FILES)
        if form.is_valid():
            soutenance = form.save(commit=False)
            soutenance.etudiant = user
            soutenance.save()
            return redirect('soutenances_utilisateur')  # Redirection vers la même page après soumission
    else:
        form = SoutenanceForm()
    
    context = {
        'soutenances': soutenances,
        'role': user.role,  # Ajouter le rôle de l'utilisateur au contexte pour le template
        'form': form,  # Ajouter le formulaire au contexte
    }
    return render(request, 'soutenance/soutenances_utilisateur.html', context)



@login_required
def upload_pdf(request, soutenance_id):
    soutenance = get_object_or_404(Soutenance, pk=soutenance_id)

    if request.method == 'POST':
        pdf_file = request.FILES.get('pdf_file')
        if pdf_file:
            soutenance.pdf_file = pdf_file
            soutenance.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': 'Aucun fichier PDF fourni.'}, status=400)

    return JsonResponse({'success': False, 'error': 'Méthode de requête non valide.'}, status=405)


@login_required
def delete_pdf(request, soutenance_id):
    soutenance = get_object_or_404(Soutenance, pk=soutenance_id)

    if request.method == 'POST':
        if soutenance.pdf_file:
            soutenance.pdf_file.delete(save=True)
            messages.success(request, 'Fichier PDF supprimé avec succès.')
    
    return redirect('soutenances-utilisateur')  # Redirection vers la liste des soutenances de l'utilisateur

def download_pdf(request, soutenance_id):
    soutenance = get_object_or_404(Soutenance, pk=soutenance_id)
    # Assurez-vous que votre modèle Soutenance a un champ pdf_file
    if soutenance.pdf_file:
        # Remplacez 'chemin/vers/votre/fichier.pdf' par le chemin réel de votre fichier PDF
        with open(soutenance.pdf_file.path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/pdf')
            response['Content-Disposition'] = 'inline; filename=' + soutenance.pdf_file.name
            return response
    else:
        return HttpResponse("Fichier PDF non trouvé", status=404)