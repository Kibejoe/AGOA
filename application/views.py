from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from .models import CompanyDetails, Employee
from .forms import CompanyForm, ProductForm, MachineForm, EmployeeForm
from django.contrib import messages

CustomUser = get_user_model

# Create your views here.
def company_form(request):
    if request.method == 'POST':
        form = CompanyForm(request.POST, request.FILES)

        if form.is_valid():

            company_form = form.save(commit=False)
            company_form.user = request.user
            company_form.save()
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
            product_form = form.save(commit=False)
            company = CompanyDetails.objects.get(user=request.user)
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
            employee_form = form.save(commit=False)
            company = CompanyDetails.objects.get(user=request.user)
            employee_form.company = company
            employee_form.save()

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
            machinery_form = form.save(commit=False)
            company = CompanyDetails.objects.get(user=request.user)
            machinery_form.company = company
            machinery_form.save()

            return redirect('machinery-form')
        
    else:
        form = MachineForm()

    context = {
        'form': form
    }
    return render(request, 'application/machinery_form.html', context)