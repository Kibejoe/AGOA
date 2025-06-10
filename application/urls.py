from django.urls import path
from . import views

urlpatterns = [
    path('company-form/',views.company_form, name='company-form' ),
    path('product-form/',views.product_form, name='product-form' ),
    path('employee-form/',views.employee_form, name='employee-form' ),
    path('machinery-form/',views.machinery_form, name='machinery-form' ),

    path('company_list/',views.companies_list, name='company-list' ),
    path('product-list/',views.product_list, name='product-list' ),
    path('employee-list/',views.employee_list, name='employee-list' ),
    path('machinery-list/',views.machinery_list, name='machinery-list' ),

    path('company-edit/<int:pk>',views.company_edit,name='company-edit'),
    path('product-edit/<int:company_id>/<int:product_id>',views.product_edit,name='product-edit'),
    path('employee-edit/<int:company_id>/<int:employee_id>',views.employee_edit,name='employee-edit'),
    path('machinery-edit/<int:company_id>/<int:machinery_id>',views.machinery_edit,name='machinery-edit'),

    path('review-application/',views.review_application, name='review-application' ),
    path('download-certificate/<int:company_id>',views.download_certificate, name='download-certificate' ),
]