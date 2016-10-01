from django.shortcuts import render
from django.http import HttpResponse
from atavirtual.models import CargaHoraria 
from atavirtual.forms import atividadeForm
from cadastro.models import User
from datetime import datetime, timedelta


def horario(request):
	user = User.objects.get(id=request.user.id)
	data = {}
	data['form'] = atividadeForm
	data['saida'] = 'Ata Virtual da EJECT'
	data['lista_entrada_saida'] = CargaHoraria.objects.all()
    
	form = atividadeForm(request.POST or None)
	if request.method == "POST":
		if form.is_valid():
			atividade = form.cleaned_data["atividade"]
			horario = CargaHoraria()
			horario.atividade = atividade
			horario.nome = user.first_name
			horario.cargo = user.userinfo.cargo
			horario.entrada_usuario = user.last_login
			now = horario.entrada_usuario 
			now = now + timedelta(minutes = 90)
			horario.saida_usuario = now
			request.session.set_expiry(5400)
			horario.save()
			
	return render(request , 'horario.html' , data  )

