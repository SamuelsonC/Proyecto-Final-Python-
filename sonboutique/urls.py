
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

# Aquí se definen las rutas de la aplicación
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('vendor/', include('vendor.urls')),
    path('product/', include('product.urls')),
    path('cart/', include('cart.urls')),
    path('order/', include('order.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
