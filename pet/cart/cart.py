from decimal import Decimal
from django.conf import settings
from main_page.models import Product


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, override_quantity=False):
        product_id = str(product.id)

        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,
                                     'price': str(product.price)}
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity

        else:
            self.cart[product_id]['quantity'] += quantity

        self.save()


    def save(self):
        self.session.modified = True

    
    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)

        cart = self.cart.copy()

        for product in products:
            item = cart[str(product.id)]
            item['product'] = product
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            item['product_id'] = product.id

            if product.discount and product.discount > 0:
                item['discount'] = product.discount
                item['sell_price'] = format(item['price'] * (1 - product.discount / 100), '.2f')
            else:
                item['discount'] = 0
                item['sell_price'] = item['price']

            yield item



    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())
    

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def get_total_price(self):
        return format(
        sum(
        (Decimal(item['price']) * (1 - Decimal(item['product'].discount) / 100)) * item['quantity']
        for item in self.cart.values()
        ),
        '.2f'
)
