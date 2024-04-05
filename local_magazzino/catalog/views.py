from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .forms import MaterialeForm, CaricoForm, ModificaMaterialeForm

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
			# instance.unita_misura = form.clean_unita_misura()
			instance.sottoscorta = form.clean_sottoscorta()
			instance.save()

			return HttpResponseRedirect(reverse("lista_modifica_materiale"))
	else:
		proposed_codice = instance.codice
		proposed_descrizione = instance.descrizione
		# proposed_unita_misura = instance.unita_misura
		proposed_sottoscorta = instance.sottoscorta

		form = MaterialeForm(
			initial={
				# "unita_misura": proposed_unita_misura,
				# "codice": proposed_codice,
				'codice': proposed_codice,
				"descrizione": proposed_descrizione,
				"sottoscorta": proposed_sottoscorta
			})

	context = {
		"form": form,
		"instance": instance,
	}

	return render(request, "catalog/modifica_materiale.html", context)


@login_required
def aggiungi_materiale(request):
	if request.method == "POST":

		form = MaterialeForm(request.POST)

		if form.is_valid():
			codice = form.clean_codice()
			descrizione = form.clean_descrizione()
			# unita_misura = form.clean_unita_misura()
			sottoscorta = form.clean_sottoscorta()

			# nuovo_materiale = Materiale(descrizione=descrizione, unita_misura=unita_misura, sottoscorta=sottoscorta)
			nuovo_materiale = Materiale(codice=codice, descrizione=descrizione, sottoscorta=sottoscorta)
			nuovo_materiale.save()
			return HttpResponseRedirect(reverse('materiali'))

	else:

		form = MaterialeForm()

	context = {
		"form": form,
	}

	return render(request, "catalog/aggiungi_materiale.html", context)


# def cancella_materiale(request):


def carico_materiale(request):
	if request.method == "POST":
		form = CaricoForm(request.POST)

		if form.is_valid():
			materiale = form.clean_materiale()
			quantita = form.clean_quantita()
			magazzino = form.clean_magazzino()

			nuovo_carico = Movimenti(materiale=materiale, quantita=quantita, magazzino=magazzino)
			nuovo_carico.save()

			materiale.giacenza += quantita
			materiale.save()

			return HttpResponseRedirect(reverse('movimenti'))

	else:
		form = CaricoForm()

	context = {
		"form": form,
	}

	return render(request, "catalog/carico.html", context)


def scarico_materiale(request):
	if request.method == "POST":
		form = CaricoForm(request.POST)

		if form.is_valid():
			materiale = form.clean_materiale()
			quantita = form.clean_quantita()
			magazzino = form.clean_magazzino()

			nuovo_carico = Movimenti(materiale=materiale, quantita=quantita, magazzino=magazzino)
			nuovo_carico.save()

			materiale.giacenza += quantita
			materiale.save()

			return HttpResponseRedirect(reverse('movimenti'))

	else:
		form = CaricoForm()

	context = {
		"form": form,
	}

	return render(request, "catalog/carico.html", context)
# def carico(request):
# 	if request.method == "POST":
# 		form = CaricoForm(request.POST)
#
# 		if form.is_valid():
# 			pass
# 			return HttpResponseRedirect(reverse('movimenti'))
# 		else
