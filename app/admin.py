from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Vendor, Product

# Custom User Admin
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('email', 'role', 'is_staff', 'is_superuser', 'is_active')
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'password', 'role')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'is_active', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'role', 'is_staff', 'is_superuser', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)

# Vendor Admin
class VendorAdmin(admin.ModelAdmin):
    list_display = ('user', 'company_name')
    search_fields = ('company_name',)

# Product Admin
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'vendor', 'old_price', 'new_price', 'discount_percentage', 'start_date', 'expiry_date')
    list_filter = ('category', 'vendor', 'start_date', 'expiry_date')
    search_fields = ('name', 'category', 'vendor__user__email')

# Registering Models
admin.site.register(User, CustomUserAdmin)
admin.site.register(Vendor, VendorAdmin)
admin.site.register(Product, ProductAdmin)
