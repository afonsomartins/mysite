from django import forms


class atividadeForm(forms.Form):
	atividade = forms.CharField(label='O que está fazendo?', max_length=200)
	