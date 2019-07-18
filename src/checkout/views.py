from django.shortcuts import render, get_object_or_404, redirect
import stripe
from .forms import OrderForm, PaymentForm
from django.conf import settings
from django.contrib import messages
from django.utils import timezone
from products.models import Product
from .models import OrderLineItem

# Create your views here.
stripe.api_key = settings.STRIPE_SECRET

def checkout(request):
   
   order_form = OrderForm(request.POST or None)
   payment_form = PaymentForm(request.POST or None)

   if order_form.is_valid() and payment_form.is_valid():
      order = order_form.save(commit=False)
      order.date = timezone.now()
      order.save()


      cart = request.session.get('cart', {})
      total = 0
      for id, quantity in cart.items():
         product = get_object_or_404(Product, pk=id)
         total += quantity * product.price
         order_line_item = OrderLineItem(
            order = order,
            product = product,
            quantity = quantity
         )

         if product.stock > quantity:
            new_stock = product.stock - quantity
            product.stock = new_stock
            product.save()

         else:
            print(product, "not enough at stock")
            context = {
               'order_form': order_form,
               'payment_form': payment_form,
               'publishable': settings.STRIPE_PUBLISHABLE,
               'product': product,
               'quantity': product.stock,
               'stock': "Not enough in stock",
            }

            return render(request, "checkout.html", context)

         order_line_item.save()

      if request.user.is_authenticated:
         try:
            customer = stripe.Charge.create(
               amount = int(total * 100),
               currency = "EUR",
               description = request.user.email,
               card = payment_form.cleaned_data['stripe_id']
            )
         except stripe.error.CardError:
            messages.error(request, "Your card was declined")
      else:
         try:
            customer = stripe.Charge.create(
               amount = int(total * 100),
               currency = "EUR",
               card = payment_form.cleaned_data['stripe_id']
            )
         except stripe.error.CardError:
            messages.error(request, "Your card was declined")
     

      if customer.paid:
         messages.error(request, "You have successfully paid")
         request.session['cart'] = {}
         return redirect('home')
      else:
         messages.error(request, "Unable o take payment")
      
   context = {
      'order_form': order_form,
      'payment_form': payment_form,
      'publishable': settings.STRIPE_PUBLISHABLE
   }

   return render(request, "checkout.html", context)

