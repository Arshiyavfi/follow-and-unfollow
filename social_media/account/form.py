from typing import Any
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class UseRegesterationForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form control', 'placeholder':'Enter your user name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form control', 'placeholder':'Enter your email'}))
    password1 = forms.CharField(label='password', widget=forms.PasswordInput(attrs={'class':'form control', 'placeholder':'Enter your password'}))
    password2 = forms.CharField(label='confrim password', widget=forms.PasswordInput(attrs={'class':'form control', 'placeholder':'Enter your password'}))

    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email).exists()
        if user:
            raise ValidationError('Thise emaile already exist.')
        return email
    
    def clean(self):
        cd = super().clean()
        p1 = cd.get('password1')
        p2 = cd.get('password2')
        if p1 and p2 and p1 != p2:
            raise ValidationError('password must mach.')
        
class UserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form control', 'placeholder':'Enter your user name'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form control', 'placeholder':'Enter your password'}))