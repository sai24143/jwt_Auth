from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.timezone import now
from django.utils.text import slugify
from datetime import timedelta


# User Manager
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, role='user', **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, role=role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, role='admin', **extra_fields)

# User Model
class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('staff', 'Staff'),
        ('vendor', 'Vendor'),
        ('user', 'User'),
    ]
    username = None
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

# Vendor Model
class Vendor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='vendor')
    company_name = models.CharField(max_length=255)

# Product Model
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=100)
    start_date = models.DateField()
    expiry_date = models.DateField()
    free_delivery = models.BooleanField(default=False)
    delivery_amount = models.FloatField(null=True, blank=True)
    image = models.ImageField(upload_to='products/')
    old_price = models.FloatField()
    new_price = models.FloatField()
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    url = models.SlugField(unique=True, blank=True)
    
    def save(self, *args, **kwargs):
        self.url = slugify(self.name + '-' + str(now().timestamp()))
        self.expiry_date = self.start_date + timedelta(days=7)
        super().save(*args, **kwargs)

    @property
    def discount_percentage(self):
        return round(((self.old_price - self.new_price) / self.old_price) * 100, 2)
    
    @property
    def discount_amount(self):
        return round(self.old_price - self.new_price, 2)
