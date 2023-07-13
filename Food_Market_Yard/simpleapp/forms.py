from django import forms
from django.core.exceptions import ValidationError
from .models import Product
class ProductForm(forms.ModelForm):
   class Meta:
       model = Product
       fields = '__all__'

   def clean(self):
       cleaned_data = super().clean()
       name = cleaned_data.get("name")
       description = cleaned_data.get("description")

       if name == description:
           raise ValidationError(
               "Описание не должно быть идентично названию."
           )

       return cleaned_data