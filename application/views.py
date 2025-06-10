import os
import qrcode
import base64
from io import BytesIO
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.conf import settings
from django.contrib.staticfiles import finders
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.contrib.sites.shortcuts import get_current_site
from .models import CompanyDetails, Product, Machinery, Employee, AGOAApplication
from .forms import CompanyForm, ProductForm, MachineForm, EmployeeForm
from weasyprint import HTML, CSS



CustomUser = get_user_model

def get_company_details(request):

    try:
        companies = CompanyDetails.objects.filter(user=request.user)
        if not companies.exists():
            raise CompanyDetails.DoesNotExist
    except CompanyDetails.DoesNotExist: 
        messages.error(request, "Please fill in company details first.")
        return redirect('company-form')
    return companies


# Create your views here.
def company_form(request):
    if request.method == 'POST':
        form = CompanyForm(request.POST, request.FILES)

        if form.is_valid():

            company = form.save(commit=False)
            company.user = request.user
            company.save()
            if 'add_another' in request.POST:
                messages.success(request, 'Company saved. You can add another one.')
                form = CompanyForm()
                return render(request, 'application/company_form.html', {'form': form})
            
            elif 'submit' in request.POST:
                messages.success(request, 'Company saved successfully.')
                return redirect('product-form')

        
    else:
        form = CompanyForm()

    context ={
        'form': form,
    }
    return render(request, 'application/company_form.html', context)

def product_form(request):
    companies = get_company_details(request)
    if isinstance(companies, HttpResponseRedirect):
        return companies

    if request.method == 'POST':
        form = ProductForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()

            if 'add_another' in request.POST:
                messages.success(request, 'Product Saved. You can add another one')
                form = ProductForm(user=request.user)
                return render(request, 'application/product_form.html', {'form': form})
            
            elif 'submit' in request.POST:
                messages.success(request, 'Product saved successfully')
                return redirect('employee-form')
        
    else:
        form = ProductForm(user=request.user)

    context = {
        'form': form
    }

    return render(request, 'application/product_form.html', context)

def employee_form(request):
    companies = get_company_details(request)
    if isinstance(companies, HttpResponseRedirect):
        return companies

    if request.method == 'POST':
        form = EmployeeForm(request.POST, user=request.user)
        if form.is_valid():
            
            form.save()
            messages.success(request, 'Staff details filled in successfully')
            return redirect('machinery-form')

        else:
            messages.error(request, 'Staff details for this company submitted already')

    else:
        form = EmployeeForm(user=request.user)

    context = {
        'form': form
    }

    return render(request, 'application/employee_form.html', context)

def machinery_form(request):

    companies = get_company_details(request)
    if isinstance(companies, HttpResponseRedirect):
        return companies

    if request.method == 'POST':
        form = MachineForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Machinery details filled successfully')
            return redirect('machinery-form')
        
        else:
            messages.error(request, 'Machinery details for this company submitted already')
        
    else:
        form = MachineForm(user=request.user)

    context = {
        'form': form
    }
    return render(request, 'application/machinery_form.html', context)






def companies_list(request):
    companies = CompanyDetails.objects.filter(user=request.user)
    return render(request, 'lists/companies_list.html', {'companies':companies})

def product_list(request):
    companies = CompanyDetails.objects.filter(user=request.user)
    products = Product.objects.filter(company__in=companies)

    return render(request, 'lists/products_list.html', {'products':products})

def employee_list(request):
    companies = CompanyDetails.objects.filter(user=request.user)
    employees = Employee.objects.filter(company__in=companies)

    return render(request, 'lists/employees_list.html', {'employees':employees})

def machinery_list(request):
    companies = CompanyDetails.objects.filter(user=request.user)
    machinery = Machinery.objects.filter(company__in=companies)

    return render(request, 'lists/machinery_list.html', {'machinery':machinery})


def company_edit(request, pk):

    company = CompanyDetails.objects.get(user=request.user, pk=pk)

    if request.method == 'POST':
        form = CompanyForm(request.POST, request.FILES, instance=company)
        if form.is_valid():
            form.save()
            messages.success(request,'Company Details Updated')
            return redirect('company-list')
        
    else:
        form = CompanyForm(instance=company)

    return render(request,'edits/company_edit.html',{'form':form})

def product_edit(request, company_id, product_id):
    company = CompanyDetails.objects.get(user=request.user, pk=company_id)
    product = Product.objects.get(company=company, id=product_id)

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        form.fields.pop('company', None)

        if form.is_valid():
            form.save()
            messages.success(request,'Product Details Updated')
            return redirect('product-list')
        
    else:
        form = ProductForm(instance=product)
        form.fields.pop('company', None)


    return render(request,'edits/product_edit.html', {'form': form})

def employee_edit(request, company_id, employee_id):

    company = CompanyDetails.objects.get(user=request.user, id=company_id)
    employee = Employee.objects.get(company=company, id=employee_id)

    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        form.fields.pop('company', None)
        if form.is_valid():
            form.save()
            messages.success(request, 'Employee updated')
            return redirect('employee-list')
        else:
            print('errors', form.errors)
    else:
        form = EmployeeForm(instance=employee)
        form.fields.pop('company', None)

    context = {
        'form': form,
    }


    
    return render(request,'edits/employee_edit.html', context)



def machinery_edit(request, company_id, machinery_id):

    company = CompanyDetails.objects.get(user=request.user, id=company_id)
    machinery = Machinery.objects.get(company=company, id=machinery_id)

    if request.method == 'POST':
        form = MachineForm(request.POST, instance=machinery)
        form.fields.pop('company', None)

        if form.is_valid():
            form.save()
            messages.success(request, 'Machinery updated')
            return redirect('machinery-list')
    else:
        form = MachineForm(instance=machinery)
        form.fields.pop('company', None)


    return render(request,'edits/machinery_edit.html', {'form':form})

def review_application(request):

    try:
        companies = CompanyDetails.objects.filter(user=request.user).prefetch_related('products')
    except CompanyDetails.DoesNotExist:
        messages.error(request, 'You need to provide company details')
        return redirect('company-form')
    
    applications = AGOAApplication.objects.filter(company__in=companies) #filter applications by the user
    submitted_company_ids = applications.values_list('company_id', flat=True) #get the ids

    if request.method == 'POST':
        company_id = request.POST.get('company_id')

        company = companies.get(id=company_id) #get that specific company
        if company.id not in submitted_company_ids:
            AGOAApplication.objects.create(company=company) #create an application for that company
            messages.success(request, f'Application for {company.name} submitted successfully.')
            return redirect('review-application')
        
    company_data = []

    for company in companies:
        if company.id in submitted_company_ids:
            continue
        products = company.products.all()
        machinery = getattr(company, 'machinery_details', None)
        employees = getattr(company, 'employees', None)

        missing_sections = []

        if not products.exists():
            missing_sections.append('products')
        if not machinery:
            missing_sections.append('machinery')
        if not employees:
            missing_sections.append('employees')
        
        
        total_machines = machinery.total_machines if machinery else 0
        total_employees = employees.employee_count if employees else 0

        company_data.append({
            'company': company,
            'products': products,
            'machinery_total': total_machines,
            'employee_total': total_employees,
            'application_exists':applications.filter(company=company).exists(),
            'missing_sections': missing_sections,
        })


    all_submitted = not company_data and companies.exists()

    return render(request, 'application/review_application.html',{
        'company_data':company_data,
        'all_submitted': all_submitted
    })

def download_certificate(request,company_id):

    if request.method == 'POST':
        company = CompanyDetails.objects.get(id=company_id)
        try:
            application = AGOAApplication.objects.get(company=company)
        except AGOAApplication.DoesNotExist:
            application = None


    app_details = f'Application {application.application_number} made by {application.company.user.email}'
    qr = qrcode.make(app_details)
    buffer = BytesIO()

    qr.save(buffer, format="PNG")
    qr_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
    
    html_string = render_to_string('application/certificate.html', {
        'application': application,
        'qr_code':qr_base64
    })
    css_path = finders.find('css/cert.css')
    pdf = HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf(stylesheets=[CSS(css_path)])

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="AGOA_Certificate.pdf"'
    return response

