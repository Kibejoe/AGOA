from django import forms

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

CustomUser = get_user_model()

class RegistrationForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            "placeholder":"Enter Password"
        }
    ))

    confirm_password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            "placeholder":"Confirm Password"
        }
    ))

    class Meta:
        model = CustomUser
        fields = ['firstname', 'lastname', 'email', 'phone', 'password']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise ValueError('Passwords do not match')
        
    def clean_email(self):
        email = self.cleaned_data.get('email')

        if CustomUser.objects.get(email=email).exists():
            raise ValidationError('User with this email already exists')
        
        return email
    

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        "placeholder":"Input Password"
    }))


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(attrs={
            'class': 'form-control mt-3',
            'placeholder': 'Input your registered email'
        })
    )


class ResetPasswordForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter new password',
        'class': 'form-control'
    }))

    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm password',
        'class': 'form-control'
    }))

    def clean(self):
        cleaned_data = super().clean()

        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        if new_password != confirm_password:
            raise ValueError('Passwords do not match')
        

        
    
