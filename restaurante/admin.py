import csv
import io

from django import forms
from django.contrib import admin
from django.shortcuts import redirect, render
from django.urls import path

from .models import PerfilUsuario, Mesa, Platillo, Comanda, DetalleComanda, Reserva

admin.site.site_header = "Administración SunSet"
admin.site.site_title = "Panel SunSet"
admin.site.index_title = "Control de Operaciones del Restaurante"


# ==========================================
# IMPORTACIÓN MASIVA DE PLATILLOS VÍA CSV
# ==========================================

class CsvImportForm(forms.Form):
    csv_file = forms.FileField(label='Archivo CSV')


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
    change_list_template = "admin/platillos_list.html"

    def get_urls(self):
        urls = super().get_urls()
        info = self.model._meta.app_label, self.model._meta.model_name
        urls_extra = [
            path(
                'importar-csv/',
                self.admin_site.admin_view(self.importar_csv),
                name='%s_%s_importar_csv' % info,
            ),
        ]
        return urls_extra + urls

    def importar_csv(self, request):
        """Carga masiva de Platillos desde un archivo CSV.

        Formato esperado (con encabezados): nombre,precio,categoria,descripcion,disponible
        """
        if request.method == "POST":
            form = CsvImportForm(request.POST, request.FILES)
            if form.is_valid():
                archivo = request.FILES['csv_file']
                datos = io.TextIOWrapper(archivo.file, encoding='utf-8')
                lector = csv.DictReader(datos)

                creados = 0
                errores = 0
                for fila in lector:
                    try:
                        Platillo.objects.update_or_create(
                            nombre=fila['nombre'].strip(),
                            defaults={
                                'precio': fila['precio'].strip(),
                                'categoria': fila.get('categoria', 'FUERTE').strip().upper() or 'FUERTE',
                                'descripcion': fila.get('descripcion', '').strip(),
                                'disponible': fila.get('disponible', 'True').strip().lower() in ('true', '1', 'si', 'sí'),
                            },
                        )
                        creados += 1
                    except (KeyError, ValueError):
                        errores += 1

                self.message_user(request, f'Se importaron {creados} platillo(s) desde el CSV.')
                if errores:
                    self.message_user(
                        request,
                        f'{errores} fila(s) no se pudieron importar por datos inválidos.',
                        level='WARNING',
                    )
                return redirect('..')
        else:
            form = CsvImportForm()

        contexto = {
            'form': form,
            'opts': self.model._meta,
            'title': 'Importar Platillos desde CSV',
        }
        return render(request, 'admin/platillo_csv_form.html', contexto)


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


