import django_filters
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import Materiale, Magazzino


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
	articolo = forms.CharField()
	taglia = forms.IntegerField()
	descrizione = forms.CharField()
	sottoscorta = forms.IntegerField()

	def clean_articolo(self):
		data = self.cleaned_data["articolo"]
		return data

	def clean_taglia(self):
		data = self.cleaned_data["taglia"]
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
	descrizione = forms.CharField()
	sottoscorta = forms.IntegerField()

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


class MovimentoForm(forms.Form):
	# materiale = forms.ModelChoiceField(queryset=Materiale.objects.all())
	materiale = forms.CharField(max_length=20)
	quantita = forms.IntegerField()

	magazzino = forms.ModelChoiceField(queryset=Magazzino.objects.all())

	def __init__(self, *args, **kwargs):
		super(MovimentoForm, self).__init__(*args, **kwargs)
		self.fields["materiale"].widget.attrs.update({"autofocus": "autofocus"})

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


class TrasferimentoForm(forms.Form):
	materiale = forms.ModelChoiceField(queryset=Materiale.objects.all())
	quantita = forms.IntegerField()

	def clean_materiale(self):
		data = self.cleaned_data["materiale"]
		return data

	def clean_quantita(self):
		data = self.cleaned_data["quantita"]

		if data < 0:
			raise ValidationError(_("La quantità di trasferimento non può essere negativa"))
		if data == 0:
			raise ValidationError(_("La quantità di trasferimento non può essere 0"))

		return data

	def clean_magazzino(self):
		data = self.cleaned_data["magazzino"]
		return data


class MagazzinoForm(forms.Form):
	localita = forms.CharField(max_length=3)
	descrizione = forms.CharField()

	def clean_localita(self):
		data = self.cleaned_data["localita"]
		if len(data) > 3:
			raise ValidationError(_("Max 3 caratteri"))
		return data

	def clean_descrizione(self):
		data = self.cleaned_data["descrizione"]

		if False:
			return ValidationError(_("Errore"))
		return data


class ModificaMagazzinoForm(forms.Form):
	descrizione = forms.CharField()

	def clean_descrizione(self):
		data = self.cleaned_data["descrizione"]
		if False:
			return ValidationError(_("Errore"))
		return data


class MaterialeFilter(django_filters.FilterSet):
	class Meta:
		model = Materiale
		fields = ["codice", "descrizione"]
