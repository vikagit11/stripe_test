# main/urls.py
from django.urls import path
from django.views.generic import TemplateView
from . import views 

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    
    path('item/<int:id>/', views.get_item, name='item_detail'),
    path('buy/<int:id>/', views.buy_item, name='buy_item'),

    path('order/<int:id>/', views.order_detail, name='order_detail'),
    path('buy_order/<int:id>/', views.buy_order, name='buy_order'),

    path('success/', TemplateView.as_view(template_name='success.html'), name='success'),
    path('cancel/', TemplateView.as_view(template_name='cancel.html'), name='cancel'),
]
