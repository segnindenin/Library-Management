from django import forms
from .models import Auteur, Emprunt, Livre, Fournisseur, Client

class LivreForm(forms.ModelForm):
    class Meta:
        model = Livre
        fields = ['isbn', 'titre', 'auteur', 'editeur', 'classification', 'date_achat', 'prix_achat', 'quantite', 'couverture','fournisseur', ]
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
        fields = '__all__'

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
