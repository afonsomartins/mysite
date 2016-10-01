from django.conf.urls import patterns, url, include
from django.conf import settings
from cadastro.views import *
#auth_urls imports
from distutils.version import LooseVersion
from django import get_version
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import views as auth_views
#CustomPasswordResetForm
from cadastro.forms import CustomPasswordResetForm

urlpatterns = [
	url(r'^$',
			LoginCadastroView.as_view(),
			name='login'),
    url(r'^perfil/edit/$',
            EditarPerfilView.as_view(),
            name='edit_perfil'),
    url(r'^perfil/$',
            PerfilView.as_view(),
            name='perfil'),
]

#auth_urls
urlpatterns += [
    url(r'^logout/$',
        auth_views.logout,
        {'template_name': 'registration/logout.html'},
        name='auth_logout'),
    url(r'^password/change/$',
        auth_views.password_change,
        {'post_change_redirect': reverse_lazy('auth_password_change_done')},
        name='auth_password_change'),
    url(r'^password/change/done/$',
        auth_views.password_change_done,
        name='auth_password_change_done'),
    url(r'^password/reset/$',
        auth_views.password_reset,
        {
        'post_reset_redirect': reverse_lazy('auth_password_reset_done'),
        'password_reset_form': CustomPasswordResetForm,
        },
        name='auth_password_reset'),
    url(r'^password/reset/complete/$',
        auth_views.password_reset_complete,
        name='auth_password_reset_complete'),
    url(r'^password/reset/done/$',
        auth_views.password_reset_done,
        name='auth_password_reset_done'),
]


if (LooseVersion(get_version()) >= LooseVersion('1.6')):
    urlpatterns += [
        url(r'^password/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$',
            auth_views.password_reset_confirm,
            {'post_reset_redirect': reverse_lazy('auth_password_reset_complete')},
            name='auth_password_reset_confirm')
    ]
else:
    urlpatterns += [
        url(r'^password/reset/confirm/(?P<uidb36>[0-9A-Za-z]{1,13})-(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
            auth_views.password_reset_confirm,
            {'post_reset_redirect': reverse_lazy('auth_password_reset_complete')},
            name='auth_password_reset_confirm')
    ]
