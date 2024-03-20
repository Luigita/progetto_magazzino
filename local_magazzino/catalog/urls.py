from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('materiali/', views.MaterialiView.as_view(), name='materiali'),
	path('movimenti/', views.MovimentiView.as_view(), name='movimenti'),
	path('materiale_view/<pk>', views.MaterialeDetail.as_view(), name='materiale_view'),
	path('movimento_view/<pk>', views.MovimentoDetail.as_view(), name='movimento_view'),
]
