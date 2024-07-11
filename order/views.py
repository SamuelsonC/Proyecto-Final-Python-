from django.shortcuts import render
from product.models import Product
from django.db.models import Sum
import plotly.graph_objects as go 
import plotly.io as pio
import io
import base64

def top_selling_products(request):
    # Obtener los datos de los productos más vendidos
    top_products = Product.objects.annotate(total_sold=Sum('items__quantity')).order_by('-total_sold')[:10]

    # Crear la gráfica
    product_names = [product.title for product in top_products]
    units_sold = [product.total_sold for product in top_products]

    fig = go.Figure(data=[
        go.Bar(x=product_names, y=units_sold, marker_color='blue')
    ])

    fig.update_layout(
        title='Top Selling Products',
        xaxis_title='Products',
        yaxis_title='Units Sold'
    )

    # Convertir la gráfica a imagen
    buffer = io.BytesIO()
    pio.write_image(fig, buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph_url = base64.b64encode(image_png).decode('utf8')

    # Pasar la URI de la imagen a la plantilla
    return render(request, 'order/top_selling_products.html', {'graph': graph_url})


def update_stock(product_id, quantity_sold):
    product = Product.objects.get(id=product_id)
    product.stock -= quantity_sold
    product.save()
    product.check_stock_and_notify()
    
