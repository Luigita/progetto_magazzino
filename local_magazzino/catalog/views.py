from django.contrib.auth import aget_user
from django.http import HttpResponse, HttpResponseRedirect, FileResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.template import RequestContext
from django.urls import reverse
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
import io
# import barcode

from reportlab.graphics.barcode import code128

from django.views.generic.detail import SingleObjectMixin

from .forms import MaterialeForm, MovimentoForm, ModificaMaterialeForm, MaterialeFilter, TrasferimentoForm, \
	MagazzinoForm, ModificaMagazzinoForm

# Create your views here.

from .models import Materiale, Movimenti, Magazzino
from django.views import generic


class MaterialiView(LoginRequiredMixin, generic.ListView):
	model = Materiale
	context_object_name = 'materiale_list'


class ModificaMaterialeView(LoginRequiredMixin, generic.ListView):
	model = Materiale
	context_object_name = 'lista_modifica_materiale'
	template_name = "catalog/lista_modifica_materiale.html"


class CancellaMaterialeView(LoginRequiredMixin, generic.ListView):
	model = Materiale
	context_object_name = 'lista_cancella_materiale'
	template_name = "catalog/lista_cancella_materiale.html"


class MaterialeDetail(LoginRequiredMixin, generic.DetailView):
	model = Materiale
	context_object_name = "materiale_detail"
	template_name = "catalog/materiale_detail.html"


class MagazziniView(LoginRequiredMixin, generic.ListView):
	model = Magazzino
	context_object_name = "magazzino_list"


class ModificaMagazzinoView(LoginRequiredMixin, generic.ListView):
	model = Magazzino
	context_object_name = "lista_modifica_magazzini"
	template_name = "catalog/lista_modifica_magazzini.html"


class MagazzinoDetail(LoginRequiredMixin, generic.DetailView):
	model = Magazzino
	context_object_name = "magazzino_detail"
	template_name = "catalog/magazzino_detail.html"


class MovimentiView(LoginRequiredMixin, generic.ListView):
	model = Movimenti
	context_object_name = 'movimenti_list'


class MovimentoDetail(LoginRequiredMixin, generic.DetailView):
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
			instance.sottoscorta = form.clean_sottoscorta()
			instance.save()

			return HttpResponseRedirect(reverse("lista_modifica_materiale"))
	else:
		proposed_descrizione = instance.descrizione
		proposed_sottoscorta = instance.sottoscorta

		form = ModificaMaterialeForm(
			initial={
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
			articolo = form.clean_articolo()
			taglia = form.clean_taglia()
			descrizione = form.clean_descrizione()
			sottoscorta = form.clean_sottoscorta()

			codice = articolo + str(taglia)

			if Materiale.objects.filter(codice=codice):
				messages.error(request, "Codice non univoco.")
			else:
				nuovo_materiale = Materiale(codice=codice, articolo=articolo, taglia=taglia,
											descrizione=descrizione, sottoscorta=sottoscorta, creatore=request.user)
				nuovo_materiale.save()
				return HttpResponseRedirect(reverse('materiali'))

	else:

		form = MaterialeForm()

	context = {
		"form": form,
	}

	return render(request, "catalog/aggiungi_materiale.html", context)


@login_required
def cancella_materiale(request, pk):
	instance = get_object_or_404(Materiale, pk=pk)
	if instance.delete():
		return render(request, "catalog/conferma_cancellazione.html")
	raise ValueError()


@login_required
def aggiungi_magazzino(request):
	if request.method == "POST":
		form = MagazzinoForm(request.POST)

		if form.is_valid():
			localita = form.clean_localita()
			descrizione = form.clean_descrizione()

			if Magazzino.objects.filter(localita=localita):
				messages.error(request, "Codice non univoco")
			else:
				nuovo_magazzino = Magazzino(localita=localita, descrizione=descrizione)
				nuovo_magazzino.save()
				return HttpResponseRedirect(reverse('magazzini'))

	else:
		form = MagazzinoForm()

	context = {
		"form": form,
	}

	return render(request, "catalog/aggiungi_magazzino.html", context)


@login_required
def modifica_magazzino(request, pk):
	instance = get_object_or_404(Magazzino, pk=pk)

	if request.method == "POST":
		form = ModificaMagazzinoForm(request.POST)

		if form.is_valid():
			instance.descrizione = form.clean_descrizione()
			instance.save()

			return HttpResponseRedirect(reverse('lista_modifica_magazzini'))

	else:
		proposed_descrizione = instance.descrizione

		form = ModificaMagazzinoForm(
			initial={
				"descrizione": proposed_descrizione
			}
		)

	context = {
		"form": form,
		"instance": instance,
	}

	return render(request, "catalog/modifica_magazzino.html", context)


@login_required
def carico_materiale(request):
	if request.method == "POST":
		form = MovimentoForm(request.POST)

		if form.is_valid():
			materiale = form.clean_materiale()
			quantita = form.clean_quantita()
			magazzino = form.clean_magazzino()

			materiale_codice = get_object_or_404(Materiale, codice=materiale)
			# crea il movimento
			nuovo_carico = Movimenti(materiale=materiale_codice, quantita=quantita, magazzino=magazzino)
			nuovo_carico.save()

			# TODO: FARE IN MODO CHE SE ESISTE GIA MODIFICA LA GIACENZA
			# materiale.magazzini_giacenza.filter(new_materiale=materiale, new_magazzino=magazzino.localita)
			# materiale.magazzini_giacenza.set(magazzino, through_defaults={"giacenza": nuovo_carico.quantita})
			# materiale.magazzini_giacenza.update(giacenza=materiale.magazzini_giacenza.giacenza + nuovo_carico.quantita)

			# TODO: SI POTREBBE RIMUOVERE COME IMPLEMENTAZIONE- da togliere, ora solo per debug
			# print(materiale.get_giacenza_magazzino(magazzino))

			# aggiorna il materiale aggiungendo la quantita caricata alla quantita in giacenza
			materiale_codice.carico_materiale(quantita)

			return HttpResponseRedirect(reverse('movimenti'))

	else:
		proposed_magazzino = Magazzino.objects.get(localita__exact="NAP")

		form = MovimentoForm(
			initial={
				"magazzino": proposed_magazzino
			}
		)

	context = {
		"form": form,
	}

	return render(request, "catalog/carico.html", context)


@login_required
def scarico_materiale(request):
	if request.method == "POST":
		form = MovimentoForm(request.POST)

		if form.is_valid():
			materiale = form.clean_materiale()
			quantita = form.clean_quantita()
			magazzino = form.clean_magazzino()

			materiale_db = get_object_or_404(Materiale, codice=materiale)

			errore_quantita = materiale_db.giacenza

			materiale_db.giacenza -= quantita

			if materiale_db.giacenza >= 0:
				nuovo_scarico = Movimenti(materiale=materiale_db, quantita=-quantita, magazzino=magazzino)
				nuovo_scarico.save()
				materiale_db.save()

				return HttpResponseRedirect(reverse('movimenti'))

			else:
				# TODO: METTERE UN REDIRECT A UNA PAGINA DI ERRORE CHE TI PERMETTE POI DI TORNARE INDIETRO
				return HttpResponse("Errore quantita, sono disponibili solo " + str(errore_quantita) + " pezzi")

	else:
		proposed_magazzino = Magazzino.objects.get(localita__exact="MIL")
		proposed_quantita = 1

		form = MovimentoForm(
			initial={
				"magazzino": proposed_magazzino,
				"quantita": proposed_quantita
			}
		)

	context = {
		"form": form,
	}

	return render(request, "catalog/scarico.html", context)


@login_required
def trasferimento_magazzino(request):
	if request.method == "POST":
		form = TrasferimentoForm(request.POST)

		if form.is_valid():
			materiale = form.clean_materiale()
			quantita = form.clean_quantita()

			errore_quantita = materiale.giacenza

			if (materiale.giacenza - quantita) >= 0:
				materiale.giacenza -= quantita
				nuovo_scarico = Movimenti(materiale=materiale, quantita=-quantita, magazzino=Magazzino.objects.get(pk=1))
				nuovo_scarico.save()
				materiale.save()

				nuovo_carico = Movimenti(materiale=materiale, quantita=quantita, magazzino=Magazzino.objects.get(pk=2))
				nuovo_carico.save()

				# print(materiale.get_giacenza_magazzino(Magazzino.objects.get(pk=1)))
				# print(materiale.get_giacenza_magazzino(Magazzino.objects.get(pk=2)))

				materiale.carico_materiale(quantita)

				return HttpResponseRedirect(reverse('movimenti'))

			else:
				# TODO: METTERE UN REDIRECT A UNA PAGINA DI ERRORE CHE TI PERMETTE POI DI TORNARE INDIETRO
				return HttpResponse("Errore quantita, sono disponibili solo " + str(errore_quantita) + " pezzi")

	else:
		form = TrasferimentoForm()

	context = {
		"form": form,
	}

	return render(request, "catalog/carico.html", context)


@login_required
def cerca_materiale(request):
	# if request.method == "GET":
	#
	# 	form = MaterialeFilter(request.GET)
	#
	# 	if form.is_valid():
	#
	# 		return HttpResponseRedirect(reverse('materiali'))
	#
	# else:

	f = MaterialeFilter(request.GET, queryset=Materiale.objects.all())
	return render(request, 'catalog/materiale_filter.html', {'filter': f})


def genera_etichetta(request, pk):
	instance = get_object_or_404(Materiale, pk=pk)

	buffer = io.BytesIO()

	# Create the PDF object, using the buffer as its "file."
	p = canvas.Canvas(buffer)

	# Draw things on the PDF. Here's where the PDF generation happens.
	# See the ReportLab documentation for the full list of functionality.
	# p.drawString(100, 100, (instance.codice))

	barcode = code128.Code128(instance.codice, barHeight=10 * mm, barWidth=1.2)
	barcode.drawOn(p, 10, 100)
	p.drawString(20, 140, ("Codice materiale: " + instance.codice))

	p.showPage()
	p.save()

	# FileResponse sets the Content-Disposition header so that browsers
	# present the option to save the file.
	buffer.seek(0)
	return FileResponse(buffer, as_attachment=True, filename=(instance.descrizione + ".pdf"))
