from django.contrib import admin
from atavirtual.models import CargaHoraria




class CargaHorariaAdmin (admin.ModelAdmin):
	model = CargaHoraria
	list_display = ('id','nome' ,'cargo', 'entrada_usuario','saida_usuario','atividade')
	list_filter = ('entrada_usuario',)
	
	'''def __init__(self, arg):
		super(, self).__init__()
		self.arg = arg'''


admin.site.register(CargaHoraria,CargaHorariaAdmin)


