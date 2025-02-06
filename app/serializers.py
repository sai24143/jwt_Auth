from .models  import Product
from rest_framework import serializers
from rest_framework import serializers, viewsets, permissions
from rest_framework_simplejwt.authentication import JWTAuthentication


# Serializers
class ProductSerializer(serializers.ModelSerializer):
    discount_percentage = serializers.SerializerMethodField()
    discount_amount = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = '__all__'
    
    def get_discount_percentage(self, obj):
        return obj.discount_percentage
    
    def get_discount_amount(self, obj):
        return obj.discount_amount

# Permissions
class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'

class IsVendor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'vendor'

class IsUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'user'
