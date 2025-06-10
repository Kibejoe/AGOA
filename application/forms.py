from django import forms
from .models import CompanyDetails, Product, Machinery, Employee, AGOAApplication



class CompanyForm(forms.ModelForm):
    class Meta:
        model = CompanyDetails
        exclude = ['user']
        labels = {
            'email': 'Company Email'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

class UserRestrictedCompanyForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if 'company' in self.fields:
            if user:
                self.fields['company'].queryset = CompanyDetails.objects.filter(user=user)
            else:
                self.fields['company'].queryset = CompanyDetails.objects.none()


class ProductForm(UserRestrictedCompanyForm):
    class Meta:
        model = Product
        fields = '__all__'
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
        self.fields['company'].empty_label = 'Select Company'

        self.fields['production_quantity_per_month'].label = "Production Quantity per Month (pcs)"
        self.fields['time_to_produce'].label = "Time to Produce (e.g., 3 days, 2:00:00)"
        self.fields['storage_area'].label = "Storage Area (m²)"
        self.fields['production_area'].label = "Production Area (m²)"
        self.fields['office_area'].label = "Office Area (m²)"
        self.fields['current_order_quantity'].label = "Current Order Quantity (pcs)"

class MachineForm(UserRestrictedCompanyForm):
    class Meta:
        model = Machinery
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_label, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'

            elif isinstance(field.widget, forms.Select):
                field.widget.attrs['class'] = 'form-select'
            else:
                field.widget.attrs['class'] = 'form-control'

            self.fields['company'].empty_label = 'Select Company'



class EmployeeForm(UserRestrictedCompanyForm):
    class Meta:
        model = Employee
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.Select):
                field.widget.attrs['class'] = 'form-select'
            else:
                field.widget.attrs['class'] = 'form-control'

        self.fields['company'].empty_label = 'Select Company'



class AGOAApplicationAdminForm(forms.ModelForm):
    class Meta:
        model = AGOAApplication
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get("status")
        comments = cleaned_data.get("comments")

        if status == "rejected" and not comments:
            self.add_error("comments", "Please provide a reason for rejection.")

        


