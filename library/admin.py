from django.contrib import admin
from .models import Fournisseur, Livre, Client, Emprunt

admin.site.register(Fournisseur)
admin.site.register(Livre)
admin.site.register(Client)
admin.site.register(Emprunt)
