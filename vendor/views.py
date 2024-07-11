from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

from .models import Vendor
from product.models import Product
from .forms import ProductForm

# Converting Title into Slug
from django.utils.text import slugify

# Create your views here.
# Para crear una vista, se debe crear una función que reciba un request y retorne un response
# Para renderizar un template, se debe usar la función render de Django
# Para redireccionar a otra ruta, se debe usar la función redirect de Django

# Esta función se encarga de renderizar el template vendor/vendors.html
def vendors(request):
    return render(request, 'vendor/vendors.html')

# Esta función se encarga de renderizar el template vendor/vendor.html
def become_vendor(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            vendor = Vendor.objects.create(name=user.username, created_by=user)

            return redirect('core:home')
    else:
        form = UserCreationForm()   

    return render(request, 'vendor/become_vendor.html', {'form': form})


@login_required # este decorador de Django requiere que el usuario esté autenticado para acceder a la vista
def vendor_admin(request):
    vendor = request.user.vendor
    products = vendor.products.all()
    orders = vendor.orders.all()
    for order in orders:
        order.vendor_amount = 0
        order.vendor_paid_amount = 0
        order.fully_paid = True

        for item in order.items.all():
            if item.vendor == request.user.vendor:
                if item.vendor_paid:
                    order.vendor_paid_amount += item.get_total_price()
                else:
                    order.vendor_amount += item.get_total_price()
                    order.fully_paid = False


    return render(request, 'vendor/vendor_admin.html', {'vendor': vendor, 'products': products, 'orders': orders})

@login_required
# Esta función se encarga de renderizar el template vendor/add_product.html
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            product = form.save(commit=False) # Because we have not given vendor yet
            product.vendor = request.user.vendor
            product.slug = slugify(product.title)
            product.save() #finally save

            return redirect('vendor:vendor-admin')

    else:
        form = ProductForm

    return render(request, 'vendor/add_product.html', {'form': form})


@login_required
# Esta función se encarga de renderizar el template vendor/edit_product.html
def edit_vendor(request):
    vendor = request.user.vendor

    if request.method == 'POST':
        name  = request.POST.get('name', '')
        email = request.POST.get('email', '')

        if name:
            vendor.created_by.email = email
            vendor.created_by.save()

            vendor.name = name
            vendor.save

            return redirect('vendor:vendor-admin')

    return render(request, 'vendor/edit_vendor.html', {'vendor': vendor})

@login_required
# Esta función se encarga de renderizar el template vendor/logout.html
def logout_vendor(request):
    logout(request)
    return redirect('core:home')

 # esta función se encarga de renderizar el template vendor/edit_product.html
def vendors(request):
    vendors = Vendor.objects.all()
    return render(request, 'vendor/vendors.html', {'vendors': vendors})
# esta función se encarga de renderizar el template vendor/vendor.html
def vendor(request, vendor_id):
    vendor = get_object_or_404(Vendor, pk=vendor_id)
    return render(request, 'vendor/vendor.html', {'vendor': vendor})


