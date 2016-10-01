from django.db import models
from datetime import datetime, timedelta
class CargaHoraria(models.Model):
	nome = models.CharField(max_length=100)
	cargo = models.CharField(max_length=100)
	atividade = models.TextField()
	entrada_usuario = models.DateTimeField()
	saida_usuario = models.DateTimeField()
	
