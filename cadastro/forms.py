from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
#CustomPasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import authenticate, get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template import loader
from django.core.mail import EmailMultiAlternatives
from django.forms import ModelForm, Form

# from ckeditor.widgets import CKEditorWidget
from cadastro.models import *


class CadastroForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'required': True,
            'maxLength': 30}),
        label='Usuário',
        )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'required': True,
            'maxLength':254}),
        )
    password = forms.CharField(
        max_length=150, 
        widget=forms.PasswordInput(attrs={
            'required': True, 
            'minLength':8, 
            'maxLength':50
            }),
        )
    nome = forms.CharField(
        widget=forms.TextInput(attrs={
            'required': True, 
            'maxLength':50,
            }),
        )
    sobrenome = forms.CharField(
        widget=forms.TextInput(attrs={
            'required': True, 
            'maxLength':50,
            }),
        )
    whatsapp = forms.CharField(
        widget=forms.TextInput(attrs={
            'required': True,
            'minLength':14,
            'maxLength':15}),
        )


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'required': True,
            'maxLength': 30}),
        label='Usuário',
        )
    password = forms.CharField(
        max_length=150, 
        widget=forms.PasswordInput(attrs={
            'required': True, 
            'minLength':8, 
            'maxLength':50
            }),
        )

class CustomPasswordResetForm(forms.Form):
    email = forms.EmailField(label=_("Email"), max_length=254)

    def send_mail(self, subject_template_name, email_template_name,
                  context, from_email, to_email, html_email_template_name=None):
        """
        Sends a django.core.mail.EmailMultiAlternatives to `to_email`.
        """
        subject = loader.render_to_string(subject_template_name, context)
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())
        body = loader.render_to_string(email_template_name, context)

        email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])
        if html_email_template_name is not None:
            html_email = loader.render_to_string(html_email_template_name, context)
            email_message.attach_alternative(html_email, 'text/html')
        email_message.send()

    def get_users(self, email):
        """Given an email, return matching user(s) who should receive a reset.

        This allows subclasses to more easily customize the default policies
        that prevent inactive users and users with unusable passwords from
        resetting their password.

        """
        aluno = Aluno.objects.all().filter(email=email)
        if aluno:
            active_users = get_user_model()._default_manager.filter(
                username=aluno[0].user_referencia.username, is_active=True)
        else:
            active_users = []
        return (u for u in active_users if u.has_usable_password())

    def save(self, domain_override=None,
             subject_template_name='registration/password_reset_subject.txt',
             email_template_name='registration/password_reset_email.html',
             use_https=False, token_generator=default_token_generator,
             from_email=None, request=None, html_email_template_name=None, extra_email_context=None):
        """
        Generates a one-use only link for resetting password and sends to the
        user.
        """
        email = self.cleaned_data["email"]
        for user in self.get_users(email):
            if not domain_override:
                current_site = get_current_site(request)
                site_name = current_site.name
                domain = current_site.domain
            else:
                site_name = domain = domain_override
            context = {
                'email': user.aluno.email,
                'domain': domain,
                'site_name': site_name,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'user': user,
                'token': token_generator.make_token(user),
                'protocol': 'https' if use_https else 'http',
            }
            self.send_mail(subject_template_name, email_template_name,
                           context, from_email, user.aluno.email,
                           html_email_template_name=html_email_template_name)

            
#Retorna lista de fields de um modelo excluindo alguns.
def set_all_fields_except(Model, exclude_fields):
    fields = []
    for field in Model._meta.fields:
        is_exclude_field = False
        for exclude_field in exclude_fields:
            if field.name==exclude_field:
                is_exclude_field = True
        if not is_exclude_field:
            fields.append(field.name)
    return fields

class AlunoForm(ModelForm):
    class Meta:
        model = Aluno
        fields = set_all_fields_except(model,[
            'user_referencia',
            'criado',
            'atualizado',
            'efetivado',
            'cargo',
            ])


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = set_all_fields_except(model,[
            'password',
            ])