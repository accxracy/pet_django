from django.db import models
from main_page.models import Product
from login.models import User


class Order(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.SET_DEFAULT,
                             blank=True, null=True, default=None)
    
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField()
    city = models.CharField(max_length=125)
    address = models.CharField(max_length=275)
    postal_code = models.CharField(max_length=25)
    time = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)


    class Meta:
        ordering = ['-time']
        indexes = [
            models.Index(fields=['-time'])
        ]

    def __str__(self):
        return f'order {self.id}'
    
    def total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

class OrderItem(models.Model):
    order = models.ForeignKey(Order, 
                              related_name='items',
                              on_delete=models.CASCADE)
    
    product = models.ForeignKey(Product, 
                                related_name='order',
                                on_delete=models.CASCADE)
    
    price = models.DecimalField(max_digits=10, 
                                decimal_places=2)
    
    quantity = models.PositiveBigIntegerField(default=1)


    def __str__(self):
        return f'{self.id}'
    
    def get_cost(self):
        return self.price * self.quantity
