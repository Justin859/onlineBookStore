import urllib
from django import forms
from django.core.validators import MinValueValidator

class BookForm(forms.Form):
    book_id = forms.IntegerField()
    title = forms.CharField()
    quantity = forms.IntegerField(min_value=1, max_value=10)
    price = forms.DecimalField()
    delete = forms.ChoiceField(widget=forms.CheckboxInput, choices=((True, True), (False, False)))

class CheckOutForm(forms.Form):
    merchant_id = forms.IntegerField(widget=forms.HiddenInput(), initial=10004715)
    merchant_key = forms.CharField(widget=forms.HiddenInput(), initial='dhdw9uqzmpzo0')
    return_url = forms.CharField(widget=forms.HiddenInput(), initial='http://127.0.0.1:5000/success')
    cancel_url = forms.CharField(widget=forms.HiddenInput(), initial='http://127.0.0.1:5000/cancel')
    notify_url = forms.CharField(widget=forms.HiddenInput(), initial='http://127.0.0.1:5000/notify')
    name_first = forms.CharField(widget=forms.HiddenInput())
    name_last = forms.CharField(widget=forms.HiddenInput())
    amount = forms.IntegerField()
    item_name = forms.CharField()