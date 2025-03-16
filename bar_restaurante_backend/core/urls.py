from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    MesasViewSet, CategoriasViewSet, ProductosViewSet, InventarioViewSet,
    ProveedoresViewSet, PedidosViewSet, Productos_PedidoViewSet,
    UsuariosViewSet, PagosViewSet, Historial_PreciosViewSet, ReportesViewSet
)

router = DefaultRouter()
router.register(r'mesas', MesasViewSet)
router.register(r'categorias', CategoriasViewSet)
router.register(r'productos', ProductosViewSet)
router.register(r'inventario', InventarioViewSet)
router.register(r'proveedores', ProveedoresViewSet)
router.register(r'pedidos', PedidosViewSet)
router.register(r'productos-pedido', Productos_PedidoViewSet)
router.register(r'usuarios', UsuariosViewSet)
router.register(r'pagos', PagosViewSet)
router.register(r'historial-precios', Historial_PreciosViewSet)
router.register(r'reportes', ReportesViewSet)

urlpatterns = [
    path('', include(router.urls)),
]