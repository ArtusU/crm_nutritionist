from django import forms
from django.forms import fields
from leads.models import Nutritionist


class NutritionistModelForm(forms.ModelForm):
    class Meta:
        model = Nutritionist
        fields = (
            'user',
        )