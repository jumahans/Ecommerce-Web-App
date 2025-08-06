from django import forms
from .models import MyCart, UserProfile
from django.contrib.auth.models import User

class MyCartForm(forms.ModelForm):
    class Meta:
        model = MyCart
        fields = ['product', 'quantity', 'shipping']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image']
        widgets = {
            'image': forms.FileInput(attrs={
                "class": 'form-controls', 'accept': 'image/*'
            })
        }

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

class UserImageForm(forms.Form):
    image = forms.ImageField()

    widgets = {
        'image': forms.FileInput(attrs={
            "class" :'form-controls', 'accept' : 'image*/'
        })
    }

    # def __init__(self, *args, **kwargs):
    #     self.user = kwargs.pop('user', None)
    #     super().__init__(*args, **kwargs)

    # def save(self, commit=True):
    #     instance = super().save(commit=False)
    #     if self.user:
    #         instance.user = self.user
    #     if commit:
    #         instance.save()
    #     return instance