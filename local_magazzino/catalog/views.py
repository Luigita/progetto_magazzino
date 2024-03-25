from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .forms import ModificaMaterialeForm

# Create your views here.

from .models import Materiale, Movimenti
from django.views import generic


class MaterialiView(LoginRequiredMixin, generic.ListView):
	model = Materiale
	context_object_name = 'materiale_list'


class ModificaMaterialeView(LoginRequiredMixin, generic.ListView):
	model = Materiale
	context_object_name = 'lista_modifica_materiale'
	template_name = "catalog/lista_modifica_materiale.html"


class MaterialeDetail(generic.DetailView):
	model = Materiale
	context_object_name = "materiale_detail"
	template_name = "catalog/materiale_detail.html"


class MovimentiView(LoginRequiredMixin, generic.ListView):
	model = Movimenti
	context_object_name = 'movimenti_list'


class MovimentoDetail(generic.DetailView):
	model = Movimenti
	context_object_name = "movimento_detail"
	template_name = "catalog/movimento_detail.html"


@login_required  # è usato per vedere se l'utente è loggato
def index(request):
	"""View function for home page of site."""
	num_materiali = Materiale.objects.all().count()
	num_movimenti = Movimenti.objects.all().count()

	num_visits = request.session.get("num_visits", 0)
	request.session["num_visits"] = num_visits + 1

	context = {
		'num_materiali': num_materiali,
		'num_movimenti': num_movimenti,
		"num_visits": num_visits,
	}

	# Render the HTML template index.html with the data in the context variable
	return render(request, 'index.html', context=context)


@login_required
def modifica_materiale(request, pk):
	instance = get_object_or_404(Materiale, pk=pk)

	if request.method == "POST":
		form = ModificaMaterialeForm(request.POST)

		if form.is_valid():
			instance.descrizione = form.clean_descrizione()
			instance.unita_misura = form.clean_unita_misura()
			instance.sottoscorta = form.clean_sottoscorta()
			instance.save()

			# TODO: DA AGGIUNGERE QUALCOSA IN REVERSE, al momento ritorna la pagina web relativa alla lista dei materiali
			return HttpResponseRedirect(reverse("materiali"))
	else:
		proposed_unita_misura = instance.unita_misura
		form = ModificaMaterialeForm(initial={"unita_misura": proposed_unita_misura})

	context = {
		"form": form,
		"instance": instance,
	}

	return render(request, "catalog/modifica_materiale.html", context)

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
