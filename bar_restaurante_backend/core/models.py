from django.db import models
import bcrypt

class Mesas(models.Model):
    numero = models.IntegerField(unique=True)
    estado = models.CharField(max_length=20, default='disponible')
    ubicacion = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f'Mesa {self.numero}'

class Categorias(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

class Productos(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.ForeignKey(Categorias, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

class Inventario(models.Model):
    producto = models.ForeignKey(Productos, on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    unidad_medida = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.producto.nombre} - {self.cantidad} {self.unidad_medida}'

class Proveedores(models.Model):
    nombre = models.CharField(max_length=100)
    contacto = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre

class Pedidos(models.Model):
    mesa = models.ForeignKey(Mesas, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, default='abierto')

    def __str__(self):
        return f'Pedido {self.id} - Mesa {self.mesa.numero}'

class Productos_Pedido(models.Model):
    pedido = models.ForeignKey(Pedidos, on_delete=models.CASCADE)
    producto = models.ForeignKey(Productos, on_delete=models.CASCADE)
    cantidad = models.IntegerField()

    def __str__(self):
        return f'{self.producto.nombre} - {self.cantidad}'

class Usuarios(models.Model):
    nombre = models.CharField(max_length=100)
    usuario = models.CharField(max_length=50, unique=True)
    contrasena = models.CharField(max_length=255)
    rol = models.CharField(max_length=20)

    def save(self, *args, **kwargs):
        if self.contrasena and not self.contrasena.startswith('$2b$'):
            # Debug print
            #print(f"Encriptando contraseña para usuario: {self.usuario}")
            password = self.contrasena.encode('utf-8')
            salt = bcrypt.gensalt()
            hashed = bcrypt.hashpw(password, salt)
            self.contrasena = hashed.decode('utf-8')
            #print(f"Contraseña encriptada: {self.contrasena}")
        super().save(*args, **kwargs)

    def check_password(self, raw_password):
        try:
            return bcrypt.checkpw(
                str(raw_password).encode('utf-8'),
                self.contrasena.encode('utf-8')
            )
        except Exception as e:
            #print(f"Error al verificar contraseña: {e}")
            return False

    def __str__(self):
        return self.nombre

class Pagos(models.Model):
    pedido = models.ForeignKey(Pedidos, on_delete=models.CASCADE)
    metodo_pago = models.CharField(max_length=50)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Pago {self.id} - Pedido {self.pedido.id}'

class Historial_Precios(models.Model):
    producto = models.ForeignKey(Productos, on_delete=models.CASCADE)
    precio_anterior = models.DecimalField(max_digits=10, decimal_places=2)
    precio_nuevo = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_cambio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.producto.nombre} - {self.fecha_cambio}'

class Reportes(models.Model):
    tipo = models.CharField(max_length=50)
    fecha = models.DateField()
    datos = models.JSONField()

    def __str__(self):
        return f'{self.tipo} - {self.fecha}'