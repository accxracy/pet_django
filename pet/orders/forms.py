from django import forms
from .models import Order

class OrderCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        order = super().save(commit=False)
        if self.request and self.request.user.is_authenticated:
            order.user = self.request.user
        if commit:
            order.save()
        return order

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'city', 'address', 'postal_code']
