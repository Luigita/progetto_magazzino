from django.contrib import admin

from .models import Materiale, Movimenti


# admin.site.register(Materiale)
# admin.site.register(Movimenti)

# Define the admin class
class MaterialeAdmin(admin.ModelAdmin):
	list_display = ("descrizione", "unita_misura", "sottoscorta")


# Register the admin class with the associated model
admin.site.register(Materiale, MaterialeAdmin)


class MovimentiAdmin(admin.ModelAdmin):
	list_display = ("data_movimento", "materiale", "quantita", "magazzino")


admin.site.register(Movimenti, MovimentiAdmin)

# from .models import Author, Genre, Book, BookInstance
# # Register your models here.
# admin.site.register(Book)
# admin.site.register(Author)
# admin.site.register(Genre)
# admin.site.register(BookInstance)
