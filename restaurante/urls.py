from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'api/mesas', views.MesaViewSet, basename='api_mesas')
router.register(r'api/platillos', views.PlatilloViewSet, basename='api_platillos')
router.register(r'api/comandas', views.ComandaViewSet, basename='api_comandas')

urlpatterns = [
    # Autenticación
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('perfil/', views.perfil_view, name='perfil'),

    # Rutas Web (HTML)
    path('', views.menu_view, name='menu'),
    path('cocina/', views.cocina_view, name='cocina'),
    path('comanda/nueva/', views.crear_comanda_action, name='crear_comanda'),
    path('comanda/<int:comanda_id>/estado/', views.cambiar_estado_action, name='cambiar_estado'),

    # Rutas API
    path('', include(router.urls)),
]
