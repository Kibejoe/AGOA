from django.contrib import admin
from .models import CompanyDetails, ProductCategory, Product, MachinerySection, Machinery, Department, Employee, AGOAApplication

admin.site.register(CompanyDetails)
admin.site.register(ProductCategory)
admin.site.register(Product)
admin.site.register(MachinerySection)
admin.site.register(Machinery)
admin.site.register(Department)
admin.site.register(Employee)
admin.site.register(AGOAApplication)

