

from restaurante.models import Mesa, Platillo, Comanda, DetalleComanda, Reserva


class MesaDAO:

    @staticmethod
    def listar():
        return Mesa.objects.all()

    @staticmethod
    def obtener(mesa_id):
        return Mesa.objects.filter(id=mesa_id).first()

    @staticmethod
    def crear(numero, capacidad):
        return Mesa.objects.create(numero=numero, capacidad=capacidad)

    @staticmethod
    def cambiar_estado(mesa_id, nuevo_estado):
        mesa = Mesa.objects.filter(id=mesa_id).first()
        if mesa:
            mesa.estado = nuevo_estado
            mesa.save(update_fields=['estado'])
        return mesa

    @staticmethod
    def eliminar(mesa_id):
        return Mesa.objects.filter(id=mesa_id).delete()


class PlatilloDAO:

    @staticmethod
    def listar_disponibles():
        return Platillo.objects.filter(disponible=True)

    @staticmethod
    def listar_todos():
        return Platillo.objects.all()

    @staticmethod
    def obtener(platillo_id):
        return Platillo.objects.filter(id=platillo_id).first()

    @staticmethod
    def crear(nombre, precio, categoria, descripcion=''):
        return Platillo.objects.create(
            nombre=nombre, precio=precio,
            categoria=categoria, descripcion=descripcion
        )

    @staticmethod
    def actualizar(platillo_id, **datos):
        Platillo.objects.filter(id=platillo_id).update(**datos)
        return PlatilloDAO.obtener(platillo_id)

    @staticmethod
    def eliminar(platillo_id):
        return Platillo.objects.filter(id=platillo_id).delete()


class ComandaDAO:

    @staticmethod
    def listar_activas():
        return Comanda.objects.exclude(estado__in=['PAGADO', 'CANCELADO'])

    @staticmethod
    def obtener(comanda_id):
        return Comanda.objects.filter(id=comanda_id).first()

    @staticmethod
    def crear(mesa_id, mesero=None):
        return Comanda.objects.create(mesa_id=mesa_id, mesero=mesero)

    @staticmethod
    def agregar_platillo(comanda_id, platillo_id, cantidad=1):
        return DetalleComanda.objects.create(
            comanda_id=comanda_id, platillo_id=platillo_id, cantidad=cantidad
        )

    @staticmethod
    def cambiar_estado(comanda_id, nuevo_estado):
        comanda = Comanda.objects.filter(id=comanda_id).first()
        if comanda:
            comanda.estado = nuevo_estado
            comanda.save(update_fields=['estado'])
        return comanda


class ReservaDAO:

    @staticmethod
    def listar(cliente=None):
        if cliente:
            return Reserva.objects.filter(cliente=cliente)
        return Reserva.objects.all()

    @staticmethod
    def crear(cliente, mesa_id, fecha_hora, num_personas):
        return Reserva.objects.create(
            cliente=cliente, mesa_id=mesa_id,
            fecha_hora=fecha_hora, num_personas=num_personas
        )

    @staticmethod
    def cancelar(reserva_id):
        reserva = Reserva.objects.filter(id=reserva_id).first()
        if reserva:
            reserva.estado = 'CANCELADA'
            reserva.save(update_fields=['estado'])
        return reserva