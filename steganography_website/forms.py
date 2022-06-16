from django import forms

from django.forms import ModelForm
from .models import StegoObjctStore

LAYER_CHOICES= [
    ('red', 'RED / R'),
    ('green', 'GREEN / G'),
    ('blue', 'BLUE / B'),
    ]

class EncodindForm(forms.Form):

	user_input = forms.ImageField()
	secret_data_path = forms.FileField()
	layer_choice = forms.CharField(widget = forms.Select(choices = LAYER_CHOICES , attrs={'class' : 'form-control'}))
	stego_file_name = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control'}))
	file_location = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control'}))


class DecodingForm(forms.Form):

	user_input = forms.ImageField()
	layer_choice = forms.CharField(widget = forms.Select(choices = LAYER_CHOICES , attrs={'class' : 'form-control'}))
	stego_file_name = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control'}))
	file_location = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control'}))


class StegoObjectStoreForm(ModelForm):
	class Meta:
		model = StegoObjctStore
		fields = ('name', 'image')