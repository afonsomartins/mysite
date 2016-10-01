from django.conf.urls import url
from atavirtual.views import *

urlpatterns = [
    url(r'^inicio/$', horario, name='horario'),
    
]