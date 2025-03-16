from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import (
    Mesas, Categorias, Productos, Inventario, Proveedores,
    Pedidos, Productos_Pedido, Usuarios, Pagos, Historial_Precios, Reportes
)
from .serializer import (
    MesasSerializer, CategoriasSerializer, ProductosSerializer, InventarioSerializer,
    ProveedoresSerializer, PedidosSerializer, Productos_PedidoSerializer,
    UsuariosSerializer, PagosSerializer, Historial_PreciosSerializer, ReportesSerializer
)
from rest_framework_simplejwt.tokens import RefreshToken

class MesasViewSet(viewsets.ModelViewSet):
    queryset = Mesas.objects.all()
    serializer_class = MesasSerializer

    @action(detail=False, methods=['get'])
    def disponibles(self, request):
        mesas = Mesas.objects.filter(estado='disponible')
        serializer = self.get_serializer(mesas, many=True)
        return Response(serializer.data)

class CategoriasViewSet(viewsets.ModelViewSet):
    queryset = Categorias.objects.all()
    serializer_class = CategoriasSerializer

class ProductosViewSet(viewsets.ModelViewSet):
    queryset = Productos.objects.all()
    serializer_class = ProductosSerializer

    @action(detail=False, methods=['get'])
    def por_categoria(self, request):
        categoria_id = request.query_params.get('categoria_id')
        productos = Productos.objects.filter(categoria_id=categoria_id)
        serializer = self.get_serializer(productos, many=True)
        return Response(serializer.data)

class InventarioViewSet(viewsets.ModelViewSet):
    queryset = Inventario.objects.all()
    serializer_class = InventarioSerializer

class ProveedoresViewSet(viewsets.ModelViewSet):
    queryset = Proveedores.objects.all()
    serializer_class = ProveedoresSerializer

class PedidosViewSet(viewsets.ModelViewSet):
    queryset = Pedidos.objects.all()
    serializer_class = PedidosSerializer

    @action(detail=False, methods=['get'])
    def activos(self, request):
        pedidos = Pedidos.objects.filter(estado='abierto')
        serializer = self.get_serializer(pedidos, many=True)
        return Response(serializer.data)

class Productos_PedidoViewSet(viewsets.ModelViewSet):
    queryset = Productos_Pedido.objects.all()
    serializer_class = Productos_PedidoSerializer

from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Usuarios
from .serializer import UsuariosSerializer
from rest_framework.decorators import action
import bcrypt

class UsuariosViewSet(viewsets.ModelViewSet):
    queryset = Usuarios.objects.all()
    serializer_class = UsuariosSerializer

    @action(detail=False, methods=['POST'])
    def login(self, request):
        usuario = request.data.get('usuario')
        contrasena = request.data.get('contrasena')
        
        try:
            user = Usuarios.objects.get(usuario=usuario)
            
            if bcrypt.checkpw(contrasena.encode('utf-8'), user.contrasena.encode('utf-8')):
                # Generar token JWT
                refresh = RefreshToken.for_user(user)
                return Response({
                    'access': str(refresh.access_token),
                    'refresh': str(refresh),
                    'user': {
                        'id': user.id,
                        'nombre': user.nombre,
                        'usuario': user.usuario,
                        'rol': user.rol
                    },
                    'message': 'Login exitoso'
                })
            else:
                return Response({
                    'error': 'Credenciales inválidas'
                }, status=status.HTTP_401_UNAUTHORIZED)
        except Usuarios.DoesNotExist:
            return Response({
                'error': 'Credenciales inválidas'
            }, status=status.HTTP_404_NOT_FOUND)

    def create(self, request, *args, **kwargs):
        print("Datos recibidos en create:", request.data)
        data = request.data.copy()  # Hacer una copia de los datos
        
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
           # print("Datos validados (incluyendo contraseña):", serializer.validated_data)
            usuario = serializer.save()  # Esto llamará al create del serializer
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        print("Errores de validación:", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PagosViewSet(viewsets.ModelViewSet):
    queryset = Pagos.objects.all()
    serializer_class = PagosSerializer

class Historial_PreciosViewSet(viewsets.ModelViewSet):
    queryset = Historial_Precios.objects.all()
    serializer_class = Historial_PreciosSerializer

class ReportesViewSet(viewsets.ModelViewSet):
    queryset = Reportes.objects.all()
    serializer_class = ReportesSerializer
