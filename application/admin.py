from django.contrib import admin
from .models import CompanyDetails, ProductCategory, Product, Machinery, Employee, AGOAApplication
from .forms import AGOAApplicationAdminForm


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


class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['company', 'application_user', 'application_number', 'status', 'submitted_at']
    search_fields = ['company__name', 'company__user__email']
    list_filter = ['status', 'submitted_at', 'company__user']  
    readonly_fields = ['company', 'application_number']

    form = AGOAApplicationAdminForm

    def has_add_permission(self, request):
        return False  # Disables the "Add" button in admin

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_continue'] = False
        extra_context['show_save_and_add_another'] = False
        return super().change_view(request, object_id, form_url, extra_context=extra_context)
    
    def application_user(self, obj):
        return obj.company.user
    
    application_user.short_description = 'User'


    class Media:
        js = ('js/comments_toggle.js',)



class ProductAdmin(ReadOnlyAdmin):
    list_display = ['name', 'company', 'category']

class EmployeeAdmin(ReadOnlyAdmin):
    list_display = ['company', 'company_user']

    def company_user(self, obj):
        return obj.company.user
    
    company_user.short_description = 'User'

class MachineryAdmin(ReadOnlyAdmin):
    list_display = ['company', 'company_user']

    def company_user(self, obj):
        return obj.company.user
    
    company_user.short_description = 'User'


admin.site.register(CompanyDetails, CompanyAdmin)
admin.site.register(ProductCategory)
admin.site.register(Product, ProductAdmin)
admin.site.register(Machinery, MachineryAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(AGOAApplication, ApplicationAdmin)

