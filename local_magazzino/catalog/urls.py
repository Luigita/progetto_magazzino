from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('materiale/', views.MaterialeView.as_view(), name='materiale'),
]