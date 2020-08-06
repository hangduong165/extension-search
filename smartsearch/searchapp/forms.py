from django import forms
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.contrib.auth.models import User
from .models import Profile


class SearchForm(forms.Form):
    search_text = forms.CharField(widget=forms.TextInput(attrs={'class': 'input is-medium'}))


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['age']
