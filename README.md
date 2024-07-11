
# Web sencilla para proveedores-compradores usando Django
Este es un sitio web de comercio electrónico simple de múltiples proveedores construido con Django.

En este sitio web, los proveedores (tiendas) pueden registrarse y agregar sus productos.

Y los usuarios pueden visitar el producto y comprar pagando con Tarjeta de Débito/Crédito (Stripe).

Luego, el proveedor recibe la notificación por correo electrónico sobre el pedido y debe entregar el producto al cliente según los detalles de la dirección.

El código lo he escrito en inglés emulando un proyecto real, sin embargo, los comentarios y aclaraciones los haré en español.

En caso de que se quisiera, se podría eliminar la base de datos y crear nuevas categorías para otros proyectos, aquí dejo un script sencillo para ello:
"""
import os
import django

# Configura el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ProyectoFinal.settings')
django.setup()

from product.models import Category

# Lista de categorías para crear
categories = ['Electronics', 'Clothing', 'Books']

for category_name in categories:
    Category.objects.get_or_create(name=category_name)

print("Categorías creadas exitosamente.") """+

Solo faltaría ejecutar el script desde el terminal.

# Características del proyecto

# Los administradores podrán
1. Gestionar Categoría (Agregar, Actualizar, Filtrar y Eliminar)
2. Gestionar Productos (Agregar, Actualizar, Filtrar y Eliminar)
3. Gestionar Usuarios (Actualizar, Filtrar y Eliminar)
4. Gestionar Pedidos (Ver y Procesar)

# 2. Los proveedores podrán
1. Agregar productos
2. Obtener pedidos y gestionarlos
3. Recibir notificación Cuando un usuario realiza un pedido
4. Actualizar Perfil


#  Los usuario podrán 
1. Agregar al Carrito
2. Hacer pedidos y pagar con Tarjeta de débito/crédito 
3. Recibir notificación por correo electrónico sobre la confirmación del pedido

## Instalar y ejecutar el proyecto

# Requisitos:
- Tener instalado el control de versiones de git

- Tener instalado Python

- Tener instalado el instalador "pip"

# Instalación
**1. Crear un entorno virtual y activarlo**
 (Algunos IDE como PyCharm tienen una pestaña dónde hacerlo automáticamente)
Proceso en terminal:

En Windows

$  python -m venv .venv

En Mac:

$  python3 -m venv venv


Activar el mismo

En windows:

$  source venv/scripts/activate

En Mac:

$  source venv/bin/activate

**4. Instalar los paquetes, generado automáticamente con pip 'requirements.txt'**

$  pip install -r requirements.txt

*5. Arrancar la app*

Para terminal de Windows:

$ python manage.py runserver

Para terminal de Mac:

$ python3 manage.py runserver


*6. Para acceder a las potestades del ADMIN*

Crear un "super user" (Admin)

Comando para Windows:

$  python manage.py createsuperuser


Comando para Mac:

$  python3 manage.py createsuperuser

Añadir correo electrónico, usuario y contraseña.
