from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Emprunt, Livre
from django.db.models import Sum

@receiver(m2m_changed, sender=Emprunt.livres.through)
def update_livre_disponible(sender, instance, action, **kwargs):
    if action in ['post_add', 'post_remove', 'post_clear']:
        print(f"Signal déclenché pour {instance}")
        for livre in instance.livres.all():
            total_emprunte = livre.LivreEmprunted.filter(etat='emprunté').count()
            total_achete = livre.achats.aggregate(Sum('quantite'))['quantite__sum'] or 0
            livre.total_disponible = total_achete - total_emprunte
            livre.save()
