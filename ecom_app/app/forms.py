from django import forms
from .models import MyCart, UserProfile
from django.contrib.auth.models import User


class MyCartForm(forms.ModelForm):
    class Meta:
        model = MyCart
        fields = ['product', 'quantity', 'shipping']


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-controls'}),
            'email': forms.EmailInput(attrs={'class': 'form-controls'}),
            'first_name': forms.TextInput(attrs={'class': 'form-controls'}),
            'last_name': forms.TextInput(attrs={'class': 'form-controls'}),
        }


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image', 'phone', 'address', 'bio']