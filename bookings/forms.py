from django import forms
from .models import Booking, Item, Client

class BookingForm(forms.ModelForm):
    items = forms.ModelMultipleChoiceField(
        queryset=Item.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-select', 'id': 'id_items'})
    )

    class Meta:
        model = Booking
        fields = ['client', 'event_name', 'start_date', 'end_date', 'notes', 'items']
        widgets = {
            'client': forms.Select(attrs={'class': 'form-select'}),
            'event_name': forms.TextInput(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class AddItemsForm(forms.Form):
    new_items = forms.ModelMultipleChoiceField(
        queryset=Item.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={
            'class': 'form-select',
            'id': 'id_new_items'
        })
    )

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'email', 'phone', 'notes']

