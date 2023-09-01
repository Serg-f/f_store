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

    class Meta:
        model = Order
        fields = ('first_name', 'last_name', 'email', 'address')
