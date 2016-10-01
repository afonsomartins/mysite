from django.shortcuts import render
from django.contrib.sites.shortcuts import get_current_site
from django.views.generic import TemplateView, FormView, UpdateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group, User
from django.contrib.auth.hashers import check_password
from django.contrib.auth import login, authenticate

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy

from cadastro.forms import *
from cadastro.models import *
from treinamento.views import *

#Cria um objeto de uma classe Form específica e popula todos os seus fields.
def popular_form(request, Form):
    form = Form()
    for field in form.fields:
        setattr(form, field, request.POST.get(field))
    return form

class LoginCadastroView(TemplateView):

    def get_template_names(self):
        return ["index.html"]

    def get_context_data(self, **kwargs):
        context = super(LoginCadastroView, self).get_context_data(**kwargs)
        context['form_login'] = LoginForm()
        context['form_cadastro'] = CadastroForm()
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()

        # Processa o request e chama a validação de login
        if (request.POST.get('login') == "ENTRAR"):
            tentativa_de_login = popular_form(request, LoginForm)
            return self.login(request, tentativa_de_login)

        # Processa o request e chama a validação de cadastro    
        elif (request.POST.get('cadastro') == "ENVIAR"):
            tentativa_de_cadastro = popular_form(request, CadastroForm)
            return self.cadastro(request, tentativa_de_cadastro)

        return super(TemplateView, self).render_to_response(context)

    #Validação de login
    def login(self, request, loginform):
        context = self.get_context_data()
        user_existe = User.objects.all().filter(username=loginform.username)
        if user_existe:
            password = user_existe[0].password
            if check_password(loginform.password, password):
                user = authenticate(
                    username=loginform.username, 
                    password=loginform.password)
                login(request, user)
                return HttpResponseRedirect(reverse('meus_treinamentos'))
            else:
                context['alerta_login']=["Usuário ou senha inseridos estão incorretos."]
        else:
            context['alerta_login']=["Usuário não está cadastrado."]
        return super(TemplateView, self).render_to_response(context)

    #Validação de cadastro
    def cadastro(self, request, cadastroform):
        context = self.get_context_data()
        email_ja_existe = Aluno.objects.all().filter(email=cadastroform.email)
        username_ja_existe = User.objects.all().filter(username=cadastroform.username)
        if email_ja_existe:
            context['alerta_cadastro'] = ["Email já está cadastrado."]
        elif username_ja_existe:
            context['alerta_cadastro'] = ["Usuário já está cadastrado."]
        else:
            novo_user = User.objects.create_user(
                username=cadastroform.username,
                password=cadastroform.password
                )
            novo_aluno = Aluno()
            novo_aluno.user_referencia = novo_user
            novo_aluno.email = cadastroform.email
            novo_aluno.nome = cadastroform.nome
            novo_aluno.sobrenome = cadastroform.sobrenome
            novo_aluno.whatsapp = cadastroform.whatsapp
            novo_aluno.save()
            log = authenticate(
                username=cadastroform.username, 
                password=cadastroform.password,
                )
            login(request, log)
            return HttpResponseRedirect(reverse('meus_treinamentos'))
        return super(TemplateView, self).render_to_response(context)


class PerfilView(BaseView, TemplateView):
    template_name = "perfil.html"

class EditarPerfilView(BaseView, UpdateView):
    form_class = AlunoForm
    template_name = "editar_perfil.html"
    success_url = reverse_lazy('perfil')

    def get_object(self, **kwargs):
        return Aluno.objects.get(user_referencia=self.request.user)