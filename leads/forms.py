from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.http import request
from .models import Lead, Nutritionist, Category, FollowUp

User = get_user_model()

class LeadModelForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = (
            'first_name',
            'last_name',
            'age',
            'nutritionist',
            'description',
            'phone_number',
            'email',
            'profile_picture'
        )

    def clean_email(self):
        data = self.cleaned_data['email']
        # if data != "*@*.*":
        #     raise ValidationError('Your email must consist @ sign.')
        return data
    
    def clean(self):
        pass
        # first_name = self.cleaned_data['first_name']
        # last_name = self.cleaned_data['last_name']
        # if first_name + last_name != "Mimi Vegas":
        #     raise ValidationError("You name is not Mimi Vegas")


class LeadForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    age = forms.IntegerField(min_value=16)

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username",)
        field_classes = {'username': UsernameField}

class AssignNutritionistForm(forms.Form):
    nutritionist = forms.ModelChoiceField(queryset=Nutritionist.objects.none())


    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request")
        nutritionists = Nutritionist.objects.filter(organization=request.user.organization)
        super(AssignNutritionistForm, self).__init__(*args, **kwargs)
        self.fields["nutritionist"].queryset = nutritionists


class LeadCategoryUpdateForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = (
            'category',
        )

class CategoryModelForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = (
            'name',
        )


class FollowUpModelForm(forms.ModelForm):
    class Meta:
        model = FollowUp
        fields = (
            'notes',
            'file'
        )


        