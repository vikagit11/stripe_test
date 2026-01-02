from django.db import models

class Item(models.Model):
    CURRENCY_CHOICES = [
        ('usd', 'USD'),
        ('eur', 'EUR'),
    ]
    
    name = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    price = models.IntegerField(verbose_name="Цена", default=0)  
    
    currency = models.CharField(
        max_length=3, 
        choices=CURRENCY_CHOICES, 
        default='usd',
        verbose_name="Валюта"
    )
    
    
    def __str__(self):
        return self.name
        
    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        

class Discount(models.Model):
    value = models.IntegerField(default=0, verbose_name="Скидка в %")
    
    def __str__(self):
        return f"Скидка {self.value}%"

    class Meta:
        verbose_name = "Скидка"
        verbose_name_plural = "Скидки"

class Tax(models.Model):
    value = models.IntegerField(default=0, verbose_name="Налог в %")
    
    def __str__(self):
        return f"Налог {self.value}%"

    class Meta:
        verbose_name = "Налог"
        verbose_name_plural = "Налоги"

class Order(models.Model):
    items = models.ManyToManyField(Item, verbose_name="Товары")
    discount = models.ForeignKey(Discount, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Скидка")
    tax = models.ForeignKey(Tax, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Налог")
    
    def get_total_cost(self):                                                 # Считаем общую сумму всех товаров в заказе                                                  
        total = 0
        for item in self.items.all():
            total += item.price
        return total

    def __str__(self):
        return f"Заказ #{self.id}"

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"