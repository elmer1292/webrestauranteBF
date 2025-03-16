from rest_framework import serializers
from .models import (
    Mesas, Categorias, Productos, Inventario, Proveedores,
    Pedidos, Productos_Pedido, Usuarios, Pagos, Historial_Precios, Reportes
)

class MesasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mesas
        fields = ['id', 'numero', 'estado', 'ubicacion']

class CategoriasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categorias
        fields = ['id', 'nombre', 'descripcion']

class ProductosSerializer(serializers.ModelSerializer):
    categoria_nombre = serializers.ReadOnlyField(source='categoria.nombre')

    class Meta:
        model = Productos
        fields = ['id', 'nombre', 'descripcion', 'precio', 'categoria', 'categoria_nombre']

class InventarioSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.ReadOnlyField(source='producto.nombre')

    class Meta:
        model = Inventario
        fields = ['id', 'producto', 'producto_nombre', 'cantidad', 'unidad_medida']

class ProveedoresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedores
        fields = ['id', 'nombre', 'contacto']

class Productos_PedidoSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.ReadOnlyField(source='producto.nombre')

    class Meta:
        model = Productos_Pedido
        fields = ['id', 'pedido', 'producto', 'producto_nombre', 'cantidad']

class PedidosSerializer(serializers.ModelSerializer):
    productos = Productos_PedidoSerializer(many=True, read_only=True, source='productos_pedido_set')
    mesa_numero = serializers.ReadOnlyField(source='mesa.numero')

    class Meta:
        model = Pedidos
        fields = ['id', 'mesa', 'mesa_numero', 'fecha', 'estado', 'productos']

class UsuariosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuarios
        fields = ['id', 'nombre', 'usuario', 'contrasena', 'rol']
        extra_kwargs = {
            'contrasena': {'write_only': True}
        }

    def create(self, validated_data):
        print("Datos en serializer create:", validated_data)  # Debug
        return Usuarios.objects.create(**validated_data)

class PagosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pagos
        fields = ['id', 'pedido', 'metodo_pago', 'monto', 'fecha']

class Historial_PreciosSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.ReadOnlyField(source='producto.nombre')

    class Meta:
        model = Historial_Precios
        fields = ['id', 'producto', 'producto_nombre', 'precio_anterior', 'precio_nuevo', 'fecha_cambio']

class ReportesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reportes
        fields = ['id', 'tipo', 'fecha', 'datos']