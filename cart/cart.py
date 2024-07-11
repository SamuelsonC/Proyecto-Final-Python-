from django.conf import settings

from product.models import Product

# Esta clase representa un carrito de compras
class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)

        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}

        self.cart = cart
# Esta función devuelve un iterador que recorre los elementos del carrito
    def __iter__(self):
        for p in self.cart.keys():
            self.cart[str(p)]['product'] = Product.objects.get(pk=p)

        for item in self.cart.values():
            item['total_price'] = item['product'].price * item['quantity']

            yield item
# Esta función devuelve la cantidad de elementos en el carrito
    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())
# Esta función añade un producto al carrito
    def add(self, product_id, quantity=1, update_quantity=False):
        product_id = str(product_id)

        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 1, 'id': product_id}

        if update_quantity:
            self.cart[product_id]['quantity'] += int(quantity)
            
            if self.cart[product_id]['quantity'] == 0:
                self.remove(product_id)
        
        self.save()
# Esta función remueve un producto del carrito
    def remove(self, product_id):
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()
# Esta función guarda el carrito en la sesión
    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True
# Esta función vacía el carrito
    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
# Esta función devuelve el costo total de los productos en el carrito
    def get_total_cost(self):
        for p in self.cart.keys():
            self.cart[str(p)]['product'] = Product.objects.get(pk=p)

        return sum(item['quantity'] * item['product'].price for item in self.cart.values())

        
