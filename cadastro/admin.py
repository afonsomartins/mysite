from django.contrib import admin
from cadastro.models import *


class AlunoAdmin(admin.ModelAdmin):
	list_display = []
	for field in Aluno._meta.fields :
		list_display.append(field.name)


class UserInfoAdmin(admin.ModelAdmin):
	list_display = []
	for field in UserInfo._meta.fields :
		list_display.append(field.name)

admin.site.register(UserInfo, UserInfoAdmin)
admin.site.register(Aluno, AlunoAdmin)