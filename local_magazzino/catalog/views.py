from django.http import HttpResponse
from django.shortcuts import render

from django.urls import reverse

# Create your views here.

from .models import Materiale, Movimenti
from django.views import generic


class MaterialiView(generic.ListView):
	model = Materiale
	context_object_name = 'materiale_list'


class MaterialeDetail(generic.DetailView):
	model = Materiale
	context_object_name = "materiale_detail"
	template_name = "catalog/materiale_detail.html"


class MovimentiView(generic.ListView):
	model = Movimenti
	context_object_name = 'movimenti_list'


class MovimentoDetail(generic.DetailView):
	model = Movimenti
	context_object_name = "movimento_detail"
	template_name = "catalog/movimento_detail.html"


def index(request):
	"""View function for home page of site."""
	num_materiali = Materiale.objects.all().count()
	num_movimenti = Movimenti.objects.all().count()

	context = {
		'num_materiali': num_materiali,
		'num_movimenti': num_movimenti,
	}

	# Render the HTML template index.html with the data in the context variable
	return render(request, 'index.html', context=context)

#
# def materiali(request):
# 	return render(request, "catalog/materiale_list.html")
#
#
# def materiale_view(request):
# 	id_materiale = Materiale.id_materiale
#
# 	return render(request, "catalog/materiale_detail.html", context=id_materiale)
#
#
# def movimenti(request):
# 	return render(request, "catalog/movimenti_list.html")
