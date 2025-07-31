import json
from math import ceil

import razorpay
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import Product

# Create your views here.
from math import ceil
from django.shortcuts import render
from .models import Product, Contact, Order, OrderUpdate
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q


def welcome(request):
    return render(request, 'shop/welcome.html')  #Renders a welcome page (shop/welcome.html).

def index(request):
    allProds = []
    # Get unique categories from products
    categories = Product.objects.values_list('category', flat=True).distinct() #Groups products by category.

    for cat in categories:  #Creates chunks of 4 for carousel slides.
        # Get all products in this category
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))

        allProds.append({
            'title': cat,
            'chunks': [prod[i:i + 4] for i in range(0, n, 4)],
            'range': range(nSlides)
        })

    context = {'allprods': allProds}
    return render(request, 'shop/index.html', context) #Sends grouped products (all prods) to index.html.

#about(request)
def about(request):
    return render(request, 'shop/about.html')

#contact(request)
def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        contact = Contact(name=name, email=email, phone=phone, message=message)
        contact.save()

        # For now, just print to console or handle as needed
        print("🔔 Contact Form Submitted:")
        print(f"Name: {name}")
        print(f"Email: {email}")
        print(f"Phone: {phone}")
        print(f"Message: {message}")

        messages.success(request, "Thank you for contacting us! We will get back to you soon.")
        return render(request, 'shop/contact.html')

    return render(request, 'shop/contact.html')

#tracker(request)
def tracker(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        email = request.POST.get('email')
        #Lets users track orders using order_id + email.
        #Loads current order updates and product details.
        #items_json = json.loads(order.items_json)
        try:
            order = Order.objects.get(id=order_id, email=email)
            updates = OrderUpdate.objects.filter(order_id=order).order_by('-timestamp')

            # Get current delivery status from the latest update
            current_status = updates[0].update_desc if updates else "No updates yet"

            items_json = json.loads(order.items_json)

            products = []
            for pid, info in items_json.items():
                try:
                    product = Product.objects.get(product_id=int(pid))
                    product.qty = info.get('qty', 1)
                    product.subtotal = round(product.price * product.qty, 2)
                    product.delivery_status = current_status  # assign latest status
                    products.append(product)
                except Product.DoesNotExist:
                    continue

            return render(request, 'shop/tracker.html', {
                'order': order,
                'updates': updates,
                'products': products,
                'current_status': current_status
            })

        except Order.DoesNotExist:
            return render(request, 'shop/tracker.html',
                          {'error': 'Order not found. Please check your Order ID and Email.'})

    return render(request, 'shop/tracker.html')


def search(request):
    return render(request, 'shop/search.html')


def productView(request, id):  # ✅ `id` is the parameter from URL
    product = Product.objects.get(product_id=id)  # ✅ use `id` directly
    print(product)
    return render(request, 'shop/productview.html', {'product': product})


#checkout(request) → Form submission handler
#Handles checkout form.
#Gets all form data + cart JSON.
#Saves Order.
#Redirects to thankyou page with order_id.
@csrf_exempt
def checkout(request):
    if request.method == "POST":
        cartdata = request.POST.get("cartdata")
        name = request.POST.get("name")
        email = request.POST.get("email")
        address = request.POST.get("address")
        city = request.POST.get("city")
        state = request.POST.get("state")
        zip_code = request.POST.get("zip")
        payment_method = request.POST.get("payment_method")
        amount = float(request.POST.get("amount", "0"))

        order = Order.objects.create(
            name=name, email=email, address=address, city=city, state=state,
            zip_code=zip_code, payment_method=payment_method,
            items_json=cartdata, amount=amount
        )

        return redirect(f"/shop/thankyou/?order_id={order.id}")
    return render(request, "shop/checkout.html")


from django.shortcuts import render


def proceed_to_payment(request):
    order_id = request.GET.get("order_id")
    try:
        order = Order.objects.get(id=order_id)
        return render(request, 'shop/payment/proceed.html', {'order': order})
    except Order.DoesNotExist:
        return redirect('index')


from django.shortcuts import render, redirect
from .models import Order

#proceed_to_payment(request)
#Renders intermediate payment step.

#payment_success(request)
#Handles the success page after payment.
#If order ID is missing/invalid → shows dummy test success.
#Else fetches actual order and renders success info.
def payment_success(request):
    order_id = request.POST.get('order_id') or request.GET.get('order_id')

    # Fallback if no order_id or invalid
    if not order_id or not order_id.isdigit():
        return render(request, 'shop/payment/payment_success.html', {
            'order_id': 'TEST123',
            'email': 'test@example.com',
            'amount': 999,
        })

    try:
        order = Order.objects.get(id=int(order_id))
        return render(request, 'shop/payment/payment_success.html', {
            'order_id': order.id,
            'email': order.email,
            'amount': order.amount,

        })
    except Order.DoesNotExist:
        return render(request, 'shop/payment/payment_success.html', {
            'order_id': 'INVALID',
            'email': 'not found',
            'amount': 0,
        })

#thankyou(request)
#Shown after placing an order.
#Receives and shows order_id.
def thankyou(request):
    order_id = request.GET.get('order_id')
    return render(request, 'shop/thankyou.html', {'order_id': order_id})

#SEARCH FUNCTIONALITY
from django.shortcuts import render
from .models import Product

def search(request):
    query = request.GET.get('query', '')
    results = []

    if query:
        results = Product.objects.filter(product_name__icontains=query)  # Simple name-based search

    context = {
        'query': query,
        'results': results
    }

    return render(request, 'shop/search.html', context)
