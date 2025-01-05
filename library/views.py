from django.contrib import messages
from django.db.models import Count
from django.shortcuts import render, redirect
from library.models import Auteur, Fournisseur, Livre, Client
from .forms import AuteurForm, EmpruntForm, LivreForm, FournisseurForm, AdherentForm

def home(request):
    livres = Livre.objects.all()
    return render(request, 'index.html', {'livres': livres})

def auteurs(request):
    return render(request, 'auteurs.html')

def add_auteur(request):
    if request.method == 'POST':
        form = AuteurForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('auteurs')
    else:
        form = AuteurForm()
    return render(request, 'auteurs.html', {'form': form}) 

def adherent_inactif(request):
    return render(request, 'adherent_inactif.html')  

def adherent_list(request):
    form = AdherentForm()
    return render(request, 'adherent_list.html', {'form': form})

def add_adherent(request):
    if request.method == 'POST':
        form = AdherentForm(request.POST)
        if form.is_valid():
            form.save()
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
            # Calculer le nombre de livres actuellement empruntés avec l'état "emprunté"
            total_livres_empruntes = (
                client.emprunts.filter(etat='emprunté')
                .annotate(nb_livres=Count('livres'))
                .aggregate(total=Count('livres'))['total'] or 0
            )
            # Nombre de livres dans le nouvel emprunt
            livres_dans_nouvel_emprunt = form.cleaned_data['livres'].count()
            # Validation : total des livres empruntés (avec "emprunté") doit être inférieur à 4
            if total_livres_empruntes + livres_dans_nouvel_emprunt > 3:
                messages.error(
                    request,
                    f"Ce client ne peut pas emprunter plus de 3 livres avec l'état 'emprunté'."
                )
            else:
                emprunt = form.save(commit=False)
                emprunt.save()
                form.save_m2m()  # Sauvegarder les relations ManyToMany
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
    auteurs = Auteur.objects.all()
    fournisseur = Fournisseur.objects.all()
    return render(request, 'book_list.html', {
        'fournisseur':fournisseur,
        'auteurs':auteurs,
        'form': form})

def add_book(request):
    auteurs = Auteur.objects.all()
    fournisseurs = Fournisseur.objects.all()
    if request.method == 'POST':
        form = LivreForm(request.POST, request.FILES)
        if form.is_valid():
            livre = form.save(commit=False)  # Ne sauvegarde pas encore en base
            livre.save()  # Sauvegarde l'objet principal
            form.save_m2m()  # Sauvegarde les relations ManyToMany
            messages.success(request, "Livre ajouté avec succès.")
            return redirect('book-list')
        else:
            messages.error(request, "Erreur lors de l'ajout du livre. Veuillez vérifier les informations fournies.")
    else:
        form = LivreForm()

    return render(request, 'book_list.html', {
        'fournisseur': fournisseurs,
        'auteurs': auteurs,
        'form': form,
    })


def add_fournisseur(request):
    if request.method == 'POST':
        form = FournisseurForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = FournisseurForm()
    return render(request, 'index.html', {'form': form})

def history(request):
    return render(request, 'history.html')
