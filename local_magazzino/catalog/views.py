from django.shortcuts import render

# Create your views here.

from .models import Materiale, Movimenti
from django.views import generic


class MaterialeView(generic.ListView):
	model = Materiale
	context_object_name = 'materiale_list'


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
