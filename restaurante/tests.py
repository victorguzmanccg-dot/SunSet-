from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Group
from .models import Mesa, Platillo, Comanda, DetalleComanda


class SunSetTestCase(TestCase):
    def setUp(self):
        # Datos base que usan varias pruebas
        self.mesa = Mesa.objects.create(numero=1, capacidad=4)
        self.platillo = Platillo.objects.create(
            nombre="Tacos al Pastor",
            precio=85.00,
            categoria="FUERTE",
            disponible=True,
        )
        # Usuario operador, con permiso para entrar a cocina/comandas
        self.operador = User.objects.create_user(username="mesero1", password="clave123")
        grupo_operador, _ = Group.objects.get_or_create(name="Operador")
        self.operador.groups.add(grupo_operador)

    def test_crear_comanda_con_detalle(self):
        """El DAO crea una comanda y el total se calcula solo al agregar un platillo."""
        comanda = Comanda.objects.create(mesa=self.mesa, mesero=self.operador)
        DetalleComanda.objects.create(comanda=comanda, platillo=self.platillo, cantidad=2)
        comanda.refresh_from_db()
        self.assertEqual(comanda.total, 170.00)  # 85.00 x 2

    def test_cambiar_estado_comanda(self):
        """El estado de una comanda se puede actualizar correctamente."""
        comanda = Comanda.objects.create(mesa=self.mesa, mesero=self.operador)
        comanda.estado = "PREPARANDO"
        comanda.save()
        comanda.refresh_from_db()
        self.assertEqual(comanda.estado, "PREPARANDO")

    def test_menu_view_accesible_con_login(self):
        """La vista del menú responde correctamente a un usuario con sesión iniciada."""
        self.client.login(username="mesero1", password="clave123")
        response = self.client.get(reverse('menu'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Tacos al Pastor")

    def test_cocina_bloqueada_sin_login(self):
        """Un usuario sin sesión no puede entrar a la vista de cocina."""
        response = self.client.get(reverse('cocina'))
        self.assertNotEqual(response.status_code, 200)

    def test_api_lista_platillos(self):
        """El endpoint de la API responde con éxito."""
        response = self.client.get('/api/platillos/')
        self.assertEqual(response.status_code, 200)