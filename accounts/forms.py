from django import forms

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

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
            self.fields[field].widget.attrs['class'] = 'form-control mb-3'

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError('Passwords do not match')
        
        if password:
            try:
                validate_password(password)
            except ValidationError as e:
                self.add_error('password', e)


        
        
        
    def clean_email(self):
        email = self.cleaned_data.get('email')

        try:
            CustomUser.objects.get(email=email)
            raise forms.ValidationError('User with this email already exists')
        except CustomUser.DoesNotExist:
            return email
    
class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        "placeholder":"Input Password"
    }))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control mb-3'

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

        

        
    
