from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('materiali/', views.MaterialiView.as_view(), name='materiali'),
	path('movimenti/', views.MovimentiView.as_view(), name='movimenti'),
	path('materiale_detail/<int:pk>', views.MaterialeDetail.as_view(), name='materiale_view'),
	path('movimento_detail/<int:pk>', views.MovimentoDetail.as_view(), name='movimento_view'),
	path('modifica_materiale/<int:pk>/', views.modifica_materiale, name='modifica_materiale'),
	path('modifica_materiale/', views.ModificaMaterialeView.as_view(), name='lista_modifica_materiale'),
]