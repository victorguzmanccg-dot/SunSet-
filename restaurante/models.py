from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


# ==========================================
# 1. USUARIO Y ROLES (Servicio de Autenticación)
# ==========================================

class PerfilUsuario(models.Model):
    ROLES = [
        ('ADMIN', 'Administrador'),
        ('OPERADOR', 'Operador'),
        ('CLIENTE', 'Cliente Final'),
    ]
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    rol = models.CharField(max_length=10, choices=ROLES, default='CLIENTE')

    def __str__(self):
        return f"{self.usuario.username} ({self.get_rol_display()})"
    
# ==========================================
# 2. MESA (soporte físico del restaurante)
# ==========================================

class Mesa(models.Model):
    ESTADOS = [
        ('LIBRE', 'Libre'),
        ('OCUPADA', 'Ocupada'),
        ('RESERVADA', 'Reservada'),
    ]
    numero = models.PositiveIntegerField(unique=True)
    capacidad = models.PositiveIntegerField(default=4)
    estado = models.CharField(max_length=10, choices=ESTADOS, default='LIBRE')

    def __str__(self):
        return f"Mesa {self.numero} ({self.get_estado_display()})"


# ==========================================
# 3. PLATILLO (Servicio de Menú/Inventario)
# ==========================================

class Platillo(models.Model):
    CATEGORIAS = [
        ('ENTRADA', 'Entrada'),
        ('FUERTE', 'Plato fuerte'),
        ('BEBIDA', 'Bebida'),
        ('POSTRE', 'Postre'),
    ]
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    categoria = models.CharField(max_length=10, choices=CATEGORIAS, default='FUERTE')
    disponible = models.BooleanField(default=True)
    imagen = models.ImageField(upload_to='platillos/', blank=True, null=True)

    def __str__(self):
        return self.nombre

    def clean(self):
        if self.precio is not None and self.precio <= 0:
            raise ValidationError({'precio': 'El precio debe ser mayor a cero.'})
        
# ==========================================
# 4. COMANDA (cabecera del pedido)
# ==========================================

class Comanda(models.Model):
    ESTADOS = [
        ('PENDIENTE', 'Pendiente'),
        ('PREPARANDO', 'Preparando'),
        ('LISTO', 'Listo'),
        ('ENTREGADO', 'Entregado'),
        ('PAGADO', 'Pagado'),
        ('CANCELADO', 'Cancelado'),
    ]
    mesa = models.ForeignKey(Mesa, on_delete=models.PROTECT, related_name='comandas')
    mesero = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='comandas_atendidas'
    )
    estado = models.CharField(max_length=10, choices=ESTADOS, default='PENDIENTE')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comanda #{self.id} - Mesa {self.mesa.numero} ({self.get_estado_display()})"

    def recalcular_total(self):
        """Suma los subtotales de todos los detalles y actualiza el total."""
        nuevo_total = sum(detalle.subtotal for detalle in self.detalles.all())
        self.total = nuevo_total
        self.save(update_fields=['total'])


# ==========================================
# 5. DETALLECOMANDA (líneas de la orden)
# ==========================================

class DetalleComanda(models.Model):
    comanda = models.ForeignKey(Comanda, on_delete=models.CASCADE, related_name='detalles')
    platillo = models.ForeignKey(Platillo, on_delete=models.PROTECT, related_name='detalles')
    cantidad = models.PositiveIntegerField(default=1)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
        self.subtotal = self.platillo.precio * self.cantidad
        super().save(*args, **kwargs)
        self.comanda.recalcular_total()

    def __str__(self):
        return f"{self.cantidad}x {self.platillo.nombre} (Comanda #{self.comanda_id})"
    
# ==========================================
# 6. RESERVA (Servicio de Comandas - reservaciones)
# ==========================================

class Reserva(models.Model):
    ESTADOS = [
        ('CONFIRMADA', 'Confirmada'),
        ('CANCELADA', 'Cancelada'),
        ('COMPLETADA', 'Completada'),
    ]
    cliente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservas')
    mesa = models.ForeignKey(Mesa, on_delete=models.PROTECT, related_name='reservas')
    fecha_hora = models.DateTimeField()
    num_personas = models.PositiveIntegerField(default=2)
    estado = models.CharField(max_length=10, choices=ESTADOS, default='CONFIRMADA')

    def __str__(self):
        return f"Reserva de {self.cliente.username} - Mesa {self.mesa.numero} ({self.fecha_hora})"

    def clean(self):
        if self.num_personas > self.mesa.capacidad:
            raise ValidationError(
                f'La mesa {self.mesa.numero} tiene capacidad para {self.mesa.capacidad} personas, '
                f'no para {self.num_personas}.'
            )