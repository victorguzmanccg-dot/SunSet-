from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from rest_framework import viewsets

from .models import Mesa, Platillo, Comanda
from .serializers import MesaSerializer, PlatilloSerializer, ComandaSerializer, ReservaSerializer
from .forms import PlatilloModelForm
from .dao.sunsetdao import PlatilloDAO, ComandaDAO, MesaDAO


# ==========================================
# CONTROL DE ACCESO POR GRUPOS DE DJANGO
# ==========================================
# Capa adicional de RBAC sobre PerfilUsuario: los grupos "Operador" y
# "Administrador" deben crearse desde el admin de Django (/admin/auth/group/)
# y asignarse a los usuarios correspondientes.

def es_operador_o_admin(user):
    return user.is_authenticated and (
        user.groups.filter(name__in=['Operador', 'Administrador']).exists()
        or user.is_staff
    )


# ==========================================
# VISTAS WEB (HTML) - Login / Perfil
# ==========================================

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('perfil')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    return render(request, 'mainvista/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def perfil_view(request):
    rol = getattr(request.user.perfil, 'rol', 'Sin rol asignado')
    return render(request, 'mainvista/perfil.html', {'rol': rol})


# ==========================================
# VISTAS WEB (HTML) - Menú (Lectura) y Platillos (Altas vía ModelForm)
# ==========================================

@login_required
def menu_view(request):
    platillos = PlatilloDAO.listar_disponibles()
    return render(request, 'mainvista/menu.html', {'platillos': platillos})


@login_required
@user_passes_test(es_operador_o_admin, login_url='/admin/login/')
def crear_platillo_view(request):
    if request.method == 'POST':
        form = PlatilloModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Platillo agregado correctamente.')
            return redirect('menu')
    else:
        form = PlatilloModelForm()
    return render(request, 'mainvista/platillo_form.html', {'form': form})

@login_required
@user_passes_test(es_operador_o_admin, login_url='/admin/login/')
def agregar_al_menu_action(request):
    """Agrega un platillo directo desde el menú a una comanda de una mesa dada."""
    if request.method == 'POST':
        platillo_id = request.POST.get('platillo_id')
        mesa_numero = request.POST.get('mesa_numero')

        mesa = MesaDAO.obtener(mesa_numero) if mesa_numero and mesa_numero.isdigit() else None
        if not mesa:
            mesa, _ = Mesa.objects.get_or_create(numero=mesa_numero or 1, defaults={'capacidad': 4})

        comanda = ComandaDAO.listar_activas().filter(mesa=mesa).first()
        if not comanda:
            comanda = ComandaDAO.crear(mesa_id=mesa.id, mesero=request.user)

        ComandaDAO.agregar_platillo(comanda.id, platillo_id, cantidad=1)
        messages.success(request, f'Platillo agregado a la comanda de la mesa {mesa.numero}.')

    return redirect('menu')


# ==========================================
# VISTAS WEB (HTML) - Comandas (Altas / Cambios)
# ==========================================

@login_required
@user_passes_test(es_operador_o_admin, login_url='/admin/login/')
def cocina_view(request):
    comandas = ComandaDAO.listar_activas()
    return render(request, 'mainvista/cocina.html', {'comandas': comandas})


@login_required
@user_passes_test(es_operador_o_admin, login_url='/admin/login/')
def crear_comanda_action(request):
    if request.method == 'POST':
        mesa_id = request.POST.get('mesa_id')
        ComandaDAO.crear(mesa_id=mesa_id, mesero=request.user)
        messages.success(request, 'Comanda creada correctamente.')
    return redirect('cocina')


@login_required
@user_passes_test(es_operador_o_admin, login_url='/admin/login/')
def cambiar_estado_action(request, comanda_id):
    if request.method == 'POST':
        nuevo_estado = request.POST.get('estado')
        ComandaDAO.cambiar_estado(comanda_id, nuevo_estado)
    return redirect('cocina')


# ==========================================
# API REST (DRF ViewSets)
# ==========================================

class MesaViewSet(viewsets.ModelViewSet):
    queryset = Mesa.objects.all()
    serializer_class = MesaSerializer


class PlatilloViewSet(viewsets.ModelViewSet):
    queryset = Platillo.objects.all()
    serializer_class = PlatilloSerializer


class ComandaViewSet(viewsets.ModelViewSet):
    queryset = Comanda.objects.all()
    serializer_class = ComandaSerializer