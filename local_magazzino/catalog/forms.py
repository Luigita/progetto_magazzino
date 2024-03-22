from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class ModificaMaterialeForm(forms.Form):
	# descrizione = forms.CharField(max_length=50, unique=True)
	quantita = forms.IntegerField()
	unita_misura = forms.CharField()
	sottoscorta = forms.IntegerField()


# creatore = forms.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)


def clean_unita_misura(self):
	data = self.cleaned_data["unita_misura"]

	if len(data) > 3:
		raise ValidationError(_("max 3 caratteri"))

	return data
