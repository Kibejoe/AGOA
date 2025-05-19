from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings

from .forms import RegistrationForm, LoginForm, ForgotPasswordForm, ResetPasswordForm
from django.contrib import messages
from application.models import CompanyDetails,AGOAApplication


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

        return redirect('login')


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


def forgot_password(request):

    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            try:
                user = CustomUser.objects.get(email=email)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)
                reset_url = request.build_absolute_uri(reverse('reset-password', args=[uid, token]))

                send_mail(
                    subject='Password Reset Link',
                    message=render_to_string('accounts/password_reset_email.html',{
                            'user': user,
                            'reset_url': reset_url
                        }
                    ),
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[email]
                )

                messages.success(request, 'Reset password from your email')
                return redirect('forgot-password')

            except CustomUser.DoesNotExist:
                messages.error(request, 'User with that email does not exist')
                return redirect('forgot-password')

    else:
        form = ForgotPasswordForm()

    return render(request, 'accounts/forgot_password.html', {'form': form})

def reset_password(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except CustomUser.DoesNotExist:
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = ResetPasswordForm(request.POST)

            if form.is_valid():
                new_password = form.cleaned_data.get('new_password')
                confirm_password = form.cleaned_data.get('confirm_password')

                if new_password == confirm_password:
                    user.set_password(new_password)
                    user.save()
                    messages.success(request, 'Password reset successfully')
                    return redirect('login')
                
                else:
                    messages.error(request, 'Passwords do not match')
        
        else:
            form = ResetPasswordForm()

        context = {
            'form':form, 
            'uidb64':uidb64, 
            'token': token
        }

        return render(request, 'accounts/reset_password.html', context)

    else:
        messages.error(request, 'Reset link expired')
        return redirect('forgot-password')
        


@login_required
def dashboard(request):

    try:

        company = CompanyDetails.objects.get(user=request.user)
        pending_count = AGOAApplication.objects.filter(company=company, status='pending').count()
        application = AGOAApplication.objects.filter(company=company)

    except CompanyDetails.DoesNotExist:
        company = None
        pending_count = 0
        application = None

    context = {
        'pending_count': pending_count,
        'application': application
    }

    return render(request, 'accounts/dashboard.html', context)

@login_required
def my_applications(request):
    try:
        company = CompanyDetails.objects.get(user=request.user)
        application = AGOAApplication.objects.get(company=company)

    except (CompanyDetails.DoesNotExist, AGOAApplication.DoesNotExist):
        company = None
        application = None
        

    context = {
        'company': company,
        'application': application
    }
    return render(request, 'accounts/my_applications.html', context)


