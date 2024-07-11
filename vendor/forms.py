from django.forms import ModelForm, models

from product.models import Product
# Un formulario en Django es una clase que hereda de django.forms.Form
# Cada atributo de la clase representa un campo en el formulario

# Esta clase representa un formulario de datos en la aplicación
class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'image', 'title', 'description', 'price']