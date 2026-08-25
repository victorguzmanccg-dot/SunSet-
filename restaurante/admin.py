from django.contrib import admin
from .models import PerfilUsuario, Mesa, Platillo, Comanda, DetalleComanda, Reserva

admin.site.site_header = "Administración SunSet"
admin.site.site_title = "Panel SunSet"
admin.site.index_title = "Control de Operaciones del Restaurante"


@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'rol')
    list_filter = ('rol',)


@admin.register(Mesa)
class MesaAdmin(admin.ModelAdmin):
    list_display = ('numero', 'capacidad', 'estado')
    list_filter = ('estado',)


@admin.register(Platillo)
class PlatilloAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'precio', 'categoria', 'disponible')
    list_filter = ('categoria', 'disponible')
    search_fields = ('nombre',)


class DetalleComandaInline(admin.TabularInline):
    model = DetalleComanda
    extra = 1


@admin.register(Comanda)
class ComandaAdmin(admin.ModelAdmin):
    list_display = ('id', 'mesa', 'mesero', 'estado', 'total', 'fecha')
    list_filter = ('estado', 'fecha')
    inlines = [DetalleComandaInline]


@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'mesa', 'fecha_hora', 'num_personas', 'estado')
    list_filter = ('estado', 'fecha_hora')


