from django.contrib import admin
from .models import CompanyDetails, ProductCategory, Product, Machinery, Employee, AGOAApplication



class ReadOnlyAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        return [field.name for field in self.model._meta.fields]

    def has_add_permission(self, request):
        return False  # Disables the "Add" button in admin

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save'] = False
        extra_context['show_save_and_continue'] = False
        extra_context['show_save_and_add_another'] = False
        return super().change_view(request, object_id, form_url, extra_context=extra_context)
      
class CompanyAdmin(ReadOnlyAdmin):
    list_display = ['name', 'email', 'user', 'kra_pin']
    search_fields = ['name', 'email']
    list_filter = ['created_at']


class ApplicationAdmin(ReadOnlyAdmin):
    list_display = ['company', 'status', 'submitted_at']
    search_fields = ['company__name']
    list_filter = ['status', 'submitted_at']  

class ProductAdmin(ReadOnlyAdmin):
    list_display = ['name', 'company', 'category']


admin.site.register(CompanyDetails, CompanyAdmin)
admin.site.register(ProductCategory)
admin.site.register(Product, ProductAdmin)
admin.site.register(Machinery, ReadOnlyAdmin)
admin.site.register(Employee, ReadOnlyAdmin)
admin.site.register(AGOAApplication, ApplicationAdmin)

