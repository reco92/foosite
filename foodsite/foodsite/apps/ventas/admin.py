from django.contrib import admin
from foodsite.apps.ventas.models import Cliente,Restaurante,Platillo,Registro_reservacion,Registro_pedido

admin.site.register(Cliente)
admin.site.register(Restaurante)
admin.site.register(Platillo)
admin.site.register(Registro_reservacion)
admin.site.register(Registro_pedido)
