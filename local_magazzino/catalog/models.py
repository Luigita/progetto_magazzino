from django.db import models

from django.urls import reverse  # Used in get_absolute_url() to get URL for specified ID

from django.db.models import UniqueConstraint  # Constrains fields to unique values
from django.db.models.functions import Lower  # Returns lower cased value of field

from django.db import models
from django.utils import timezone

from django.conf import settings

from django.contrib.auth.models import User


class Magazzino(models.Model):
	localita = models.CharField(max_length=3, unique=True)
	descrizione = models.CharField(max_length=50, null=True)

	class Meta:
		verbose_name = "Magazzino"
		verbose_name_plural = "Magazzini"

	def __str__(self):
		return self.localita

	def get_absolute_url(self):
		return reverse("magazzino_view", args=[str(self.pk)])


class Materiale(models.Model):
	"""Modello rappresentante un materiale presente in magazzino"""

	codice = models.CharField(max_length=70, null=True, blank=False, unique=True)

	articolo = models.CharField(max_length=50, null=True, blank=False)
	taglia = models.IntegerField(null=True, blank=False)

	descrizione = models.CharField(max_length=50, null=False, blank=False)
	unita_misura = models.CharField(max_length=5, null=False, blank=False, default="PZ")
	sottoscorta = models.IntegerField()
	creatore = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)



	# TODO: QUANDO SI FA IL CARICO A MAGAZZINO SALVARE IL FIELD
	magazzini_giacenza = models.ManyToManyField(Magazzino, blank=True, through="MaterialeMagazzino")

	giacenza = models.IntegerField(default=0)

	class Meta:
		verbose_name = "Materiale"
		verbose_name_plural = "Materiali"

	def __str__(self):
		return self.descrizione

	def get_absolute_url(self):
		return reverse("materiale_view", args=[str(self.pk)])

	def get_url_etichetta(self):
		return reverse("genera_etichetta", args=[str(self.pk)])

	def id_materiale(self):
		"""Create a string for the id. This is required to display id in Admin."""
		return self.id

	def carico_materiale(self, quantita):
		self.giacenza += quantita
		self.save()

	# def get_giacenza_magazzino(self, magazzino):
	# 	giacenza = 0
	# 	for mov in Movimenti.objects.all():
	# 		if mov.materiale == self and mov.magazzino == magazzino:
	# 			giacenza += mov.quantita
	# 	return giacenza

	def get_giacenze(self):
		giacenza = 0
		giacenze = ""
		for mag in Magazzino.objects.all():
			for mov in Movimenti.objects.filter(magazzino__pk__exact=mag.pk):
				if mov.materiale == self:
					giacenza += mov.quantita
			giacenze += mag.localita + " " + str(giacenza) + "\n"
			giacenza = 0
		return giacenze

	def get_giacenza_milano(self):
		giacenza = 0
		for mov in Movimenti.objects.filter(magazzino__pk__exact=2):
			if mov.materiale == self:
				giacenza += mov.quantita
		return giacenza

	def get_giacenza_napoli(self):
		giacenza = 0
		for mov in Movimenti.objects.filter(magazzino__pk__exact=1):
			if mov.materiale == self:
				giacenza += mov.quantita
		return giacenza


class Movimenti(models.Model):
	"""Modello rappresentante la movimentazione di un materiale"""
	materiale = models.ForeignKey("Materiale", on_delete=models.CASCADE, null=True, related_name="movimenti")
	quantita = models.IntegerField(blank=False, null=False)

	# TODO: METTERE UTENTE LOGGATO COME PREDEFINITO
	creatore = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

	magazzino_choices = [
		("NAP", "Napoli"),
		("MIL", "Milano"),
	]
	magazzino = models.ForeignKey("Magazzino", on_delete=models.SET_NULL, null=True, related_name="magazzini")
	# magazzino = models.CharField(max_length=3, choices=magazzino_choices)

	data_movimento = models.DateTimeField(unique=True, auto_now_add=True)

	class Meta:
		verbose_name = "Movimento"
		verbose_name_plural = "Movimenti"

	def get_absolute_url(self):
		return reverse("movimento_view", args=[str(self.pk)])

	def __str__(self):
		return f"{str(self.materiale)} {str(self.quantita)} {str(self.magazzino)}"


class MaterialeMagazzino(models.Model):
	materiale = models.ForeignKey(Materiale, on_delete=models.CASCADE, null=True, related_name="new_materiale")
	magazzino = models.ForeignKey(Magazzino, on_delete=models.CASCADE, related_name="new_magazzino")
	giacenza = models.IntegerField(default=0)
