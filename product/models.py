# Form Images
from io import BytesIO
from os import name
from PIL import Image
from django.core.files import File

from django.db import models
from vendor.models import Vendor
from django.contrib import messages


# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=55)
    ordering = models.IntegerField(default=0)

    class Meta:
        ordering = ['ordering']

    def __str__(self):
        return self.title


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, related_name="products", on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=55)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    added_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='uploads/', blank=True, null=True) # Campo para la miniatura de la imagen
    initial_stock = models.PositiveIntegerField(default=20) # Stock inicial
    stock = models.PositiveIntegerField()
    # Añado umbral de stock para la notificación
    stock_threshold = models.FloatField(default=0.9) # 90% de stock
    
    #esto muestra un mensaje en la consola, pero en un proyecto real se enviaría un correo electrónico
    def send_low_stock_notification(self, request):
        messages.warning(request, f"Low stock alert: Only {self.stock} units left for {self.title}! Initial stock was {self.initial_stock}.")
        
    #para que todos los productos tengan un stock inicial minimo de 20
    def save(self, *args, **kwargs):
        if not self.initial_stock:
            self.initial_stock = self.stock
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-added_date']

    def __str__(self):
        return self.title

    # este método se encarga de retornar la URL de la imagen y si no hay imagen, retorna una imagen por defecto
    def get_thumbnail(self):
        if self.thumbnail:
            return self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()
                return self.thumbnail.url
            
            else:
                # Imagen por defecto
                return 'https://via.placeholder.com/240x180.jpg'
    
   # este método se encarga de crear una miniatura de la imagen
    def make_thumbnail(self, image, size=(300, 200)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)

        thumbnail = File(thumb_io, name=image.name)

        return thumbnail


