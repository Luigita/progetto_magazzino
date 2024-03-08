from django.contrib import admin

from .models import Materiale, Movimenti

admin.site.register(Materiale)
admin.site.register(Movimenti)

# from .models import Author, Genre, Book, BookInstance
# # Register your models here.
# admin.site.register(Book)
# admin.site.register(Author)
# admin.site.register(Genre)
# admin.site.register(BookInstance)