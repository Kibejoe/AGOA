from django.urls import path
from . import views

urlpatterns=[
    path('register/', views.register, name="register" ),
    path('register_activate/<uidb64>/<token>', views.register_activate, name="register-activate"),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard')
]