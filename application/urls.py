from django.urls import path
from . import views

urlpatterns = [
    path('company-form/',views.company_form, name='company-form' ),
    path('product-form/',views.product_form, name='product-form' ),
    path('employee-form/',views.employee_form, name='employee-form' ),
    path('machinery-form/',views.machinery_form, name='machinery-form' ),
]