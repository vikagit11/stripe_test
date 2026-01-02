from django.contrib import admin
from .models import Item, Order, Discount, Tax

@admin.register(Item)                                                       # Настройка для Товаров (Item
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'description')                         # колонки  в таблице
    
@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('id', 'value')

@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):
    list_display = ('id', 'value')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_total_cost', 'discount', 'tax')           # ID заказа и Общую сумму
