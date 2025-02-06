from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import  viewsets, permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Product
from .serializers import ProductSerializer, IsAdmin, IsVendor


def home(request):
    return HttpResponse("working....")



class ProductViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'DELETE']:
            return [IsAdmin() | IsVendor()]
        return [permissions.AllowAny()]