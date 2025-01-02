from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('auteurs/', views.auteurs, name="auteurs"),
    path('adherent-inactif/', views.adherent_inactif, name="adherent-inactif"),
    path('adherent-list/', views.adherent_list, name="adherent-list"),
    path('book-emprunt/', views.book_emprunt, name="book-emprunt"),
    path('book-list/', views.book_list, name="book-list"),
    path('history/', views.history, name="history"),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)