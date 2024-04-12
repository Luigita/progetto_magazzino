from django.urls import path
# from django_filters.views import FilterView

from . import views
from .models import Materiale

urlpatterns = [
	path('', views.index, name='index'),
	path('materiali/', views.MaterialiView.as_view(), name='materiali'),
	path('movimenti/', views.MovimentiView.as_view(), name='movimenti'),
	path('materiale_detail/<int:pk>', views.MaterialeDetail.as_view(), name='materiale_view'),
	path('movimento_detail/<int:pk>', views.MovimentoDetail.as_view(), name='movimento_view'),

	path("genera_etichetta/<int:pk>", views.genera_etichetta, name="genera_etichetta"),

	path('aggiungi_materiale/', views.aggiungi_materiale, name='aggiungi_materiale'),

	path('lista_modifica_materiale/modifica_materiale/<int:pk>/', views.modifica_materiale, name='modifica_materiale'),
	path('lista_modifica_materiale/', views.ModificaMaterialeView.as_view(), name='lista_modifica_materiale'),

	path('lista_cancella_materiale/cancella_materiale/<int:pk>/', views.cancella_materiale, name='cancella_materiale'),
	path('lista_cancella_materiale/', views.CancellaMaterialeView.as_view(), name='lista_cancella_materiale'),

	path('carico/', views.carico_materiale, name='carico'),
	path('scarico/', views.scarico_materiale, name='scarico'),
	path('trasferimento/', views.trasferimento_magazzino, name='trasferimento'),
]
