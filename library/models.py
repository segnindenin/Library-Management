from PIL import Image
from django.db import models
from django.forms import ValidationError
from django.core.validators import RegexValidator
from django.utils import timezone

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
    auteur = models.ManyToManyField(Auteur, related_name='LivreAuteur')
    classification = models.CharField(max_length=50)
    couverture = models.ImageField(upload_to='couvertures/', blank=True, null=True)
    def save(self, *args, **kwargs):
        """Redimensionne l'image avant de la sauvegarder."""
        super().save(*args, **kwargs)
        if self.couverture:
            img = Image.open(self.couverture.path)
            output_size = (700, 900)
            img = img.resize(output_size, Image.LANCZOS)
            img.save(self.couverture.path)
    def __str__(self):
        return self.titre
    @property
    def nbre_livre_total(self):
        return self.achats.aggregate(total=models.Sum('quantite'))['total'] or 0
    @property
    def nbre_livre_dispo(self):
        emprunte = self.EmpruntLivre.aggregate(total=models.Count('id_livre_emprunt'))['total'] or 0
        return self.nbre_livre_total - emprunte

class Achat(models.Model):
    id_achat = models.AutoField(primary_key=True)
    isbn_livre = models.ForeignKey(Livre, on_delete=models.CASCADE, related_name="achats")
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.CASCADE, related_name="achats")
    date_achat = models.DateField(default=timezone.now)
    prix_achat = models.DecimalField(max_digits=10, decimal_places=2)
    quantite = models.PositiveIntegerField()
    editeur = models.CharField(max_length=255)
    def __str__(self):
        return f"{self.isbn_livre} chez {self.fournisseur}"

class Client(models.Model):
    n_cni_reci = models.CharField(primary_key=True, max_length=13)
    nom = models.CharField(max_length=255)
    prenom = models.CharField(max_length=255)
    nbre_livre_emprunte = models.PositiveIntegerField(default=0)
    adresse = models.TextField()
    telephone = models.CharField(
        max_length=14,
        validators=[RegexValidator(
        regex=r'^\d+$', 
        message="Ce champ doit contenir uniquement des chiffres.")],)
    def save(self, *args, **kwargs):
        if self.nbre_livre_emprunte > 3:
            raise ValidationError("Un client ne peut pas emprunter plus de 3 livres.")
        super().save(*args, **kwargs)
    def __str__(self):
        return f"{self.prenom} {self.nom}"

class Emprunt(models.Model):
    id_emprunt = models.AutoField(primary_key=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="emprunts")
    date_emprunt = models.DateField()
    date_retour_prevue = models.DateField()
    etat = models.CharField(max_length=20, choices=[('emprunté', 'Emprunté'), ('non rendu', 'Non Rendu'), ('rendu', 'Rendu')])
    livres = models.ManyToManyField(Livre, related_name='LivreEmprunt')
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.etat in ['emprunté', 'non rendu']:
            self.client.nbre_livre_emprunte += self.livres.count()
            self.client.save()
    def __str__(self):
        return f"Emprunt {self.id_emprunt} - {self.client}"

class LivreEmprunt(models.Model):
    id_livre_emprunt = models.AutoField(primary_key=True)
    id_emprunt = models.ForeignKey(Emprunt, on_delete=models.CASCADE, related_name="EmpruntLivre")
    isbn_livre = models.ForeignKey(Livre, on_delete=models.CASCADE, related_name="EmpruntLivre")
    date_retour_effectif = models.DateField(blank=True, null=True)
    condition = models.CharField(max_length=20, choices=[('bonne', 'Bonne'), ('mauvaise', 'Mauvaise')])
    def __str__(self):
        return f"{self.id_emprunt} - {self.isbn_livre}"
    def save(self, *args, **kwargs):
        if self.date_retour_effectif and not self.pk:
            livre = self.isbn_livre
            livre_dispo = livre.nbre_livre_dispo + 1
            Livre.objects.filter(pk=livre.pk).update(nbre_livre_dispo=livre_dispo)
        super().save(*args, **kwargs)