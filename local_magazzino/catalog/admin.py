from django.contrib import admin

from .models import Materiale, Movimenti, Magazzino, MaterialeMagazzino


# Define the admin class
@admin.register(Materiale)
class MaterialeAdmin(admin.ModelAdmin):
	list_display = ("codice", "descrizione", "unita_misura", "sottoscorta", "giacenza", "creatore")


@admin.register(Movimenti)
class MovimentiAdmin(admin.ModelAdmin):
	list_display = ("data_movimento", "materiale", "quantita", "magazzino", "creatore")


@admin.register(Magazzino)
class MagazzinoAdmin(admin.ModelAdmin):
	list_display = ("localita","descrizione")


@admin.register(MaterialeMagazzino)
class MaterialeMagazzinoAdmin(admin.ModelAdmin):
	list_display = ("materiale", "magazzino", "giacenza")
