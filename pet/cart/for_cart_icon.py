from .cart import Cart

def cart_info(request):
    return {'cart': Cart(request)}