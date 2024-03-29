from orders.models import Order
from django import forms


class SetHtmlClassMixin(forms.Form):
    def __init__(self, *args, **kwargs):
        fields_for_edit = ('first_name', 'last_name', 'email', 'address')
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name in fields_for_edit:
                field.widget.attrs['class'] = 'form-control'


class OrderForm(SetHtmlClassMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['address'].widget.attrs['placeholder'] = 'Enter your address here'
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter your first name here'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter your last name here'

    class Meta:
        model = Order
        fields = ('first_name', 'last_name', 'email', 'address')
