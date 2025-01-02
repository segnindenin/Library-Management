from tkinter import Image
from django.db import models
from django.forms import ValidationError

class Fournisseur(models.Model):
    id_fournisseur = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=255)
    adresse = models.TextField()
    telephone = models.CharField(max_length=15)

    def __str__(self):
        return self.nom

class Livre(models.Model):
    isbn = models.CharField(primary_key=True, max_length=13)  # ISBN est l'identifiant unique
    titre = models.CharField(max_length=255)
    auteur = models.CharField(max_length=255)
    editeur = models.CharField(max_length=255)
    classification = models.CharField(max_length=50)
    date_achat = models.DateField()
    prix_achat = models.DecimalField(max_digits=10, decimal_places=2)
    quantite = models.PositiveIntegerField()
    fournisseurs = models.ManyToManyField(Fournisseur, related_name='LivreFournisseur', blank=True,)  # Relation N-N via une table intermédiaire
    def __str__(self):
        return self.titre
    def save(self, *args, **kwargs):
        """Redimensionne l'image avant de la sauvegarder."""
        super().save(*args, **kwargs)
        if self.couverture:
            img = Image.open(self.couverture.path)
            # Redimensionne l'image à 700x900
            output_size = (700, 900)
            img = img.resize(output_size, Image.ANTIALIAS)
            img.save(self.couverture.path)

class Client(models.Model):
    id_client = models.AutoField(primary_key=True)
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
    livres = models.ManyToManyField(Livre, related_name='EmpruntLivre', blank=True,)  # Relation N-N via une table intermédiaire

    def save(self, *args, **kwargs):
        if self.client.emprunts.count() >= 3:
            raise ValidationError("Un client ne peut pas emprunter plus de 3 livres.")
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"Emprunt {self.id_emprunt} - {self.client}"
