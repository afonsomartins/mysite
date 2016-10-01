from django.db import models
from django.contrib.auth.models import User

CHOICE_STATUS = (
    ('achando fácil', 'achando fácil'),
    ('tentando','tentando'),
    ('com dificuldades por problemas pessoais','com dificuldades por problemas pessoais'),
    ('em época de provas','em época de provas'),
    )

CHOICE_CARGO = (
    ('Aluno', 'Aluno'),
    ('Trainee', 'Trainee'),
    ('Membro EJECT', 'Membro EJECT'),
    ('Desenvolvimento Humano','Desenvolvimento Humano'),
    ('Administração','Administração'),
    )


class Aluno(models.Model):
    user_referencia = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=254, unique=True)
    criado = models.DateTimeField(auto_now_add=True, auto_now=False)
    atualizado = models.DateTimeField(auto_now_add=False, auto_now=True)
    nome = models.CharField(max_length=50)
    sobrenome = models.CharField(max_length=50)
    whatsapp = models.CharField(max_length=15)
    cargo = models.CharField(
        max_length=100,
        choices=CHOICE_CARGO,
        default='Aluno',
        )
    efetivado = models.BooleanField(default=False)
    status = models.CharField(
        max_length=100,
        choices=CHOICE_STATUS,
        default='achando fácil',
        )
    def nome_completo(self):
        return nome+' '+sobrenome

    def __str__(self):
        return self.nome

class UserInfo(models.Model):
    user_referencia = models.OneToOneField(User, on_delete=models.CASCADE)
    cargo = models.CharField(max_length=100)
    