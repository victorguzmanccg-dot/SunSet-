from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from rest_framework import viewsets

from .models import Mesa, Platillo, Comanda
from .serializers import MesaSerializer, PlatilloSerializer, ComandaSerializer, ReservaSerializer
from .dao.sunsetdao import PlatilloDAO, ComandaDAO, MesaDAO


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
# VISTAS WEB (HTML) - Menú (Lectura)
# ==========================================

@login_required
def menu_view(request):
    platillos = PlatilloDAO.listar_disponibles()
    return render(request, 'mainvista/menu.html', {'platillos': platillos})


# ==========================================
# VISTAS WEB (HTML) - Comandas (Altas / Cambios)
# ==========================================

@login_required
def cocina_view(request):
    comandas = ComandaDAO.listar_activas()
    return render(request, 'mainvista/cocina.html', {'comandas': comandas})


@login_required
def crear_comanda_action(request):
    if request.method == 'POST':
        mesa_id = request.POST.get('mesa_id')
        ComandaDAO.crear(mesa_id=mesa_id, mesero=request.user)
        messages.success(request, 'Comanda creada correctamente.')
    return redirect('cocina')


@login_required
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
