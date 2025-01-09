from django.contrib import messages
from django.db.models import Count
from django.shortcuts import render, redirect
from library.models import *
from .forms import *


def home(request):
    livres = Livre.objects.prefetch_related('achats').all()
    livres_dispo = Livre.objects.all()
    fournisseurs = Fournisseur.objects.all()
    classifications = {}
    total_books = 0
    total_cost = 0
    for livre in livres:
        classification = livre.classification
        nbre_livre = livre.nbre_livre_total
        cost = sum(achat.prix_achat * achat.quantite for achat in livre.achats.all())
        if classification not in classifications:
            classifications[classification] = {'nbre_livre': 0, 'cost': 0}
        classifications[classification]['nbre_livre'] += nbre_livre
        classifications[classification]['cost'] += cost
        total_books += nbre_livre
        total_cost += cost
    for classification in classifications:
        classifications[classification]['per_biblio'] = (
            classifications[classification]['nbre_livre'] / total_books * 100 if total_books > 0 else 0
        )
    first_four_classifications = list(classifications.items())[:4]
    remaining_classifications = list(classifications.items())[4:]
    return render(request, 'index.html', {
        'first_four_classifications': first_four_classifications,
        'remaining_classifications': remaining_classifications,
        'total_books': total_books,
        'total_cost': total_cost,
        'livres_dispo': livres_dispo,
        'fournisseurs': fournisseurs
    })

    
def auteurs(request):
    auteurs = Auteur.objects.all()
    auteurs_livres = []
    for auteur in auteurs:
        livres = auteur.LivreAuteur.all()
        auteurs_livres.append((auteur, livres))
    total_livres = Achat.objects.count()
    livres_empruntes = Emprunt.objects.filter(etat__in=['emprunté', 'non rendu']).count()
    pourcentage_livres_empruntes = round((livres_empruntes / total_livres * 100), 2) if total_livres > 0 else 0
    return render(request, 'auteurs.html', {
        'auteurs_livres': auteurs_livres,
        'nbres_auteurs': auteurs.count(),
        'nbres_livres': total_livres,
        'nbres_adherents': Client.objects.count(),
        'nbres_exemplaires': Achat.objects.count(),
        'nbres_livres_empruntes': livres_empruntes,
        'pourcentage_livres_empruntes': pourcentage_livres_empruntes
    })

def add_auteur(request):
    if request.method == 'POST':
        form = AuteurForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Auteur mis à jour avec succès.")
            return redirect('auteurs')
    else:
        form = AuteurForm()
    return render(request, 'auteurs.html', {'form': form}) 

def adherent_inactif(request):
    inactifs = Client.objects.filter(emprunts__isnull=True)
    return render(request, 'adherent_inactif.html', {'inactifs': inactifs})

def adherent_list(request):
    adherents = Client.objects.all()
    return render(request, 'adherent_list.html', {'adherents': adherents})

def update_adherent(request, adherent_id):
    adherent = Client.objects.get(id=adherent_id)
    if request.method == 'POST':
        form = AdherentForm(request.POST, instance=adherent)
        if form.is_valid():
            form.save()
            messages.success(request, "Lecteur mis à jour avec succès.")
            return redirect('adherent-list')
        else:
            messages.error(request, "Erreur lors de la mise à jour de l'adhérent.")
    else:
        form = AdherentForm(instance=adherent)
    return render(request, 'update_adherent.html', {'form': form, 'adherent': adherent})

def delete_adherent(request, adherent_id):
    adherent = Client.objects.get(id=adherent_id)
    if request.method == 'POST':
        adherent.delete()
        messages.success(request, "Lecteur supprimé avec succès.")
        return redirect('adherent-list')
    return render(request, 'delete_adherent.html', {'adherent': adherent})

def add_adherent(request):
    if request.method == 'POST':
        form = AdherentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Lecteur ajouté avec succès.")
            return redirect('adherent-list')
    else:
        form = AdherentForm()
    return render(request, 'adherent_list.html', {'form': form})

def book_emprunt(request):
    clients = Client.objects.all()
    livres = Livre.objects.all()
    form = EmpruntForm()
    return render(request, 'book_emprunt.html', {
        'clients': clients,
        'emprunts': Emprunt.objects.all(),
        'livres': livres,
        'form': form
    })

def add_emprunt(request):
    clients = Client.objects.all()
    livres = Livre.objects.all()
    if request.method == 'POST':
        form = EmpruntForm(request.POST)
        if form.is_valid():
            client = form.cleaned_data['client']
            total_livres_empruntes = (
                client.emprunts.filter(etat='emprunté')
                .annotate(nb_livres=Count('livres'))
                .aggregate(total=Count('livres'))['total'] or 0
            )
            livres_dans_nouvel_emprunt = form.cleaned_data['livres'].count()
            if total_livres_empruntes + livres_dans_nouvel_emprunt > 3:
                messages.error(
                    request,
                    f"Ce client ne peut pas emprunter plus de 3 livres avec l'état 'emprunté'."
                )
            else:
                emprunt = form.save(commit=False)
                emprunt.save()
                form.save_m2m()
                for livre in form.cleaned_data['livres']:
                    LivreEmprunt.objects.create(
                        id_emprunt=emprunt,
                        isbn_livre=livre,
                        condition='bonne'
                    )
                messages.success(request, "Emprunt enregistré avec succès.")
                return redirect('book-emprunt')
    else:
        form = EmpruntForm()
    return render(request, 'book_emprunt.html', {
        'form': form,
        'clients': clients,
        'livres': livres,
    })

def book_list(request):
    form = LivreForm()
    return render(request, 'book_list.html', {
        'fournisseurs':Fournisseur.objects.all(),
        'auteurs':Auteur.objects.all(),
        'livres': Livre.objects.all(),
        'form': form})

def add_book(request):
    if request.method == 'POST':
        form = LivreForm(request.POST, request.FILES)
        if form.is_valid():
            livre = form.save(commit=False) 
            livre.save() 
            form.save_m2m()
            messages.success(request, "Livre ajouté avec succès.")
            return redirect('book-list')
        else:
            messages.error(request, "Erreur lors de l'ajout du livre. Veuillez vérifier les informations fournies.")
    else:
        form = LivreForm()
    return render(request, 'book_list.html', {
        'fournisseurs': Fournisseur.objects.all(),
        'auteurs': Auteur.objects.all(),
        'livres': Livre.objects.all(),
        'form': form,
    })

def add_fournisseur(request):
    if request.method == 'POST':
        form = FournisseurForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Fournisseur ajouté avec succès.")
            return redirect('home')
    else:
        form = FournisseurForm()
    return render(request, 'index.html', {'form': form})

def new_purchase(request):
    if request.method == 'POST':
        form = AchatsForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Achat ajouté avec succès.")
            return redirect('home')
    else:
        form = FournisseurForm()
    return render(request, 'index.html', {'form': form})

def history(request):
    return render(request, 'history.html')
