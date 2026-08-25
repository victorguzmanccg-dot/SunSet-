from rest_framework import serializers
from .models import Mesa, Platillo, Comanda, DetalleComanda, Reserva


class MesaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mesa
        fields = '__all__'


class PlatilloSerializer(serializers.ModelSerializer):
    class Meta:
        model = Platillo
        fields = '__all__'


class DetalleComandaSerializer(serializers.ModelSerializer):
    platillo_nombre = serializers.CharField(source='platillo.nombre', read_only=True)

    class Meta:
        model = DetalleComanda
        fields = ['id', 'platillo', 'platillo_nombre', 'cantidad', 'subtotal']


class ComandaSerializer(serializers.ModelSerializer):
    detalles = DetalleComandaSerializer(many=True, read_only=True)
    mesa_numero = serializers.IntegerField(source='mesa.numero', read_only=True)

    class Meta:
        model = Comanda
        fields = ['id', 'mesa', 'mesa_numero', 'mesero', 'estado', 'total', 'fecha', 'detalles']


class ReservaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reserva
        fields = '__all__'