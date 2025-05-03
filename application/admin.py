from django.contrib import admin
from .models import CompanyDetails, ProductCategory, Product, Machinery, Employee, AGOAApplication


class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'user', 'kra_pin']

class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['company', 'status', 'submitted_at']

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'company', 'category']


admin.site.register(CompanyDetails, CompanyAdmin)
admin.site.register(ProductCategory)
admin.site.register(Product, ProductAdmin)
admin.site.register(Machinery)
admin.site.register(Employee)
admin.site.register(AGOAApplication, ApplicationAdmin)

