from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import Materiale


class AggiungiMaterialeForm(forms.Form):
	descrizione = forms.CharField()
	unita_misura = forms.CharField()
	sottoscorta = forms.IntegerField()

	def clean_descrizione(self):
		data = self.cleaned_data["descrizione"]

		if Materiale.objects.filter(descrizione=data):
			if len(data) > 50:
				raise ValidationError(_("descrizione non unica\nmax 50 caratteri "))
			raise ValidationError(_("descrizione non unica"))

		return data

	def clean_unita_misura(self):
		data = self.cleaned_data["unita_misura"]

		if len(data) > 3:
			raise ValidationError(_("max 3 caratteri"))

		return data

	def clean_sottoscorta(self):
		data = self.cleaned_data["sottoscorta"]

		if data < -99999 or data > 99999:
			raise ValidationError(_("sottoscorta deve essere compresa tra -99999 e 99999"))

		return data


class ModificaMaterialeForm(forms.Form):
	descrizione = forms.CharField()
	# quantita = forms.IntegerField()
	unita_misura = forms.CharField()
	sottoscorta = forms.IntegerField()

	# creatore = forms.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

	def clean_descrizione(self):
		data = self.cleaned_data["descrizione"]

		# verifica l'unicita della descrizione
		if Materiale.objects.filter(descrizione=data):
			if len(data) > 50:
				raise ValidationError(_("descrizione non unica\nmax 50 caratteri "))
			raise ValidationError(_("descrizione non unica"))

		return data

	def clean_unita_misura(self):
		data = self.cleaned_data["unita_misura"]

		if len(data) > 3:
			raise ValidationError(_("max 3 caratteri"))

		return data

	def clean_sottoscorta(self):
		data = self.cleaned_data["sottoscorta"]

		if data < -99999 or data > 99999:
			raise ValidationError(_("sottoscorta deve essere compresa tra -99999 e 99999"))

		return data
