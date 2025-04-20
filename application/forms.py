from django import forms
from .models import CompanyDetails, Product, Machinery, Employee

class CompanyForm(forms.ModelForm):
    class Meta:
        model = CompanyDetails
        exclude = ['user']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ['company']
        widgets = {
            'expected_completion_date': forms.DateInput(
                attrs={'type': 'date'}, format="%Y-%m-%d"
            )
        }

        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class MachineForm(forms.ModelForm):
    class Meta:
        model = Machinery
        exclude = ['company']


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        exclude = ['company']
