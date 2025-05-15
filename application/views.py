from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from .models import CompanyDetails, Product, Machinery, Employee, AGOAApplication
from .forms import CompanyForm, ProductForm, MachineForm, EmployeeForm
from django.contrib import messages
from django.template.loader import render_to_string
from weasyprint import HTML, CSS
from django.http import HttpResponse
import os
from django.conf import settings
from django.contrib.staticfiles import finders


CustomUser = get_user_model

# Create your views here.
def company_form(request):
    if request.method == 'POST':
        form = CompanyForm(request.POST, request.FILES)

        if form.is_valid():

            company_form = form.save(commit=False)
            company_form.user = request.user
            company_form.save()
            messages.success(request, 'Company details filled in successfully')
            return redirect('product-form')
        
    else:
        form = CompanyForm()
        
    context ={
        'form': form
    }
    return render(request, 'application/company_form.html', context)

def product_form(request):

    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():

            try:
                company = CompanyDetails.objects.get(user=request.user)
            except CompanyDetails.DoesNotExist:
                messages.error(request, 'Fill in Company Details First')
                return render(request, 'application/product_form.html', {'form': form})

            product_form = form.save(commit=False)
            product_form.company = company
            product_form.save()

            if 'add_another' in request.POST:
                messages.success(request, 'Product Saved. You can add another one')
                form = ProductForm()
                return render(request, 'application/product_form.html', {'form': form})
            
            elif 'submit' in request.POST:
                messages.success(request, 'Product saved successfully')
                return redirect('employee-form')
        
    else:
        form = ProductForm()

    context = {
        'form': form
    }

    return render(request, 'application/product_form.html', context)

def employee_form(request):

    if request.method == 'POST':
        form = EmployeeForm(request.POST)

        if form.is_valid():
            try:
                company = CompanyDetails.objects.get(user=request.user)
            except CompanyDetails.DoesNotExist:
                messages.error(request, 'Fill in Company Details First')
                return render(request, 'application/employee_form.html', {'form': form})
            
            employee_form = form.save(commit=False)
            employee_form.company = company
            employee_form.save()

            messages.success(request, 'Staff details filled in successfully')

            return redirect('machinery-form')
        
    else:
        form = EmployeeForm()

    context = {
        'form': form
    }

    return render(request, 'application/employee_form.html', context)

def machinery_form(request):
    if request.method == 'POST':
        form = MachineForm(request.POST)
        if form.is_valid():
            try:
                company = CompanyDetails.objects.get(user=request.user)
            except CompanyDetails.DoesNotExist:
                messages.error(request, 'Fill in Company Details First')
                return render(request, 'application/machinery_form.html')
            machinery_form = form.save(commit=False)
            machinery_form.company = company
            machinery_form.save()

            messages.success(request, 'Machinery details filled successfully')

            return redirect('machinery-form')
        
    else:
        form = MachineForm()

    context = {
        'form': form
    }
    return render(request, 'application/machinery_form.html', context)

def review_application(request):

    try:
        company = CompanyDetails.objects.get(user=request.user)
        product = Product.objects.get(company=company)
        machinery = Machinery.objects.get(company=company)
        employee = Employee.objects.get(company=company)

    except (CompanyDetails.DoesNotExist, Product.DoesNotExist, Machinery.DoesNotExist, Employee.DoesNotExist):
        messages.error(request, 'You need to fill in all the sections')
        return redirect('dashboard')
    
    application_exists = AGOAApplication.objects.filter(company=company).exists()


    if request.method == 'POST':
        
        application = AGOAApplication.objects.create(company=company)
        application.save()
        messages.success(request, 'Application Done Successfully')
        return redirect('review-application')
            
    context = {
        'company': company,
        'product': product,
        'machinery': machinery,
        'employee': employee,
        'application_exists': application_exists
    }

    return render(request, 'application/review_application.html', context)

def view_certificate(request):
    try:
        application = AGOAApplication.objects.get(company__user=request.user)

    except AGOAApplication.DoesNotExist:
        application = None

    context = {
        'application': application
    }

    return render(request, 'application/certificate_page.html', context)


def download_certificate(request):
    try:
        application = AGOAApplication.objects.get(company__user = request.user)
    except AGOAApplication.DoesNotExist:
        application = None

    html_string = render_to_string('application/certificate.html', {'application': application})
    css_path = finders.find('css/cert.css')
    pdf = HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf(stylesheets=[CSS(css_path)])

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="AGOA_Certificate.pdf"'
    return response
