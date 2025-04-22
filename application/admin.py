from django.contrib import admin
from .models import CompanyDetails, ProductCategory, Product, Machinery, Employee, AGOAApplication

admin.site.register(CompanyDetails)
admin.site.register(ProductCategory)
admin.site.register(Product)
admin.site.register(Machinery)
admin.site.register(Employee)
admin.site.register(AGOAApplication)

