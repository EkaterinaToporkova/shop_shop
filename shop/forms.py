from django import forms

from shop.models import Product


class ImageForm(forms.ModelForm):

   class Meta:
      model = Product
      fields = ['image']