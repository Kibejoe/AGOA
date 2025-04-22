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

        
class Machinery(models.Model):
    company = models.OneToOneField(CompanyDetails, on_delete=models.CASCADE, related_name='machinery_details', null=True)

    # Cutting section
    cutting_machines = models.IntegerField(null=True, blank=True)
    fabric_notcher = models.IntegerField(null=True, blank=True)
    band_cutting = models.IntegerField(null=True, blank=True)
    edge_cutting = models.IntegerField(null=True, blank=True)
    pattern_cutter = models.IntegerField(null=True, blank=True)

    # Stitching section
    single_needle = models.IntegerField(null=True, blank=True)
    sn_computer = models.IntegerField(null=True, blank=True)
    double_needle = models.IntegerField(null=True, blank=True)
    bar_tack = models.IntegerField(null=True, blank=True)
    overlock_3th = models.IntegerField(null=True, blank=True)
    overlock_4th = models.IntegerField(null=True, blank=True)
    overlock_5th = models.IntegerField(null=True, blank=True)
    waist_band_machines = models.IntegerField(null=True, blank=True)
    special_loops = models.IntegerField(null=True, blank=True)
    feed_of_arms = models.IntegerField(null=True, blank=True)
    collar_turners = models.IntegerField(null=True, blank=True)
    button_holing = models.IntegerField(null=True, blank=True)
    button_attach = models.IntegerField(null=True, blank=True)
    computer_welt_machine = models.IntegerField(null=True, blank=True)
    computer_button_holing = models.IntegerField(null=True, blank=True)
    eyelet_button_holing = models.IntegerField(null=True, blank=True)
    snap_buttoning = models.IntegerField(null=True, blank=True)
    fusing_machines = models.IntegerField(null=True, blank=True)
    blind_stitch_hemming = models.IntegerField(null=True, blank=True)
    fabric_inspector = models.IntegerField(null=True, blank=True)
    thread_suckers = models.IntegerField(null=True, blank=True)
    weighing_scales = models.IntegerField(null=True, blank=True)
    water_feed_pump = models.IntegerField(null=True, blank=True)
    strapping_machines = models.IntegerField(null=True, blank=True)
    thread_winders = models.IntegerField(null=True, blank=True)
    clocking_machines = models.IntegerField(null=True, blank=True)

    # Laundry section
    industrial_washing_machine = models.IntegerField(null=True, blank=True)
    air_compressors = models.IntegerField(null=True, blank=True)
    sample_washers = models.IntegerField(null=True, blank=True)
    electric_heated_dryers = models.IntegerField(null=True, blank=True)
    steam_heated_dryers = models.IntegerField(null=True, blank=True)
    steam_boilers = models.IntegerField(null=True, blank=True)
    hydro_extractors = models.IntegerField(null=True, blank=True)

    # Finishing section
    manual_presser = models.IntegerField(null=True, blank=True)
    iron_steam = models.IntegerField(null=True, blank=True)
    iron_ordinary = models.IntegerField(null=True, blank=True)
    fuel_pump = models.IntegerField(null=True, blank=True)
    generators = models.IntegerField(null=True, blank=True)

    # Health facility
    inhouse_clinic = models.BooleanField(default=False)

    # Totals
    total_machines = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"Facility Detail for {self.company.name}"

    class Meta:
        verbose_name = 'Machinery'
        verbose_name_plural = 'Machinery'


    
class Employee(models.Model):

    company = models.OneToOneField(CompanyDetails, on_delete=models.CASCADE, related_name='employees', null=True)

    # Administrative & directors

    administrative_staff = models.IntegerField(null=True)


    # Cutting section
    cutting_cutters=models.IntegerField(null=True)				
    cutting_spreaders=models.IntegerField(null=True)					
    cutting_supervisors=models.IntegerField(null=True) 						
    cutting_assistants=models.IntegerField(null=True)				
    cutting_helpers=models.IntegerField(null=True)

    # Production section

    production_supervisors=models.IntegerField(null=True)				
    production_stitchers=models.IntegerField(null=True)						
    production_line_checkers=models.IntegerField(null=True)				
    production_packers = models.IntegerField(null=True)

    #Finishing departments

    finishing_supervisors= models.IntegerField(null=True)					
    finishing_stitchers= models.IntegerField(null=True)					
    finishing_checkers= models.IntegerField(null=True)					
    finishing_helpers	= models.IntegerField(null=True)			
    finishing_pressing= models.IntegerField(null=True)					
    finishing_packing	= models.IntegerField(null=True)				
    finishing_final_inspector = models.IntegerField(null=True)

    #Sampling departments

    sampling_pattern_makers	= models.IntegerField(null=True)		
    sampling_stitchers= models.IntegerField(null=True)				
    sampling_supervisors = models.IntegerField(null=True)

    class Meta:
        verbose_name = 'Employee'
        verbose_name_plural = 'Employees'

    def __str__(self):
        return f"{self.company.name}"


class AGOAApplication(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('more_info', 'Needs More Information'),
    ]

    company = models.OneToOneField(CompanyDetails, on_delete=models.CASCADE, related_name='applications', null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    class Meta:
        verbose_name='AGOAApplication'
        verbose_name_plural = 'AGOAApplications'


    def __str__(self):
        return f"{self.company.name} - {self.status} ({self.submitted_at.date()})"
