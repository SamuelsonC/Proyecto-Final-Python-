from django.urls import path

from order.views import top_selling_products


app_name = 'order'


urlpatterns = [
     path('top-selling-products/', top_selling_products, name='top-selling-products'),
]
