from django import forms


class CartForm(forms.Form):
    name = forms.CharField(max_length=100, label='Ваше имя')
    phone = forms.IntegerField(label='Номер телефона')
    address = forms.CharField(max_length=1000, label='Адрес для доставки')