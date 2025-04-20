from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings

from .forms import RegistrationForm, LoginForm
from django.contrib import messages



CustomUser = get_user_model()


def register(request):

    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            firstname = form.cleaned_data.get('firstname')
            lastname = form.cleaned_data.get('lastname')
            email = form.cleaned_data.get('email')
            phone = form.cleaned_data.get('phone')
            password = form.cleaned_data.get('password')

            user = CustomUser.objects.create_user(
                firstname=firstname,
                lastname=lastname,
                email=email,
                phone=phone,
                password=password,
            )

            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            activate_url = request.build_absolute_uri(reverse('register-activate', args=[uid, token]))

            send_mail(
                subject='Account Activation',
                message=render_to_string('accounts/account_verification.html',{
                    'user': user,
                    'activate_url':activate_url,
                }),
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email]
            )

            messages.success(request, "Please activate your account from your email")

            return redirect('/accounts/login/?command=verification&email='+email)

    else:
        form = RegistrationForm()

    return render(request, 'accounts/register.html', {'form':form})


def register_activate(request, uidb64, token):
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64)) 
        user = CustomUser.objects.get(pk=uid)

    except(CustomUser.DoesNotExist, ValueError):
        user=None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active=True
        user.save()

        return redirect('register')


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            user = authenticate(request, email=email, password=password)

            if user:
                login(request, user)
                messages.success(request, 'Login Successful')
                return redirect('dashboard')
            
            else:
                messages.error(request, 'Invalid login credentials')
                return redirect('login')

    else:
        form = LoginForm()

    return render(request,'accounts/login.html', {'form':form})


def logout_view(request):

    logout(request)
    messages.success(request, 'You are logged out')
    return redirect('login')


@login_required
def dashboard(request):
    return render(request, 'accounts/dashboard.html')