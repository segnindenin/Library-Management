from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('auteurs/', views.auteurs, name="auteurs"),
    path('add-auteur/', views.add_auteur, name="add-auteur"),
    path('adherent-inactif/', views.adherent_inactif, name="adherent-inactif"),
    path('adherent-list/', views.adherent_list, name="adherent-list"),
    path('add-adherent/', views.add_adherent, name='add-adherent'),
    path('book-emprunt/', views.book_emprunt, name="book-emprunt"),
    path('add-emprunt/', views.add_emprunt, name='add-emprunt'),
    path('book-list/', views.book_list, name="book-list"),
    path('add-book/', views.add_book, name='add-book'),
    path('add-fournisseur/', views.add_fournisseur, name='add-fournisseur'),
    path('history/', views.history, name="history"),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)