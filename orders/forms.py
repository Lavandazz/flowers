import re

from django import forms


class CreateOrderForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    phone_number = forms.CharField()
    requires_delivery = forms.ChoiceField(
        choices=[
            ("0", False),
            ("1", True),
        ],
    )
    delivery_address = forms.CharField(required=False)
    comment = forms.CharField(required=False)

    def clean_phone_number(self):
        """ Валидация номера телефона """
        # Берем номер телефона из формы
        data = self.cleaned_data['phone_number']

        if not data.isdigit():
            raise forms.ValidationError("Номер телефона должен содержать только цифры")

        pattern = re.compile(r'^\d{10}$')
        if not pattern.match(data):
            raise forms.ValidationError("Неверный формат номера")

        return data

    def clean(self):
        cleaned_data = super().clean()
        requires_delivery = cleaned_data.get('requires_delivery')  # Ловит кнопку доставки строка "0" или "1"
        delivery_address = cleaned_data.get('delivery_address')  # Ловит комментарий
        print('Работает clean, requires_delivery', requires_delivery, 'delivery_address', delivery_address)
        if requires_delivery == "1" and not delivery_address:
            self.add_error('delivery_address', 'Укажите адрес доставки')

        return cleaned_data