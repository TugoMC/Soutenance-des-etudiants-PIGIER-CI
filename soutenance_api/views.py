from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Soutenance
from django.forms.models import model_to_dict
from .serializers import SoutenanceSerializer
from authapp.models import CustomUser  
from django.contrib.auth.decorators import login_required
from .forms import SoutenanceForm
from django.contrib import messages
from django.http import HttpResponse
from django.db.models import Q


@login_required
def soutenance_list(request):
    if request.method == 'POST':
        form = SoutenanceForm(request.POST, request.FILES)
        if form.is_valid():
            soutenance = form.save()
            membres_jury_ids = request.POST.getlist('membres_jury')
            soutenance.membres_jury.set(membres_jury_ids)
            return redirect('soutenance-list')
        else:
            return JsonResponse(form.errors, status=400)

    soutenances = Soutenance.objects.all()
    superviseurs = CustomUser.objects.filter(role=CustomUser.SUPERVISEUR)
    etudiants = CustomUser.objects.filter(role=CustomUser.ETUDIANT)
    membres_jury = CustomUser.objects.filter(role=CustomUser.MEMBRE_JURY)

    context = {
        'soutenances': soutenances,
        'superviseurs': superviseurs,
        'etudiants': etudiants,
        'membres_jury': membres_jury,
        'HEURE_CHOICES': Soutenance.HEURE_CHOICES,
        'form': SoutenanceForm(),
    }
    return render(request, 'soutenance_api/soutenances_list.html', context)


@login_required
def soutenance_detail(request, id):
    soutenance = Soutenance.objects.get(id=id)
    
    if request.headers.get('accept') == 'application/json':
        
        soutenance_json = model_to_dict(soutenance)
        return JsonResponse(soutenance_json)
    else:
        
        return render(request, 'soutenance_api/soutenances_detail.html', {'soutenance': soutenance})


@login_required
def soutenance_update(request, id):
    soutenance = get_object_or_404(Soutenance, id=id)
    
    if request.method == 'POST' or request.method == 'PUT':  
        form = SoutenanceForm(request.POST, request.FILES, instance=soutenance)
        if form.is_valid():
            soutenance = form.save(commit=False)
            soutenance.save()
            form.save_m2m()  
            return redirect('soutenance-list')
        else:
            return JsonResponse(form.errors, status=400)
    else:
        form = SoutenanceForm(instance=soutenance)
        superviseurs = CustomUser.objects.filter(role=CustomUser.SUPERVISEUR)
        etudiants = CustomUser.objects.filter(role=CustomUser.ETUDIANT)
        membres_jury = CustomUser.objects.filter(role=CustomUser.MEMBRE_JURY)

        context = {
            'form': form,
            'superviseurs': superviseurs,
            'etudiants': etudiants,
            'membres_jury': membres_jury,
            'soutenance': soutenance,
        }
        return render(request, 'soutenance_api/soutenances_list.html', context)


@login_required
def soutenance_delete(request, id):
    soutenance = get_object_or_404(Soutenance, id=id)
    if request.method == 'POST':
        soutenance.delete()
        return redirect('soutenance-list')
    
@login_required
def user_list(request):
    query = request.GET.get('query', '')  
    filiere = request.GET.get('filiere', '')  

   
    users = CustomUser.objects.all()

   
    if query:
        users = users.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(username__icontains=query)
        )

    
    if filiere:
        users = users.filter(filiere__icontains=filiere)

    context = {
        'users': users,
        'query': query,
        'filiere': filiere,
    }
    return render(request, 'user/user_list.html', context)


@login_required
def soutenances_utilisateur(request):
    user = request.user  

    if user.role == CustomUser.ETUDIANT:
        soutenances = Soutenance.objects.filter(etudiant=user)
    elif user.role == CustomUser.SUPERVISEUR:
        soutenances = Soutenance.objects.filter(superviseur=user)
    elif user.role == CustomUser.MEMBRE_JURY:
        soutenances = Soutenance.objects.filter(membres_jury=user)
    else:
        soutenances = None  
    
    if request.method == 'POST':
        form = SoutenanceForm(request.POST, request.FILES)
        if form.is_valid():
            soutenance = form.save(commit=False)
            if user.role == CustomUser.ETUDIANT:
                soutenance.etudiant = user
            elif user.role == CustomUser.SUPERVISEUR:
                soutenance.superviseur = user
            soutenance.save()
            return redirect('soutenances_utilisateur')
    else:
        form = SoutenanceForm()
    
    context = {
        'soutenances': soutenances,
        'role': user.role, 
        'form': form, 
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
    
    return redirect('soutenances-utilisateur')  

def download_pdf(request, soutenance_id):
    soutenance = get_object_or_404(Soutenance, pk=soutenance_id)
   
    if soutenance.pdf_file:
       
        with open(soutenance.pdf_file.path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/pdf')
            response['Content-Disposition'] = 'inline; filename=' + soutenance.pdf_file.name
            return response
    else:
        return HttpResponse("Fichier PDF non trouvé", status=404)