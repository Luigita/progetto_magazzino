# from django.db import models
#
#
# # Create your models here.
#
# class Materiale(models.Model):
# 	"""Modello rappresentante un materiale presente in magazzino"""
# 	descrizione = models.CharField(max_length="200")
# 	unita_misura = models.CharField(max_length="2")
# 	sottoscorta = models.IntegerField()
#
# 	def __str__(self):
# 		return self.descrizione
#
#
# # def get_absolute_url(self):
# # 	return reverse()
#
#
# class Movimenti(models.Model):
# 	"""Modello rappresentante la movimentazione di un materiale"""
# 	materiale = Materiale
# 	quantita = models.IntegerField()
# 	magazzino = models.CharField(max_length="3")
# 	data_movimento = models.DateTimeField()
#
# 	def __str__(self):
# 		return self.materiale
