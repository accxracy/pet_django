from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']




@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'city', 
                    'address', 'postal_code', 'paid', 'time', 'updated']
    
    list_filter = ['paid', 'time', 'updated']

    inlines = [OrderItemInline]