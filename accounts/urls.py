from django.urls import path
from . import views

urlpatterns=[
    path('register/', views.register, name="register" ),
    path('register_activate/<uidb64>/<token>', views.register_activate, name="register-activate"),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name='logout'),
    path('forgot-password/', views.forgot_password, name='forgot-password'),
    path('reset-password/<uidb64>/<token>/', views.reset_password, name='reset-password'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('my-applications/', views.my_applications, name='my-applications'),
]