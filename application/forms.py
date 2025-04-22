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
            ),
        }

        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.Select):
                field.widget.attrs['class'] = 'form-select'
            else:
                field.widget.attrs['class'] = 'form-control'

        self.fields['category'].empty_label = 'Select Category'


class MachineForm(forms.ModelForm):
    class Meta:
        model = Machinery
        exclude = ['company']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_label, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'

            else:
                field.widget.attrs['class'] = 'form-control'


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        exclude = ['company']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
