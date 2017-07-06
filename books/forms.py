import urllib
from django import forms
from django.core.validators import MinValueValidator

class BookForm(forms.Form):
    book_id = forms.IntegerField()
    title = forms.CharField()
    quantity = forms.IntegerField(min_value=1, max_value=10)
    price = forms.DecimalField()
    delete = forms.ChoiceField(widget=forms.CheckboxInput, choices=((True, True), (False, False)))