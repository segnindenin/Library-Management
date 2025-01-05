from PIL import Image
from django.db import models
from django.forms import ValidationError

class Fournisseur(models.Model):
    id_fournisseur = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=255)
    adresse = models.TextField()
    telephone = models.CharField(max_length=15)

    def __str__(self):
        return self.nom

class Auteur(models.Model):
    id_auteur = models.AutoField(primary_key=True)
    nom_auteur = models.CharField(max_length=255)
    prenom_auteur = models.CharField(max_length=255)
    date_naissance = models.DateField()
    date_deces = models.DateField(blank=True, null=True)
    nationalite = models.CharField(max_length=255)
    def __str__(self):
        return f"{self.prenom_auteur} {self.nom_auteur}"
    
class Livre(models.Model):
    isbn = models.CharField(primary_key=True, max_length=13)  # ISBN est l'identifiant unique
    titre = models.CharField(max_length=255)
    auteur = models.ManyToManyField(Auteur, related_name='LivreAuteur', ) 
    editeur = models.CharField(max_length=255)
    classification = models.CharField(max_length=50)
    date_achat = models.DateField()
    prix_achat = models.DecimalField(max_digits=10, decimal_places=2)
    quantite = models.PositiveIntegerField()
    couverture = models.ImageField(upload_to='couvertures/', blank=True, null=True)
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.CASCADE,  related_name='achats', null=True)  
    def save(self, *args, **kwargs):
        """Redimensionne l'image avant de la sauvegarder."""
        super().save(*args, **kwargs)
        if self.couverture:
            img = Image.open(self.couverture.path)
            # Redimensionne l'image à 700x900
            output_size = (700, 900)
            img = img.resize(output_size, Image.LANCZOS)
            img.save(self.couverture.path)
    def __str__(self):
        return self.titre
    # def clean(self):
    #     super().clean()
    #     if not self.auteur.exists():  # Vérifie qu'au moins un auteur est associé
    #         raise ValidationError("Un livre doit avoir au moins un auteur.")
    

class Client(models.Model):
    n_cni_reci = models.CharField(primary_key=True, max_length=13)
    nom = models.CharField(max_length=255)
    prenom = models.CharField(max_length=255)
    adresse = models.TextField()
    telephone = models.CharField(max_length=15)
    def __str__(self):
        return f"{self.prenom} {self.nom}"

class Emprunt(models.Model):
    id_emprunt = models.AutoField(primary_key=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="emprunts")
    date_emprunt = models.DateField()
    date_retour_prevue = models.DateField()
    etat = models.CharField(max_length=20, choices=[('emprunté', 'Emprunté'), ('non rendu', 'Non Rendu')])
    livres = models.ManyToManyField(Livre, related_name='EmpruntLivre', ) 

    def save(self, *args, **kwargs):
        if self.client.emprunts.exists() and self.client.emprunts.all().count() >= 3:
            raise ValidationError("Un client ne peut pas emprunter plus de 3 livres.")
        else:
            super().save(*args, **kwargs)
    def __str__(self):
        return f"Emprunt {self.id_emprunt} - {self.client}"
