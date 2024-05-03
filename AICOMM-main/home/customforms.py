from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django import forms

from.models import UserProfile

class CreateUserForm(UserCreationForm):
    class Meta:
        model=User
        fields=['username', 'email', 'password1', 'password2']


#class UpdateUserForm(UserChangeForm):
 #   email = forms.EmailField(label="Email", required=True)

 #   class Meta:
 #       model = User
 #       fields = ['username', 'email']
from django import forms
from django.forms import widgets
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['email','phone_number', 'address', 'city', 'country']
        widgets = {
            'email':widgets.TextInput(attrs={'placeholder': 'Email...'}),
            'phone_number': widgets.TextInput(attrs={'placeholder': 'Phone Number...'}),
            'address': widgets.TextInput(attrs={'placeholder': 'Address...'}),
            'city': widgets.TextInput(attrs={'placeholder': 'City...'}),
            'country': widgets.TextInput(attrs={'placeholder': 'Country...'}),
        }