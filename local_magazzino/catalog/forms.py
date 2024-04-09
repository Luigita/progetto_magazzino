from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import Materiale


# class AggiungiMaterialeForm(forms.Form):
# 	descrizione = forms.CharField()
# 	unita_misura = forms.CharField()
# 	sottoscorta = forms.IntegerField()
#
# 	def clean_descrizione(self):
# 		data = self.cleaned_data["descrizione"]
#
# 		if Materiale.objects.filter(descrizione=data):
# 			if len(data) > 50:
# 				raise ValidationError(_("descrizione non unica\nmax 50 caratteri "))
# 			raise ValidationError(_("descrizione non unica"))
#
# 		return data
#
# 	def clean_unita_misura(self):
# 		data = self.cleaned_data["unita_misura"]
#
# 		if len(data) > 3:
# 			raise ValidationError(_("max 3 caratteri"))
#
# 		return data
#
# 	def clean_sottoscorta(self):
# 		data = self.cleaned_data["sottoscorta"]
#
# 		if data < -99999 or data > 99999:
# 			raise ValidationError(_("sottoscorta deve essere compresa tra -99999 e 99999"))
#
# 		return data


class MaterialeForm(forms.Form):
	codice = forms.CharField()
	descrizione = forms.CharField()
	# quantita = forms.IntegerField()
	# unita_misura = forms.CharField()
	sottoscorta = forms.IntegerField()

	# creatore = forms.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

	def clean_codice(self):
		data = self.cleaned_data["codice"]

		# verifica l'unicita della codice
		if Materiale.objects.filter(codice=data):
			if len(data) > 50:
				raise ValidationError(_("codice non unico\nmax 50 caratteri "))
			raise ValidationError(_("codice non unico"))

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

	def clean_descrizione(self):
		data = self.cleaned_data["descrizione"]
		return data


class ModificaMaterialeForm(forms.Form):
	codice = forms.CharField()
	descrizione = forms.CharField()
	# quantita = forms.IntegerField()
	# unita_misura = forms.CharField()
	sottoscorta = forms.IntegerField()

	# creatore = forms.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
	def __init__(self, *args, **kwargs):
		super(ModificaMaterialeForm, self).__init__(*args, **kwargs)
		instance = getattr(self, 'instance', None)
		if instance and instance.pk:
			self.fields['codice'].widget.attrs["readonly"] = True

	def clean_codice(self):
		instance = getattr(self, 'instance', None)
		if instance and instance.pk:
			return instance.codice
		else:
			return self.cleaned_data['codice']

	def clean_sottoscorta(self):
		data = self.cleaned_data["sottoscorta"]

		if data < -99999 or data > 99999:
			raise ValidationError(_("sottoscorta deve essere compresa tra -99999 e 99999"))

		return data

	def clean_descrizione(self):
		data = self.cleaned_data["descrizione"]
		return data


class CancellazioneMateriale(forms.Form):
	materiale = forms.ModelChoiceField(queryset=Materiale.objects.all())

	def clean_materiale(self):
		data = self.cleaned_data["materiale"]
		return data


class CaricoForm(forms.Form):
	materiale = forms.ModelChoiceField(queryset=Materiale.objects.all())
	quantita = forms.IntegerField()

	magazzino_choices = (
		("NAP", "Napoli"),
		("MIL", "Milano"),
	)
	magazzino = forms.ChoiceField(choices=magazzino_choices)

	def clean_materiale(self):
		data = self.cleaned_data["materiale"]
		return data

	def clean_quantita(self):
		data = self.cleaned_data["quantita"]

		if data < 0:
			raise ValidationError(_("La quantità di carico non può essere negativa"))
		if data == 0:
			raise ValidationError(_("La quantità di carico non può essere 0"))

		return data

	def clean_magazzino(self):
		data = self.cleaned_data["magazzino"]
		return data
