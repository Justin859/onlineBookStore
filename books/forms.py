import urllib

from django import forms
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import User

# Custom validators

def validate_user(value):
    user = User.objects.filter(username=value)
    if user:
        raise ValidationError(
            _('%(value)s already exists'),
            params={'value': value},
        )

# Forms        

class BookForm(forms.Form):
    book_id = forms.IntegerField()
    title = forms.CharField()
    quantity = forms.IntegerField(min_value=1, max_value=10)
    price = forms.DecimalField()
    delete = forms.ChoiceField(widget=forms.CheckboxInput, choices=((True, True), (False, False)))

class CheckOutForm(forms.Form):
     merchant_id = forms.IntegerField(widget=forms.HiddenInput(), initial=10004715)
     merchant_key = forms.CharField(widget=forms.HiddenInput(), initial='dhdw9uqzmpzo0')
     return_url = forms.CharField(widget=forms.HiddenInput(), initial='http://desolate-basin-41691.herokuapp.com/success')
     cancel_url = forms.CharField(widget=forms.HiddenInput(), initial='http://desolate-basin-41691.herokuapp.com/cancel')
     notify_url = forms.CharField(widget=forms.HiddenInput(), initial='http://desolate-basin-41691.herokuapp.com/notify/')
     name_first = forms.CharField(widget=forms.HiddenInput())
     name_last = forms.CharField(widget=forms.HiddenInput())
     amount = forms.IntegerField()

class SignupForm(forms.Form):
    username = forms.EmailField(max_length=55, label='your email address', validators=[validate_user])
    password1 = forms.CharField(max_length=255, label='create a password')
    password2 = forms.CharField(max_length=255, label='re-enter password')
    firstname = forms.CharField(min_length=2, max_length=255, label='your firstname')
    lastname = forms.CharField(min_length=2, max_length=255, label='your lastname')

    def clean(self):

        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")

        return self.cleaned_data
