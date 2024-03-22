from django.contrib import admin

from .models import Materiale, Movimenti


# Define the admin class
@admin.register(Materiale)
class MaterialeAdmin(admin.ModelAdmin):
	list_display = ("descrizione", "unita_misura", "sottoscorta", "creatore")


@admin.register(Movimenti)
class MovimentiAdmin(admin.ModelAdmin):
	list_display = ("data_movimento", "materiale", "quantita", "magazzino", "creatore")

