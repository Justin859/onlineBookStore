from django import forms

class BookForm(forms.Form):
    book_id = forms.IntegerField()
    title = forms.CharField()
    quantity = forms.IntegerField()
    price = forms.DecimalField()
    delete = forms.ChoiceField(widget=forms.CheckboxInput, choices=((True, True), (False, False)))