import stripe
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views import View
from .models import Item, Order 

stripe.api_key = settings.STRIPE_SECRET_KEY

def get_item(request, id):
    item = get_object_or_404(Item, id=id)
    
    return render(request, 'item_detail.html', {
        'item': item,
        'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY
    })

def buy_item(request, id):
    item = get_object_or_404(Item, id=id)
    
    if item.currency == 'eur':
        stripe.api_key = settings.STRIPE_SECRET_KEY_EUR
    else:
        stripe.api_key = settings.STRIPE_SECRET_KEY_USD
    
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': item.currency,
                'product_data': {
                    'name': item.name,
                },
                'unit_amount': item.price * 100,
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=request.build_absolute_uri('/success/'),
        cancel_url=request.build_absolute_uri('/cancel/'),
    )
    return JsonResponse({'id': session.id})


class HomeView(View):
    def get(self, request):
        items = Item.objects.all()
        return render(request, 'home.html', {'items': items})


def order_detail(request, id):                                        # Определяем валюту заказа по первому товару
    order = get_object_or_404(Order, id=id)                    
    first_item = order.items.first()
    currency = 'usd'                                                  # Считаем, что в одном заказе товары одной валюты              
    if first_item and first_item.currency == 'eur':
        currency = 'eur'                                                          
    if currency == 'eur':
        public_key = settings.STRIPE_PUBLIC_KEY_EUR
    else:
        public_key = settings.STRIPE_PUBLIC_KEY_USD
    return render(request, 'order_detail.html', {
        'order': order,
        'STRIPE_PUBLIC_KEY': public_key
    })

def buy_order(request, id):
    order = get_object_or_404(Order, id=id)
                                                                    
    first_item = order.items.first()
    currency = 'usd'
    if first_item and first_item.currency == 'eur':
        currency = 'eur'
        stripe.api_key = settings.STRIPE_SECRET_KEY_EUR          
    else:
        stripe.api_key = settings.STRIPE_SECRET_KEY_USD            
    
                                                            
    tax_rate_id = None                                        # Если у заказа есть налог, создаем его в Stripe
    if order.tax:
        tax_rate = stripe.TaxRate.create(
            display_name="Налог",
            description="НДС",
            percentage=order.tax.value,                       # Берем цифру избазы 
            inclusive=False,                                  # Налог добавляется сверху цены 
        )
        tax_rate_id = tax_rate.id
    
                                                               # Собираем список товаров для Stripe
    items_list = []
    for item in order.items.all():
        line_item = {
            'price_data': {
                'currency': currency,
                'product_data': {
                    'name': item.name,
                },
                'unit_amount': item.price * 100,
            },
            'quantity': 1,
        }
                                                                 # Если налог создан, прикрепляем его к товару
        if tax_rate_id:
            line_item['tax_rates'] = [tax_rate_id]
            
        items_list.append(line_item)
        
    discounts_list = []                                          # Если у заказа есть скидка, создаем купон в Stripe
    if order.discount:
        coupon = stripe.Coupon.create(
            percent_off=order.discount.value,                    # Берем цифру из базы
            duration='once',
        )
        discounts_list.append({'coupon': coupon.id})

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=items_list,
        discounts=discounts_list,                                # Передаем скидку сюда
        mode='payment',
        locale='en',
        success_url=request.build_absolute_uri('/success/'),
        cancel_url=request.build_absolute_uri('/cancel/'),
    )

    return JsonResponse({'id': session.id})