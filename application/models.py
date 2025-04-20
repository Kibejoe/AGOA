from django.db import models
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

class CompanyDetails(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='company')
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    email = models.EmailField()
    business_permit = models.FileField(upload_to='media/business_permits')
    epz_licence = models.FileField(upload_to='media/epz_licences')
    kra_pin = models.CharField(max_length=50)
    compliance_cert = models.FileField(upload_to='media/compliance')
    lr_number = models.CharField(max_length=50)
    registration_cert = models.FileField(upload_to='media/registrations', null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'CompanyDetails'
        verbose_name_plural = 'CompanyDetails'

    def __str__(self):
        return self.name
    

class ProductCategory(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'ProductCategory'
        verbose_name_plural = 'ProductCategories'

    def __str__(self):
        return self.name
    

class Product(models.Model):
    name = models.CharField(max_length=50)
    company = models.ForeignKey(CompanyDetails, on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name="product_categories")
    sitc_code = models.CharField(max_length=50)
    hts_code = models.CharField(max_length=50)
    style_number = models.CharField(max_length=50)
    fabric_content = models.CharField(max_length=100)

    description = models.TextField()
    production_quantity_per_month = models.IntegerField()

    time_to_produce = models.DurationField()
    unit = models.CharField(max_length=20, default='pcs')

    fabric_source = models.CharField(max_length=100, blank=True, null=True)
    accessories_source = models.CharField(max_length=100, blank=True, null=True)

    # Area in square meters
    storage_area = models.DecimalField(max_digits=10, decimal_places=2)
    production_area = models.DecimalField(max_digits=10, decimal_places=2)
    office_area = models.DecimalField(max_digits=10, decimal_places=2)

    current_order_type = models.CharField(max_length=100)
    current_order_quantity = models.PositiveIntegerField()
    expected_completion_date = models.DateField()

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'


    def __str__(self):
        return f"{self.name} - {self.production_quantity_per_month} pcs/mo"


class MachinerySection(models.Model):
    name = models.CharField(max_length=50)


    class Meta:
        verbose_name = 'MachinerySection'
        verbose_name_plural = 'MachinerySections'

    def __str__(self):
        return self.type_name
    
    
    
class Machinery(models.Model):
    company = models.ForeignKey(CompanyDetails, on_delete=models.CASCADE, related_name='company_machines', null=True)
    section = models.ForeignKey(MachinerySection, on_delete=models.CASCADE)
    type_name = models.CharField(max_length=100)
    number = models.PositiveIntegerField()


    class Meta:
        verbose_name = 'Machinery'
        verbose_name_plural = 'Machineries'

    def __str__(self):
        return f"{self.type_name} - {self.number}"


class Department(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Department'
        verbose_name_plural = 'Departments'

    def __str__(self):
        return self.name
    
class Employee(models.Model):
    company = models.ForeignKey(CompanyDetails, on_delete=models.CASCADE, related_name='company_employees', null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    role_name = models.CharField(max_length=50)
    number = models.IntegerField()

    class Meta:
        verbose_name = 'Employee'
        verbose_name_plural = 'Employees'

    def __str__(self):
        return f"{self.role_name} - {self.number}"


class AGOAApplication(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('more_info', 'Needs More Information'),
    ]

    company = models.ForeignKey(CompanyDetails, on_delete=models.CASCADE, related_name='applications', null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    class Meta:
        verbose_name='AGOAApplication'
        verbose_name_plural = 'AGOAApplications'


    def __str__(self):
        return f"{self.company.name} - {self.status} ({self.submitted_at.date()})"
