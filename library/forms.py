from django import forms
from library.models import *

class LivreForm(forms.ModelForm):
    class Meta:
        model = Livre
        fields = ['isbn', 'titre', 'auteur', 'classification', 'couverture']
        widgets = {
            'auteur': forms.CheckboxSelectMultiple(), 
        }

class FournisseurForm(forms.ModelForm):
    class Meta:
        model = Fournisseur
        fields = '__all__'

class AdherentForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['n_cni_reci', 'nom', 'prenom', 'adresse', 'telephone']

class AuteurForm(forms.ModelForm):
    class Meta:
        model = Auteur
        fields = '__all__'

class EmpruntForm(forms.ModelForm):
    class Meta:
        model = Emprunt
        fields = ['client', 'date_emprunt', 'date_retour_prevue', 'etat', 'livres']
        widgets = {
            'livres': forms.CheckboxSelectMultiple(), 
        }

class AchatsForm(forms.ModelForm):
    class Meta:
        model = Achat
        fields = ['isbn_livre', 'fournisseur', 'date_achat', 'prix_achat', 'quantite', 'editeur']

class LivreEmpruntForm(forms.ModelForm):
    class Meta:
        model = LivreEmprunt
        fields = '__all__'