from django.shortcuts import render, redirect
from .models import Livre
from .forms import LivreForm

def home(request):
    return render(request, 'index.html')

def auteurs(request):
    return render(request, 'auteurs.html') 

def adherent_inactif(request):
    return render(request, 'adherent_inactif.html')  

def adherent_list(request):
    return render(request, 'adherent_list.html')  
 
def book_emprunt(request):
    return render(request, 'book_emprunt.html')  

def book_list(request):
    if request.method == 'POST':
        form = LivreForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = LivreForm()
    return render(request, 'book_list.html', {'form': form})

def history(request):
    return render(request, 'history.html')

