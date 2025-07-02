from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
import uuid

class AdminManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('enabled', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class Admin(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255, blank=True)
    photo = models.ImageField(upload_to='admin_photos/', blank=True, null=True)
    
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    enabled = models.BooleanField(default=True)
    removed = models.BooleanField(default=False)
    
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)
    
    objects = AdminManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
    
    def __str__(self):
        return self.email

class AdminPassword(models.Model):
    user = models.OneToOneField(Admin, on_delete=models.CASCADE, related_name='password_info')
    password_reset_token = models.CharField(max_length=255, blank=True, null=True)
    password_reset_expires = models.DateTimeField(blank=True, null=True)
    logged_sessions = models.JSONField(default=list)
    
    def __str__(self):
        return f"Password info for {self.user.email}"

class Customer(models.Model):
    """
    Renamed from Client to avoid confusion with tenant.Client
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=50, blank=True)
    country = models.CharField(max_length=100, blank=True)
    address = models.TextField(blank=True)
    email = models.EmailField(blank=True)
    
    created_by = models.ForeignKey(Admin, on_delete=models.SET_NULL, null=True, related_name='created_customers')
    assigned = models.ForeignKey(Admin, on_delete=models.SET_NULL, null=True, related_name='assigned_customers')
    
    enabled = models.BooleanField(default=True)
    removed = models.BooleanField(default=False)
    
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

class PaymentMode(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    
    created_by = models.ForeignKey(Admin, on_delete=models.SET_NULL, null=True)
    
    enabled = models.BooleanField(default=True)
    removed = models.BooleanField(default=False)
    
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    reference = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=15, decimal_places=2)
    
    created_by = models.ForeignKey(Admin, on_delete=models.SET_NULL, null=True)
    
    enabled = models.BooleanField(default=True)
    removed = models.BooleanField(default=False)
    
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

class Quote(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    number = models.CharField(max_length=50)
    year = models.IntegerField()
    date = models.DateField()
    expiry_date = models.DateField(null=True, blank=True)
    client = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='quotes')
    
    sub_total = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    tax_total = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    
    note = models.TextField(blank=True)
    status = models.CharField(max_length=50, default='draft')
    pdf = models.CharField(max_length=255, blank=True)
    
    created_by = models.ForeignKey(Admin, on_delete=models.SET_NULL, null=True)
    
    enabled = models.BooleanField(default=True)
    removed = models.BooleanField(default=False)
    
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Quote #{self.number} - {self.client.name}"

class QuoteItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    quote = models.ForeignKey(Quote, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=15, decimal_places=2)
    total = models.DecimalField(max_digits=15, decimal_places=2)
    
    def __str__(self):
        return f"{self.name} - {self.quote.number}"

class Invoice(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    number = models.CharField(max_length=50)
    year = models.IntegerField()
    date = models.DateField()
    expiry_date = models.DateField(null=True, blank=True)
    client = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='invoices')
    
    sub_total = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    tax_total = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    credit = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    
    note = models.TextField(blank=True)
    status = models.CharField(max_length=50, default='draft')
    pdf = models.CharField(max_length=255, blank=True)
    
    quote = models.ForeignKey(Quote, on_delete=models.SET_NULL, null=True, blank=True, related_name='invoices')
    created_by = models.ForeignKey(Admin, on_delete=models.SET_NULL, null=True)
    
    enabled = models.BooleanField(default=True)
    removed = models.BooleanField(default=False)
    
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Invoice #{self.number} - {self.client.name}"

class InvoiceItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=15, decimal_places=2)
    total = models.DecimalField(max_digits=15, decimal_places=2)
    
    def __str__(self):
        return f"{self.name} - {self.invoice.number}"

class Payment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    number = models.CharField(max_length=50)
    year = models.IntegerField()
    date = models.DateField()
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    
    payment_mode = models.ForeignKey(PaymentMode, on_delete=models.SET_NULL, null=True)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='payments')
    client = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='payments')
    
    note = models.TextField(blank=True)
    ref = models.CharField(max_length=100, blank=True)
    pdf = models.CharField(max_length=255, blank=True)
    
    created_by = models.ForeignKey(Admin, on_delete=models.SET_NULL, null=True)
    
    enabled = models.BooleanField(default=True)
    removed = models.BooleanField(default=False)
    
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Payment #{self.number} - {self.client.name}"

class Setting(models.Model):
    key = models.CharField(max_length=100, primary_key=True)
    value = models.JSONField(default=dict)
    
    def __str__(self):
        return self.key
