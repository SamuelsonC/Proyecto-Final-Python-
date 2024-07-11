from django.contrib.auth.models import User
from django.db import models
from django.db.models.fields.related import OneToOneField

# Create your models here.
# Un modelo en Django es una clase que hereda de django.db.models.Model
# Cada atributo de la clase representa una columna en la tabla de la base de datos
# Cada instancia de la clase representa una fila en la tabla de la base de datos
# Cada atributo de la clase es una instancia de una subclase de django.db.models.Field
# Cada subclase de Field representa un tipo de dato en la base de datos
# Cada subclase de Field tiene argumentos que permiten configurar la columna en la base de datos

# Esta clase representa un modelo de datos en la base de datos
class Vendor(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.OneToOneField(User, related_name='vendor', on_delete=models.CASCADE)
    # Un modelo puede tener un campo que haga referencia a otro modelo
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name

    def get_balance(self):
        items = self.items.filter(vendor_paid=False, order__vendors__in=[self.id])
        return sum((item.product.price * item.quantity) for item in items)

    def get_paid_amount(self):
        items = self.items.filter(vendor_paid=True, order__vendors__in=[self.id])
        return sum((item.product.price * item.quantity) for item in items)

